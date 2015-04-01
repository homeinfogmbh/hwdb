#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='terminallib',
    version='1.0.0',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    packages=['terminallib'],
    requires=['peewee'],
    data_files=[('/usr/local/etc', ['files/usr/local/etc/termgr.conf'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
