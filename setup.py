#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


os.chdir(os.path.dirname(sys.argv[0]) or ".")


exec(open("src/winfspy/_version.py", encoding="utf-8").read())


requirements = open("requirements.txt").read().split("\n")


setup(
    name="winfspy",
    version=__version__,
    description="CFFI bindings for WinFSP",
    long_description=open("README.rst", "rt").read(),
    url="https://github.com/Scille/winfspy",
    author="Emmanuel Leblond",
    author_email="emmanuel.leblond@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["_cffi_src", "_cffi_src.*"]),
    install_requires=requirements,
    setup_requires=requirements,
    cffi_modules=["./src/_cffi_src/build_bindings.py:ffibuilder"],
    # for cffi
    zip_safe=False,
)
