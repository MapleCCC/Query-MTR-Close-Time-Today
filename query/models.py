import re
from datetime import date, datetime

from bs4.element import Tag

from .config import *

__all__ = ['FlipArea', 'TrainServiceInfo', 'TSI']


class FlipArea:
    """
    An OO abstraction for flip area of the website
    """

    def __init__(self, tag: Tag):
        # simple sanity check
        assert tag.name == 'div' and tag['id'] == 'flip-area'
        self._tag = tag
        self._check_validity()

        alist_TSI_div_tag = self._tag.find_all(id=TSI_DIV_ID_PATTERN)
        self._TSI_list = list(map(TrainServiceInfo, alist_TSI_div_tag))

    __slots__ = ['_tag', '_TSI_list']

    @property
    def number_of_train_service_info(self) -> int:
        return len(self._TSI_list)

    def sorted_tsi(self) -> list:
        return sorted(self._TSI_list, key=lambda tsi: tsi.release_datetime)

    def _check_validity(self):
        pass


class TrainServiceInfo:
    """
    An OO abstraction for train service information blocks of the website.
    """

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
