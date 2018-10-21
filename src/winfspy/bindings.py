import os
import time

from .utils import get_winfsp_dir
from .ntstatus import NTSTATUS
from .filetime import filetime_now


# WinFSP's DLL is not available system-wide, so we have first to retrieve it
# (using either user-provided environ variable or the infamous windows
# registry) and customize the PATH environ variable before loading the
# bindings (themselves triggering the dynamic loading of WinFSP's DLL)

os.environ["PATH"] = f"{get_winfsp_dir('bin')};{os.environ.get('PATH')}"

from ._bindings import ffi, lib
