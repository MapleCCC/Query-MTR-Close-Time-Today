# Query MTR Close Time Today/Tonight

## Background

Due to recent social movements in Hong Kong, the local subway system MTR has to early close every day. And the early close time is different from day to day. It brings some inconvenience to people. This tool is to ease the life for those people.

## Usage

```bash
# query MTR close time today
$ python driver.py

# register an automatic mail notifier
$ python driver.py --register-mail-notifier

# get detailed help message
$ python driver.py --help
'
usage: driver.py [-h] [-b] [-v] [-d] [--fall-back]
                 [--fire-browser | --register-mail-notifier [EMAIL_ADDRESS]]

Query when will MTR close today.

optional arguments:
  -h, --help            show this help message and exit
  -b, --brute-force     Find the close time with brute-force strategy. Script
                        runs faster and consumes less memory, but the result
                        might be less reliable.
  -v, --verbose         Increase verbosity
  -d, --debug           Run in debug mode
  --fall-back           Decide whether to resume with normal mode query after
                        brute force query failed
  --fire-browser        When query fails, open the train service info
                        announcement website in browser instead.
  --register-mail-notifier [EMAIL_ADDRESS]
                        Register an entry in scheduler for when update is
                        detected, send an email to EMAIL_ADDR
'
```

## Install

Prerequisites: Python 3.x and `schedule` library.

```bash
git clone https://github.com/MapleCCC/Query-MTR-Close-Time-Today.git

pip install -r requirements.txt
```

## Miscellaneous

The third-party library `schedule` is intentionally loaded as git submodule/subtree instead of pip module, in case pip installation permission can't be easily acquired under some circumstances.

All python code are heavily type annotated.
