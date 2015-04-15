"""Library for terminal remote control"""

from homeinfolib.system import run
from .config import ssh, screenshot
from .abc import TerminalAware
from tempfile import NamedTemporaryFile
from os.path import splitext
from os import unlink

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
        return ' '.join(['-i', ssh['PRIVATE_KEY_TERMGR']])

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return ' '.join(['-e', ''.join(['"', ssh['SSH_BIN']]),
                         ''.join([self._identity_file, '"'])])

    def _user_host(self, user):
        """Returns the respective user@host string"""
        return '@'.join([user, str(self.terminal.ipv4addr)])

    def _remote(self, cmd, user):
        """Makes a command remote"""
        return ' '.join([ssh['SSH_BIN'], self._identity_file,
                         self._user_host(user),
                         ''.join(['"', cmd, '"'])])

    def _remote_file(self, src, user):
        """Returns a remote file path"""
        return ':'.join([self._user_host(user), src])

    def _rsync(self, user, src, dst):
        """Returns an rsync command line to retrieve
        src file from terminal to local file dst
        """
        return ' '.join([ssh['RSYNC_BIN'], self._remote_shell,
                         self._remote_file(src, user), dst])

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
        user = screenshot['USER']  # Use X11 server hosts's user account
        scrot_cmd = self._scrot_cmd(fname)
        return self.execute(scrot_cmd, user=user)

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

    def execute(self, cmd, user=None):
        """Executes a certain command on a remote terminal"""
        user = user or ssh['USER']
        return run(self._remote(cmd, user), shell=True)

    def getfile(self, file, user=None):
        """Gets a file from a remote terminal"""
        user = user or ssh['USER']
        with NamedTemporaryFile('wb', delete=False) as tmp:
            temp_name = tmp.name
        try:
            rsync = self._rsync(user, file, tmp.name)
            pr = run(rsync, shell=True)
            if pr:
                with open(temp_name, 'rb') as tmp:
                    return tmp.read()
            else:
                return pr
        finally:
            unlink(temp_name)
