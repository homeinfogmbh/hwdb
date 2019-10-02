"""Library for terminal remote control."""

from subprocess import DEVNULL, CalledProcessError, check_call

from requests import ConnectionError, Timeout, put  # pylint: disable=W0622

from terminallib.config import CONFIG, LOGGER
from terminallib.exceptions import SystemOffline, TerminalConfigError


__all__ = ['RemoteControllerMixin']


class RemoteControllerMixin:
    """Controls a terminal remotely."""

    @property
    def ipv4address(self):
        """Returns the system's IPv4 address."""
        try:
            return self.system.openvpn.ipv4address
        except AttributeError:
            raise TerminalConfigError('Terminal has no OpenVPN address.')

    @property
    def url(self):
        """Returns the system's URL."""
        return f'http://{self.ipv4address}'

    @property
    def is_online(self):
        """Pings the system."""
        try:
            self.ping()
        except CalledProcessError:
            return False

        return True

    def ping(self, *, count=3):
        """Pings the system."""
        return check_call((
            CONFIG['binaries']['PING'], '-qc', str(count),
            str(self.ipv4address)), stdout=DEVNULL, stderr=DEVNULL)

    def put(self, json):
        """Executes a PUT request."""
        url = self.url
        LOGGER.debug('Executing PUT request on %s with JSON:\n%s', url, json)

        try:
            return put(url, json=json)
        except (ConnectionError, Timeout):
            raise SystemOffline()

    def exec(self, command, **kwargs):
        """Runs the respective command."""
        json = dict(kwargs)
        json['command'] = command
        return self.put(json)
