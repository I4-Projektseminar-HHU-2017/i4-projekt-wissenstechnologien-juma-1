import asyncio
import sys

import aiohttp

from src.exceptions import *
from src.util import *


class UrlHook:

    def __init__(self, urls: list or str, sema_limit=5):
        if isinstance(urls, list):
            if len(urls) == 0:
                raise InvalidURL("No URLs found.")
            else:
                for url in urls:
                    if is_valid_url(url):
                        continue
                    else:
                        raise InvalidURL("Valid URL expected, not '{}'.\nPlease ensure the URL has a valid format and is of type 'str'.".format(url))
            self.url_cache = urls
        elif isinstance(urls, str):
            url = urls
            if not is_valid_url(url):
                raise InvalidURL("Valid URL expected, not '{}'.\nPlease ensure the URL has a valid format and is of type 'str'.".format(url))
            else:
                self.url_cache = [url]

        self.agent = {'User-Agent': 'Mozilla/5.0'}
        self.semaphore = asyncio.BoundedSemaphore(sema_limit)

    async def ping(self, url: str):
        session = aiohttp.ClientSession(headers=self.agent)
        ping_success = False
        try:
            with aiohttp.Timeout(5):
                async with self.semaphore, session.head(url) as response:
                    if response.status == 200:  # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                        ping_success = True
        except Exception as e:
            print(e, sys.exc_info()[0])
        finally:
            session.close()
            if ping_success:
                return True
            else:
                return False

    async def make_soup(self):
        async with self.semaphore:
            for url in self.url_cache:
                if await self.ping(url):
                    return "ping to {} successful".format(url)
                else:
                    return "ping to {} failed".format(url)

