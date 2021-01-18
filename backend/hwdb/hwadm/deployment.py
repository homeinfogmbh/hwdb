"""Handles deployments."""

from argparse import Namespace
from logging import getLogger

from mdb import Address

from hwdb.orm.deployment import Deployment


__all__ = ['add', 'batch_add']


LOGGER = getLogger('hwadm')


def from_address(args: Namespace, address: Address) -> None:
    """Adds a deployment from an address."""

    select = Deployment.address == address
    select &= Deployment.customer == args.customer
    select &= Deployment.type == args.type
    select &= Deployment.connection == args.connection
    select &= Deployment.annotation == args.annotation

    try:
        deployment = Deployment.get(select)
    except Deployment.DoesNotExist:
        deployment = Deployment(
            customer=args.customer, type=args.type, address=address,
            annotation=args.annotation, connection=args.connection)
        deployment.save()
        LOGGER.info('Added deployment #%i.', deployment.id)
    else:
        LOGGER.info('Using existing deployment #%i.', deployment.id)


def batch_add(args: Namespace) -> bool:
    """Adds multiple deployments from a file matching a regex."""

    result = True

    for path in args.file:
        with path.open('r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                match = args.regex.fullmatch(line)

                if match is not None:
                    address = Address.add_by_address(*match.groups())
                    from_address(args, address)
                else:
                    LOGGER.error('Could not parse address from: %s', line)
                    result = False

    return result


def add(args: Namespace) -> bool:
    """Adds a deployment."""

    address = (args.street, args.house_number, args.zip_code, args.city)
    address = Address.add_by_address(address)
    from_address(args, address)
    return True
