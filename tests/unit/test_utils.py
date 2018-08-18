import pytest
from datetime import datetime

from benedict.utils import *


def test_to_timestamp():
    dt = datetime(2018, 1, 1)
    ts = totimestamp(dt)
    dt2 = datetime.utcfromtimestamp(ts)
    assert ts == 1514764800
    assert dt == dt2
