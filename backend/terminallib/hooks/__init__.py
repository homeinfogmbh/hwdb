"""Post DB transaction hooks."""

from terminallib.hooks.bind9 import bind9cfgen
from terminallib.hooks.nagios import nagioscfgen
from terminallib.hooks.openvpn import openvpncfgen


__all__ = ['bind9cfgen', 'nagioscfgen', 'openvpncfgen', 'run']


def run():
    """Runs all hooks."""

    success_bind9 = bind9cfgen()
    success_nagios = nagioscfgen()
    success_openvpn = openvpncfgen()
    return success_bind9 and success_nagios and success_openvpn
