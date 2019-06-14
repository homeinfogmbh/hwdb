"""Command line argument parsing."""

from argparse import ArgumentParser
from datetime import datetime

from mdb import Customer

from terminallib.enumerations import Connection, OperatingSystem, Type
from terminallib.orm.deployment import Deployment
from terminallib.orm.system import System


def date(string):
    """Parses a date."""

    return datetime.strptime(string, '%Y-%m-%d').date()


def _add_new_system_parser(subparsers):
    """Adds a parser to add new systems."""

    parser = subparsers.add_parser('sys', help='add new systems')
    parser.add_argument(
        '-n', '--amount', type=int, default=1, help='amount of systems to add')
    parser.add_argument(
        '-d', '--deployment', type=Deployment.__getitem__,
        help='the deployment of the system')
    parser.add_argument('--key', help='the OpenVPN key to use')
    parser.add_argument(
        '--mtu', type=int, help='the MTU for the OpenVPN tunnel')
    parser.add_argument(
        '-m', '--manufacturer', type=Customer.__getitem__,
        help="the system's manufacturer")
    parser.add_argument(
        '-o', '--operating-system', type=OperatingSystem,
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
        'customer', type=Customer.__getitem__,
        help='the owner of the deployment')
    parser.add_argument('street', help='the street name')
    parser.add_argument('house_number', help='the house number')
    parser.add_argument('zip_code', help='the ZIP code')
    parser.add_argument('city', help='the city')
    parser.add_argument('-t', '--type', type=Type, help='the system type')
    parser.add_argument(
        '-c', '--connection', type=Connection, default=Connection.DSL,
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
    parser.add_argument(
        'system', type=System.__getitem__, help='the system to deploy')
    parser.add_argument(
        'deployment', type=Deployment.__getitem__, help='the deployment site')


def _add_undeploy_parser(subparsers):
    """Adds a parser for undeploying systems."""

    parser = subparsers.add_parser('undeploy', help='undeploy systems')
    parser.add_argument(
        'system', nargs='+', type=System.__getitem__,
        help='the system to deploy')

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
    return parser.parse_args()
