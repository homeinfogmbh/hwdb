#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='1.1.0-1',
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
        # Miscellaneous scripts
        ('/usr/lib/terminals',
         ['files/usr/lib/terminals/bindcfg-gen',
          'files/usr/lib/terminals/chkstats',
          'files/usr/lib/terminals/chksync',
          'files/usr/lib/terminals/openvpncfg-gen']),
        # Utilty script
        ('/usr/bin', ['files/usr/bin/termutil'])],
    description=("HOMEINFO's terminal libary"))
