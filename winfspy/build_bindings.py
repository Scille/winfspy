import os
import sys
from cffi import FFI

# see: https://docs.python.org/3/library/platform.html#platform.architecture
is_64bits = sys.maxsize > 2 ** 32


BASEDIR = os.path.dirname(os.path.abspath(__file__))

# import `get_winfsp_dir` the violent way to avoid dependency on __init__.py
exec(open(f"{BASEDIR}/utils.py").read())
WINFSP_DIR = get_winfsp_dir()


ffibuilder = FFI()


ffibuilder.set_source(
    "winfspy._bindings",
    """
    #include <winfsp/winfsp.h>
    """,
    include_dirs=[f"{WINFSP_DIR}/inc"],
    libraries=["winfsp-" + ("x64" if is_64bits else "x86")],
    library_dirs=[f"{WINFSP_DIR}/lib"],
)


with open(BASEDIR + "/winfsp.cdef.h") as fd:
    ffibuilder.cdef(fd.read())


if __name__ == "__main__":
    ffibuilder.compile()
