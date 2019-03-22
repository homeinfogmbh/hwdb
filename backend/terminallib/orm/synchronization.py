"""Synchronization logging."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField

from peeweeplus import CascadingFKField

from terminallib.orm.common import TerminalModel
from terminallib.orm.terminal import Terminal


__all__ = ['Synchronization']


class Synchronization(TerminalModel):
    """Synchronization log.

    Recommended usage:

        with Synchronization.start(terminal) as sync:
            <do_sync_stuff>

            if sync_succeded:
                sync.status = True
            else:
                sync.status = False
    """

    terminal = CascadingFKField(Terminal, column_name='terminal')
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
    def start(cls, terminal, result=None):
        """Start a synchronization for this terminal."""
        sync = cls()
        sync.terminal = terminal
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

    def to_json(self, *args, terminal=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(*args, **kwargs)

        if terminal:
            dictionary['terminal'] = self.terminal.to_json(*args, **kwargs)

        return dictionary
