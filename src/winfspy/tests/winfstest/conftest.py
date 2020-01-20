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
    # Option already added (via the pluging module)
    except ValueError:
        pass


def get_available_drive():
    for letter in "RSTUVWXYZ":
        path = pathlib.Path(f"{letter}:")
        if not path.exists():
            return path
    raise RuntimeError("No available drive found")


@pytest.fixture
def file_system_path(request):
    path = request.config.getoption("--file-system-path")
    if path:
        yield path
        return
    drive = get_available_drive()
    fs = create_memory_file_system(drive)
    fs.start()
    yield drive
    fs.stop()
