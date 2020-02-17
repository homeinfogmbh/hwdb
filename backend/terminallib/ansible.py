"""Ansible configuration generation."""

from collections import defaultdict
from configparser import ConfigParser

from terminallib.enumerations import OperatingSystem, Type


__all__ = ['AnsibleMixin']


BLOCK_SIZE = 50


class AnsibleMixin:
    """Mixin for providing methods for ansible configuration."""

    @classmethod
    def ansible_groups(cls, block_size=BLOCK_SIZE):
        """Returns ansible groups."""
        groups = defaultdict(list)
        block = 0

        for index, system in enumerate(cls, start=1):
            groups['systems'].append(system)

            if system.operating_system == OperatingSystem.ARCH_LINUX:
                groups['linux-systems'].append(system)
            else:   # Probably a Windows system.
                groups['windows-systems'].append(system)

            if system.deployment:
                if system.deployment.type == Type.DDB:
                    groups['DDB'].append(system)
                else:   # Probably an E-TV.
                    groups['E-TV'].append(system)

            if block_size is not None:
                if index % block_size == 0:
                    block += 1

                groups[f'block-{block}'].append(system)

        return groups

    @classmethod
    def ansible_hosts(cls, block_size=BLOCK_SIZE, config_parser=None):
        """Returns a config parser for ansible hosts."""
        if not config_parser:
            config_parser = ConfigParser(allow_no_value=True)

        for group, systems in cls.ansible_groups(block_size=block_size):
            config_parser.add_section(group)

            for system in systems:
                config_parser.set(group, str(system.openvpn.ipv4address))

        return config_parser
