"""Digital signage displays."""

from peewee import JOIN
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Select

from mdb import Address, Company, Customer

from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment
from hwdb.orm.system import System
from hwdb.orm.openvpn import OpenVPN


__all__ = ['Display']


class Display(BaseModel):   # pylint: disable=R0903
    """A physical display out in the field."""

    address = ForeignKeyField(
        Address, null=True, column_name='address', backref='displays',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    annotation = CharField(255, null=True)
    system = ForeignKeyField(
        System, null=True, column_name='system', backref='displays',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    installed = DateTimeField(null=True)
    make = CharField(255, null=True)   # Hardware make.
    model = CharField(255, null=True)   # Hardware model.
    serial_number = CharField(255, null=True)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> Select:
        """Selects systems."""
        if not cascade:
            return super().select(*args, **kwargs)

        dep_customer = Customer.alias()
        dep_company = Company.alias()
        dep_address = Address.alias()
        lpt_address = Address.alias()
        dataset = Deployment.alias()
        ds_customer = Customer.alias()
        ds_company = Company.alias()
        ds_address = Address.alias()
        ds_lpt_address = Address.alias()
        args = {
            cls, Address, System, Customer, Company, Deployment, dep_customer,
            dep_company, dep_address, lpt_address, dataset, ds_customer,
            ds_company, ds_address, ds_lpt_address, OpenVPN, *args
        }
        return super().select(*args, **kwargs).join(
            # Address
            Address, join_type=JOIN.LEFT_OUTER).join_from(
            # System
            cls, System, join_type=JOIN.LEFT_OUTER).join_from(
            # Operator
            System, Customer, join_type=JOIN.LEFT_OUTER).join(
            Company, join_type=JOIN.LEFT_OUTER).join_from(
            # Deployment
            System, Deployment, on=System.deployment == Deployment.id,
            join_type=JOIN.LEFT_OUTER).join(
            dep_customer, join_type=JOIN.LEFT_OUTER).join(
            dep_company, join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, dep_address, on=Deployment.address == dep_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, lpt_address,
            on=Deployment.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            # Dataset
            System, dataset, on=System.dataset == dataset.id,
            join_type=JOIN.LEFT_OUTER).join(
            ds_customer, join_type=JOIN.LEFT_OUTER).join(
            ds_company, join_type=JOIN.LEFT_OUTER).join_from(
            dataset, ds_address, on=dataset.address == ds_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            dataset, ds_lpt_address, on=dataset.lpt_address == ds_lpt_address,
            join_type=JOIN.LEFT_OUTER).join_from(
            # OpenVPN
            System, OpenVPN, join_type=JOIN.LEFT_OUTER)
