import urllib.request
import sys
import time

from http import HTTPStatus
from bs4 import BeautifulSoup


class BSoupAdapter:

    def __init__(self, url: str):
        self.url = url
        self.url_soup = self.make_soup()

    """
    Create a soup object.

    If too many requests are being sent and the program halts due to a 429 HTTPError (Too many requests), a 10 second pausing timer
    has been added. The method will be called again after that timer is over.
    """
    def make_soup(self):
        req = urllib.request.Request(self.url, headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        try:
            with urllib.request.urlopen(req) as url_dump:  # with open() closes opened object automatically
                if url_dump.getcode() == HTTPStatus.OK:
                    soup = BeautifulSoup(url_dump.read().decode('utf-8'), 'html5lib')
                    return soup
        except urllib.request.HTTPError as e:
            if e.code == 429:  # simple spam protection handling
                print("{} Server side spam protection triggered, retrying in 10 seconds...".format(self.url))
                time.sleep(10)
                return self.make_soup()
            else:
                print(e, sys.exc_info()[0], "on URL: {}".format(self.url))
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(e, sys.exc_info()[0])

    """
    # PrettyPrint the HTML code from the created soup
    """
    def pretty_print(self):
        if self.url_soup is not None:
            print(self.url_soup.prettify())
        else:
            self.make_soup()
            print(self.url_soup.prettify())

    """
    Method to get soup object for better Syntax (to prevent e.g. soup.soup)
    """
    def get_url_soup(self):
        return self.url_soup
