#! /usr/bin/env python3

from setuptools import setup

setup(
    name='hwdb',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
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
        'hwdb.tools'
    ],
    requires=[
        'configlib',
        'mdb',
        'peewee',
        'peeweeplus',
        'requests',
        'syslib'
    ],
    entry_points={
        'console_scripts': [
            'hwadm = hwdb.hwadm:main',
            'hwutil =  hwdb.hwutil:main'
        ]
    },
    data_files=[
        ('/usr/share/terminals', [
            'files/openvpn.conf.temp',
            'files/pacman.conf.temp',
            'files/homeinfo.intranet.zone.temp'
        ])
    ],
    description="HOMEINFO's hardware libary."
)
