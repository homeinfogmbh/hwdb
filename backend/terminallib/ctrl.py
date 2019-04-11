"""Library for terminal remote control."""

from subprocess import CalledProcessError, check_call
from tempfile import NamedTemporaryFile

from syslib import run

from terminallib.config import CONFIG, LOGGER
from terminallib.exceptions import TerminalConfigError


__all__ = ['is_online', 'CustomSSHOptions', 'RemoteController']


def _get_options(options):
    """Returns the respective options as command line string."""

    if not options:
        return ''

    if isinstance(options, str):
        return options

    return ' '.join(str(option) for option in options)


def is_online(system):
    """Determines whether the respective system is online."""

    openvpn = system.openvpn

    if openvpn is None:
        return False

    command = (CONFIG['binaries']['PING'], '-qc', '3', str(openvpn.ipv4address))

    try:
        check_call(command)
    except CalledProcessError:
        return False

    return True


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


class RemoteController:
    """Controls a terminal remotely."""

    def __init__(self, user, system, *, keyfile=None):
        """Initializes a remote terminal controller."""
        self.user = user
        self.system = system
        self.keyfile = keyfile or '/home/{}/.ssh/terminals'.format(self.user)
        self.ssh_options = {
            # Trick SSH it into not checking the host key.
            'UserKnownHostsFile': CONFIG['ssh']['USER_KNOWN_HOSTS_FILE'],
            'StrictHostKeyChecking': CONFIG['ssh']['STRICT_HOST_KEY_CHECKING'],
            # Set timeout to avoid blocking of rsync / ssh call.
            'ConnectTimeout': CONFIG['ssh']['CONNECT_TIMEOUT']}

    @property
    def ipv4address(self):
        """Returns the system's IPv4 address."""
        try:
            return self.system.openvpn.ipv4address
        except AttributeError:
            raise TerminalConfigError('Terminal has no OpenVPN address.')

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
        return '{}@{}'.format(self.user, self.ipv4address)

    def remote(self, cmd, *args):
        """Makes a command remote."""
        yield from self.ssh_cmd
        yield self.user_host
        yield str(cmd)

        for arg in args:
            yield str(arg)

    def remote_file(self, src):
        """Returns a remote file path."""
        return "{}:'{}'".format(self.user_host, src)

    def extra_options(self, options):
        """Returns an CustomSSHOptions context
        manager for this remote controller.
        """
        return CustomSSHOptions(options, self)

    def rsync(self, dst, *srcs, options=None):
        """Returns the respective rsync command."""
        srcs = ' '.join("'{}'".format(src) for src in srcs)
        options = _get_options(options)
        binary = CONFIG['ssh']['RSYNC_BIN']
        cmd = (binary, options, self.remote_shell, srcs, dst)
        cmd = ' '.join(cmd)
        LOGGER.debug(cmd)
        return cmd

    def execute(self, cmd, *args, shell=False):
        """Executes a certain command on a remote system."""
        if shell:
            remote_cmd = ' '.join(self.remote(cmd, *args))
        else:
            remote_cmd = tuple(self.remote(cmd, *args))

        LOGGER.debug('Executing: "%s".', remote_cmd)
        return run(remote_cmd, shell=shell)

    def get(self, file, options=None):
        """Gets a file from a remote system."""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self.rsync(
                tmp.name, [self.remote_file(file)], options=options)
            result = run(rsync, shell=True)
            LOGGER.debug(str(result))

            if result:
                return tmp.read()

            return result

    def send(self, dst, *srcs, options=None):
        """Sends files to a remote system."""
        command = self.rsync(self.remote_file(dst), *srcs, options=options)
        LOGGER.debug('Executing: "%s".', command)
        result = run(command, shell=True)
        LOGGER.debug(str(result))
        return result

    def mkdir(self, directory, parents=False, binary='/usr/bin/mkdir'):
        """Creates a remote directory."""
        if parents:
            return self.execute(binary, '-p', str(directory))

        return self.execute(binary, str(directory))
