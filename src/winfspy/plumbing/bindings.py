import os

from .get_winfsp_dir import get_winfsp_dir

# WinFSP's DLL is not available system-wide, so we have first to retrieve it
# (using either user-provided environ variable or the infamous windows
# registry) and customize the PATH environ variable before loading the
# bindings (themselves triggering the dynamic loading of WinFSP's DLL)

os.environ["PATH"] = f"{get_winfsp_dir('bin')};{os.environ.get('PATH')}"

from ._bindings import ffi, lib


def enable_debug_log():
    stderr_handle = lib.GetStdHandle(lib.STD_ERROR_HANDLE)
    lib.FspDebugLogSetHandle(stderr_handle)


__all__ = ("ffi", "lib")
