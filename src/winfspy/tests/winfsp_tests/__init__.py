from .conftest import pytest_addoption
from distutils.spawn import find_executable

__all__ = ["pytest_addoption", "WINFSP_TESTS_EXECUTABLE"]

WINFSP_TESTS_EXECUTABLE = find_executable("winfsp-tests-x86")

if WINFSP_TESTS_EXECUTABLE is None:
    raise RuntimeError(
        """\
The `winfsp-tests-x86` executable cannot be found.
Make sure it's been downloaded and added to a directory available through %PATH%.\
"""
    )
