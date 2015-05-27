"""Terminal setup configuration"""

from configparser import ConfigParser

__all__ = ['db', 'monitoring', 'net', 'openvpn', 'pacman', 'screenshot', 'ssh']

CONFIG_FILE = '/usr/local/etc/terminals.conf'
config = ConfigParser()
config.read(CONFIG_FILE)

db = config['db']
monitoring = config['monitoring']
net = config['net']
openvpn = config['openvpn']
pacman = config['pacman']
screenshot = config['screenshot']
ssh = config['ssh']
