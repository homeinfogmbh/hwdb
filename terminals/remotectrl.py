"""Library for terminal remote control"""

from os.path import splitext
from os import unlink
from datetime import datetime
from tempfile import NamedTemporaryFile
from homeinfo.lib.system import run
from .config import ssh, screenshot
from .abc import TerminalAware

__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    @property
    def _identity_file(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return ' '.join(['-i', ssh['PRIVATE_KEY_TERMGR']])

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return ' '.join(['-e', ''.join(['"', ssh['SSH_BIN']]),
                         ''.join([self._identity_file, '"'])])

    @property
    def _user_host(self):
        """Returns the respective user@host string"""
        return '@'.join([ssh['USER'], str(self.terminal.ipv4addr)])

    def _remote(self, cmd):
        """Makes a command remote"""
        return ' '.join([ssh['SSH_BIN'], self._identity_file,
                         self._user_host,
                         ''.join(['"', cmd, '"'])])

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
        display_cmd = ' '.join(['export',
                                ''.join(['='.join(['DISPLAY',
                                                   display]),
                                         ';'])])
        return ' '.join([display_cmd, scrot_cmd, scrot_args, fname])

    def _mkscreenshot(self, fname):
        """Creates a screenshot on the remote terminal"""
        scrot_cmd = self._scrot_cmd(fname)
        return (self.execute(scrot_cmd), datetime.now())

    @property
    def screenshot(self):
        """Returns a screenshot"""
        return self.get_screenshot(thumbnail=False)

    @property
    def thumbnail(self):
        """Returns a thumbnail of a screenshot"""
        return self.get_screenshot(thumbnail=True)

    def get_screenshot(self, thumbnail=False):
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

    def execute(self, cmd):
        """Executes a certain command on a remote terminal"""
        return run(self._remote(cmd), shell=True)

    def getfile(self, file):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('wb', delete=False) as tmp:
            temp_name = tmp.name
        try:
            rsync = self._rsync(file, tmp.name)
            pr = run(rsync, shell=True)
            if pr:
                with open(temp_name, 'rb') as tmp:
                    return tmp.read()
            else:
                return pr
        finally:
            unlink(temp_name)
