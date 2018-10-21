# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

# inspired by @Mostafa-Hamdy-Elgiar on GithubGist with the Filetimes.py file

from __future__ import print_function

import ctypes
from ctypes.wintypes import DWORD

from datetime import datetime
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


# I coded this in a way that is going to make doing these time conversions
# really easy. The FILETIME class is a python version of the
# C Windows datatype structure. this can be used for this purpose for setting
# and getting filetimes. This class can be constructed with no values passed.
# then using ctypes.byref() the instance can be passed to the
# Kernel32.GetFileTime function. then by using one of the properties the
# conversions are made.

# You can also supply values on construction so the class can be passed to
# set the filetime as well.
# the constructor accepts 2 parameters. Most of the time you will only pass a
# single value. The values passed can be

# low byte 32 bit integer, high byte 32bit integer

# this is what Windows uses and stores in this structure. I did this so if
# needed the values can be set

# 64 bit integer (long)
# this can be either a float/int of the Unix Epoch time,
# or the Windows Epoch Time. an easy way of getting the time and passing it
# FILETIME(time.time())

# time.time_struct instance
# This example you would not do but for the sake of example the time.time()
# returns the current time since the Unix Epoch in float(seconds). the
# time.localtime() accepts the float and returns a time.time_struct instance
# so if you were storing times for some reason. you could store them as
# int/float(seconds) and using localtime create the time.time_struct instance.
# FILETIME(time.localtime(time.time()))

# datetime.datetime instance,
# same kind of a thing as the above 2 examples.
# FILETIME(datetime.datetime.now())

# passing anything to the constructor is almost only going to be done if you
# are going to set the file time

# properties.
# unix_epoch_seconds
#      number of seconds since the Unix Epoch
# windows_epoch_seconds
#      number of seconds since the Windows Epoch
# unix_epoch_datetime
#      datetime.datetime instance
# seconds
#      same as unix_epoch_seconds
# minutes
#      number of minutes since Unix Epoch
# hours
#      number of hours since Unix Epoch
# days
#      number of days since Unix Epoch
# int(instance)
#      same as unix_epoch_seconds
# float(instance)
#      unix_epoch_seconds with fractions of a second
# str(instance)
#      formatted string representation of the time for your locale.


class _FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", DWORD), ("dwHighDateTime", DWORD)]

    def __init__(self, dwLowDateTime=None, dwHighDateTime=None):

        if dwLowDateTime is None and dwHighDateTime is None:
            super(_FILETIME, self).__init__()

        else:
            if dwHighDateTime is None:
                if isinstance(dwLowDateTime, datetime):
                    dwLowDateTime = time.mktime(datetime.now().timetuple())

                elif isinstance(dwLowDateTime, time.struct_time):
                    dwLowDateTime = time.mktime(dwLowDateTime)

                else:
                    try:
                        dwLowDateTime = dwLowDateTime.seconds
                    except AttributeError:
                        pass

                dwLowDateTime = int(dwLowDateTime)
                if (dwLowDateTime - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS < 0:
                    dwLowDateTime = (
                        dwLowDateTime * HUNDREDS_OF_NANOSECONDS
                    ) + EPOCH_AS_FILETIME

                dwHighDateTime = dwLowDateTime >> 32
                dwLowDateTime = dwLowDateTime - ((dwLowDateTime >> 32) << 32)

            self.dwLowDateTime = DWORD(dwLowDateTime)
            self.dwHighDateTime = DWORD(dwHighDateTime)

            super(_FILETIME, self).__init__(dwLowDateTime, dwHighDateTime)

    @property
    def unix_epoch_seconds(self):
        val = (self.dwHighDateTime << 32) + self.dwLowDateTime
        return (val - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS

    @property
    def windows_epoch_seconds(self):
        val = (self.dwHighDateTime << 32) + self.dwLowDateTime
        return val / HUNDREDS_OF_NANOSECONDS

    @property
    def unix_epoch_datetime(self):
        return datetime.utcfromtimestamp(self.unix_epoch_seconds)

    @property
    def seconds(self):
        return self.unix_epoch_seconds

    @property
    def minutes(self):
        return int(self.seconds / 60)

    @property
    def hours(self):
        return int(self.minutes / 60)

    @property
    def days(self):
        return int(self.hours / 24)

    def __int__(self):
        return self.unix_epoch_seconds

    def __float__(self):
        val = (self.dwHighDateTime << 32) + self.dwLowDateTime
        return (val - EPOCH_AS_FILETIME) / float(HUNDREDS_OF_NANOSECONDS)

    def __str__(self):
        dt = datetime.utcfromtimestamp(self.unix_epoch_seconds)
        return dt.strftime("%c")


FILETIME = _FILETIME
PFILETIME = ctypes.POINTER(_FILETIME)


def filetime_now():
    return FILETIME(time.time()).windows_epoch_seconds
