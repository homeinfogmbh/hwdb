"""Handles deployments."""

from logging import getLogger

from mdb import Address

from hwdb.orm.deployment import Deployment


__all__ = ['add']


LOGGER = getLogger('hwadm')


def add(args):
    """Adds a deployment."""

    address = (args.street, args.house_number, args.zip_code, args.city)
    address = Address.add_by_address(address)
    address.save()
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

    return True
