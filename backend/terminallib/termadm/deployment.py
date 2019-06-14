"""Handles deployments."""

from logging import getLogger

from mdb import Address

from terminallib.orm.deployment import Deployment


__all__ = ['add']


LOGGER = getLogger('termadm')


def add(args):
    """Adds a deployment."""

    address = (args.street, args.house_number, args.zip_code, args.city)
    address = Address.add_by_address(address)
    address.save()
    select = Deployment.address == address
    select &= Deployment.customer == args.customer
    select &= Deployment.type == args.type

    try:
        deployment = Deployment.get(select)
    except Deployment.DoesNotExist:
        deployment = Deployment(
            customer=args.customer, type=args.type, address=address)
        deployment.save()
        LOGGER.info('Added deployment #%i.', deployment.id)
    else:
        LOGGER.info('Using existing deployment #%i.', deployment.id)

    return True
