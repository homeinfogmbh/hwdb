"""Library for terminal remote control."""

from contextlib import suppress
from subprocess import DEVNULL, CalledProcessError, check_call

from requests import ConnectionError, Timeout, put  # pylint: disable=W0622

from terminallib.config import CONFIG, LOGGER
from terminallib.exceptions import SystemOffline, TerminalConfigError


__all__ = ['RemoteControllerMixin']


PORT = 8000


class BasicControllerMixin:
    """Controls a terminal remotely."""

    @property
    def ipv4address(self):
        """Returns the system's IPv4 address."""
        try:
            return self.openvpn.ipv4address
        except AttributeError:
            raise TerminalConfigError('Terminal has no OpenVPN address.')

    @property
    def url(self):
        """Returns the system's URL."""
        return f'http://{self.ipv4address}:{PORT}'

    @property
    def online(self):
        """Checks whether the system is online."""
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

    def put(self, json, *, timeout=10):
        """Executes a PUT request."""
        url = self.url
        LOGGER.debug('Executing PUT request on %s with JSON:\n%s', url, json)

        try:
            return put(url, json=json, timeout=timeout)
        except ConnectionError:
            raise SystemOffline()

    def exec(self, command, *, _timeout=10, **kwargs):
        """Runs the respective command."""
        json = dict(kwargs)
        json['command'] = command
        return self.put(json, timeout=_timeout)


class RemoteControllerMixin(BasicControllerMixin):
    """Enhanced controller functions."""

    def beep(self, *args):
        """Beeps the system."""
        return self.exec('beep', args=args)

    def unlock_pacman(self):
        """Safely removes the pacman lockfile."""
        return self.exec('unlock-pacman')

    def reboot(self):
        """Reboots the system."""
        with suppress(Timeout):
            return self.exec('reboot')

    def application(self, state=None):
        """Manages the application.
        state=True: Enables the application
        state=False: Disables the application
        state=None: Queries the application state.
        """
        return self.exec('application', state=state)
