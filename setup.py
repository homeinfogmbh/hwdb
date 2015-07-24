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
    data_files=[('/etc', ['files/etc/terminals.conf']),
                ('/usr/share/terminals',
                 ['files/usr/share/terminals/pacman.conf.temp',
                  'files/usr/share/terminals/openvpn.conf.temp',
                  'files/usr/share/terminals/nagios.contact.temp',
                  'files/usr/share/terminals/nagios.contactgroup.temp',
                  'files/usr/share/terminals/nagios.hostgroup.temp',
                  'files/usr/share/terminals/nagios.terminal.temp'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
