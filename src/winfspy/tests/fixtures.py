import pathlib

import pytest
from winfspy.memfs import create_memory_file_system


def pytest_addoption(parser):
    try:
        parser.addoption(
            "--file-system-path",
            action="store",
            type=str,
            default=None,
            help="A path to the file system to test",
        )
        parser.addoption(
            "--enable-stream-tests", action="store_true", default=False, help="Enable stream tests",
        )
    # Options already added (via the pluging module)
    except ValueError:
        pass


def get_available_drive():
    for letter in "RSTUVWXYZ":
        path = pathlib.Path(f"{letter}:")
        if not path.exists():
            return path
    raise RuntimeError("No available drive found")


@pytest.fixture(params=["as_drive", "as_directory"])
def as_drive(request):
    return request.param == "as_drive"


@pytest.fixture()
def file_system_path(request, tmp_path, as_drive):
    path = request.config.getoption("--file-system-path")
    # Skip one as_drive parameter if file system path is provided
    if path and as_drive:
        pytest.skip()

    # Run with provided file system path
    if path:
        yield path
        return

    # Run a winfspy.memfs file system
    path = get_available_drive() if as_drive else tmp_path / "mountpoint"
    fs = create_memory_file_system(path, testing=True)
    fs.start()
    yield path
    fs.stop()


@pytest.fixture
def enable_stream_tests(request):
    option = request.config.getoption("--enable-stream-tests")
    return bool(option)


@pytest.fixture
def memfs_tests(request):
    option = request.config.getoption("--file-system-path")
    return not bool(option)
