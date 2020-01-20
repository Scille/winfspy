import os
import sys

import pytest

WINFSTEST_DIR = os.path.dirname(__file__)

if __name__ == "__main__":
    errcode = pytest.main([WINFSTEST_DIR] + sys.argv[1:], plugins=["winfspy.tests.winfstest"])
    sys.exit(errcode)
