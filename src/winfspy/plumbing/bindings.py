import os
import sys
from ctypes.util import find_library

from .get_winfsp_dir import get_winfsp_bin_dir, get_winfsp_library_name

# WinFSP's DLL is not available system-wide, so we have to first retrieve it
# (using either user-provided environ variable or the infamous windows
# registry) and use the dedicated python call `os.add_dll_directory`
# to add the `bin` path to the DLL search path. If the python version is lower
# than 3.8, `os.add_dll_directory` is not available and we have to fallback
# to the old way of adding a dll directory: customize the PATH environ
# variable.

WINFSP_BIN_DIR = get_winfsp_bin_dir()

# Modifiy %PATH% in any case as it is used by `ctypes.util.find_library`
os.environ["PATH"] = f"{WINFSP_BIN_DIR};{os.environ.get('PATH')}"
if sys.version_info >= (3, 8):
    os.add_dll_directory(WINFSP_BIN_DIR)

if not find_library(get_winfsp_library_name()):
    raise RuntimeError(f"The WinFsp DLL could not be found in {WINFSP_BIN_DIR}")

try:
    from ._bindings import ffi, lib  # noqa
except Exception as exc:
    raise RuntimeError(f"The winfsp binding could not be imported\n{exc}")


def enable_debug_log():
    stderr_handle = lib.GetStdHandle(lib.STD_ERROR_HANDLE)
    lib.FspDebugLogSetHandle(stderr_handle)


__all__ = ("ffi", "lib")
