#!/usr/bin/env python

from sys import version_info
from version import __version__

python_interpreter_version = version_info[0], version_info[1]
if python_interpreter_version >= (2, 7):
    from setuptools import setup
    name = "wiki.wiki_page_view"


setup(
    name=name,
    version=__version__,
    description="wiki page view",
    packages=["wiki_page_view"],
)
