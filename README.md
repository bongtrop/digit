# digit

Digit is the tool that help you to analyze git information from .git directory on website.

I found the tool like [GitTools](https://github.com/internetwache/GitTools) to dump the source code from website with .git directory. GitTools have to dump objects from .git directory then use git command to analyze. But I only need the tool that can analyze .git directory without downloading and easy to dig into the git object.

Github [https://github.com/bongtrop/digit](https://github.com/bongtrop/digit)

## Requirements

- Python 2 but i think that code can use in python 3
- Python module that you can see in requirements.txt

## Installation

It's simple like the other python project.

### pip 

```bash
pip install digit
# or
pip install git+https://github.com/bongtrop/digit.git
```

### Manual

```bash
git clone https://github.com/bongtrop/digit.git
cd digit
pip install -r requirements.txt
python setup.py install
```

## Usage

just ```digit -h```. 

```bash
Usage: digit.py [options] GIT_URL
Dig git information from .git directory on website.

Options:
  -h, --help            show this help message and exit
  -o OBJECT, --object=OBJECT
                        Object\'s sha1
  -w FILENAME, --write=FILENAME
                        Write blob to file
```

## Contribution

I dont mind the way that you will contribute. Just do it. below is example.

- email
- create issue
- pull request
- carrier pigeon
- tell my friend to tell me
- foo bar

## License

Please see [LICENSE](LICENSE) file.
