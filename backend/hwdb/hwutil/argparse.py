"""Arguments parsing for termutil."""

from argparse import ArgumentParser

from hwdb.pseudotypes import connection
from hwdb.pseudotypes import customer
from hwdb.pseudotypes import operating_system
from hwdb.pseudotypes import type_
from hwdb.pseudotypes import deployment
from hwdb.pseudotypes import system
from hwdb.tools.deployment import DEFAULT_FIELDS as DEPLOYMENT_FIELDS
from hwdb.tools.deployment import DeploymentField
from hwdb.tools.system import DEFAULT_FIELDS as SYSTEM_FIELDS
from hwdb.tools.system import SystemField


__all__ = ['get_args']


def _add_parser_list_systems(subparsers):
    """Adds args to list systems."""

    parser = subparsers.add_parser('sys', help='list systems')
    parser.add_argument(
        'id', nargs='*', type=int, metavar='id',
        help='filter for systems with the respective IDs')
    parser.add_argument(
        '-C', '--customer', nargs='+', type=customer, metavar='customer',
        help='filter for the respective customers')
    parser.add_argument(
        '-D', '--deployment', nargs='+', type=deployment, metavar='deployment',
        help='filter for the respective deployments')
    parser.set_defaults(deployed=None)
    parser.add_argument(
        '-o', '--operating-system', nargs='+', type=operating_system,
        metavar='os', help='filter for the respective operating systems')
    parser.add_argument(
        '-m', '--manufacturer', nargs='+', type=customer,
        metavar='manufacturer', help='filter for the respective manufacturers')
    parser.add_argument(
        '-c', '--configured', action='store_true', dest='configured',
        help='filter for configured systems')
    parser.add_argument(
        '-a', '--available', action='store_false', dest='configured',
        help='filter for available systems')
    parser.add_argument(
        '-d', '--deployed', action='store_true', dest='deployed',
        help='filter for deployed systems')
    parser.add_argument(
        '-u', '--undeployed', action='store_false', dest='deployed',
        help='filter for undeployed systems')
    parser.add_argument(
        '-f', '--fields', type=SystemField, nargs='+', default=SYSTEM_FIELDS,
        metavar='field', help='specifies the fields to print')


def _add_parser_list_deployments(subparsers):
    """Adds a parser to list deployments."""

    parser = subparsers.add_parser('dep', help='list deployments')
    parser.add_argument(
        'id', nargs='*', type=int, metavar='id',
        help='filter for deployments with the respective IDs')
    parser.add_argument(
        '-C', '--customer', nargs='+', type=customer, metavar='customer',
        help='filter for the respective customers')
    parser.add_argument(
        '--testing', type=int, metavar='testing',
        help='filter for testing deployments')
    parser.add_argument(
        '-t', '--type', nargs='+', type=type_, metavar='type',
        help='filter for the respective types')
    parser.add_argument(
        '-c', '--connection', nargs='+', type=connection,
        metavar='connection', help='filter for the respective connections')
    parser.add_argument(
        '-s', '--system', nargs='+', type=system,
        metavar='system', help='filter for the respective systems')
    parser.add_argument(
        '-f', '--fields', type=DeploymentField, nargs='+',
        default=DEPLOYMENT_FIELDS, metavar='field',
        help='specifies the fields to print')


def _add_parser_list(subparsers):
    """Adds listing args."""

    parser = subparsers.add_parser('ls', help='list records')
    target = parser.add_subparsers(dest='target')
    _add_parser_list_systems(target)
    _add_parser_list_deployments(target)


def _add_parser_find_systems(subparsers):
    """Adds a parser to find systems."""

    parser = subparsers.add_parser('sys', help='find digital signage systems')
    parser.add_argument(
        'pattern', help='filter for systems of the respective pattern')
    parser.add_argument(
        'house_number', nargs='?',
        help='filter for systems of the respective house number')


def _add_parser_find_deployments(subparsers):
    """Adds a parser to find deployments."""

    parser = subparsers.add_parser('dep', help='find deployments')
    parser.add_argument(
        'pattern', help='filter for deployments of the respective pattern')
    parser.add_argument(
        'house_number', nargs='?',
        help='filter for deployments of the respective house number')


def _add_parser_find(subparsers):
    """Adds a parser for searching."""

    parser = subparsers.add_parser('find', help='find records')
    target = parser.add_subparsers(dest='target')
    _add_parser_find_systems(target)
    _add_parser_find_deployments(target)


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