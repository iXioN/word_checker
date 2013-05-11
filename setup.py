#!/usr/bin/python
# -*- coding: utf-8 -*-

""" word_checker setup.py script """

# word_checker
# Version
import sys
from setuptools import setup
from word_checker import __version__


setup(
    name="word_checker",
    version=__version__,
    description='a simple python word checker',
    license='LGPLv3',
    author='Antonin Lacombe',
    author_email='antonin.lacombe@gmail.com',
    package_dir={"word_checker" : "src/word_checker"},
    url='https://github.com/iXioN/word_checker',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
