"""Terminals adminstration."""

from logging import DEBUG, INFO, basicConfig, getLogger

from hwdb.config import LOG_FORMAT
from hwdb.hooks import bind9cfgen, openvpncfgen
from hwdb.hwadm.argparse import get_args
from hwdb.hwadm.deployment import add as add_deploment
from hwdb.hwadm.deployment import batch_add as add_deploments
from hwdb.hwadm.system import add as add_system, dataset, deploy


__all__ = ['main']


DESCRIPTION = 'Command line tool to administer HOMEINFO terminals.'
LOGGER = getLogger('hwadm')
TERMGR_USER = 'termgr'


def main() -> int:
    """Runs the terminal administration CLI."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)
    success = False
    hooks = None

    if args.action == 'add':
        if args.target == 'dep':
            success = add_deploment(args)
        if args.target == 'deps':
            success = add_deploments(args)
        elif args.target == 'sys':
            for _ in range(args.amount):
                add_system(args)

            success = True
            hooks = (bind9cfgen, openvpncfgen)
    elif args.action == 'deploy':
        deploy(args)
        success = True
    elif args.action == 'dataset':
        dataset(args)
        success = True
    elif args.action == 'run-hooks':
        hooks = args.hooks

        if args.no_hooks:
            LOGGER.error('Are you kidding me?')
        else:
            success = True

    if success and hooks and not args.no_hooks:
        for hook in hooks:
            hook()

    return 0 if success else 1
