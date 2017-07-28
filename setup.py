#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='latest',
    author='Richard Neumann',
    package_dir={'homeinfo': ''},
    packages=['homeinfo.terminals'],
    data_files=[
        # Template files
        ('/usr/share/terminals',
         ['files/openvpn.conf.temp',
          'files/pacman.conf.temp']),
        # Executables
        ('/usr/local/bin',
         ['files/termutil',
          'files/chkstats',
          'files/chksync',
          'files/refresh-termstats']),
        ('/usr/local/sbin',
         ['files/bindcfg-gen',
          'files/openvpncfg-gen']),
        # Systemd units
        ('/usr/lib/systemd/system',
         ['files/refresh-termstats.service',
          'files/refresh-termstats.timer'])],
    description=("HOMEINFO's terminal libary"))
