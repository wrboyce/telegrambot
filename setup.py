#!/usr/bin/env python
""" Copyright 2015 Will Boyce """
from setuptools import setup, find_packages

import telegrambot


setup(
    name='telegrambot',
    version=telegrambot.__version__,
    description='Pluggable Python Telegram Bot',
    long_description=file('README.rst').read(),
    author='Will Boyce',
    author_email='me@willboyce.com',
    url='https://www.github.com/wrboyce/telegrambot',
    license='License :: OSI Approved :: Apache Software License',
    install_requires=['humanize', 'requests'],
    packages=find_packages(),
    package_data={'': ['README.md', 'README.rst', 'LICENCE']},
    include_package_data=True,
    entry_points={'console_scripts': ['telegrambot = telegrambot.cli:main']},
    platforms=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
)
