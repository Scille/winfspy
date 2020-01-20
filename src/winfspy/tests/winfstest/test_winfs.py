"""Test suite for windows file system."""

import uuid
import types
import pathlib

from functools import partial
from datetime import datetime, timezone
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
    return windatetime.isoformat().replace("+00:00", "Z")


def create_result_dict(info, keys):
    result = dict(zip(keys, info))
    for key in ("CreationTime", "LastAccessTime", "LastWriteTime"):
        if key not in keys:
            continue
        result[key] = windatetime_to_datetime(result[key])
    for key in ("FileSize", "FileIndex"):
        if f"{key}Low" not in keys:
            continue
        low = result.pop(f"{key}Low")
        high = result.pop(f"{key}High")
        result[key] = high << 32 | low
    return result


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
    return create_result_dict(file_info, keys)


def find_data_to_dict(find_data):
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
    return create_result_dict(find_data, keys)


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
    # Windows API call
    lst = win32file.FindFilesW(path)

    # Convert find data to a list of dict
    return list(map(find_data_to_dict, lst))


def move_file_ex(path, new_file_name, flags):
    # Windows API call
    win32file.MoveFileExW(path, new_file_name, flags)


def set_end_of_file(path, length):
    # First windows API call
    handle = win32file.CreateFileW(
        path,
        SYMBOLS.GENERIC_WRITE,
        SYMBOLS.FILE_SHARE_READ | SYMBOLS.FILE_SHARE_WRITE | SYMBOLS.FILE_SHARE_DELETE,
        None,
        SYMBOLS.OPEN_EXISTING,
        SYMBOLS.FILE_FLAG_OPEN_REPARSE_POINT | SYMBOLS.FILE_FLAG_BACKUP_SEMANTICS,
        0,
    )

    # Second windows API call
    assert handle != win32file.INVALID_HANDLE_VALUE
    win32file.SetFileInformationByHandle(
        handle, SYMBOLS.FileEndOfFileInfo, length,
    )

    # Close the handle
    # This is necessary since we use a single process
    # for running all the commands from a single test case
    win32file.CloseHandle(handle)


def set_file_time(path, creation_time, last_access_time, last_write_time):
    # First windows API call
    handle = win32file.CreateFileW(
        path,
        SYMBOLS.GENERIC_WRITE,
        SYMBOLS.FILE_SHARE_READ | SYMBOLS.FILE_SHARE_WRITE | SYMBOLS.FILE_SHARE_DELETE,
        None,
        SYMBOLS.OPEN_EXISTING,
        SYMBOLS.FILE_FLAG_OPEN_REPARSE_POINT | SYMBOLS.FILE_FLAG_BACKUP_SEMANTICS,
        0,
    )

    # Prepare arguments
    def prepare(x):
        if x == 0:
            return None
        if isinstance(x, int):
            from datetime import timezone

            x = datetime(year=x, month=1, day=1, tzinfo=timezone.utc)
        return x

    creation_time = prepare(creation_time)
    last_access_time = prepare(last_access_time)
    last_write_time = prepare(last_write_time)

    # Second windows API call
    assert handle != win32file.INVALID_HANDLE_VALUE
    win32file.SetFileTime(
        handle, creation_time, last_access_time, last_write_time,
    )

    # Close the handle
    # This is necessary since we use a single process
    # for running all the commands from a single test case
    win32file.CloseHandle(handle)


OPERATIONS = {
    "CreateFile": create_file,
    "DeleteFile": delete_file,
    "GetFileInformation": get_file_information,
    "SetFileAttributes": set_file_attributes,
    "CreateDirectory": create_directory,
    "RemoveDirectory": remove_directory,
    "FindFiles": find_files,
    "MoveFileEx": move_file_ex,
    "SetEndOfFile": set_end_of_file,
    "SetFileTime": set_file_time,
}


# Test helpers


def unique_name():
    return f"%s\\{uuid.uuid4()}"


def expect(base_path, runner, cmd, expected):
    """Test routine that complies with the semantics of the winfstest test cases

    Return a tuple corresponding to: (errno, <result(s) iterable>)
    """
    expected = expected or None
    print(f"** Running command:")
    print(f"-> {cmd}")
    print(f"-> Expecting: {expected}")

    args = cmd.split()
    kwargs = {}
    if args[0] == "-e":
        args = args[1:]
        kwargs["raise_last_error"] = True

    def parse(x):
        if x.startswith("%s"):
            return x % base_path
        try:
            dt = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return eval(x, SYMBOL_DICT)

    operation = OPERATIONS[args[0]]
    args = list(map(parse, args[1:]))

    if not expected or callable(expected):
        result = runner(operation, *args, **kwargs)
        print(f"-> Got: {result}")
        if callable(expected):
            assert expected((result,))

        if not isinstance(result, list):
            result = (result,)
        return None, result

    with pytest.raises(pywintypes.error) as context:
        runner(operation, *args, **kwargs)

    errno, _, message = context.value.args
    print(f"-> Got: errno={errno}, message={message!r}")
    assert errno == getattr(winerror, expected), f"Expected {expected}, got {message}"
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
    "test_module_path", TEST_MODULES, ids=[path.name for path in TEST_MODULES],
)
def test_winfs(test_module_path, file_system_path, process_runner):
    module_number = int(test_module_path.name[:2])

    # Test with concurrent accesses or security descriptors are currently not supported
    if module_number > 7:
        pytest.xfail()

    do_expect = partial(expect, file_system_path, process_runner)
    globs = {
        "uniqname": unique_name,
        "expect": do_expect,
        "testeval": assert_,
        "testdone": lambda: None,
    }
    test_module = open(test_module_path).read()

    print(f"Running test module {test_module_path.name}:")
    print("```")
    print(test_module)
    print("```")

    test_module = test_module.replace("from winfstest import *", "")
    exec(test_module, globs)
