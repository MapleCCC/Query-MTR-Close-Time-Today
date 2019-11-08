# Query MTR Close Time Today/Tonight

[![Build Status](https://travis-ci.org/MapleCCC/Query-MTR-Close-Time-Today.svg?branch=master)](https://travis-ci.org/MapleCCC/Query-MTR-Close-Time-Today)

## Background

Due to recent social movements in Hong Kong, the local subway system MTR has to early close every day. And the close time is different from day to day. It brings some inconvenience to people. This tool is intended to ease people's life.

## Usage

```bash
# query MTR close time today
$ python driver.py
港鐵各綫(機場快綫除外)、輕鐵及港鐵巴士服務將於晚上11時結束。

# register an automatic mail notifier
$ python driver.py --register-mail-notifier
Register mail notifier successfully!

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
                        Register an entry in scheduler, periodically run and
                        detect update, send a notification email to
                        EMAIL_ADDRESS.
'
```

Note that the script actually `try its best effort`. It's inevitable to have to make certain amounts of assumptions about the web content structure and announcement context pattern. These assumptions have different confidence to hold true for various periods. The script has been carefully and intentionally written with the principle `failure is better than unsoundness` in mind, adhereing to a more restricted fault-tolerant style, in order to reduce chance of yielding unsoundness as much as possible. However it's impossible to eradicate all the unsoundness, due to the natural complexity and uncertainty of third-party website. Be advised that the query result could be unreliable and use to your own risk.

## Install

> Prerequisites: Python 3.6 and some optional third-party libraries, if more advanced feature support is desired.

```bash
git clone https://github.com/MapleCCC/Query-MTR-Close-Time-Today.git

# optionally install library support for advanced features, e.g., register email notifier.
python -m pip install --upgrade -r requirements.txt
```

# Test

`Pytest` is used to run the tests.

```bash
# install pytest if not already
python -m pip install --upgrade -r test_requirements.txt

python -m pytest tests
```

## Miscellaneous

All python code are heavily type annotated.

# License

[WTFPL 2.0](./LICENSE)
