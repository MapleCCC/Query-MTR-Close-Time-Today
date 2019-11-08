import re

MTR_TSI_ANNOUNCEMENT_URL = 'http://www.mtr.com.hk/alert/tsi_simpletxt_title_tc.html'
TSI_DIV_ID_PATTERN = re.compile(r'TSI_(?P<tsi_id>[0-9]*)')
RELEASE_DATETIME_DIV_TEXT_PATTERN = re.compile(
    r"此訊息發放時間 : "
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) "
    r"(?P<hour>\d{2}):(?P<minute>\d{2})")
CLOSE_TIME_ANNOUNCEMENT_PATTERN = re.compile(r"港鐵各綫.*將於晚上(?P<time>\d*)時結束。")
