===============================
WinFSPy
===============================

.. image:: https://ci.appveyor.com/api/projects/status/jg07bt75a9r78ou4/branch/master?svg=true
        :target: https://ci.appveyor.com/project/touilleMan/winfspy/branch/master
        :alt: Appveyor CI Status

.. image:: https://codecov.io/gh/Scille/winfspy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Scille/winfspy

.. image:: https://img.shields.io/pypi/v/winfspy.svg
        :target: https://pypi.python.org/pypi/winfspy
        :alt: Pypi Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black
        :alt: Code style: black

Bindings for `WinFSP <http://www.secfs.net/winfsp/>`_ version 1.4 and onward.

Winfspy consists of three important modules:

- ``winfspy``: expose the WinFSP API
- ``winfspy.memfs``: a memory file system based on winfspy
- ``winfspy.tests.winfsp_tests``: a test suite for black box testing
- ``winfspy.tests.winfstest``: a lighter test suite for black box testing


Requirements and installation
-----------------------------

`WinFSP <http://www.secfs.net/winfsp/>`_ version 1.4 or higher has to be installed separately.

Then install winfspy using pip::

    $ pip install winfspy


WinFSP python API
-----------------

Usage::

    from winfspy import (
        FileSystem,
        BaseFileSystemOperations,
        enable_debug_log,
        FILE_ATTRIBUTE,
        CREATE_FILE_CREATE_OPTIONS,
        NTStatusObjectNameNotFound,
        NTStatusDirectoryNotEmpty,
        NTStatusNotADirectory,
        NTStatusObjectNameCollision,
        NTStatusAccessDenied,
        NTStatusEndOfFile,
    )


Winfspy memory file system
---------------------------

Usage::

    # Run the memory fs as X: drive in verbose mode
    $ python -m winfspy.memfs X: -v

    # More information
    $ python -m winfspy.memfs


Winfsp-tests test suite
-----------------------

This test suite integrates the external test suite of
`winfsp-tests <https://github.com/billziss-gh/winfsp/tree/master/tst/winfsp-tests>`_.

Usage::

    # Install winfspy with the test dependencies
    $ pip install winfspy[test]

    # Run the winfstest test suite on an existing X: drive
    $ python winfspy.tests.winfsp_tests --file-system-path X:

    # More information about pytest
    $ python winfspy.tests.winfsp_tests -h


Winfstest test suite
--------------------

This test suite is taken from
`secfs.test.winfstest <https://bitbucket.org/billziss/secfs.test/>`_.
It is basic yet useful to test common use cases.

Usage::

    # Install winfspy with the test dependencies
    $ pip install winfspy[test]

    # Run the winfstest test suite on an existing X: drive
    $ python winfspy.tests.winfstest --file-system-path X:

    # More information about pytest
    $ python winfspy.tests.winfstest -h


License
-------

Free software: BSD
