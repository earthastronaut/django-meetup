#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Install django-meetup 
AUTHOR: dylangregersen
DATE: Tue Sep 16 09:01:37 2014
"""
import os
import meetup
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

install_requires = open("requirements.txt").read().split("\n")
readme = open('README.rst').read()+"\nLicense\n-------\n"+open("LICENSE").read()

setup(
    name="django-meetup",
    version=meetup.__version__,
    packages=find_packages(),  
    include_package_data=True,  
    url="https://github.com/astrodsg/django-meetup",
    description="General purpose Django Meetup database to sync with Meetup.com.",
    long_description=readme,
    license="3-clause BSD style license",
    author="Dylan Gregersen",
    author_email = "gregersen.dylan@gmail.com",
    platforms=["any"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,    
)
