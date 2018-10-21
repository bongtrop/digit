#!/usr/bin/env python

import requests
import optparse
import zlib
import string
import os

__version__ = '1.0.1'
__doc__ = \
"""%prog [options] GIT_URL
Digit is the tool that help you to analyze git information from .git directory on website."""

def is_sha1(h):
    return len(h)==40 and all(c in string.hexdigits for c in h)

def main():
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--object', help='Object\'s sha1', dest='object')
    parser.add_option('-w', '--write', help='Write blob to file', dest='filename')

    (opts, args) = parser.parse_args()

    if len(args)!=1:
        parser.error('URL not given')

    url = args[0]
    url = url.rstrip("/")
    if not url.endswith(".git"):
        url += "/.git"

    if not opts.object:
        print "====================== digit by Bongtrop ======================"
        print "[*] DUMP config file"
        r = requests.get(url + "/config")
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            print "=================================================="
            print r.content.strip()
            print "=================================================="
        print

        print "[*] DUMP HEAD file"
        r = requests.get(url + "/HEAD")
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            print "=================================================="
            print r.content.strip()
            if len(r.content.strip().split(" ")) == 2:
                r = requests.get(url + "/" + r.content.strip().split(" ")[1])
                print "\t|"
                print "\t--> " + r.content.strip()
            print "=================================================="
        print

        print "[*] DUMP logs/HEAD file"
        r = requests.get(url + "/logs/HEAD")
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
        r = requests.get(url + "/objects/%s/%s" % (h[:2], h[2:]))
        if r.status_code != 200:
            print "\t[ERROR] What's happen??????"
        else:
            content =  zlib.decompress(r.content)
            print "=================================================="
            if content[:4] == 'tree':
                entries = content[content.index('\x00')+1:]
                while len(entries) > 0:
                    mode, filename = entries[:entries.index('\x00')].split(" ")
                    entries = entries[entries.index('\x00')+1:]
                    h = entries[:20]
                    entries = entries[20:]

                    print "%s\t%s\t%s" % (h.encode("hex"), mode, filename)
            else:
                data = content[content.index('\x00')+1:]
                data = data.strip()
                print data
                if content.startswith('blob') and opts.filename:
                    if os.path.exists(opts.filename):
                        if raw_input("\nFile already exist, wanna replace? (y/n):").lower() != 'y':
                            exit()
                    with open(opts.filename, 'wb') as f:
                        f.write(data)
            print "=================================================="

if __name__ == "__main__":
    main()
