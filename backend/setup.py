#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='terminallib',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    packages=[
        'terminallib',
        'terminallib.hooks',
        'terminallib.orm',
        'terminallib.termadm',
        'terminallib.termutil',
        'terminallib.tools'],
    scripts=[
        'files/chkapp',
        'files/termadm',
        'files/termutil'],
    data_files=[
        ('/usr/share/terminals', [
            'files/openvpn.conf.temp',
            'files/pacman.conf.temp',
            'files/homeinfo.intranet.zone.temp'])],
    description=("HOMEINFO's terminal libary."))
