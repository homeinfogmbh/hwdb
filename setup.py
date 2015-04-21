#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='1.0.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    package_dir={'homeinfo': ''},
    packages=['homeinfo.terminals'],
    requires=['peewee'],
    data_files=[('/usr/local/etc', ['files/usr/local/etc/terminallib.conf']),
                ('/usr/local/sbin', ['files/usr/local/sbin/build-key-terminal']),
                ('/usr/local/share/terminals',
                 ['files/usr/local/share/terminals/pacman.conf.temp',
                  'files/usr/local/share/terminals/openvpn.conf.temp'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
