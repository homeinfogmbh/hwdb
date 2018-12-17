"""Library for terminal remote control."""

from enum import Enum
from tempfile import NamedTemporaryFile

from syslib import run

from terminallib.common import TerminalAware
from terminallib.config import CONFIG
from terminallib.exceptions import InvalidCommand


__all__ = ['Backend', 'CustomSSHOptions', 'RemoteController']


def _get_sources(sources):
    """Returns the respective source paths as command line string."""

    return ' '.join("'{}'".format(source) for source in sources)


def _get_options(options):
    """Returns the respective options as command line string."""

    if not options:
        return ''

    return ' '.join(str(option) for option in options)


class Backend(Enum):
    """File transfer backend."""

    RSYNC = 'rsync'
    SCP = 'scp'

    def __str__(self):
        """Returns the backend name."""
        return self.value


class CustomSSHOptions:
    """Sets custom SSH options."""

    def __init__(self, options, remote_controller):
        """Sets the custom SSH options."""
        self.options = options
        self.remote_controller = remote_controller
        self.previous_options = {}

    def __enter__(self):
        """Spplies the custom SSH options."""
        self.previous_options = dict(self.remote_controller.ssh_options)
        self.remote_controller.ssh_options.update(self.options)

    def __exit__(self, *_):
        """Resets the custom SSH options."""
        self.remote_controller.ssh_options = self.previous_options


class RemoteController(TerminalAware):
    """Controls a terminal remotely."""

    def __init__(self, user, terminal, keyfile=None, white_list=None,
                 black_list=None, logger=None):
        """Initializes a remote terminal controller."""
        super().__init__(terminal, logger=logger)
        self.user = user
        self.keyfile = keyfile or '/home/{}/.ssh/terminals'.format(self.user)
        self.white_list = white_list    # May be None → allow all.
        self.black_list = black_list or []

        if self.terminal.connection:
            connect_timeout = self.terminal.connection.timeout
        else:
            connect_timeout = CONFIG['ssh']['CONNECT_TIMEOUT']

        self.ssh_options = {
            # Trick SSH it into not checking the host key.
            'UserKnownHostsFile': CONFIG['ssh']['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking': CONFIG['ssh']['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call.
            'ConnectTimeout': connect_timeout}

    @property
    def ssh_cmd(self):
        """Returns the SSH basic command line."""
        result = [CONFIG['ssh']['SSH_BIN'], '-i', self.keyfile]

        for option, value in self.ssh_options.items():
            result += ['-o', '{}={}'.format(option, value)]

        return result

    @property
    def remote_shell(self):
        """Returns the rsync remote shell."""
        return '-e "{}"'.format(' '.join(self.ssh_cmd))

    @property
    def user_host(self):
        """Returns the respective user@host string."""
        return '{}@{}'.format(self.user, self.terminal.ipv4addr)

    def remote(self, cmd, *args):
        """Makes a command remote."""
        yield from self.ssh_cmd
        yield self.user_host
        yield cmd
        yield from args

    def remote_file(self, src):
        """Returns a remote file path."""
        return "{}:'{}'".format(self.user_host, src)

    def extra_options(self, options):
        """Returns an CustomSSHOptions context
        manager for this terminal controller.
        """
        return CustomSSHOptions(options, self)

    def _file_transfer_command(self, binary, dst, *srcs, options=None):
        """Returns the respective file transfer command."""
        srcs = _get_sources(srcs)
        options = _get_options(options)
        cmd = (binary, options, self.remote_shell, srcs, dst)
        cmd = ' '.join(cmd)
        self.logger.debug(cmd)
        return cmd

    def rsync(self, dst, *srcs, options=None):
        """Returns an rsync command line to
        send or receive the respective files.
        """
        return self._file_transfer_command(
            CONFIG['ssh']['RSYNC_BIN'], dst, *srcs, options=options)

    def scp(self, dst, *srcs, options=None):
        """Returns an scp command line to
        send or receive the respective files.
        """
        return self._file_transfer_command(
            CONFIG['ssh']['SCP_BIN'], dst, *srcs, options=options)

    def check_command(self, cmd):
        """Checks the command against the white- and blacklists."""
        if cmd in self.black_list:
            return False

        return self.white_list is None or cmd in self.white_list

    def execute(self, cmd, *args, shell=False):
        """Executes a certain command on a remote terminal."""
        if self.check_command(cmd):
            if shell:
                remote_cmd = ' '.join(self.remote(cmd, *args))
            else:
                remote_cmd = tuple(self.remote(cmd, *args))

            self.logger.debug('Executing: "%s".', remote_cmd)
            return run(remote_cmd, shell=shell)

        raise InvalidCommand()

    def get(self, file, options=None):
        """Gets a file from a remote terminal."""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self.rsync(
                tmp.name, [self.remote_file(file)], options=options)
            result = run(rsync, shell=True)
            self.logger.debug(str(result))

            if result:
                return tmp.read()

            return result

    def send(self, dst, *srcs, backend=Backend.RSYNC, options=None):
        """Sends files to a remote terminal."""
        self.logger.debug('Using backend: %s.', backend)

        if backend == Backend.RSYNC:
            command = self.rsync(self.remote_file(dst), *srcs, options=options)
        elif backend == Backend.SCP:
            command = self.scp(self.remote_file(dst), *srcs, options=options)
        else:
            raise NotImplementedError()

        result = run(command, shell=True)
        self.logger.debug(str(result))
        return result

    def mkdir(self, directory, parents=False, binary='/usr/bin/mkdir'):
        """Creates a remote directory."""
        if parents:
            return self.execute(binary, '-p', str(directory))

        return self.execute(binary, str(directory))
