"""Library for terminal remote control"""

from os.path import splitext, join
from datetime import datetime
from tempfile import NamedTemporaryFile
from itertools import chain
from homeinfo.lib.system import run, ProcessResult
from .config import ssh, screenshot
from .abc import TerminalAware

__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    # Options for SSH to trick it into not checking the host key
    _SSH_OPTS = {'UserKnownHostsFile': '/dev/null',
                 'StrictHostKeyChecking': 'no'}

    def __init__(self, user, terminal, keyfile=None, white_list=None, bl=None):
        """Initializes a remote terminal controller"""
        super().__init__(terminal)
        self._user = user
        self._keyfile = keyfile
        # Commands white and black list
        self._white_list = white_list
        self._black_list = bl

    @property
    def user(self):
        """Returns the user name"""
        return self._user

    @property
    def keyfile(self):
        """Returns the path to the SSH key file"""
        return self._keyfile or join(
            '', 'home', self.user, '.ssh', 'terminals')

    @property
    def _identity_file(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return ' '.join(['-i', self.keyfile])

    @property
    def _ssh_opts(self):
        """Returns options for SSH"""
        return ' '.join([
            ' '.join(['-o', '='.join([key, self._SSH_OPTS[key]])])
            for key in self._SSH_OPTS])

    @property
    def _ssh_cmd(self):
        """Returns the SSH basic command line"""
        return ' '.join([ssh['SSH_BIN'], self._identity_file,
                         self._ssh_options])

    @property
    def _rsync_shell(self):
        """Returns the rsync remote shell"""
        return ' '.join(['-e', ''.join(['"', self._ssh_cmd, '"'])])

    @property
    def _user_host(self):
        """Returns the respective user@host string"""
        return '@'.join([self.user, str(self.terminal.ipv4addr)])

    def _remote(self, cmd, *args):
        """Makes a command remote"""
        return ' '.join(chain([self._ssh_cmd, self._user_host, cmd], args))

    def _remote_file(self, src):
        """Returns a remote file path"""
        return ':'.join([self._user_host, src])

    def _rsync(self, src, dst):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst
        """
        return ' '.join([ssh['RSYNC_BIN'], self._remote_shell,
                         self._remote_file(src), dst])

    def _scrot_cmd(self, fname):
        """Creates the command line for a scrot execution"""
        scrot_cmd = screenshot['SCROT_BIN']
        scrot_args = ' '.join([screenshot['SCROT_ARGS'],
                               screenshot['THUMBNAIL_PERCENT']])
        display = screenshot['DISPLAY']
        display_cmd = ' '.join(
            ['export', ''.join(['='.join(['DISPLAY', display]), ';'])])
        return ' '.join([display_cmd, scrot_cmd, scrot_args, fname])

    def _check_command(self, cmd):
        """Checks the command against the white- and blacklists"""
        result = True
        if self._white_list is not None:
            if cmd not in self._white_list:
                result = False
        if self._black_list is not None:
            if cmd in self._black_list:
                result = False
        return result

    def execute(self, cmd, *args):
        """Executes a certain command on a remote terminal"""
        if self._check_command(cmd):
            return run(self._remote(cmd, *args), shell=True)
        else:
            return ProcessResult(3, stderr='Command not allowed.'.encode())

    def getfile(self, file):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self._rsync(file, tmp.name)
            pr = run(rsync, shell=True)
            if pr:
                return tmp.read()
            else:
                return pr


class DisplayController(RemoteController):
    """Remote controller for display interactions"""

    def _mkscreenshot(self, fname):
        """Creates a screenshot on the remote terminal"""
        scrot_cmd = self._scrot_cmd(fname)
        return (self.execute(scrot_cmd), datetime.now())

    def screenshot(self, quality=None):
        """Returns a screenshot"""
        return self.get_screenshot(thumbnail=False)

    @property
    def thumbnail(self):
        """Returns a thumbnail of a screenshot"""
        return self.get_screenshot(thumbnail=True)

    def get_screenshot(self, full=True, thumbnail=False):
        """Creates a screenshot on the terminal and
        fetches its content to the local machine
        """
        screenshot_file = screenshot['SCREENSHOT_FILE']
        fname, ext = splitext(screenshot_file)
        thumbnail_file = ''.join(['-'.join([fname, 'thumb']), ext])
        screenshot_result, timestamp = self._mkscreenshot(screenshot_file)
        if screenshot_result:
            if thumbnail:
                data = self.getfile(thumbnail_file)
            else:
                data = self.getfile(screenshot_file)
            return (data, timestamp)
        else:
            return None
