# -*- coding: utf-8 -*-

"""
Internal support library
"""

__author__ = 'MapleCCC, <littlelittlemaple@gmail.com>'


import re

import requests
from bs4 import BeautifulSoup

from .config import *
from .models import FlipArea
from .type_check.type_check import type_check
from .utils import remove_capture_group_from_pattern

__all__ = ['brute_force_query', 'normal_mode_query']


def get_html_text_from_url(url: str) -> str:
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text


def get_soup_from_url(url: str) -> BeautifulSoup:
    # choose 'lxml' parser for better performance
    return BeautifulSoup(get_html_text_from_url(url), 'lxml')


def brute_force_query(verbose: bool = False) -> str:
    if verbose:
        print("Scraping website...")
    text = get_html_text_from_url(MTR_TSI_ANNOUNCEMENT_URL)
    if verbose:
        print("Finish scraping\nStart parsing and retrieving...")
    match = re.search(CLOSE_TIME_ANNOUNCEMENT_PATTERN, text)
    if match:
        # Note that the result could be unreliable, since
        # revision to previous announcement could be possible.
        return match.group(0)
    else:
        return "Probably no train service information related to early close of train service is posted today."


@type_check
def normal_mode_query(verbose: bool = False) -> str:
    if verbose:
        print("Scraping website...")

    soup = get_soup_from_url(MTR_TSI_ANNOUNCEMENT_URL)

    if verbose:
        print("Finish scraping\nStart parsing and retrieving...")

    flip_area = FlipArea(soup.find(id='flip-area'))

    if verbose:
        print(
            f"Found {flip_area.number_of_train_service_info} train service info in flip area")

    for tsi in flip_area.sorted_tsi():
        if not tsi.IsReleasedToday():
            return "Probably no train service information related to early close of train service is posted today."

        text = tsi.get_sliding_text()
        matches = re.findall(remove_capture_group_from_pattern(
            CLOSE_TIME_ANNOUNCEMENT_PATTERN), text)

        if len(matches) == 0:
            continue
        elif len(matches) == 1:
            return matches[0]
        else:
            raise ValueError(
                f"Something went wrong when parsing the text: {text}")

    return "Probably no train service information related to early close of train service is posted today."
