"""Common variables and functions."""

from functools import wraps
from os import geteuid
from subprocess import check_call


__all__ = ['SYSTEMCTL', 'root', 'systemctl']


SYSTEMCTL = '/bin/systemctl'


def root(logger):
    """Decorates a fucntion to require root privileges."""

    def decorator(function):
        """Decorates the function."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the original function."""
            if geteuid() != 0:
                logger.error('You must be root to run %s.', function.__name__)
                exit(1)

            function(*args, **kwargs)

        return wrapper

    return decorator


def systemctl(*args):
    """Runs systemctl."""

    return check_call((SYSTEMCTL,) + args)
