#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='latest',
    author='Richard Neumann',
    package_dir={'homeinfo': ''},
    packages=['homeinfo.terminals'],
    data_files=[
        # Main configuration
        ('/etc', ['files/terminals.conf']),
        # Template files
        ('/usr/share/terminals',
         ['files/openvpn.conf.temp',
          'files/pacman.conf.temp']),
        # Executables
        ('/usr/bin',
         ['files/termutil',
          'files/bindcfg-gen',
          'files/chkstats',
          'files/chksync',
          'files/openvpncfg-gen'])],
    description=("HOMEINFO's terminal libary"))
