"""OpenVPN config generator."""

from logging import getLogger
from pathlib import Path
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622

from terminallib.hooks.common import root, systemctl
from terminallib.config import CONFIG
from terminallib.orm.system import System


__all__ = ['openvpncfgen']


LOGGER = getLogger('openvpn')
OPENVPN_SERVICE = 'openvpn-server@terminals.service'
TEMPLATE = '''
# Generated by openvpncfg-gen.
# DO NOT EDIT THIS FILE MANUALLY!
# System #{}.

ifconfig-push {} {}
'''     # Mandatory empty line at end of file.


def generate_config():
    """Generates the respective configuration files."""

    clients_dir = Path(CONFIG['OpenVPN']['clients_dir'])
    netmask = CONFIG['OpenVPN']['netmask']

    for system in System:
        openvpn = system.openvpn

        if openvpn is None:
            LOGGER.error('Terminal %i has no VPN configuration.', system.id)
            continue

        config_text = TEMPLATE.format(system.id, openvpn.ipv4address, netmask)
        file_name = openvpn.key or str(openvpn.id)
        file_path = clients_dir.joinpath(file_name)

        with file_path.open('w') as cfg:
            cfg.write(config_text)


@root(LOGGER)
def openvpncfgen():
    """Runs the OpenVPN config generator."""

    LOGGER.info('Generating configuration.')

    try:
        systemctl('restart', OPENVPN_SERVICE)
    except CalledProcessError:
        exit(1)

    exit(0)
