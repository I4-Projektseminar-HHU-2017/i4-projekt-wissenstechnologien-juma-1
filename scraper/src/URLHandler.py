import re
import itertools
import time

from src.bsoupadapter import BSoupAdapter
from src.const import *
from concurrent.futures import ThreadPoolExecutor, as_completed


class ProductListHandler:
    def __init__(self, bsoup_adapter: BSoupAdapter, category: str, filtering: str, sorting: str):
        self.bsoup_adapter = bsoup_adapter
        self.soup = self.bsoup_adapter.get_url_soup()
        self.category = category
        self.filtering = filtering
        self.sorting = sorting

    """
    Returns a list of links of all product items available to the soup
    """
    def find_all_product_hrefs(self):
        if self.soup is not None:
            return [BASE_URL + a['href'] + '/user-reviews'
                    for a in (div.find('a')
                              for div in self.soup.find_all('div', {'class': 'product_item product_title'}))
                    if a]
        else:
            return None

    """
    PrettyPrint soup
    """
    def pretty_print(self):
        if self.soup is not None:
            self.bsoup_adapter.pretty_print()


class UserReviewHandler:
    def __init__(self, bsoup_adapter: BSoupAdapter, category: str):
        self.bsoup_adapter = bsoup_adapter
        self.soup = self.bsoup_adapter.get_url_soup()
        self.category = category

    """
    Extract points and text from a user-review to a product, represented by the url.
    The url needs to be a parameter because of the ThreadPoolExecutor.

    Returns a list of dictionaries which contain all user-reviews as points and texts pairs.
    """
    def extract_review_data(self, url=None):
        data = []
        if self.soup is not None:
            if url is None:
                reviews = self.soup.find_all('div', class_='review_section')
            else:
                soup = BSoupAdapter(url=url).get_url_soup()
                reviews = soup.find_all('div', class_='review_section')
            for elem in reviews:
                points = elem.find('div', class_=re.compile(r'metascore_w user (medium|large) (tvshow|game|album) (negative|mixed|positive) indiv'))
                content = elem.find('div', class_='review_body')
                if content is not None and points is not None:  # skip other stuff
                    if content.find('span', class_='inline_expand_collapse inline_collapsed'):  # check if text is collapsed
                        text = content.find('span', class_='blurb blurb_expanded')
                    else:
                        text = content
                    if text is not None:
                        data.append({'points': int(points.text.strip()), 'text': text.text.strip()})  # strip texts, put them into a dictionary and append them to a list
            return data
        else:
            return None

    """
    Return a list of all available page links to the classes url, if any.

    Note: Metacritic starts counting pages at 0 instead of 1. So the first page is 0, the second page is 1 and so on...
    """
    def find_all_user_review_pages(self):
        if self.soup is not None:
            if not self.soup.find('div', class_='msg msg_no_reviews'):  # no review class
                last_page = self.soup.find('li', class_='page last_page')  # last_page class in case reviews have been pagified
                if last_page is not None:
                    num = last_page.find('a', class_='page_num')  # last_page class always contains the last page_num (conveniently)
                    if num is not None:
                        num = int(num.text.strip()) - 1
                        page_links = []
                        while num != -1:
                            page_links.append(self.bsoup_adapter.url + '?page=' + str(num))
                            num -= 1
                        return sorted(page_links, key=lambda x: int(x[-1]))
                else:
                    return [self.bsoup_adapter.url + '?page=0']
            else:
                return None
        else:
            return None

    def execute_review_extraction(self):
        urls = self.find_all_user_review_pages()

        if urls is not None:
            if len(urls) != 1:

                """
                ThreadPool to scrape through links a little faster.
                """
                pool = ThreadPoolExecutor(THREADPOOL_SIZE)  # pool size should ideally be not larger than 8
                data = []
                with pool as executor:
                    print("Extracting user-reviews from " + self.extract_product_from_url() + "... ({} pages)\n".format(len(urls)))

                    # each thread in the pool gets assigned the same task of calling self.extract_review_data just with different urls
                    start_time = time.time()
                    results_in_future = {executor.submit(self.extract_review_data, url): url for url in urls}

                    for current_future in as_completed(results_in_future):  # as_completed seems to be a magic method...
                        current_url = results_in_future[current_future]
                        try:
                            if current_future.result() is not None:
                                data.append(current_future.result())  # the return value of the self.extract_review_data method is collected here
                                print(current_url + ' Extraction successful')
                        except KeyboardInterrupt:
                            executor.shutdown(wait=True)
                            return None
                        except Exception as exc:
                            print('{} generated an exception: {}'.format(current_url, exc))
                            print('Halting process...')
                            executor.shutdown(wait=True)
                            print("------------------------------------\n")
                            return None

                    executor.shutdown(wait=True)

                end_time = round(time.time() - start_time, 3)
                merged_pool_results = list(itertools.chain.from_iterable(data))  # merge all the lists collected from the thread pools into one list, so we get a huge list of dictionaries

                print("\nScraping data from {} was successful. Collected a total of {} reviews in {}secs.".format(self.extract_product_from_url(), len(merged_pool_results), end_time))
                return merged_pool_results
            else:

                """
                In case user-review section of the product only has 1 page
                """
                url = urls[0]
                print("Extracting user-reviews from " + self.extract_product_from_url() + "... (1 page)\n")
                start_time = time.time()
                data = self.extract_review_data(url=url)
                end_time = round(time.time() - start_time, 3)
                print("{} Extraction successful.".format(url))
                print("\nScraping data from {} was successful. Collected a total of {} reviews in {}secs.".format(self.extract_product_from_url(), len(data), end_time))
                return data
        else:

            """
            In case product does not have any user-reviews
            """
            return []

    """
    Get the product name from the url.

    Very naive way to get this, but usually the title is located right before the last object, which (in this class) is '/user-review'
    """
    def extract_product_from_url(self):
        segments = self.bsoup_adapter.url.replace(BASE_URL, "")
        segments = segments.split('/')
        if self.category in ['games', 'albums']:
            return segments[-2]
        elif self.category in ['tv']:
            return ''.join(segments[-3:-2])

    """
    PrettyPrint soup
    """
    def pretty_print(self):
        if self.soup is not None:
            self.bsoup_adapter.pretty_print()
