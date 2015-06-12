"""Terminal setup configuration"""

from configparser import ConfigParser

__all__ = ['db', 'net']

CONFIG_FILE = '/etc/terminals.conf'
config = ConfigParser()
config.read(CONFIG_FILE)

db = config['db']
net = config['net']
