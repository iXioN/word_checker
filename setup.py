#!/usr/bin/python
# -*- coding: utf-8 -*-

""" word_checker setup.py script """

# word_checker
# Version
from os.path import abspath, dirname, join

try:
    __version__=file(join(root, "version")).readline().rstrip().rstrip("\n")
except Exception, e:
    print "Warning, cannot read version file (%s)" % e
    __version__="0.0.1"
    
# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name="word_checker",
    version=__version__,
    description='a simple python word checker',
    author='Antonin Lacombe',
    author_email='antonin.lacombe@gmail.com',
   package_dir={"word_checker" : "src/word_checker"},
    url='https://github.com/iXioN/word_checker',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
      ],
)
