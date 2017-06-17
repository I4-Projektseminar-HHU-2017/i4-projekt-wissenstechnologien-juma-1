import sys
from src.const import *
from src.urlhook import UrlHook
from src.input_validator import *
from src.util import *
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


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


class RunCmd:

    def __init__(self):
        print("==================")
        print("Metacritic Scraper")
        print("==================\n\n")
        print("Use -h to view the list of avalailable commands\n\n")
        self.parser = get_parser()
        self.input_loop()

    def input_loop(self):
        while True:
            user_input = self.parse(input())
            if user_input != "":
                #print(user_input)
                if 'scrape' in user_input:
                    self.do_scrape(user_input)

    def parse(self, user_input: str):
        if not is_empty(user_input):
            if self.parser is not None:
                return vars(self.parser.parse_args(user_input.split(' ')))
            else:
                self.parser = get_parser()
                return self.parser.parse_args(user_input.split(' '))
        else:
            return ""

    def do_exit(self):
        sys.exit("Program terminated")

    def do_scrape(self, user_input: dict):
        invalid_input_found = False
        filtering = ""
        category = ""
        sort = ""

        try:
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

            to_scrape = BASE_URL + "/browse/" + category + "/score/metascore/" + filtering + "/filtered?sort=" + sort
            url_hook = UrlHook(url=to_scrape, category=category, filtering=filtering, sorting=sort)
            url_hook.make_soup()
            #print(url_hook.pretty_print())
            print(url_hook.find_product_hrefs())

if __name__ == "__main__":
    run = RunCmd()
