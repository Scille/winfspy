import os
import sys
import winreg
import pathlib


def winreg_get_value(rootkey, keyname, valname):
    try:
        with winreg.OpenKey(rootkey, keyname, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
            return str(winreg.QueryValueEx(key, valname)[0])
    except WindowsError:
        return None


def get_winfsp_dir(suffix=None):
    """Return base winfsp directory.

    It's used in three places:
    - {winfsp_dir}\\inc: include directory for building the _bindings module
    - {winfsp_dir}\\lib: library directory for building the _bindings module
    - {winfsp_dir}\\bin: used to load the winfsp DLL at runtime

    This path is found using either:
    - the user-provided environ variable %WINFSP_LIBRARY_PATH%
    - the windows registry: `HKEY_LOCAL_MACHINE\\SOFTWARE\\WinFsp\\InstallDir`
    """
    path = os.environ.get("WINFSP_LIBRARY_PATH")

    if not path:
        path = winreg_get_value(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WinFsp", r"InstallDir")

    if not path:
        raise RuntimeError("The WinFsp library path is not provided")

    path = pathlib.Path(path)
    if not path.exists():
        raise RuntimeError(f"The provided WinFsp library path does not exist: {path}")

    return path / suffix if suffix else path


def get_winfsp_bin_dir():
    """Returns the directory containing the winfsp DLL to load.

    This path is found using either:
    - the user-provided environ variable %WINFSP_DEBUG_PATH% (for debugging purposes)
    - the `bin` directory in the base directory provided by `get_winfsp_dir``
    """
    path = os.environ.get("WINFSP_DEBUG_PATH")
    if path:
        path = pathlib.Path(path)
    else:
        path = get_winfsp_dir(suffix="bin")

    if not path.exists():
        raise RuntimeError(f"The provided WinFsp binary path does not exist: {path}")

    return path


def get_winfsp_library_name():
    # See:
    # https://docs.python.org/3/library/platform.html#platform.architecture
    is_64bits = sys.maxsize > 2 ** 32
    return "winfsp-" + ("x64" if is_64bits else "x86")
