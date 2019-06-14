"""Arguments parsing for termutil."""

from argparse import ArgumentParser

from terminallib.enumerations import Connection, OperatingSystem, Type
from terminallib.tools.deployment import DEFAULT_FIELDS as DEPLOYMENT_FIELDS
from terminallib.tools.deployment import DeploymentField
from terminallib.tools.system import DEFAULT_FIELDS as SYSTEM_FIELDS
from terminallib.tools.system import SystemField


__all__ = ['get_args']


def _add_parser_list_systems(subparsers):
    """Adds args to list systems."""

    parser = subparsers.add_parser('sys', help='list systems')
    parser.add_argument(
        'id', nargs='*', type=int, metavar='id',
        help='filter for systems of the respective customer')
    parser.add_argument(
        '-D', '--deployed', type=int, metavar='deployed',
        help='filter for deployed or undeployed systems')
    parser.add_argument(
        '-d', '--deployment', nargs='+', type=int, metavar='deployed',
        help='filter for the given deployments')
    parser.add_argument(
        '-o', '--operating-system', nargs='+', type=OperatingSystem,
        metavar='os', help='filter for the respective operating systems')
    parser.add_argument(
        '-f', '--fields', type=SystemField, nargs='+', default=SYSTEM_FIELDS,
        metavar='field', help='specifies the fields to print')


def _add_parser_list_deployments(subparsers):
    """Adds a parser to list deployments."""

    parser = subparsers.add_parser('dep', help='list deployments')
    parser.add_argument('id', nargs='*', type=int, metavar='id')
    parser.add_argument(
        '-C', '--customer', type=int, metavar='customer',
        help='filter for the respective customer')
    parser.add_argument(
        '--testing', type=int, metavar='testing',
        help='filter for testing deployments')
    parser.add_argument(
        '-t', '--type', nargs='+', type=Type, metavar='type',
        help='filter for the respective types')
    parser.add_argument(
        '-c', '--connection', nargs='+', type=Connection,
        metavar='connection', help='filter for the respective connections')
    parser.add_argument(
        '-f', '--fields', type=DeploymentField, nargs='+',
        default=DEPLOYMENT_FIELDS, metavar='field',
        help='specifies the fields to print')


def _add_parser_list(subparsers):
    """Adds listing args."""

    parser = subparsers.add_parser('ls', help='list records')
    parser.add_argument(
        '-s', '--separator', default='  ', metavar='separator',
        help='specifies the fields separator')
    parser.add_argument(
        '-n', '--no-header', action='store_true',
        help='do not print table header')
    target = parser.add_subparsers(dest='target')
    _add_parser_list_systems(target)
    _add_parser_list_deployments(target)


def _add_parser_find_systems(subparsers):
    """Adds a parser to find systems."""

    parser = subparsers.add_parser('sys', help='find digital signage systems')
    parser.add_argument(
        'street', help='filter for systems of the respective street')
    parser.add_argument(
        'house_number', nargs='?',
        help='filter for systems of the respective house number')
    parser.add_argument(
        'annotation', nargs='?',
        help='filter for systems of the respective annotation')


def _add_parser_find(subparsers):
    """Adds a parser for searching."""

    parser = subparsers.add_parser('find', help='find records')
    target = parser.add_subparsers(dest='target')
    _add_parser_find_systems(target)


def get_args():
    """Returns the CLI options."""

    parser = ArgumentParser(description='Terminal database query utility.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging')
    subparsers = parser.add_subparsers(dest='action')
    _add_parser_list(subparsers)
    _add_parser_find(subparsers)
    subparsers.add_parser('CSM-101', help='?')
    return parser.parse_args()
