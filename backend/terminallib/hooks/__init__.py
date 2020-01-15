"""Post DB transaction hooks."""

from terminallib.hooks.bind9 import bind9cfgen
from terminallib.hooks.openvpn import openvpncfgen


__all__ = ['HOOKS', 'bind9cfgen', 'openvpncfgen']


HOOKS = {
    'bind9': bind9cfgen,
    'openvpn': openvpncfgen
}
