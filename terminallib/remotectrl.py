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
        return ' '.join(['-i', ssh['PRIVATE_KEY_TERMGR']])

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return ' '.join(['-e', ''.join(['"', ssh['SSH_BIN']]),
                         ''.join([self._identity_file, '"'])])

    def _user_host(self, user=None):
        """Returns the respective user@host string"""
        return '@'.join([user or ssh['USER'], str(self.terminal.ipv4addr)])

    def _remote(self, cmd, user=None):
        """Makes a command remote"""
        return ' '.join([ssh['SSH_BIN'], self._identity_file,
                         self._user_host(user=user),
                         ''.join(['"', cmd, '"'])])

    def _remote_file(self, src, user=None):
        """Returns a remote file path"""
        return ':'.join([self._user_host(user=user), src])

    def _rsync(self, src, dst):
        """Returns a"""
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
        return self.execute(scrot_cmd, user=screenshot['USER'])

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
        return run(self._remote(cmd, user=user), shell=True)

    def getfile(self, file):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('rb') as tmp:
            rsync = self._rsync(file, tmp.name)
            print(tmp.name)
            pr = run(rsync, shell=True)
            if pr:
                print('all ok')
                tmp.seek(0)
                return tmp.read()
            else:
                return pr
