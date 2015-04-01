"""Abstract base classes for HOMEINFO's ORM database"""

from ..config import db
from peewee import Model, MySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.03.2015'
__all__ = ['TermgrModel']


class TermgrModel(Model):
    """Generic TermgrModel Model"""

    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('host'),
                                 user=db.get('user'),
                                 passwd=db.get('passwd'))
        schema = database.database
