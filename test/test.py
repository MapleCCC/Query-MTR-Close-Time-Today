import re
import unittest

from query import *


class TestQueryMTRCloseTime(unittest.TestCase):
    def test_integrity(self):
        pass

    def test_normal_mode_query(self):
        result = normal_mode_query()
        self.assertTrue(re.fullmatch(r'港鐵各綫.*將於晚上(?P<time>\d*)時結束。', result))


if __name__ == '__main__':
    unittest.main()
