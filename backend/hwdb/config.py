"""Terminal setup configuration."""

from logging import getLogger

from configlib import loadcfg


__all__ = ['CONFIG', 'LOGGER', 'LOG_FORMAT']


CONFIG = loadcfg('hwdb.conf')
LOGGER = getLogger('hwdb')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
