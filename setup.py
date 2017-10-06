#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.terminals',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    package_dir={'homeinfo': ''},
    packages=['homeinfo.terminals'],
    scripts=[
        'files/termutil',
        'files/chkstats',
        'files/chksync',
        'files/refresh-termstats',
        'files/bindcfg-gen',
        'files/openvpncfg-gen'],
    data_files=[
        ('/usr/share/terminals',
         ['files/openvpn.conf.temp',
          'files/pacman.conf.temp']),
        ('/usr/lib/systemd/system',
         ['files/refresh-termstats.service',
          'files/refresh-termstats.timer'])],
    description=("HOMEINFO's terminal libary."))
