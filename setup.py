#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='terminallib',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    packages=['terminallib'],
    scripts=[
        'files/termutil',
        'files/terminals',
        'files/chksync',
        'files/bindcfg-gen',
        'files/openvpncfg-gen'],
    data_files=[
        ('/usr/share/terminals',
         ['files/openvpn.conf.temp', 'files/pacman.conf.temp'])],
    description=("HOMEINFO's terminal libary."))
