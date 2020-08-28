"""Command line argument parsing."""

from argparse import ArgumentParser

from hwdb.enumerations import Connection, OperatingSystem, Type
from hwdb.hooks import bind9cfgen, openvpncfgen
from hwdb.pseudotypes import connection
from hwdb.pseudotypes import customer
from hwdb.pseudotypes import date
from hwdb.pseudotypes import deployment
from hwdb.pseudotypes import hook
from hwdb.pseudotypes import operating_system
from hwdb.pseudotypes import type_
from hwdb.pseudotypes import system


__all__ = ['get_args']


DEFAULT_HOOKS = (bind9cfgen, openvpncfgen)


def _add_new_system_parser(subparsers):
    """Adds a parser to add new systems."""

    parser = subparsers.add_parser('sys', help='add new systems')
    parser.add_argument(
        '-n', '--amount', type=int, default=1, help='amount of systems to add')
    parser.add_argument(
        '-d', '--deployment', type=deployment,
        help='the deployment of the system')
    parser.add_argument('--key', help='the OpenVPN key to use')
    parser.add_argument(
        '--mtu', type=int, help='the MTU for the OpenVPN tunnel')
    parser.add_argument(
        '-m', '--manufacturer', type=customer,
        help="the system's manufacturer")
    parser.add_argument(
        '-o', '--operating-system', type=operating_system,
        default=OperatingSystem.ARCH_LINUX,
        help='the installed operating system')
    parser.add_argument(
        '--monitor', type=int, help='set explicit monitoring flag')
    parser.add_argument(
        '-s', '--serial-number', help='the serial number of the hardware')
    parser.add_argument('--model', help='the hardware model')


def _add_new_deployment_parser(subparsers):
    """Adds a deployment parser."""

    parser = subparsers.add_parser('dep', help='add new deployments')
    parser.add_argument(
        'customer', type=customer, help='the owner of the deployment')
    parser.add_argument('street', help='the street name')
    parser.add_argument('house_number', help='the house number')
    parser.add_argument('zip_code', help='the ZIP code')
    parser.add_argument('city', help='the city')
    parser.add_argument(
        '-t', '--type', type=type_, default=Type.DDB, help='the system type')
    parser.add_argument(
        '-c', '--connection', type=connection, default=Connection.DSL,
        help='the internet connection on site')
    parser.add_argument(
        '-s', '--scheduled', type=date, help='the scheduled date')
    parser.add_argument('-a', '--annotation', help='a descriptive annotation')
    parser.add_argument(
        '--testing', action='store_true',
        help='flag the deployment as testing')


def _add_new_parser(subparsers):
    """Adds a parser for adding records."""

    parser = subparsers.add_parser('add', help='add new records')
    subparsers = parser.add_subparsers(dest='target')
    _add_new_system_parser(subparsers)
    _add_new_deployment_parser(subparsers)


def _add_deploy_parser(subparsers):
    """Adds a parser for deployment of systems."""

    parser = subparsers.add_parser('deploy', help='deploy systems')
    parser.add_argument('system', type=system, help='the system to deploy')
    parser.add_argument(
        'deployment', type=deployment, help='the deployment site')


def _add_undeploy_parser(subparsers):
    """Adds a parser for undeploying systems."""

    parser = subparsers.add_parser('undeploy', help='undeploy systems')
    parser.add_argument(
        'system', nargs='+', type=system, help='the system to deploy')


def _add_hooks_parser(subparsers):
    """Adds a parser for running hooks."""

    parser = subparsers.add_parser(
        'run-hooks', help='run post-transaction hooks')
    parser.add_argument(
        '-H', '--hooks', nargs='*', type=hook, default=DEFAULT_HOOKS,
        help='a list of hooks to run')


def get_args():
    """Parses the CLI arguments."""

    parser = ArgumentParser(description='Terminal database administration.')
    parser.add_argument(
        '-n', '--no-hooks', action='store_true',
        help='do not run post-transaction hooks')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging')
    subparsers = parser.add_subparsers(dest='action')
    _add_new_parser(subparsers)
    _add_deploy_parser(subparsers)
    _add_undeploy_parser(subparsers)
    _add_hooks_parser(subparsers)
    return parser.parse_args()
