"""Library for terminal remote control"""

from sys import stdout, stderr
from tempfile import NamedTemporaryFile
from itertools import chain

from homeinfo.lib.system import run, ProcessResult
from homeinfo.terminals.abc import TerminalAware

from .config import terminals_config

__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    def __init__(self, user, terminal, keyfile=None,
                 white_list=None, bl=None, logger=None):
        """Initializes a remote terminal controller"""
        super().__init__(terminal)
        self.user = user
        self.keyfile = keyfile or '/home/{0}/.ssh/terminals'.format(self.user)

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
            connect_timeout = terminals_config.ssh['CONNECT_TIMEOUT']

        self.SSH_OPTS = {
            # Trick SSH it into not checking the host key
            'UserKnownHostsFile':
                terminals_config.ssh['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking':
                terminals_config.ssh['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call
            'ConnectTimeout': connect_timeout}
        self.ssh_custom_opts = None

    @property
    def identity(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return '-i {0}'.format(self.keyfile)

    @property
    def ssh_options(self):
        """Returns options for SSH"""
        # Yield additional custom options iff set
        if self.ssh_custom_opts:
            for option in self.ssh_custom_opts:
                value = self.ssh_custom_opts[option]
                option_value = '-o {option}={value}'.format(
                    option=option, value=value)

                yield option_value

        for option in self.SSH_OPTS:
            # Skip options overridden by custom options
            if self.ssh_custom_opts:
                if option in self.ssh_custom_opts:
                    continue

            value = self.SSH_OPTS[option]
            option_value = '-o {option}={value}'.format(
                option=option, value=value)

            yield option_value

        # Yield additional custom options iff set
        if self.ssh_custom_opts:
            for option in self.ssh_custom_opts:
                value = self.ssh_custom_opts[option]
                option_value = '-o {option}={value}'.format(
                    option=option, value=value)

                yield option_value

    @property
    def ssh_cmd(self):
        """Returns the SSH basic command line"""
        options = ' '.join(self.ssh_options)
        return '{bin} {identity} {options}'.format(
            bin=terminals_config.ssh['SSH_BIN'],
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
        return "{0}:'{1}'".format(self.user_host, src)

    def rsync(self, dst, *srcs, options=None):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst
        """
        srcs = ' '.join("'{0}'".format(src) for src in srcs)
        options = '' if options is None else options
        cmd = '{bin} {options} {rsh} {srcs} {dst}'.format(
            bin=terminals_config.ssh['RSYNC_BIN'],
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
        """Gets a file from a remote terminal"""
        rsync = self.rsync(self.remote_file(dst), *srcs, options=options)

        self.logger.debug('Executing: {}'.format(rsync))

        pr = run(rsync, shell=True)

        self.logger.debug('Result: {0} {1} {2} {3}'.format(
            pr, pr.exit_code, pr.stdout, pr.stderr))

        return pr
