"""Arguments parsing for termutil."""

from argparse import _SubParsersAction, ArgumentParser, Namespace

from hwdb.parsers import connection
from hwdb.parsers import customer
from hwdb.parsers import deployment
from hwdb.parsers import deployment_type
from hwdb.parsers import group
from hwdb.parsers import operating_system
from hwdb.parsers import system
from hwdb.tools.deployment import DEFAULT_FIELDS as DEPLOYMENT_FIELDS
from hwdb.tools.deployment import DeploymentField
from hwdb.tools.system import DEFAULT_FIELDS as SYSTEM_FIELDS
from hwdb.tools.system import SystemField


__all__ = ['get_args']


def _add_parser_list_systems(subparsers: _SubParsersAction):
    """Adds args to list systems."""

    parser = subparsers.add_parser('sys', help='list systems')
    parser.set_defaults(deployed=None, configured=None, fitted=None)
    parser.add_argument(
        'id', nargs='*', type=int, metavar='id',
        help='filter for systems with the respective IDs'
    )
    parser.add_argument(
        '-F', '--list-fields', action='store_true',
        help='list available fields'
    )
    parser.add_argument(
        '-C', '--customer', nargs='+', type=customer, metavar='customer',
        help='filter for systems of the respective customers'
    )
    parser.add_argument(
        '-D', '--deployment', nargs='+', type=deployment, metavar='deployment',
        help='filter for systems with the respective deployments'
    )
    parser.add_argument(
        '-G', '--group', nargs='+', type=group, metavar='group',
        help='filter for systems of the respective groups'
    )
    parser.add_argument(
        '-s', '--dataset', nargs='+', type=deployment, metavar='deployment',
        help='filter for systems with the respective datasets'
    )
    parser.add_argument(
        '-o', '--operating-system', nargs='+', type=operating_system,
        metavar='os', help='filter for the respective operating systems'
    )
    parser.add_argument(
        '-c', '--configured', action='store_true', dest='configured',
        help='filter for configured systems'
    )
    parser.add_argument(
        '-a', '--available', action='store_false', dest='configured',
        help='filter for available systems'
    )
    parser.add_argument(
        '-d', '--deployed', action='store_true', dest='deployed',
        help='filter for deployed systems'
    )
    parser.add_argument(
        '-u', '--undeployed', action='store_false', dest='deployed',
        help='filter for undeployed systems'
    )
    parser.add_argument(
        '--fitted', action='store_true', dest='fitted',
        help='filter for fittet systems'
    )
    parser.add_argument(
        '--unfitted', action='store_false', dest='fitted',
        help='filter for not-fitted systems'
    )
    parser.add_argument(
        '-f', '--fields', type=SystemField, nargs='+', default=SYSTEM_FIELDS,
        metavar='field', help='specifies the fields to print'
    )


def _add_parser_list_deployments(subparsers: _SubParsersAction):
    """Adds a parser to list deployments."""

    parser = subparsers.add_parser('dep', help='list deployments')
    parser.add_argument(
        'id', nargs='*', type=int, metavar='id',
        help='filter for deployments with the respective IDs'
    )
    parser.add_argument(
        '-F', '--list-fields', action='store_true',
        help='list available fields'
    )
    parser.add_argument(
        '-C', '--customer', nargs='+', type=customer, metavar='customer',
        help='filter for the respective customers'
    )
    parser.add_argument(
        '--testing', type=int, metavar='testing',
        help='filter for testing deployments'
    )
    parser.add_argument(
        '-t', '--type', nargs='+', type=deployment_type, metavar='type',
        help='filter for the respective types'
    )
    parser.add_argument(
        '-c', '--connection', nargs='+', type=connection,
        metavar='connection', help='filter for the respective connections'
    )
    parser.add_argument(
        '-s', '--system', nargs='+', type=system,
        metavar='system', help='filter for the respective systems'
    )
    parser.add_argument(
        '-f', '--fields', type=DeploymentField, nargs='+',
        default=DEPLOYMENT_FIELDS, metavar='field',
        help='specifies the fields to print'
    )


def _add_parser_list(subparsers: _SubParsersAction):
    """Adds listing args."""

    parser = subparsers.add_parser('ls', help='list and filter records')
    target = parser.add_subparsers(dest='target')
    _add_parser_list_systems(target)
    _add_parser_list_deployments(target)


def _add_parser_find_systems(subparsers: _SubParsersAction):
    """Adds a parser to find systems."""

    parser = subparsers.add_parser('sys', help='find systems')
    parser.add_argument(
        'pattern', help='filter for systems of the respective pattern'
    )
    parser.add_argument(
        'house_number', nargs='?',
        help='filter for systems of the respective house number'
    )


def _add_parser_find_deployments(subparsers: _SubParsersAction):
    """Adds a parser to find deployments."""

    parser = subparsers.add_parser('dep', help='find deployments')
    parser.add_argument(
        'pattern', help='filter for deployments of the respective pattern'
    )
    parser.add_argument(
        'house_number', nargs='?',
        help='filter for deployments of the respective house number'
    )


def _add_parser_find(subparsers: _SubParsersAction):
    """Adds a parser for searching."""

    parser = subparsers.add_parser('find', help='find records by address')
    target = parser.add_subparsers(dest='target')
    _add_parser_find_systems(target)
    _add_parser_find_deployments(target)


def get_args() -> Namespace:
    """Returns the CLI options."""

    parser = ArgumentParser(description='Hardware database query utility.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging'
    )
    subparsers = parser.add_subparsers(dest='action')
    _add_parser_list(subparsers)
    _add_parser_find(subparsers)
    subparsers.add_parser('CSM-101', help='?')
    return parser.parse_args()
