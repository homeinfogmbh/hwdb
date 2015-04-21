"""Terminal setup configuration"""

from configparser import ConfigParser

__date__ = '12.12.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['db', 'net', 'openvpn', 'pacman', 'screenshot', 'ssh']

CONFIG_FILE = '/usr/local/etc/terminallib.conf'
config = ConfigParser()
config.read(CONFIG_FILE)

db = config['db']
net = config['net']
openvpn = config['openvpn']
pacman = config['pacman']
screenshot = config['screenshot']
ssh = config['ssh']
