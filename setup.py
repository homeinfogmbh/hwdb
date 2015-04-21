#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='1.0.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    packages=['homeinfo.terminals'],
    requires=['peewee'],
    data_files=[('/usr/local/etc', ['files/usr/local/etc/terminallib.conf'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
