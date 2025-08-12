"""Library for terminal remote control."""

from contextlib import suppress
from subprocess import DEVNULL, CalledProcessError, check_call
from typing import Optional
from urllib.parse import urljoin

from requests import Timeout, Response, get, post, put
from requests.exceptions import ChunkedEncodingError, ConnectionError

from hwdb.config import get_ping
from hwdb.enumerations import ApplicationMode
from hwdb.exceptions import SystemOffline
from hwdb.types import IPSocket


__all__ = ["RemoteControllerMixin"]


PORT_DIGSIGCLT = 8000
PORT_DIGSIGCTL = 5000


class BasicControllerMixin:
    """Controls a terminal remotely."""

    @property
    def socket(self) -> IPSocket:
        """Returns the IP socket."""
        if self.ddb_os:
            return IPSocket(self.ip_address, PORT_DIGSIGCTL)

        return IPSocket(self.ip_address, PORT_DIGSIGCLT)

    @property
    def url(self) -> str:
        """Returns the system's URL."""
        return f"http://{self.socket}"

    @property
    def online(self) -> bool:
        """Checks whether the system is online."""
        try:
            self.ping()
        except CalledProcessError:
            return False

        return True

    def ping(self, *, count: int = 3, timeout: Optional[int] = None) -> int:
        """Pings the system."""
        return check_call(
            [get_ping(), "-qc", str(count), str(self.ip_address)],
            stdout=DEVNULL,
            stderr=DEVNULL,
            timeout=timeout,
        )

    def endpoint_url(self, endpoint: Optional[str]) -> str:
        """Return the endpoint URL."""
        if endpoint is None:
            return self.url

        return urljoin(self.url, endpoint)

    def _get(
        self, *, endpoint: Optional[str] = None, timeout: Optional[int] = 10
    ) -> Response:
        """Executes a PUT request."""
        return get(self.endpoint_url(endpoint), timeout=timeout)

    def _post(
        self, json: dict, *, endpoint: Optional[str] = None, timeout: Optional[int] = 10
    ) -> Response:
        """Executes a PUT request."""
        return post(self.endpoint_url(endpoint), json=json, timeout=timeout)

    def _put(
        self, json: dict, *, endpoint: Optional[str] = None, timeout: Optional[int] = 10
    ) -> Response:
        """Executes a PUT request."""
        return put(self.endpoint_url(endpoint), json=json, timeout=timeout)

    def exec(
        self, command: str, *args: str, _timeout: Optional[int] = 10, **kwargs
    ) -> Response:
        """Runs the respective command."""
        if self.ddb_os:
            return self._post({command: None}, endpoint="/rpc", timeout=_timeout)

        json = {"args": args} if args else {}
        json.update(kwargs)
        json["command"] = command
        return self._put(json, timeout=_timeout)

    def sysinfo(self, *, timeout: Optional[int] = 10) -> Response:
        """Query system information."""
        if self.ddb_os:
            return self._get(endpoint="/sysinfo", timeout=timeout)

        return self._get()


class RemoteControllerMixin(BasicControllerMixin):
    """Enhanced controller functions."""

    def beep(self, *args: str) -> Response:
        """Beeps the system."""
        try:
            return self.exec("beep", args=args)
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error

    def unlock_pacman(self) -> Response:
        """Safely removes the pacman lockfile."""
        try:
            return self.exec("unlock-pacman")
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error

    def reboot(self) -> Optional[Response]:
        """Reboots the system."""
        with suppress(Timeout):
            try:
                return self.exec("reboot")
            except (ConnectionError, ChunkedEncodingError) as error:
                raise SystemOffline() from error

    def chromium_url(self) -> Response:
        """returns a Systems url from chromium perferences"""
        if self.ddb_os:
            return self._post({"url": None}, endpoint="/configuration", timeout=15)

    def application(self, mode: Optional[ApplicationMode] = None) -> Response:
        """Manages the application.
        state=None: Queries the application state.
        state=<else>: Set active application.
        """
        if mode is not None:
            mode = mode.name

        if self.ddb_os:
            if mode == "PRODUCTIVE":
                return self._post(
                    {"operationMode": "chromium"}, endpoint="/rpc", timeout=15
                )
            if mode == "INSTALLATION_INSTRUCTIONS":
                return self._post(
                    {"operationMode": "installationInstructions"},
                    endpoint="/rpc",
                    timeout=15,
                )
            return self._post({"operationMode": None}, endpoint="/rpc", timeout=15)

        try:
            return self.exec("application", mode=mode)
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error

    def screenshot(self, *, timeout: Optional[int] = 15) -> Response:
        """Makes a screenshot."""
        try:
            if self.ddb_os:
                return self._get(endpoint="/screenshot", timeout=timeout)

            return self.exec("screenshot", _timeout=timeout)
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error

    def apply_url(self, url: str, *, timeout: Optional[int] = 10) -> Response:
        """Set digital signage URL on new DDB OS systems."""
        try:
            return self._post({"url": url}, endpoint="/configure", timeout=timeout)
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error

    def restart_web_browser(self, *, timeout: Optional[int] = 10) -> Response:
        """Set digital signage URL on new DDB OS systems."""
        try:
            return self._post(
                {"restartWebBrowser": None}, endpoint="/rpc", timeout=timeout
            )
        except (ConnectionError, ChunkedEncodingError, Timeout) as error:
            raise SystemOffline() from error
