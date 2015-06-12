"""Terminal setup configuration"""

from configparser import ConfigParser

__all__ = ['db', 'net', 'screenshot', 'ssh']

CONFIG_FILE = '/etc/terminals.conf'
config = ConfigParser()
config.read(CONFIG_FILE)

db = config['db']
net = config['net']
screenshot = config['screenshot']
ssh = config['ssh']
