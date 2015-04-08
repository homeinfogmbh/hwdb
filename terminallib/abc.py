"""Abstract base classes for terminal setup management"""

from peewee import Model, MySQLDatabase
from homeinfolib.db import improved
from .config import db

__date__ = "23.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TermgrModel', 'TerminalAware']


@improved
class TermgrModel(Model):
    """Generic TermgrModel Model"""

    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('host'),
                                 user=db.get('user'),
                                 passwd=db.get('passwd'))
        schema = database.database


class TerminalAware():
    """Manages terminals"""

    def __init__(self, terminal):
        """Sets user name and password"""
        self.terminal = terminal

    @property
    def cid(self):
        """Returns the customer identifier"""
        return self.terminal.cid

    @property
    def tid(self):
        """Returns the terminal identifier"""
        return self.terminal.tid

    @property
    def idstr(self):
        """Returns a unique string identifier"""
        return '.'.join([str(self.tid), str(self.cid)])
