# Inspired by EventGhost Project <http://www.eventghost.org/> and
# @Mostafa-Hamdy-Elgiar on GithubGist with the Filetimes.py file

import time

# Win32 Epoch time is not the same as Unix Epoch time.
# Win32 Epoch time starts at 1/1/1601 00:00:00 where as
# Unix Epoch time starts January 1, 1970 00:00:00.
# Win32 Epoch time representation is also in hundreds of nanoseconds.
# So we need to have a couple of offsets to make the conversions

# this is the Win32 Epoch time for when Unix Epoch time started. It is in
# hundreds of nanoseconds.
EPOCH_AS_FILETIME = 116444736000000000

# This is the divider/multiplier for converting nanoseconds to
# seconds and vice versa
HUNDREDS_OF_NANOSECONDS = 10000000


def filetime_now():
    return int(time.time() * HUNDREDS_OF_NANOSECONDS) + EPOCH_AS_FILETIME
