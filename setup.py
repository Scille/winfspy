#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


os.chdir(os.path.dirname(sys.argv[0]) or ".")


test_requirements = ["pytest==3.8.0", "black==18.9b0"]


setup(
    name="winfspy",
    version="0.1",
    description="CFFI bindings for WinFSP",
    long_description=open("README.rst", "rt").read(),
    url="https://github.com/Scille/winfspy",
    author="Emmanuel Leblond",
    author_email="emmanuel.leblond@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(),
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["./winfspy/build_bindings.py:ffibuilder"],
    test_requirements=test_requirements,
    extras_require={"dev": test_requirements},
)
