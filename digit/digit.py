#!/usr/bin/env python

import requests
import optparse
import zlib
import string
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = '1.1.0'
__doc__ = \
"""%prog [options] GIT_URL
Digit is the tool that help you to analyze git information from .git directory on website."""

url = ""
ssl_verify = True

def is_sha1(h):
    return len(h)==40 and all(c in string.hexdigits for c in h)

def main():
    global url
    global ssl_verify
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--object', help='Object\'s sha1', dest='object')
    parser.add_option('-w', '--write', help='Write blob to file', dest='out')
    parser.add_option('-k', '--disable-verify', help='Disable verify ssl', action="store_false", dest='ssl_verify')

    (opts, args) = parser.parse_args()

    if len(args)!=1:
        parser.error('URL not given')

    url = args[0]
    url = url.rstrip("/")
    ssl_verify = opts.ssl_verify
    if not url.endswith(".git"):
        url += "/.git"

    if not opts.object:
        print "====================== digit by Bongtrop ======================"
        print "[*] DUMP config file"
        r = requests.get(url + "/config", verify=opts.ssl_verify)
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            print "=================================================="
            print r.content.strip()
            print "=================================================="
        print

        print "[*] DUMP HEAD file"
        r = requests.get(url + "/HEAD", verify=opts.ssl_verify)
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            print "=================================================="
            print r.content.strip()
            if len(r.content.strip().split(" ")) == 2:
                r = requests.get(url + "/" + r.content.strip().split(" ")[1], verify=opts.ssl_verify)
                print "\t|"
                print "\t--> " + r.content.strip()
            print "=================================================="
        print

        print "[*] DUMP logs/HEAD file"
        r = requests.get(url + "/logs/HEAD", verify=opts.ssl_verify)
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            print "=================================================="
            print r.content.strip()
            print "=================================================="
        print
    else:
        h = opts.object
        if not is_sha1(h):
            parser.error('Object\'s sha1 is not correct.')

        print "[*] DUMP object %s" % (h)
        data = load_object(h)
        if data:
            get_content(data, opts.out)
        else:
            print "[-] Object %s is missing !" % h

def load_object(h):
    global url
    global ssl_verify
    r = requests.get(url + "/objects/%s/%s" % (h[:2], h[2:]), verify=ssl_verify)
    if r.status_code != 200:
        return None

    return  zlib.decompress(r.content)

def get_content(data, out):
    if data.startswith('tree'):
        entries = data[data.index('\x00')+1:]
        while len(entries) > 0:
            mode, filename = entries[:entries.index('\x00')].split(" ")
            entries = entries[entries.index('\x00')+1:]
            h = entries[:20]
            entries = entries[20:]

            if out:
                nout = out + "/" + filename

                if mode == "40000":
                    os.mkdir(nout)

                ndata = load_object(h.encode("hex"))
                if ndata:
                    get_content(ndata, nout)
                else:
                    print "[-] Object %s is missing !" % h.encode("hex")
            else:
                print "%s\t%s\t%s" % (h.encode("hex"), mode, filename)
    else:
        entry = data[data.index('\x00')+1:]
        entry = entry.strip()
        if not out:
            print entry
        else:
            print "[+] Save file [ %s ]" % out

        if data.startswith('blob') and out:
            with open(out, 'wb') as f:
                f.write(data)

if __name__ == "__main__":
    main()
