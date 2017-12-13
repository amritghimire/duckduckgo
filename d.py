import logging
import signal
import subprocess
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen

try:
    import setproctitle

    setproctitle.setproctitle('duckduckgo search')
except Exception:
    pass


def sigint_handler(signum, frame):
    print('\nInterrupted.', file=sys.stderr)
    sys.exit(1)


class Link:

    def __init__(self, index_number, url="", title="", description=""):
        self.url = url
        self.title = title
        self.description = description
        self.index = index_number


signal.signal(signal.SIGINT, sigint_handler)

# Constants

_VERSION_ = '3.4'

COLORMAP = {k: '\x1b[%sm' % v for k, v in {
    'a': '30', 'b': '31', 'c': '32', 'd': '33',
    'e': '34', 'f': '35', 'g': '36', 'h': '37',
    'i': '90', 'j': '91', 'k': '92', 'l': '93',
    'm': '94', 'n': '95', 'o': '96', 'p': '97',
    'A': '30;1', 'B': '31;1', 'C': '32;1', 'D': '33;1',
    'E': '34;1', 'F': '35;1', 'G': '36;1', 'H': '37;1',
    'I': '90;1', 'J': '91;1', 'K': '92;1', 'L': '93;1',
    'M': '94;1', 'N': '95;1', 'O': '96;1', 'P': '97;1',
    'x': '0', 'X': '1', 'y': '7', 'Y': '7;1',
}.items()}

# Disguise as Firefox on Ubuntu
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'


def url_open(url):
    subprocess.call("w3m", url)


def print_err(msg):
    """Print message, verbatim, to stderr.

    ``msg`` could be any stringifiable value.
    """
    print(msg, file=sys.stderr)


BASE_URL = "https://duckduckgo.com/html/?q=Amrit+Ghimire"
html = urlopen(BASE_URL).read()
soup = BeautifulSoup(html, "lxml")
results = soup.find("div", "results")
i = 0
for result in results.find_all("div", "result"):
    i+=1
    title=result.find("div","result__title");
    print(i,"\n\n\n", result, "\n\n\n\n")
