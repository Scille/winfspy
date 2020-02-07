#!/usr/bin/env python
# Copyright (c) 2009, David Buxton <david@gasmark6.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Tools to convert between Python datetime instances and Microsoft times.
"""

import time
import ctypes
from datetime import datetime, timezone


# Win32 Epoch time is not the same as Unix Epoch time.
# Win32 Epoch time starts at 1/1/1601 00:00:00 where as
# Unix Epoch time starts January 1, 1970 00:00:00.
# Win32 Epoch time representation is also in hundreds of nanoseconds.
# So we need to have a couple of offsets to make the conversions

# http://support.microsoft.com/kb/167296
# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME

# This is the Win32 Epoch time for when Unix Epoch time started.
# It is in hundreds of nanoseconds.
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time

# Conversion factors (milliseconds and hundeds of nanoseconds)
MILLISECONDS = 1000 * 1000
MILLISEDCONDS_TO_HNS = 10


def time_ns():
    # Use time.time_ns since time.time() is not as precise
    try:
        return time.time_ns()
    # Python 3.6 compatibility: time.time_ns is not available
    except AttributeError:
        ctypes.pythonapi._PyTime_GetSystemClock.restype = ctypes.c_int64
        return ctypes.pythonapi._PyTime_GetSystemClock()


def dt_to_filetime(dt):
    """Converts a datetime to Microsoft filetime format.

    If the object is time zone-naive, it is forced to UTC before conversion.
    The resulting filetime is only precise to the milliseconds.

    >>> "%.0f" % dt_to_filetime(datetime(2009, 7, 25, 23, 0))
    '128930364000000000'
    >>> dt_to_filetime(datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc))
    116444736000000000
    >>> dt_to_filetime(datetime(1970, 1, 1, 0, 0))
    116444736000000000

    >>> now = datetime.now(timezone.utc)
    >>> assert filetime_to_dt(dt_to_filetime(now)) == now, now
    """
    # If naive datetime, assume UTC
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        dt = dt.replace(tzinfo=timezone.utc)
    milliseconds = int(dt.timestamp() * MILLISECONDS)
    return EPOCH_AS_FILETIME + MILLISEDCONDS_TO_HNS * milliseconds


def filetime_to_dt(ft):
    """Converts a Microsoft filetime number to a Python datetime.

    The resulting datetime is only precise to the milliseconds.
    The hundreds of nanoseconds information is lost during the conversion.

    >>> filetime_to_dt(116444736000000000)
    datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    >>> filetime_to_dt(128930364000000000)
    datetime.datetime(2009, 7, 25, 23, 0, tzinfo=datetime.timezone.utc)

    >>> now = filetime_now() // 10 * 10  # Only precise to the usec
    >>> assert dt_to_filetime(filetime_to_dt(now)) == now, now
    """
    milliseconds = (ft - EPOCH_AS_FILETIME) // MILLISEDCONDS_TO_HNS
    return datetime.fromtimestamp(milliseconds / MILLISECONDS, timezone.utc,)


def filetime_now():
    return time_ns() // 100 + EPOCH_AS_FILETIME


if __name__ == "__main__":
    import doctest

    doctest.testmod()
