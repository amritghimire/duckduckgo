#!/usr/bin/python

import signal
import subprocess
import sys
from termcolor import colored
import re

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus

try:
    import setproctitle

    setproctitle.setproctitle('duckduckgo search')
except Exception:
    pass


def sigint_handler(signum, frame):
    print('\nInterrupted.', file=sys.stderr)
    sys.exit(1)


class Link:

    def __init__(self, url="", title="", description=""):
        self.url = url
        self.title = title
        self.description = description


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
    os.system("w3m '" + url + "'")


def print_err(msg):
    """Print message, verbatim, to stderr.

    ``msg`` could be any stringifiable value.
    """
    print(msg, file=sys.stderr)


def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def search_for(search_term):
    base_url = "https://duckduckgo.com/html/?q="
    continues = 0
    while continues == 0:
        urls = base_url + quote_plus(search_term.strip()) + "&kp=-2"
        html = urlopen(urls).read()
        soup = BeautifulSoup(html, "lxml")
        results = soup.find("div", "results")
        lists_of_results = list()
        for result in results.find_all("div", "result"):
            title = strip_html(str(result.find("h2", "result__title")))
            url = "https://duckduckgo.com" + result.find('h2', 'result__title').a["href"]
            description = strip_html(str(result.find("a", "result__snippet")))
            lists_of_results.append(Link(url, title, description))
        q = ''
        start = 0
        zci = soup.find("div", "zci__result")
        zci_text = ""
        if zci:
            zci_text = strip_html(str(zci))
        while q != 'q':
            subprocess.call('clear')
            # print(lists_of_results, len(lists_of_results))
            if zci:
                print(colored(zci_text, "blue"))
            for i in range(start, min(start + 10, len(lists_of_results))):
                print(colored(":" + str(i) + ":", "red"), colored(lists_of_results[i].title, "blue"),
                      lists_of_results[i].description)
            if start == 0:
                q = input("Enter the link index to open or q to exit (n=> next):")
            elif start == 10:
                q = input("Enter the link index to open or q to exit (p=> previous):")
            if q.lower() == "q":
                break
            elif q.lower() == 'n' and start == 0:
                start = 10
            elif q.lower() == 'p' and start == 10:
                start = 0
            elif q[0] == ':':
                search_term = q[0:]
                q = 'q'
                continues -= 1
            else:
                try:
                    n = int(q)

                    if n < len(lists_of_results):
                        url_open(lists_of_results[n].url)
                except ValueError:
                    pass
        continues += 1


search_text = ' '.join(sys.argv[1:])
if not search_text:
    search_text = input("Enter search text: ")
search_for(search_text)
