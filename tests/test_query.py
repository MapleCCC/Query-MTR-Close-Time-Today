import re
import unittest

from query import *


class TestQueryMTRCloseTime(unittest.TestCase):
    def test_integrity(self):
        pass

    def test_normal_mode_query(self):
        result = normal_mode_query()

        possible_results_patterns = []
        possible_results_patterns.append(r'港鐵各綫.*將於晚上(?P<time>\d*)時結束。')
        possible_results_patterns.append(
            r'Probably no train service information related to early close of train service is posted today.')
        self.assertTrue(
            re.fullmatch(
                '|'.join(possible_results_patterns),
                result))

    def test_brute_force_mode_query(self):
        result = brute_force_query()
        possible_results_patterns = []
        possible_results_patterns.append(r'港鐵各綫.*將於晚上(?P<time>\d*)時結束。')
        possible_results_patterns.append(
            r'Probably no train service information related to early close of train service is posted today.')
        self.assertTrue(
            re.fullmatch(
                '|'.join(possible_results_patterns),
                result))


if __name__ == '__main__':
    unittest.main()
