"""Library for terminal remote control."""

from tempfile import NamedTemporaryFile
from itertools import chain

from syslib import run, ProcessResult

from terminallib.common import TerminalAware
from terminallib.config import CONFIG

__all__ = ['RemoteController']


class CustomSSHOptions:
    """Sets custom SSH options."""

    def __init__(self, options, remote_controller):
        """Sets the custom SSH options."""
        self.options = options
        self.remote_controller = remote_controller
        self.previous_options = {}

    def __enter__(self):
        """Spplies the custom SSH options."""
        self.previous_options = {
            key: value for key, value in
            self.remote_controller.ssh_options.items()}
        self.remote_controller.ssh_options.update(self.options)

    def __exit__(self, *_):
        """Resets the custom SSH options."""
        self.remote_controller.ssh_options = self.previous_options


class RemoteController(TerminalAware):
    """Controls a terminal remotely."""

    def __init__(self, user, terminal, keyfile=None, white_list=None,
                 black_list=None, logger=None, debug=False):
        """Initializes a remote terminal controller."""
        super().__init__(terminal, logger=logger, debug=debug)
        self.user = user
        self.keyfile = keyfile or '/home/{}/.ssh/terminals'.format(self.user)
        self.white_list = white_list    # May be None → allow all.
        self.black_list = black_list or []
        self.debug = debug

        if self.terminal.connection:
            connect_timeout = self.terminal.connection.timeout
        else:
            connect_timeout = CONFIG['ssh']['CONNECT_TIMEOUT']

        self.ssh_options = {
            # Trick SSH it into not checking the host key
            'UserKnownHostsFile': CONFIG['ssh']['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking': CONFIG['ssh']['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call
            'ConnectTimeout': connect_timeout}

    @property
    def identity(self):
        """Returns the SSH identity file argument
        with the respective identity file's path.
        """
        return '-i {}'.format(self.keyfile)

    @property
    def ssh_options_params(self):
        """Returns options for SSH."""
        for option, value in self.ssh_options.items():
            yield '-o {}={}'.format(option, value)

    @property
    def ssh_cmd(self):
        """Returns the SSH basic command line."""
        return '{} {} {}'.format(
            CONFIG['ssh']['SSH_BIN'], self.identity,
            ' '.join(self.ssh_options_params))

    @property
    def remote_shell(self):
        """Returns the rsync remote shell."""
        return '-e "{}"'.format(self.ssh_cmd)

    @property
    def user_host(self):
        """Returns the respective user@host string."""
        return '{}@{}'.format(self.user, self.terminal.ipv4addr)

    def remote(self, cmd, *args):
        """Makes a command remote."""
        return ' '.join(chain([self.ssh_cmd, self.user_host, cmd], args))

    def remote_file(self, src):
        """Returns a remote file path."""
        return "{}:'{}'".format(self.user_host, src)

    def extra_options(self, options):
        """Returns an CustomSSHOptions context
        manager for this terminal controller.
        """
        return CustomSSHOptions(options, self)

    def rsync(self, dst, *srcs, options=None):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst.
        """
        srcs = ' '.join("'{}'".format(src) for src in srcs)
        options = '' if options is None else options
        cmd = '{} {} {} {} {}'.format(
            CONFIG['ssh']['RSYNC_BIN'], options, self.remote_shell, srcs, dst)
        self.logger.debug(cmd)
        return cmd

    def check_command(self, cmd):
        """Checks the command against the white- and blacklists."""
        if cmd in self.black_list:
            return False

        return self.white_list is None or cmd in self.white_list

    def execute(self, cmd, *args):
        """Executes a certain command on a remote terminal."""
        if self.check_command(cmd):
            remote_cmd = self.remote(cmd, *args)
            self.logger.debug('Executing: {}'.format(remote_cmd))
            return run(remote_cmd, shell=True)

        return ProcessResult(3, stderr=b'Command not allowed.')

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

    def send(self, dst, *srcs, options=None):
        """Sends files to a remote terminal."""
        rsync = self.rsync(self.remote_file(dst), *srcs, options=options)
        self.logger.debug('Executing: {}'.format(rsync))
        result = run(rsync, shell=True)
        self.logger.debug(str(result))
        return result

    def mkdir(self, directory, parents=False, binary='/usr/bin/mkdir'):
        """Creates a remote directory."""
        if parents:
            return self.execute(binary, '-p', str(directory))

        return self.execute(binary, str(directory))
