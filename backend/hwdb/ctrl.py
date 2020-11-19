"""Library for terminal remote control."""

from contextlib import suppress
from subprocess import DEVNULL, CalledProcessError, check_call

from requests import Timeout, Response, put
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError     # pylint: disable=W0622

from hwdb.config import CONFIG
from hwdb.exceptions import SystemOffline


__all__ = ['RemoteControllerMixin']


PORT = 8000


class BasicControllerMixin:
    """Controls a terminal remotely."""

    @property
    def url(self) -> str:
        """Returns the system's URL."""
        return f'http://{self.ipv4address}:{PORT}'

    @property
    def online(self) -> bool:
        """Checks whether the system is online."""
        try:
            self.ping()
        except CalledProcessError:
            return False

        return True

    def ping(self, *, count: int = 3) -> int:
        """Pings the system."""
        return check_call((
            CONFIG['binaries']['PING'], '-qc', str(count),
            str(self.ipv4address)), stdout=DEVNULL, stderr=DEVNULL)

    def put(self, json: dict, *, timeout: int = 10) -> Response:
        """Executes a PUT request."""
        try:
            return put(self.url, json=json, timeout=timeout)
        except (ConnectionError, ChunkedEncodingError) as error:
            raise SystemOffline() from error

    def exec(self, command: str, *args: str, _timeout: int = 10,
             **kwargs) -> Response:
        """Runs the respective command."""
        json = {'args': args} if args else {}
        json.update(kwargs)
        json['command'] = command
        return self.put(json, timeout=_timeout)


class RemoteControllerMixin(BasicControllerMixin):
    """Enhanced controller functions."""

    def beep(self, *args: str) -> Response:
        """Beeps the system."""
        return self.exec('beep', args=args)

    def unlock_pacman(self) -> Response:
        """Safely removes the pacman lockfile."""
        return self.exec('unlock-pacman')

    def reboot(self) -> Response:
        """Reboots the system."""
        with suppress(Timeout):
            return self.exec('reboot')

    def application(self, state: bool = None) -> Response:
        """Manages the application.
        state=True: Enables the application
        state=False: Disables the application
        state=None: Queries the application state.
        """
        return self.exec('application', state=state)

    def screenshot(self) -> Response:
        """Makes a screenshot."""
        return self.exec('screenshot', _timeout=None)
