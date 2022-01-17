"""Command line argument parsing."""

from argparse import _SubParsersAction, ArgumentParser, Namespace
from pathlib import Path
from re import compile as Regex

from hwdb.enumerations import Connection, DeploymentType, OperatingSystem
from hwdb.hooks import bind9cfgen, openvpncfgen
from hwdb.parsers import connection
from hwdb.parsers import customer
from hwdb.parsers import date
from hwdb.parsers import deployment
from hwdb.parsers import group
from hwdb.parsers import hook
from hwdb.parsers import operating_system
from hwdb.parsers import deployment_type
from hwdb.parsers import system


__all__ = ['get_args']


DEFAULT_HOOKS = (bind9cfgen, openvpncfgen)
DEFAULT_ADDRESS_REGEX = Regex(
    '([\\w\\s\\-/]+)\\s+(\\d+[\\s\\-/]*\\w*),'
    '?\\s+((?:[A-Z]+\\-)?\\d+)\\s+([\\w\\s\\-/]+)'
)


def _add_new_system_parser(subparsers: _SubParsersAction):
    """Adds a parser to add new systems."""

    parser = subparsers.add_parser('sys', help='add new systems')
    parser.add_argument(
        'group', type=group, nargs='?', help='the system group'
    )
    parser.add_argument(
        '-n', '--amount', type=int, default=1, help='amount of systems to add'
    )
    parser.add_argument(
        '-d', '--deployment', type=deployment,
        help='the deployment of the system'
    )
    parser.add_argument('--key', help='the OpenVPN key to use')
    parser.add_argument(
        '--mtu', type=int, help='the MTU for the OpenVPN tunnel'
    )
    parser.add_argument(
        '-o', '--operating-system', type=operating_system,
        default=OperatingSystem.ARCH_LINUX,
        help='the installed operating system'
    )
    parser.add_argument(
        '--monitor', type=int, help='set explicit monitoring flag'
    )
    parser.add_argument(
        '-s', '--serial-number', help='the serial number of the hardware'
    )
    parser.add_argument('--model', help='the hardware model')


def _add_deployment_add_args(parser: ArgumentParser):
    """Adds arguments to parser to add deployments."""

    parser.add_argument(
        '-t', '--type', type=deployment_type, default=DeploymentType.DDB,
        help='the system type'
    )
    parser.add_argument(
        '-c', '--connection', type=connection, default=Connection.DSL,
        help='the internet connection on site'
    )
    parser.add_argument(
        '-s', '--scheduled', type=date, help='the scheduled date'
    )
    parser.add_argument('-a', '--annotation', help='a descriptive annotation')
    parser.add_argument(
        '--testing', action='store_true',
        help='flag the deployment as testing'
    )


def _add_new_deployment_parser(subparsers: _SubParsersAction):
    """Adds a deployment parser."""

    parser = subparsers.add_parser('dep', help='add new deployments')
    parser.add_argument(
        'customer', type=customer, help='the owner of the deployment'
    )
    parser.add_argument('street', help='the street name')
    parser.add_argument('house_number', help='the house number')
    parser.add_argument('zip_code', help='the ZIP code')
    parser.add_argument('city', help='the city')
    _add_deployment_add_args(parser)


def _batch_add_new_deployment_parser(subparsers: _SubParsersAction):
    """Adds a parser to batch-add deployments."""

    parser = subparsers.add_parser('deps', help='batch-adds new deployments')
    parser.add_argument(
        'customer', type=customer, help='the owner of the deployment'
    )
    parser.add_argument(
        'file', type=Path, nargs='+', metavar='file', help='source files'
    )
    parser.add_argument(
        '-r', '--regex', type=Regex, metavar='expression',
        default=DEFAULT_ADDRESS_REGEX,
        help='regular expression to extract address data from the files'
    )
    _add_deployment_add_args(parser)


def _add_new_parser(subparsers: _SubParsersAction):
    """Adds a parser for adding records."""

    parser = subparsers.add_parser('add', help='add new records')
    subparsers = parser.add_subparsers(dest='target')
    _add_new_system_parser(subparsers)
    _add_new_deployment_parser(subparsers)
    _batch_add_new_deployment_parser(subparsers)


def _add_deploy_parser(subparsers: _SubParsersAction):
    """Adds a parser for deployment of systems."""

    parser = subparsers.add_parser('deploy', help='manage system deployment')
    parser.add_argument('system', type=system, help='the system to modify')
    parser.add_argument(
        '-r', '--remove', action='store_true', help='remove the deployment'
    )
    parser.add_argument(
        '-e', '--exclusive', action='store_true',
        help='remove other systems from that deployment'
    )
    parser.add_argument(
        '-f', '--fitted', action='store_true', help='mark the system as fitted'
    )
    parser.add_argument(
        'deployment', type=deployment, nargs='?', help='the deployment site'
    )


def _add_dataset_parser(subparsers: _SubParsersAction):
    """Adds a parser for dataset of systems."""

    parser = subparsers.add_parser('dataset', help='manage system dataset')
    parser.add_argument('system', type=system, help='the system to modify')
    parser.add_argument(
        '-r', '--remove', action='store_true', help='remove the dataset'
    )
    parser.add_argument(
        'dataset', type=deployment, nargs='?', help='the dataset'
    )


def _add_hooks_parser(subparsers: _SubParsersAction):
    """Adds a parser for running hooks."""

    parser = subparsers.add_parser(
        'run-hooks', help='run post-transaction hooks'
    )
    parser.add_argument(
        '-H', '--hooks', nargs='*', type=hook, default=DEFAULT_HOOKS,
        help='a list of hooks to run'
    )


def get_args() -> Namespace:
    """Parses the CLI arguments."""

    parser = ArgumentParser(description='Hardware database administration.')
    parser.add_argument(
        '-n', '--no-hooks', action='store_true',
        help='do not run post-transaction hooks'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging'
    )
    subparsers = parser.add_subparsers(dest='action')
    _add_new_parser(subparsers)
    _add_deploy_parser(subparsers)
    _add_dataset_parser(subparsers)
    _add_hooks_parser(subparsers)
    return parser.parse_args()
