"""Library for terminal remote control"""

from tempfile import NamedTemporaryFile
from itertools import chain
from logging import getLogger

from homeinfo.lib.system import run, ProcessResult
from homeinfo.terminals.abc import TerminalAware

from .config import config

__all__ = ['RemoteController']


class CustomSSHOptions():
    """Sets custom SSH options"""

    def __init__(self, remote_controller, options):
        """Sets the custom SSH options"""
        self.remote_controller = remote_controller
        self.options = options
        self.previous_options = None

    def __enter__(self):
        """Spplies the custom SSH options"""
        self.previous_options = self.remote_controller.ssh_custom_opts
        self.remote_controller.ssh_custom_opts = self.options

    def __exit__(self, *_):
        """Resets the custom SSH options"""
        self.remote_controller.ssh_custom_opts = self.previous_options


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    def __init__(self, user, terminal, keyfile=None,
                 white_list=None, bl=None, logger=None):
        """Initializes a remote terminal controller"""
        super().__init__(terminal)
        self.user = user
        self.keyfile = keyfile or '/home/{}/.ssh/terminals'.format(self.user)

        # Commands white and black list
        self.white_list = white_list
        self.black_list = bl

        if logger is None:
            self.logger = getLogger(self.__class__.__name__)
        else:
            self.logger = logger.getChild(self.__class__.__name__)

        # Further options for SSH
        if self.terminal.connection:
            connect_timeout = self.terminal.connection.timeout
        else:
            connect_timeout = config.ssh['CONNECT_TIMEOUT']

        self.SSH_OPTS = {
            # Trick SSH it into not checking the host key
            'UserKnownHostsFile': config.ssh['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking': config.ssh['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call
            'ConnectTimeout': connect_timeout}
        self.ssh_custom_opts = None

    @property
    def identity(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return '-i {}'.format(self.keyfile)

    @property
    def ssh_options(self):
        """Returns options for SSH"""
        for option, value in self.SSH_OPTS.items():
            # Skip options overridden by custom options
            if self.ssh_custom_opts:
                if option in self.ssh_custom_opts:
                    continue

            yield '-o {option}={value}'.format(
                option=option, value=value)

        # Yield additional custom options iff set
        if self.ssh_custom_opts:
            for option, value in self.ssh_custom_opts.items():
                yield '-o {option}={value}'.format(
                    option=option, value=value)

    @property
    def ssh_cmd(self):
        """Returns the SSH basic command line"""
        options = ' '.join(self.ssh_options)
        return '{bin} {identity} {options}'.format(
            bin=config.ssh['SSH_BIN'],
            identity=self.identity,
            options=options)

    @property
    def remote_shell(self):
        """Returns the rsync remote shell"""
        return '-e "{0}"'.format(self.ssh_cmd)

    @property
    def user_host(self):
        """Returns the respective user@host string"""
        return '{0}@{1}'.format(self.user, self.terminal.ipv4addr)

    def remote(self, cmd, *args):
        """Makes a command remote"""
        return ' '.join(chain([self.ssh_cmd, self.user_host, cmd], args))

    def remote_file(self, src):
        """Returns a remote file path"""
        return "{user_host}:'{src}'".format(user_host=self.user_host, src=src)

    def rsync(self, dst, *srcs, options=None):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst
        """
        srcs = ' '.join("'{}'".format(src) for src in srcs)
        options = '' if options is None else options
        cmd = '{bin} {options} {rsh} {srcs} {dst}'.format(
            bin=config.ssh['RSYNC_BIN'],
            options=options, rsh=self.remote_shell,
            srcs=srcs, dst=dst)

        self.logger.debug(cmd)

        return cmd

    def check_command(self, cmd):
        """Checks the command against the white- and blacklists"""
        if self.white_list is not None:
            if cmd not in self.white_list:
                return False

        if self.black_list is not None:
            if cmd in self.black_list:
                return False

        return True

    def execute(self, cmd, *args):
        """Executes a certain command on a remote terminal"""
        if self.check_command(cmd):
            remote_cmd = self.remote(cmd, *args)
            self.logger.debug('Executing: {}'.format(remote_cmd))
            return run(remote_cmd, shell=True)
        else:
            return ProcessResult(3, stderr=b'Command not allowed.')

    def get(self, file, options=None):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self.rsync(
                tmp.name, [self.remote_file(file)], options=options)
            pr = run(rsync, shell=True)

            self.logger.debug(str(pr))

            if pr:
                return tmp.read()
            else:
                return pr

    def send(self, dst, *srcs, options=None):
        """Sends files to a remote terminal"""
        rsync = self.rsync(self.remote_file(dst), *srcs, options=options)

        self.logger.debug('Executing: {}'.format(rsync))

        pr = run(rsync, shell=True)

        self.logger.debug(
            'Result: {pr} {pr.exit_code} {pr.stdout} {pr.stderr}'.format(
                pr=pr))

        return pr

    def extra_options(self, options):
        """Returns an CustomSSHOptions context
        manager for this terminal controller
        """
        return CustomSSHOptions(self, options)
