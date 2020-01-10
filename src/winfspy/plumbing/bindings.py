import os
import sys

from .get_winfsp_dir import get_winfsp_dir

# WinFSP's DLL is not available system-wide, so we have to first retrieve it
# (using either user-provided environ variable or the infamous windows
# registry) and use the dedicated python call `os.add_dll_directory`
# to add the `bin` path to the DLL search path. If the python version is lower
# than 3.8, `os.add_dll_directory` is not available and we have to fallback
# to the old way of adding a dll directory: customize the PATH environ
# variable.

if sys.version_info >= (3, 8):
    os.add_dll_directory(get_winfsp_dir("bin"))
else:
    os.environ["PATH"] = f"{get_winfsp_dir('bin')};{os.environ.get('PATH')}"

from ._bindings import ffi, lib  # noqa


def enable_debug_log():
    stderr_handle = lib.GetStdHandle(lib.STD_ERROR_HANDLE)
    lib.FspDebugLogSetHandle(stderr_handle)


__all__ = ("ffi", "lib")
