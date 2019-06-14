"""Post DB transaction hooks."""

from terminallib.hooks.bind9 import bind9cfgen
from terminallib.hooks.nagios import nagioscfgen
from terminallib.hooks.openvpn import openvpncfgen


__all__ = ['HOOKS', 'bind9cfgen', 'nagioscfgen', 'openvpncfgen']


HOOKS = {
    'bind9': bind9cfgen,
    'nagios': nagioscfgen,
    'openvpn': openvpncfgen
}
