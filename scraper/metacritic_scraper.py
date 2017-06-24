import sys

from src.dataIO import *
from src.bsoupadapter import BSoupAdapter
from src.URLHandler import ProductListHandler, UserReviewHandler
from src.input_validator import *
from src.util import *
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class RunCmd:

    def __init__(self):
        print("==================")
        print("Metacritic Scraper")
        print("==================\n\n")
        print("Use -h to view the list of avalailable commands\n\n")
        self.parser = self.get_parser()
        self.input_loop()

    """
    Make a small argparser to parse some command line options.
    """
    @staticmethod
    def get_parser():
        arg_parser = ArgumentParser(description="Metacritic User-Review extractor",
                                    formatter_class=ArgumentDefaultsHelpFormatter)
        arg_parser.add_argument('scrape',
                                nargs='?',
                                action='store',
                                help='Main command of the program. Scrape some data from metacritic.com with this command and a few follow-up arguments.')
        arg_parser.add_argument('-c', '--category',
                                dest='category',
                                default='games',
                                help='Define the category where the scraper should set itself to (defaults to \'games\'). Allowed modes: {}'.format(str(METACRITIC_CATEGORIES)))
        arg_parser.add_argument('-f', '--filter',
                                dest='filter',
                                default='all',
                                help='Define the filter the scraper should apply when selecting data from metacritic.com (defaults to \'all\'). Allowed filters: {}'.format(str(METACRITIC_FILTERS)))
        arg_parser.add_argument('-s', '--sort',
                                dest='sort',
                                default='desc',
                                help='Objects are sorted by their scores respectively. Change this argument to sort either asc (=ascending) or desc (=descending).')
        return arg_parser

    """
    Input loop for this tool, accepting and checking user input with each loop.
    """
    def input_loop(self):
        while True:
            user_input = self.parse(input())
            if user_input != "":
                #print(user_input)
                if 'scrape' in user_input:
                    self.do_scrape(user_input)

    """
    Parse some input.

    Return empty string if nothing has been entered, otherwise return argparse variables as key:value pairs.
    """
    def parse(self, user_input: str):
        if not is_empty(user_input):
            if self.parser is not None:
                return vars(self.parser.parse_args(user_input.split(' ')))
            else:
                self.parser = self.get_parser()
                return self.parser.parse_args(user_input.split(' '))
        else:
            return ""

    """
    Exit the program.

    (Currently not used.)
    """
    def do_exit(self):
        sys.exit("Program terminated")

    """
    This method will be called if 'scrape' has been entered as the key command.
    """
    def do_scrape(self, user_input: dict):
        invalid_input_found = False
        filtering = ""
        category = ""
        sort = ""

        try:
            # Make sure all inputs are valid
            filtering = is_valid_scrape_filter(user_input['filter'])
            category = is_valid_scrape_category(user_input['category'])
            sort = is_valid_sorting(user_input['sort'])
        except InvalidInput as e:
            print(e, sys.exc_info()[0])
            invalid_input_found = True

        if not invalid_input_found:
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # ALL
            # http://www.metacritic.com/browse/games    /score/metascore/all/filtered?sort=desc
            # http://www.metacritic.com/browse/movies   /score/metascore/all/filtered?sort=desc
            # http://www.metacritic.com/browse/tv       /score/metascore/all/filtered?sort=desc
            # http://www.metacritic.com/browse/albums   /score/metascore/all/filtered?sort=desc

            # # # # 90DAY
            # http://www.metacritic.com/browse/albums   /score/metascore/90day/filtered?sort=desc
            # http://www.metacritic.com/browse/games    /score/metascore/90day/filtered?sort=desc
            # http://www.metacritic.com/browse/movies   /score/metascore/90day/filtered?sort=desc
            # http://www.metacritic.com/browse/tv       /score/metascore/90day/filtered?sort=desc

            # # # # BY YEAR
            # http://www.metacritic.com/browse/games    /score/metascore/year/filtered?sort=desc
            # http://www.metacritic.com/browse/albums   /score/metascore/year/filtered?sort=desc
            # http://www.metacritic.com/browse/tv       /score/metascore/year/filtered?sort=desc
            # http://www.metacritic.com/browse/movies   /score/metascore/year/filtered?sort=desc

            # # # # MOST DISCUSSED
            # http://www.metacritic.com/browse/games    /score/metascore/discussed/filtered?sort=desc
            # http://www.metacritic.com/browse/albums   /score/metascore/discussed/filtered?sort=desc
            # http://www.metacritic.com/browse/tv       /score/metascore/discussed/filtered?sort=desc
            # http://www.metacritic.com/browse/movies   /score/metascore/discussed/filtered?sort=desc

            # # # # MOST SHARED
            # http://www.metacritic.com/browse/games    /score/metascore/shared/filtered?sort=desc
            # http://www.metacritic.com/browse/albums   /score/metascore/shared/filtered?sort=desc
            # http://www.metacritic.com/browse/tv       /score/metascore/shared/filtered?sort=desc
            # http://www.metacritic.com/browse/movies   /score/metascore/shared/filtered?sort=desc

            # # # # NOTES
            # - Discussed, Shared have no Pages
            # - All, Year und 90Days have Pages
            # - Year has DropDownMenu for years
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            # Concat base url from which we start crawling
            initial_location = BASE_URL + "/browse/" + category + "/score/metascore/" + filtering + "/filtered?sort=" + sort

            # Create a ProductListHandler object to collect all products from the initial_location url
            products = ProductListHandler(bsoup_adapter=BSoupAdapter(url=initial_location), category=category, filtering=filtering, sorting=sort)

            # Create a UserReviewHandler object which gets fed the product URLs generated by ProductListHandler object
            review_handler = UserReviewHandler(bsoup_adapter=BSoupAdapter(products.find_all_product_hrefs()[0]), category=category)

            # Execute a thread pool to scrape faster
            data = review_handler.execute_review_extraction_worker_pool(8)

            # Write results to a JSON file, located within output-directory
            write_json(review_handler.extract_product_from_url(), data)


if __name__ == "__main__":
    run = RunCmd()
