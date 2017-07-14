import io
import json
import os

from src.const import *


def write_json(name: str, data: list):
    with io.open(file=OUTPUT_PATH+name+'.json', mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile)  # Write some JSON stuff into an individual file


def write_reviews_into_textfiles(data: list):
    if data and len(data) > 0:
        for review_set in data:
            path = OUTPUT_PATH + str(review_set.get('points')) + REVIEW_TXT_SUFFIX
            if os.path.exists(path):
                if os.stat(path).st_size == 0:
                    to_write = review_set.get('text') + " \n" + DELIMITER
                else:
                    to_write = "\n\n" + review_set.get('text') + " \n" + DELIMITER
                with io.open(file=path, mode='a', encoding='utf-8') as text_file:
                    text_file.write(to_write)  # Write reviews into their designated textfiles
            else:
                raise FileNotFoundError("{} could not be found. Please make sure the program\'s textfiles are saved within a directory called \'output\' located within the same directory as \'metacritic_scraper.py\'. If you are unsure, please execute \'install_scraper.bat\' again.".format(path))
        return True
    else:
        return False
