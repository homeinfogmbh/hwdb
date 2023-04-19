"""Terminals adminstration."""

from logging import DEBUG, INFO, basicConfig, getLogger

from hwdb.config import LOG_FORMAT
from hwdb.hooks import bind9cfgen, openvpncfgen
from hwdb.hwadm.argparse import get_args
from hwdb.hwadm.deployment import add as add_deployment
from hwdb.hwadm.deployment import batch_add as add_deployments
from hwdb.hwadm.system import add as add_system
from hwdb.hwadm.system import dataset
from hwdb.hwadm.system import deploy
from hwdb.hwadm.system import toggle_updating
from hwdb.parsers import systems


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
            success = add_deployment(args)
        if args.target == 'deps':
            success = add_deployments(args)
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
    elif args.action == 'toggle-updating':
        toggle_updating(systems(args.system, logger=LOGGER, strict=False))
        success = True

    if success and hooks and not args.no_hooks:
        for hook in hooks:
            hook()

    return 0 if success else 1
