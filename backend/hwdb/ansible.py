"""Ansible configuration generation."""

from collections import defaultdict
from configparser import ConfigParser

from hwdb.enumerations import OperatingSystem, Type


__all__ = ['AnsibleMixin']


BLOCK_SIZE = 50


class AnsibleMixin:
    """Mixin for providing methods for ansible configuration."""

    @classmethod
    def ansible_groups(cls, block_size=BLOCK_SIZE):
        """Returns ansible groups."""
        groups = defaultdict(list)
        ddb_block = 0

        for index, system in enumerate(cls, start=1):
            groups['systems'].append(system)

            if system.operating_system == OperatingSystem.ARCH_LINUX:
                groups['linux-systems'].append(system)
            else:   # Probably a Windows system.
                groups['windows-systems'].append(system)

            if system.deployment:
                if system.deployment.type == Type.DDB:
                    groups['DDB'].append(system)

                    if block_size is not None:
                        if index % block_size == 0:
                            ddb_block += 1

                        groups[f'ddb-block-{ddb_block}'].append(system)
                else:   # Probably an E-TV or E-TV touch.
                    groups['E-TV'].append(system)

        return groups

    @classmethod
    def ansible_hosts(cls, block_size=BLOCK_SIZE, config_parser=None):
        """Returns a config parser for ansible hosts."""
        if not config_parser:
            config_parser = ConfigParser(allow_no_value=True)

        groups = cls.ansible_groups(block_size=block_size)

        for group, systems in groups.items():
            config_parser.add_section(group)

            for system in systems:
                config_parser.set(group, system.vpn_hostname)

        return config_parser