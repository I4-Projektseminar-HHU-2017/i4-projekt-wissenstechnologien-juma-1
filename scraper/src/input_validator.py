from src.const import *
from src.exceptions import InvalidInput


def is_valid_scrape_category(category: str):
    if category.lower().strip() in METACRITIC_CATEGORIES:
        return category.lower().strip()
    else:
        raise InvalidInput("{} is not a valid mode.".format(category))


def is_valid_scrape_filter(filtering: str):
    if filtering.lower().strip() in METACRITIC_FILTERS:
        return filtering.lower().strip()
    else:
        raise InvalidInput("{} is not a valid filter.".format(filtering))


def is_valid_sorting(sorting: str):
    if sorting.lower().strip() in SORTING_CONSTANTS:
        return sorting.lower().strip()
    else:
        raise InvalidInput("{} is not a valid filter.".format(sorting))
