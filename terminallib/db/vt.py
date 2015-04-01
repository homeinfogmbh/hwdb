"""Terminal data storage"""

from datetime import datetime
from peewee import ForeignKeyField, IntegerField, CharField, DateTimeField,\
    BlobField
from homeinfolib.db import improved, create
from .abc import TermgrModel
from .terminal import Terminal

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Terminal']


@create
@improved
class TerminalHistory(TermgrModel):
    """A virtual terminal's history"""

    class Meta:
        db_table = 'vt_history'

    terminal = ForeignKeyField(Terminal, db_column='terminal',
                               related_name='vt_log')
    """The terminal this history belongs to"""
    timestamp = DateTimeField(default=datetime.now())
    """A time stamp when the command was executed"""
    command = CharField(255)
    """The command, that was issued"""
    stdout = BlobField()
    """The STDOUT result of the command"""
    stderr = BlobField()
    """The STDERR result of the command"""
    exit_code = IntegerField()
    """The exit code of the command"""
