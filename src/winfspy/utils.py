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
    path = os.environ.get("WINFSP_LIBRARY_PATH")
    if not path:
        path = reg32_get_value(
            reg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WinFsp", r"InstallDir"
        )
    else:
        raise RuntimeError("Cannot find WinFsp library, is it installed ?")

    if path and suffix:
        path = os.path.join(path, suffix)

    return path
