import re
from typing import Match, Pattern

__all__ = ['remove_capture_group_from_pattern']


def remove_capture_group_from_pattern(pattern: Pattern) -> Pattern:

    def handler(matchobj: Match) -> str:
        s = matchobj.group(0)
        return re.sub(r'P\<.*\>', r':', s)

    if isinstance(pattern, str):
        old = pattern
    elif isinstance(pattern, Pattern):
        old = pattern.pattern
    else:
        raise TypeError

    # TODO: inside group can be more groups, do we need to take care of that?
    capture_group_pattern = r'\(\?P\<.*\>.*\)'

    new = re.sub(capture_group_pattern, handler, old)
    return re.compile(new)


if __name__ == '__main__':
    p = r"港鐵各綫.*將於晚上(?P<time>\d*)時結束。"
    assert remove_capture_group_from_pattern(
        p) == re.compile(r"港鐵各綫.*將於晚上(?:\d*)時結束。")
