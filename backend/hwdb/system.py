"""Common variables and functions."""

from functools import wraps
from os import geteuid
from subprocess import check_call
from sys import exit    # pylint: disable=W0622


__all__ = ['SYSTEMCTL', 'root', 'systemctl']


SYSTEMCTL = '/bin/systemctl'


def root(logger, returncode=1):
    """Decorates a function to require root privileges."""

    def decorator(function):
        """Decorates the function."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the original function."""
            if geteuid() != 0:
                logger.error('You must be root to run %s.', function.__name__)
                exit(returncode)

            function(*args, **kwargs)

        return wrapper

    return decorator


def systemctl(*args):
    """Runs systemctl."""

    return check_call([SYSTEMCTL, *args])
