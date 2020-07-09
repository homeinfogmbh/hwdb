"""Post DB transaction hooks."""

from hwdb.hooks.bind9 import bind9cfgen
from hwdb.hooks.openvpn import openvpncfgen


__all__ = ['HOOKS', 'bind9cfgen', 'openvpncfgen']


HOOKS = {
    'bind9': bind9cfgen,
    'openvpn': openvpncfgen
}
