#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='terminallib',
    version='1.0.0',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    packages=['terminallib',
              'terminallib.db'],
    requires=['peewee'],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
