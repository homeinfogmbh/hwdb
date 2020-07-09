#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='hwdb',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    packages=[
        'hwdb',
        'hwdb.hooks',
        'hwdb.hwadm',
        'hwdb.hwutil',
        'hwdb.orm',
        'hwdb.tools'],
    scripts=['files/hwadm', 'files/hwutil'],
    data_files=[
        ('/usr/share/terminals', [
            'files/openvpn.conf.temp',
            'files/pacman.conf.temp',
            'files/homeinfo.intranet.zone.temp'])],
    description=("HOMEINFO's hardware libary."))
