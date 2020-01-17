import os
import winreg as reg


def reg32_get_value(rootkey, keyname, valname):
    key, val = None, None
    try:
        key = reg.OpenKey(rootkey, keyname, 0, reg.KEY_READ | reg.KEY_WOW64_32KEY)
        val = str(reg.QueryValueEx(key, valname)[0])
    except WindowsError:
        pass
    finally:
        if key is not None:
            reg.CloseKey(key)
    return val


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
        path = reg32_get_value(reg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WinFsp", r"InstallDir")
    else:
        raise RuntimeError("Cannot find WinFsp library, is it installed ?")

    if path and suffix:
        path = os.path.join(path, suffix)

    return path


def get_winfsp_bin_dir():
    """Returns the directory containing the winfsp DLL to load.

    This path is found using either:
    - the user-provided environ variable %WINFSP_DEBUG_PATH% (for debugging purposes)
    - the `bin` directory in the base directory provided by `get_winfsp_dir``
    """
    path = os.environ.get("WINFSP_DEBUG_PATH")
    return path if path else get_winfsp_dir(suffix="bin")
