#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='1.0.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    package_dir={'homeinfo': ''},
    requires=['peewee',
              'pyxb',
              'homeinfo.lib'],
    packages=['homeinfo.terminals'],
    data_files=[('/usr/local/etc', ['files/usr/local/etc/terminals.conf']),
                ('/usr/local/sbin',
                 ['files/usr/local/sbin/build-key-terminal',
                  'files/usr/local/sbin/hosts.gen',
                  'files/usr/local/sbin/monitoring-clients.gen',
                  'files/usr/local/sbin/openvpn-clients.gen']),
                ('/usr/local/share/terminals',
                 ['files/usr/local/share/terminals/pacman.conf.temp',
                  'files/usr/local/share/terminals/openvpn.conf.temp'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
