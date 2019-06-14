"""Terminals adminstration."""

from logging import DEBUG, INFO, basicConfig, getLogger
from sys import exit    # pylint: disable=W0622

from syslib import script

from terminallib.config import LOG_FORMAT
from terminallib.hooks import run as run_hooks
from terminallib.termadm.argparse import get_args
from terminallib.termadm.deployment import add as add_deploment
from terminallib.termadm.system import add as add_system, deploy, undeploy



__all__ = ['main']


DESCRIPTION = 'Command line tool to administer HOMEINFO terminals.'
LOGGER = getLogger(__file__)
TERMGR_USER = 'termgr'


@script
def main():
    """Runs the terminal administration CLI."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)
    success = False
    needs_hooks = False

    if args.action == 'add':
        if args.target == 'dep':
            success = add_deploment(args)
        elif args.target == 'sys':
            success = add_system(args)

        needs_hooks = True
    elif args.action == 'deploy':
        success = deploy(args)
        needs_hooks = True
    elif args.action == 'undeploy':
        success = undeploy(args)
        needs_hooks = True

    if success and needs_hooks:
        run_hooks()

    exit(0 if success else 1)
