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
    data_files=[
        # Main configuration
        ('/etc', ['files/etc/terminals.conf']),
        # Nagios 3 templates
        ('/etc/nagios3/conf.d',
         ['files/etc/nagios3/conf.d/homeinfo-terminal.cfg',
          'files/etc/nagios3/conf.d/homeinfo-terminal-commands.cfg']),
        # Miscellaneous scripts
        ('/usr/lib/terminals',
         ['files/usr/lib/terminals/bind.gen',
          'files/usr/lib/terminals/chkstats',
          'files/usr/lib/terminals/chksync',
          'files/usr/lib/terminals/nagios-config.gen',
          'files/usr/lib/terminals/openvpn-client-config.gen']),
        # Template files
        ('/usr/share/terminals',
         ['files/usr/share/terminals/bind.zone.temp',
          'files/usr/share/terminals/nagios.contact.temp',
          'files/usr/share/terminals/nagios.contactgroup.temp',
          'files/usr/share/terminals/nagios.host.temp',
          'files/usr/share/terminals/nagios.hostgroup.temp',
          'files/usr/share/terminals/nagios.service.temp',
          'files/usr/share/terminals/nagios.servicegroup.temp',
          'files/usr/share/terminals/openvpn.conf.temp',
          'files/usr/share/terminals/pacman.conf.temp']),
        # Controller script
        ('/usr/bin', ['files/usr/bin/termutil'])],
    license=open('LICENSE.txt').read(),
    description=('Homeinfo Terminal Libary')
    )
