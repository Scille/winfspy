try:
    import pytest
    import win32api
except ImportError:
    raise ImportError(
        """\
The winfspy test dependencies (pytest, pywin32) are not installed.
Install them using `pip install winfspy[test]`.
"""
    )
else:
    del pytest, win32api
