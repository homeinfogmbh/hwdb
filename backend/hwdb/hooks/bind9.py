"""Generates bind9 configuration for HOMEINFO's VPN networks."""

from logging import getLogger
from os import linesep
from pathlib import Path
from subprocess import CalledProcessError
from typing import Iterator

from hwdb.orm.system import System
from hwdb.system import root, systemctl


__all__ = ['bind9cfgen']


BIND9_SERVICE = 'bind9.service'
DNS_CONFIG = Path('/etc/bind/homeinfo.intranet.zone')
DNS_TEMPLATE = Path('/usr/share/terminals/homeinfo.intranet.zone.temp')
IN_A_RECORD = '{}\tIN\tA\t{}'
IN_AAAA_RECORD = '{}\tIN\tAAAA\t{}'
LOCAL_HOSTS_LIST = Path('/usr/local/etc/local_hosts')
LOGGER = getLogger('bind9')


def management_hosts() -> Iterator[str]:
    """Renders management network hosts."""

    try:
        with LOCAL_HOSTS_LIST.open('r', encoding='utf-8') as file:
            yield ';# Management network hosts\n'

            for line in file:
                if (line := line.strip()) and not line.startswith('#'):
                    yield IN_A_RECORD.format(*line.split())
    except FileNotFoundError:
        return


def terminal_hosts() -> Iterator[str]:
    """Renders terminal network hosts."""

    yield ';# Terminal network hosts\n'

    for system in System.select(cascade=True).where(True):
        try:
            ipv4address = system.openvpn.ipv4address
        except AttributeError:
            LOGGER.warning('No OpenVPN config for #%i.', system.id)
        else:
            yield IN_A_RECORD.format(system.hostname, ipv4address)

        if system.ipv6address is not None:
            yield IN_AAAA_RECORD.format(system.hostname, system.ipv6address)
        else:
            LOGGER.warning('No WireGuard config for #%i.', system.id)


@root(LOGGER)
def bind9cfgen() -> bool:
    """Runs generates the confi files."""

    with DNS_TEMPLATE.open('r', encoding='utf-8') as temp:
        template = temp.read()

    management = linesep.join(management_hosts())
    terminals = linesep.join(terminal_hosts())
    config = template.format(
        file=__file__, management=management, terminals=terminals)

    with DNS_CONFIG.open('w', encoding='utf-8') as dns_cfg:
        dns_cfg.write(config)

    LOGGER.info('Restarting bind9 service.')

    try:
        systemctl('restart', BIND9_SERVICE)
    except CalledProcessError:
        return False

    return True
