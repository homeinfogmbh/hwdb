"""Library for terminal pacman.conf management"""

from .config import pacman, net
from .abc import TerminalAware
from .ctrl import RemoteController

__all__ = ['PacmanConfig']


class PacmanConfig(TerminalAware):
    """Renders the pacman.conf file for a terminal"""

    def get(self):
        """Returns the rendered configuration file"""
        with open(pacman['TEMPLATE'], 'r') as temp:
            pacman_conf = temp.read()
        pacman_conf = pacman_conf.replace('<addr>', net['IPV4ADDR'])
        pacman_conf = pacman_conf.replace('<port>', net['HTTP_PRIV_PORT'])
        return pacman_conf


class Pacman(TerminalAware):
    """Wrapper for remote pacman access"""

    def __init__(self, terminal):
        """Initializes the remote controller"""
        super().__init__(terminal)
        self._remote = RemoteController(terminal)

    @property
    def _refresh_cmd(self):
        """Returns the refresh command"""
        return [pacman['BINARY'], pacman['REFRESH_CMD']]

    @property
    def _update_cmd(self):
        """Returns the refresh command"""
        return [pacman['BINARY'], pacman['UPDATE_CMD']]

    def refresh(self):
        """Refresh repository"""
        _, _, exit_code = self._remote.execute(self._refresh_cmd)
        return True if not exit_code else False

    @property
    def updates(self):
        """Yields available updates"""
        stdout, stderr, exit_code = self._remote.execute(self._update_cmd)
        if exit_code == 0:
            try:
                out_str = stdout.decode()
            except:
                pass    # TODO: handle error
            else:
                for line in out_str.split('\n'):
                    line = line.strip()
                    try:
                        pkg, old_ver, _, new_ver = line.split(' ')
                    except ValueError:
                        continue
                    else:
                        yield (pkg, old_ver, new_ver)
        elif exit_code == 1:
            pass    # TODO: No updates available
        else:
            print(stderr.decode())    # TODO: Error!
