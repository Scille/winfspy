import os

from .conftest import pytest_addoption

__all__ = ["pytest_addoption", "WINFSP_TESTS_EXECUTABLE"]


def _find_executable(executable):
    if not executable.endswith(".exe"):
        executable = f"{executable}.exe"

    if os.path.isfile(executable):
        return executable

    path = os.environ.get("PATH", None)
    paths = path.split(os.pathsep)
    for p in paths:
        f = os.path.join(p, executable)
        if os.path.isfile(f):
            # the file exists, we have a shot at spawn working
            return f

    return None


WINFSP_TESTS_EXECUTABLE = _find_executable("winfsp-tests-x86")

if WINFSP_TESTS_EXECUTABLE is None:
    raise RuntimeError(
        """\
The `winfsp-tests-x86` executable cannot be found.
Make sure it's been downloaded and added to a directory available through %PATH%.\
"""
    )
