#!/usr/bin/python

# SetEndOfFile
# truncation behavior for TRUNCATE_EXISTING, OPEN_ALWAYS, CREATE_ALWAYS, OPEN_EXISTING

from winfstest import *

name = uniqname()

expect("CreateFile %s GENERIC_WRITE 0 0 CREATE_ALWAYS FILE_ATTRIBUTE_NORMAL 0" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 0)
expect("SetEndOfFile %s 42" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 42)
expect("SetEndOfFile %s 13" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 13)
expect("DeleteFile %s" % name, 0)

expect("CreateFile %s GENERIC_WRITE 0 0 CREATE_ALWAYS FILE_ATTRIBUTE_NORMAL 0" % name, 0)
expect("SetEndOfFile %s 42" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 42)
expect("CreateFile %s GENERIC_WRITE 0 0 TRUNCATE_EXISTING 0 0" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 0)
expect("SetEndOfFile %s 42" % name, 0)
expect("CreateFile %s GENERIC_READ 0 0 TRUNCATE_EXISTING 0 0" % name, "ERROR_INVALID_PARAMETER")
expect("CreateFile %s GENERIC_WRITE 0 0 OPEN_ALWAYS FILE_ATTRIBUTE_NORMAL 0" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 42)
expect("CreateFile %s GENERIC_WRITE 0 0 OPEN_EXISTING FILE_ATTRIBUTE_NORMAL 0" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 42)
expect("CreateFile %s GENERIC_WRITE 0 0 CREATE_ALWAYS FILE_ATTRIBUTE_NORMAL 0" % name, 0)
expect("GetFileInformation %s" % name, lambda r: r[0]["FileSize"] == 0)
expect("DeleteFile %s" % name, 0)

testdone()
