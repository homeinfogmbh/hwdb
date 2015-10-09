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
                ('/etc/nagios3/conf.d',
                 ['files/etc/nagios3/conf.d/homeinfo-terminal.cfg',
                  'files/etc/nagios3/conf.d/homeinfo-commands.cfg']),
                ('/usr/lib/terminals',
                 ['files/usr/lib/terminals/build-key-terminal',
                  'files/usr/lib/terminals/hosts.gen',
                  'files/usr/lib/terminals/nagios-config.gen',
                  'files/usr/lib/terminals/openvpn-client-config.gen']),
                ('/usr/share/terminals',
                 ['files/usr/share/terminals/pacman.conf.temp',
                  'files/usr/share/terminals/openvpn.conf.temp',
                  'files/usr/share/terminals/nagios.contact.temp',
                  'files/usr/share/terminals/nagios.contactgroup.temp',
                  'files/usr/share/terminals/nagios.hostgroup.temp',
                  'files/usr/share/terminals/nagios.terminal.temp']),
                ('/usr/bin', ['files/usr/bin/termutil'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
