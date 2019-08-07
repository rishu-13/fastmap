# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""
setup(
name="fastmap",
version="0.1",
description="Fastmap algorithm for embedding graphs in Eucledean space",
license="",
author="Rishabh Pandey",
author_email="rishabhp@usc.edu",
keywords='d3m_primitive',
#packages = ['corexcontinuous', 'corextext', ]
packages=find_packages(),
url='https://github.com/rishu-13/fastmap',
download_url='https://github.com/rishu-13/fastmap',
install_requires=[],
long_description=long_description,
include_package_data = True,
classifiers=[
"Programming Language :: Python",
"Programming Language :: Python :: 3.5",
    ], 
entry_points = {
'd3m.primitives': ['data_preprocessing.fast_map.DSBOX = fastmap_primitive:fastmap']
    }
)
