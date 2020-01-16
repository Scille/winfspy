"""Test suite for windows file system."""

import os
import uuid
import pathlib
from functools import partial

import pytest
import win32api
import win32con
import win32file
import winerror


# Load symbols and test modules


def get_test_modules(base="cases"):
    base = pathlib.Path(__file__).parent / base
    for path in base.iterdir():
        if path.suffix == ".t":
            yield path


SYMBOLS = {**win32api.__dict__, **win32con.__dict__, **win32file.__dict__}
TEST_MODULES = list(get_test_modules())


# Operations


def create_file(
    path, desired_access, share_mode, sddl, creation_disposition, flags_and_attributes, zero=0
):
    assert zero == 0
    assert sddl == 0
    handle = win32file.CreateFile(
        path, desired_access, share_mode, None, creation_disposition, flags_and_attributes, 0
    )
    assert handle != win32file.INVALID_HANDLE_VALUE
    return handle


def delete_file(path):
    win32file.DeleteFile(path)


def get_file_information(path):
    raise NotImplementedError


OPERATIONS = {
    "CreateFile": create_file,
    "DeleteFile": delete_file,
    "GetFileInformation": get_file_information,
}


# Test helpers


def unique_name():
    return str(uuid.uuid4()) + ".txt"


def expect(base_path, cmd, expected):
    print(f"Running: {cmd}")
    print(f"-> expecting: {expected}")

    args = cmd.split()
    get_last_error = False
    if args[0] == "-e":
        args = args[1:]
        get_last_error = True

    def parse(x):
        return eval(x, SYMBOLS)

    operation = OPERATIONS[args[0]]
    path = os.path.join(base_path, args[1])
    args = list(map(parse, args[2:]))

    if not expected and not get_last_error:
        operation(path, *args)
        print("-> OK!")
        return

    try:
        operation(path, *args)
    except Exception as exc:
        if type(exc).__name__ != "error":
            raise
        errno, _, message = exc.args
    else:
        if get_last_error:
            errno = win32api.GetLastError()
            message = None
        else:
            errno = message = None
    assert errno == getattr(winerror, expected), f"Expected {expected}, got {message}"
    print("-> OK!")


# Tests


@pytest.mark.parametrize(
    "test_module_path", TEST_MODULES, ids=list(map(str, TEST_MODULES)),
)
def test_winfs(test_module_path, file_system_path):
    module_number = int(test_module_path.name[:2])
    if module_number > 0:
        pytest.xfail()
    do_expect = partial(expect, file_system_path)
    globs = {"uniqname": unique_name, "expect": do_expect, "testdone": lambda: None}
    test_module = open(test_module_path).read()
    test_module = test_module.replace("from winfstest import *", "")
    exec(test_module, globs)
