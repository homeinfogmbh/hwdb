"""Library for terminal remote control"""

from homeinfolib.system import run
from .config import ssh, screenshot
from .abc import TerminalAware
from tempfile import NamedTemporaryFile
from os.path import splitext

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    @property
    def _identity_file(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return ['-i', ssh['PRIVATE_KEY_TERMGR']]

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return ['-e', ''.join(['"', ssh['SSH_BIN']]),
                ''.join([self._identity_file, '"'])]

    def _user_host(self, user=None):
        """Returns the respective user@host string"""
        return ['@'.join([user or ssh['USER'], str(self.terminal.ipv4addr)])]

    def _remote(self, cmd):
        """Makes a command remote"""
        return [ssh['SSH_BIN']] + self._identity_file + self._user_host() + cmd

    def _remote_file(self, src):
        return [':'.join([self._user_host(screenshot['USER']), src])]

    def _rsync(self, src, dst):
        """Returns a"""
        return ([ssh['RSYNC_BIN']] + self._remote_shell
                + self._remote_file(src) + [dst])

    def _scrot_cmd(self, fname):
        """Creates the command line for a scrot execution"""
        scrot_cmd = [screenshot['SCROT_BIN']]
        scrot_args = [screenshot['SCROT_ARGS'],
                      screenshot['THUMBNAIL_PERCENT']]
        display = screenshot['DISPLAY']
        display_cmd = [''.join(['='.join(['export DISPLAY', display]), ';'])]
        return display_cmd + scrot_cmd + scrot_args + [fname]

    def _mkscreenshot(self, fname):
        """Creates a screenshot on the remote terminal"""
        scrot_cmd = self._scrot_cmd(fname)
        return self.execute(scrot_cmd)

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
        screenshot_result = self._mkscreenshot(screenshot_file)
        if screenshot_result:
            if thumbnail:
                result = self.getfile(thumbnail_file)
            else:
                result = self.getfile(screenshot_file)
            return result
        else:
            return None

    def execute(self, cmd):
        """Executes a certain command on a remote terminal"""
        return run(self._remote(cmd))

    def getfile(self, file):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('wb+') as tmp:
            rsync = self._rsync(file, tmp.name)
            pr = run(rsync)
            if pr:
                tmp.seek(0)
                return tmp.read()
            else:
                return pr
