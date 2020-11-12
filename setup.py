#!/usr/bin/python
# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SubRenamerQt",
    version="0.1",
    author="Zhang Zongyu",
    author_email="zongyu@novazy.net",
    description="Rename subtitle files intuitively",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6-6-6/SubRenamerQt",
    package_dir={'': 'src'},
    packages=["SubRenamerQt"],
    scripts=["bin/SubRenamerQt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["PyQt5"],
    python_requires='>=3.7',
)
