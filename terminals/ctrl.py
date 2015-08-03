"""Library for terminal remote control"""

from tempfile import NamedTemporaryFile
from itertools import chain

from homeinfo.lib.system import run, ProcessResult
from homeinfo.lib.signal import Signal
from homeinfo.lib.ipc import IPCClient
from homeinfo.lib.misc import Screenshot
from homeinfo.terminals.abc import TerminalAware

from .config import terminals_config

__all__ = ['RPCError', 'RemoteController', 'ZMQController']


class RPCError(Exception):
    """Indicated an error during a remote procedure call"""
    pass


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    def __init__(self, user, terminal, keyfile=None, white_list=None, bl=None):
        """Initializes a remote terminal controller"""
        super().__init__(terminal)
        self._user = user
        self._keyfile = keyfile
        # Commands white and black list
        self._white_list = white_list or []
        self._black_list = bl or []
        # FUrther options for SSH
        self._SSH_OPTS = {
            # Trick SSH it into not checking the host key
            'UserKnownHostsFile':
                terminals_config.ssh['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking':
                terminals_config.ssh['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call
            'ConnectTimeout': terminals_config.ssh['CONNECT_TIMEOUT']}

    @property
    def user(self):
        """Returns the user name"""
        return self._user

    @property
    def keyfile(self):
        """Returns the path to the SSH key file"""
        return self._keyfile or '/home/{0}/.ssh/terminals'.format(self.user)

    @property
    def _identity(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return '-i {0}'.format(self.keyfile)

    @property
    def _ssh_options(self):
        """Returns options for SSH"""
        return ' '.join([
            ' '.join(['-o', '='.join([key, self._SSH_OPTS[key]])])
            for key in self._SSH_OPTS])

    @property
    def _ssh_cmd(self):
        """Returns the SSH basic command line"""
        return ' '.join([terminals_config.ssh['SSH_BIN'], self._identity,
                         self._ssh_options])

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return '-e "{0}"'.format(self._ssh_cmd)

    @property
    def _user_host(self):
        """Returns the respective user@host string"""
        return '{0}@{1}'.format(self.user, self.terminal.ipv4addr)

    def _remote(self, cmd, *args):
        """Makes a command remote"""
        return ' '.join(chain([self._ssh_cmd, self._user_host, cmd], args))

    def _remote_file(self, src):
        """Returns a remote file path"""
        return '{0}:{1}'.format(self._user_host, src)

    def _rsync(self, dst, *srcs, options=None):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst
        """
        return ' '.join([terminals_config.ssh['RSYNC_BIN'], options,
                         self._remote_shell, ' '.join(srcs), dst])

    def _check_command(self, cmd):
        """Checks the command against the white- and blacklists"""
        if self._white_list is not None:
            if cmd not in self._white_list:
                return False
        if self._black_list is not None:
            if cmd in self._black_list:
                return False
        return True

    def execute(self, cmd, *args):
        """Executes a certain command on a remote terminal"""
        if self._check_command(cmd):
            return run(self._remote(cmd, *args), shell=True)
        else:
            return ProcessResult(3, stderr='Command not allowed.'.encode())

    def get(self, file, options=None):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self._rsync(
                tmp.name, [self._remote_file(file)], options=options)
            pr = run(rsync, shell=True)
            if pr:
                return tmp.read()
            else:
                return pr

    def send(self, dst, *srcs, options=None):
        """Gets a file from a remote terminal"""
        rsync = self._rsync(self._remote_file(dst), *srcs, options=options)
        # print('Executing:', rsync)
        pr = run(rsync, shell=True)
        # print('Result:', str(pr), pr.exit_code, pr.stdout, pr.stderr)
        return pr


class ZMQController():
    """Controls terminals via ZMQ"""

    def __init__(self, terminal, port, proto=None):
        """Initializes with a terminal"""
        self._terminal = terminal
        self._port = int(port)
        self._proto = proto or 'tcp'

    @property
    def terminal(self):
        """Returns a terminal ORM instance from the database"""
        return self._terminal

    @property
    def port(self):
        """Returns the remote control port"""
        return self._port

    @property
    def proto(self):
        """Returns the used protocol"""
        return self._proto

    @property
    def addr(self):
        """Returns the target terminal's IPv4 address"""
        return self.terminal.ipv4addr

    def screenshot(self, file_format='png', quality=75, thumbnail=False,
                   count=None, interval=None):
        """Yields screenshot files as byte streams"""
        screenshot = Screenshot(
            file_format, quality, thumbnail, count, interval)
        with IPCClient(self.port, proto=self.proto, addr=self.addr) as client:
            screenshot_command = repr(screenshot)
            reply = client.query(screenshot_command)
            try:
                msg = reply.decode()
            except ValueError:
                return reply
            else:
                if msg == Signal.NACK:
                    raise RPCError('Could not take remote screenshot')
                else:
                    raise RPCError('Got unexpected signal: {0}'.format(msg))

    def appreload(self, timeout=3000):
        """Reloads the application on the remote system"""
        with IPCClient(self.port, proto=self.proto, addr=self.addr) as client:
            reply = client.squery(Signal.RELOAD, timeout=timeout, linger=0)
            if reply == Signal.ACK:
                return True
            else:
                return False
