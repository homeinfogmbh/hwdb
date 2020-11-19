"""Command line interface utilities."""

from sys import stderr, stdout
from typing import Callable, Dict, Generator, Iterable


__all__ = ['formatiter', 'iterprint', 'FieldFormatter']


def formatiter(items: Iterable, mapping: Dict[object, Callable],
               keys: Iterable) -> Generator[str, None, None]:
    """Yields formatted items for console output."""

    formatters = [mapping[key] for key in keys]
    sep = ' ' if stdout.isatty() else '\t'

    if stdout.isatty():
        yield sep.join(str(formatter) for formatter in formatters)

    for item in items:
        yield sep.join(formatter.format(item) for formatter in formatters)


def iterprint(iterable: Iterable) -> bool:
    """Prints items line by line, handling multiple possible I/O errors."""

    try:
        for item in iterable:
            print(item, flush=not stdout.isatty())
    except BrokenPipeError:
        stderr.close()
        return True
    except KeyboardInterrupt:
        if stdout.isatty():
            print('\nAborted...', flush=True)

        return False

    return True


def justify(string: str, size: int, leftbound: bool = False) -> str:
    """Justifies the string."""

    if leftbound:
        return string[0:size].ljust(size)

    return string[0:size].rjust(size)


def to_string(value: object) -> str:
    """Applies builtin str() to value unless value is None, True or
    False, in which case it will return none, true respectively false
    from the keyword arguments.
    """

    none, true, false = ('-', '✓', '✗') if stdout.isatty() else ('', '1', '0')

    if value is None:
        return none

    if value is True:
        return true

    if value is False:
        return false

    return str(value)


class FieldFormatter:
    """Wrapper to access terminal properties."""

    def __init__(self, getter: Callable, caption: str, size: int = 0,
                 leftbound: bool = False):
        """Sets the field's name"""
        self.getter = getter
        self.caption = caption
        self.size = size
        self.leftbound = leftbound

    def __str__(self):
        """Returns the formatted caption."""
        return f'\033[1m{self.header}\033[0m'

    def format(self, target: object) -> str:
        """Formats the respective field for the given target."""
        if stdout.isatty():
            return justify(
                to_string(self.getter(target)), self.max,
                leftbound=self.leftbound)

        return to_string(self.getter(target))

    @property
    def max(self) -> int:
        """Returns the maximum size."""
        return max(self.size, len(self.caption))

    @property
    def header(self) -> str:
        """Returns the appropriate header text."""
        return justify(self.caption, self.max, leftbound=self.leftbound)
