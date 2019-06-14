"""Terminals adminstration."""

from logging import DEBUG, INFO, basicConfig, getLogger
from sys import exit    # pylint: disable=W0622

from syslib import script

from terminallib.config import LOG_FORMAT
from terminallib.hooks import bind9cfgen, nagioscfgen, openvpncfgen
from terminallib.termadm.argparse import get_args
from terminallib.termadm.deployment import add as add_deploment
from terminallib.termadm.system import add as add_system, deploy, undeploy



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
    hooks = set()

    if args.action == 'add':
        if args.target == 'dep':
            success = add_deploment(args)
        elif args.target == 'sys':
            for _ in range(args.amount):
                add_system(args)

            success = True
            hooks |= {bind9cfgen, nagioscfgen, openvpncfgen}
    elif args.action == 'deploy':
        success = deploy(args)
        hooks.add(nagioscfgen)
    elif args.action == 'undeploy':
        success = undeploy(args)
        hooks.add(nagioscfgen)
    elif args.action == 'run-hooks':
        hooks |= {bind9cfgen, nagioscfgen, openvpncfgen}

        if args.no_hooks:
            LOGGER.error('Are you kidding me?')
        else:
            success = True

    if success and not args.no_hooks:
        for hook in sorted(hooks):
            hook()

    exit(0 if success else 1)
