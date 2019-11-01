#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internal support library
"""

__author__ = 'MapleCCC, <littlelittlemaple@gmail.com>'

import re
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .type_check.type_check import type_check
from .utils import remove_capture_group_from_pattern

__all__ = ['brute_force_query', 'normal_mode_query']

MTR_TSI_ANNOUNCEMENT_URL = 'http://www.mtr.com.hk/alert/tsi_simpletxt_title_tc.html'
TSI_DIV_ID_PATTERN = re.compile(r'TSI_(?P<tsi_id>[0-9]*)')
RELEASE_DATETIME_DIV_TEXT_PATTERN = re.compile(
    r"此訊息發放時間 : "
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) "
    r"(?P<hour>\d{2}):(?P<minute>\d{2})")
CLOSE_TIME_ANNOUNCEMENT_PATTERN = re.compile(r"港鐵各綫.*將於晚上(?P<time>\d*)時結束。")


class FlipArea:
    def __init__(self, tag: Tag):
        # simple sanity check
        assert tag.name == 'div' and tag['id'] == 'flip-area'
        self._tag = tag
        self._check_validity()

        alist_TSI_div_tag = self._tag.find_all(id=TSI_DIV_ID_PATTERN)
        self._TSI_list = map(TrainServiceInfo, alist_TSI_div_tag)

    __slots__ = ['_tag', '_TSI_list']

    @property
    def number_of_train_service_info(self) -> int:
        return len(self._TSI_list)

    def sorted_tsi(self) -> list:
        return sorted(self._TSI_list, key=lambda tsi: tsi.release_datetime)

    def _check_validity(self):
        pass


class TrainServiceInfo:
    def __init__(self, tag: Tag):

        def extract_release_datetime() -> datetime:
            for div in self._tag.find_all('div'):
                if div.string:
                    match = re.fullmatch(
                        RELEASE_DATETIME_DIV_TEXT_PATTERN, div.string)
                    if match:
                        d = match.groupdict()
                        return datetime(**{k: int(v) for k, v in d.items()})
            raise ValueError("Invalid tag")

        # self.__class__._check_tag(tag)

        # simple sanity check
        assert tag.name == 'div'

        match = re.fullmatch(TSI_DIV_ID_PATTERN, tag['id'])
        if match:
            self.tsi_id = match.group('tsi_id')
        else:
            raise ValueError("Error in parsing tag")
        self._tag = tag
        self._release_datetime = extract_release_datetime()

    __slots__ = ['tsi_id', '_tag', '_release_datetime']

    @property
    def release_datetime(self) -> datetime:
        return self._release_datetime

    @property
    def release_date(self) -> date:
        return self._release_datetime.date()

    def IsReleasedToday(self) -> bool:
        # TODO: handle comparison beween aware date and naive date. Replace
        # locale-related today() with current time in Hong Kong area.
        return self._release_datetime.date() == date.today()

    def get_sliding_text(self) -> str:
        result = self._tag.find_all(id=re.compile(r'sliding[0-9]*'))
        if len(result) != 1:
            raise ValueError("Error in parsing tag")
        return result[0].get_text()

    # designated as classmethod, no need to have one copy to carry around by
    # every instance, which wastes memory
    @classmethod
    def _check_tag(cls, tag: Tag):
        if not tag.name == 'div' or not re.fullmatch(
                TSI_DIV_ID_PATTERN, tag['id']):
            raise ValueError('Invalid tag')


# Alias for convenience
# use shortname in REPL for convenience and cleanness,
# use whole name in script for clarity.
TSI = TrainServiceInfo


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
        return "No train service information related to early close of train service is posted today."


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
            return "No train service information related to early close of train service is posted today."

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
