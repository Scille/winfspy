#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


os.chdir(os.path.dirname(sys.argv[0]) or ".")


exec(open("src/winfspy/_version.py", encoding="utf-8").read())


test_requirements = ["pytest==3.8.0", "black==18.9b0"]


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
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["./src/_cffi_src/build_bindings.py:ffibuilder"],
    extras_require={"dev": test_requirements},
    # for cffi
    zip_safe=False,
)
