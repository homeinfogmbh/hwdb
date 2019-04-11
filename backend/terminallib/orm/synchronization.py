"""Synchronization logging."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from terminallib.orm.common import BaseModel
from terminallib.orm.system import System


__all__ = ['Synchronization']


class Synchronization(BaseModel):
    """Synchronization log.

    Recommended usage:

        with Synchronization.start(terminal) as sync:
            <do_sync_stuff>

            if sync_succeded:
                sync.status = True
            else:
                sync.status = False
    """

    system = ForeignKeyField(
        System, column_name='system', backref='synchronizations',
        on_delete='CASCADE', on_update='CASCADE')
    started = DateTimeField()
    finished = DateTimeField(null=True)
    reload = BooleanField(null=True)
    force = BooleanField(null=True)
    nocheck = BooleanField(null=True)
    result = BooleanField(null=True)
    annotation = CharField(255, null=True)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stop()

    @classmethod
    def start(cls, system, result=None):
        """Start a synchronization for this terminal."""
        sync = cls()
        sync.system = system
        sync.started = datetime.now()
        sync.result = result
        return sync

    def stop(self, force=False):
        """Stops the synchronization."""
        if force or self.result is not None:
            self.finished = datetime.now()
            self.save()
            return True

        return False

    def to_json(self, system=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(**kwargs)

        if system:
            dictionary['system'] = self.system.to_json(**kwargs)

        return dictionary
