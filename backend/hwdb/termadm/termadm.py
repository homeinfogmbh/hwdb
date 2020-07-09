"""Terminals adminstration."""

from logging import DEBUG, INFO, basicConfig, getLogger
from sys import exit    # pylint: disable=W0622

from syslib import script

from hwdb.config import LOG_FORMAT
from hwdb.hooks import bind9cfgen, openvpncfgen
from hwdb.termadm.argparse import get_args
from hwdb.termadm.deployment import add as add_deploment
from hwdb.termadm.system import add as add_system, deploy, undeploy


__all__ = ['main']


DESCRIPTION = 'Command line tool to administer HOMEINFO terminals.'
LOGGER = getLogger('termadm')
TERMGR_USER = 'termgr'


@script
def main():
    """Runs the terminal administration CLI."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)
    success = False
    hooks = None

    if args.action == 'add':
        if args.target == 'dep':
            success = add_deploment(args)
        elif args.target == 'sys':
            for _ in range(args.amount):
                add_system(args)

            success = True
            hooks = (bind9cfgen, openvpncfgen)
    elif args.action == 'deploy':
        success = deploy(args)
    elif args.action == 'undeploy':
        success = undeploy(args)
    elif args.action == 'run-hooks':
        hooks = args.hooks

        if args.no_hooks:
            LOGGER.error('Are you kidding me?')
        else:
            success = True

    if success and hooks and not args.no_hooks:
        for hook in hooks:
            hook()

    exit(0 if success else 1)
