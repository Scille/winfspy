import os
import re
import sys
from cffi import FFI

# from ._utils import get_winfsp_dir

# see: https://docs.python.org/3/library/platform.html#platform.architecture
is_64bits = sys.maxsize > 2 ** 32


BASEDIR = os.path.dirname(os.path.abspath(__file__))

# import `get_winfsp_dir` the violent way given winfspy cannot be loaded yet
exec(open(f"{BASEDIR}/../winfspy/utils.py").read())
WINFSP_DIR = get_winfsp_dir()


def strip_by_shaif(src):
    kept_src = []
    skipping = 0
    for line_count, line in enumerate(src.split("\n")):
        requirement = re.match(r"^#if(.*)", line)
        if requirement:
            # TODO: find a way to get WinFSP version...
            if not eval(requirement.groups()[0], {}, {"WINFSP_VERSION": 0}):
                skipping += 1
            continue
        elif re.match(r"^#endif", line):
            skipping -= 1
            assert skipping >= 0, f"Error at line {line_count}: {line}"
            continue
        if not skipping:
            kept_src.append(line)
    assert skipping == 0, "#if and #endif not equally balanced"
    return "\n".join(kept_src)


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
    ffibuilder.cdef(strip_by_shaif(fd.read()))


if __name__ == "__main__":
    ffibuilder.compile()
