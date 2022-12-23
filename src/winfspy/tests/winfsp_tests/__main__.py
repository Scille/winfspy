import os
import sys

import pytest

WINFSP_TESTS_DIR = os.path.dirname(__file__)

if __name__ == "__main__":
    errcode = pytest.main([WINFSP_TESTS_DIR] + sys.argv[1:], plugins=["winfspy.tests.winfsp_tests"])
    sys.exit(errcode)
