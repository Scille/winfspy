"""Test suite for windows file system."""

import os
import uuid
import types
import pathlib

from datetime import datetime
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import pytest
import win32api
import win32con
import win32file
import winerror
import winnt
import pywintypes


# Load symbols and test modules


def get_test_modules(base="cases"):
    base = pathlib.Path(__file__).parent / base
    for path in base.iterdir():
        if path.suffix == ".t":
            yield path


TEST_MODULES = list(get_test_modules())
SYMBOL_DICT = {**win32api.__dict__, **win32con.__dict__, **win32file.__dict__, **winnt.__dict__}
SYMBOLS = types.SimpleNamespace(**SYMBOL_DICT)


# Helpers


def windatetime_to_datetime(windatetime):
    string = str(windatetime)
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f%z")


def file_info_to_dict(file_info):
    keys = (
        "FileAttributes",
        "CreationTime",
        "LastAccessTime",
        "LastWriteTime",
        "VolumeSerialNumber",
        "FileSizeHigh",
        "FileSizeLow",
        "NumberOfLinks",
        "FileIndexHigh",
        "FileIndexLow",
    )
    result = dict(zip(keys, file_info))
    for key in ("CreationTime", "LastAccessTime", "LastWriteTime"):
        result[key] = windatetime_to_datetime(result[key])
    return result


def find_data_to_dict(file_info):
    keys = (
        "FileAttributes",
        "CreationTime",
        "LastAccessTime",
        "LastWriteTime",
        "FileSizeHigh",
        "FileSizeLow",
        "Reserved0",
        "Reserved1",
        "FileName",
        "AlternateFileName",
    )
    result = dict(zip(keys, file_info))
    for key in ("CreationTime", "LastAccessTime", "LastWriteTime"):
        result[key] = windatetime_to_datetime(result[key])
    return result


# Operations


def create_file(
    path,
    desired_access,
    share_mode,
    sddl,
    creation_disposition,
    flags_and_attributes,
    zero=0,
    raise_last_error=False,
):
    # Security descriptors are not supported in the tests at the moment
    assert zero == 0
    assert sddl == 0

    # Windows API call
    handle = win32file.CreateFileW(
        path, desired_access, share_mode, None, creation_disposition, flags_and_attributes, 0
    )

    # Close the handle
    # This is necessary since we use a single process
    # for running all the commands from a single test case
    assert handle != win32file.INVALID_HANDLE_VALUE
    win32file.CloseHandle(handle)

    # Used when the command is prepended with `-e`
    if raise_last_error:
        raise pywintypes.error(win32api.GetLastError(), "CreateFileW", None)


def delete_file(path):
    # Windows API call
    win32file.DeleteFile(path)


def get_file_information(path):
    # First windows API call
    handle = win32file.CreateFileW(
        path,
        SYMBOLS.FILE_READ_ATTRIBUTES,
        SYMBOLS.FILE_SHARE_READ | SYMBOLS.FILE_SHARE_WRITE | SYMBOLS.FILE_SHARE_DELETE,
        None,
        SYMBOLS.OPEN_EXISTING,
        SYMBOLS.FILE_FLAG_OPEN_REPARSE_POINT | SYMBOLS.FILE_FLAG_BACKUP_SEMANTICS,
        0,
    )

    # Second windows API call
    assert handle != win32file.INVALID_HANDLE_VALUE
    file_info = win32file.GetFileInformationByHandle(handle)

    # Close the handle
    # This is necessary since we use a single process
    # for running all the commands from a single test case
    win32file.CloseHandle(handle)

    # Convert file info into a dictionary
    return file_info_to_dict(file_info)


def set_file_attributes(path, file_attributes):
    # Windows API call
    win32file.SetFileAttributesW(path, file_attributes)


def create_directory(path, sddl):
    # Security descriptors are not supported in the tests at the moment
    assert sddl == 0

    # Windows API call
    win32file.CreateDirectoryW(path, None)


def remove_directory(path):
    # Windows API call
    win32file.RemoveDirectory(path)


def find_files(path):
    lst = win32file.FindFilesW(path)
    return list(map(find_data_to_dict, lst))


OPERATIONS = {
    "CreateFile": create_file,
    "DeleteFile": delete_file,
    "GetFileInformation": get_file_information,
    "SetFileAttributes": set_file_attributes,
    "CreateDirectory": create_directory,
    "RemoveDirectory": remove_directory,
    "FindFiles": find_files,
}


# Test helpers


def unique_name():
    return str(uuid.uuid4()) + ".txt"


def expect(base_path, runner, cmd, expected):
    print(f"Running: {cmd}")
    print(f"-> expecting: {expected}")

    args = cmd.split()
    kwargs = {}
    if args[0] == "-e":
        args = args[1:]
        kwargs["raise_last_error"] = True

    def parse(x):
        return eval(x, SYMBOL_DICT)

    operation = OPERATIONS[args[0]]
    path = os.path.join(base_path, args[1])
    args = list(map(parse, args[2:]))

    if not expected or callable(expected):
        result = runner(operation, path, *args, **kwargs)
        if callable(expected):
            assert expected((result,))
        print(f"-> OK: {result}")
        return None, result

    with pytest.raises(pywintypes.error) as context:
        runner(operation, path, *args, **kwargs)

    errno, _, message = context.value.args
    assert errno == getattr(winerror, expected), f"Expected {expected}, got {message}"
    print(f"-> OK: expected errno {errno}")
    return errno, None


# Tests


def assert_(value):
    assert value


@pytest.fixture
def process_runner():
    with ProcessPoolExecutor(max_workers=1) as executor:

        def runner(fn, *args, **kwargs):
            return executor.submit(fn, *args, **kwargs).result()

        yield runner


@pytest.mark.parametrize(
    "test_module_path", TEST_MODULES, ids=list(map(str, TEST_MODULES)),
)
def test_winfs(test_module_path, file_system_path, process_runner):
    module_number = int(test_module_path.name[:2])
    if module_number > 3:
        pytest.xfail()

    do_expect = partial(expect, file_system_path, process_runner)
    globs = {
        "uniqname": unique_name,
        "expect": do_expect,
        "testeval": assert_,
        "testdone": lambda: None,
    }
    test_module = open(test_module_path).read()
    test_module = test_module.replace("from winfstest import *", "")
    exec(test_module, globs)
