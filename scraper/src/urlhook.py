import urllib.request
import sys
from http import HTTPStatus
from bs4 import BeautifulSoup
from src.const import *


class UrlHook:

    def __init__(self, url: str, category: str, filtering: str, sorting: str):
        self.url = url
        self.soup = None
        self.category = category
        self.filtering = filtering
        self.sorting = sorting

    def make_soup(self):
        req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as url_dump:
                if url_dump.getcode() == HTTPStatus.OK:
                    soup = BeautifulSoup(url_dump.read().decode('utf-8'), 'html5lib')
                    self.soup = soup
        except urllib.request.HTTPError as e:
            print(e, sys.exc_info()[0], "on URL: {}".format(self.url))
        except Exception as e:
            print(e, sys.exc_info()[0])

    def pretty_print(self):
        if self.soup is not None:
            return self.soup.prettify()
        else:
            print("URL content not received yet via BeautifulSoup. Use urlhook.soup() before calling this method.")

    def find_product_hrefs(self):
        if self.category in ['tv', 'games', 'albums']:
            return [BASE_URL + a['href'] for a in (div.find('a') for div in self.soup.find_all('div', {'class': 'product_item product_title'})) if a]
        elif self.category in ['movies']:
            return [BASE_URL + a['href'] for a in (td.find('a') for td in self.soup.find_all('td', {'class': 'title_wrapper'})) if a]


