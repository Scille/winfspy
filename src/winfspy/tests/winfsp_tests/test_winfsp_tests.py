import os
import shutil
import tempfile
import subprocess

import pytest
import pathlib

from winfspy.plumbing.get_winfsp_dir import get_winfsp_bin_dir
from . import WINFSP_TESTS_EXECUTABLE

MEMFS_XFAIL_LIST = [
    # GetFinalPathNameByHandle is not supported at the moment
    "getfileinfo_name_test",
    # Reparse point are not supported at the moment
    "reparse_guid_test",
    "reparse_nfs_test",
    # Require administrator priviledge
    "reparse_symlink_test",
    "reparse_symlink_relative_test",
]

MEMFS_AS_DIR_XFAIL_LIST = [
    "create_test",
    "getfileinfo_test",
    "getfileinfo_name_test",
    "getvolinfo_test",
]


def get_winfsp_tests_env():
    env = dict(os.environ)
    env["PATH"] = f"{get_winfsp_bin_dir()};{env.get('PATH')}"
    return env


def list_test_cases():
    result = subprocess.run(
        [WINFSP_TESTS_EXECUTABLE, "--external", "--list"],
        check=True,
        stdout=subprocess.PIPE,
        env=get_winfsp_tests_env(),
    )
    return result.stdout.decode().split()


TEST_CASES = list_test_cases()


@pytest.fixture
def file_system_tempdir(file_system_path):
    tempdir = tempfile.mkdtemp(dir=file_system_path, prefix="winfsp-tests-")
    tempdir = pathlib.Path(tempdir)
    yield tempdir
    shutil.rmtree(tempdir, ignore_errors=True)


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_winfsp_tests(test_case, file_system_tempdir, enable_stream_tests, memfs_tests, as_drive):
    if test_case.startswith("stream_") and not enable_stream_tests:
        pytest.skip()

    if memfs_tests and test_case in MEMFS_XFAIL_LIST:
        pytest.xfail()

    if memfs_tests and test_case.startswith("stream_"):
        pytest.xfail()

    if memfs_tests and not as_drive and test_case in MEMFS_AS_DIR_XFAIL_LIST:
        pytest.xfail()

    result = subprocess.run(
        [WINFSP_TESTS_EXECUTABLE, "--external", "--resilient", test_case],
        stdout=subprocess.PIPE,
        cwd=file_system_tempdir,
        env=get_winfsp_tests_env(),
    )
    print(result.stdout.decode())
    result.check_returncode()
