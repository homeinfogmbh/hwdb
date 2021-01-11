"""Legacy smart TVs."""

from peewee import JOIN, CharField, ForeignKeyField, ModelSelect

from mdb import Address, Company, Customer

from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment


__all__ = ['SmartTV']


class SmartTV(BaseModel):
    """A smart TV."""

    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='smart_tvs',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    make = CharField(255, null=True)   # Hardware make.
    model = CharField(255, null=True)   # Hardware model.
    serial_number = CharField(255, null=True)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects systems."""
        if not cascade:
            return super().select(*args, **kwargs)

        lpt_address = Address.alias()
        args = {
            cls, Deployment, Customer, Company, Address, lpt_address, *args
        }
        return super().select(*args, **kwargs).join(
            Deployment, join_type=JOIN.LEFT_OUTER).join(
            Customer, join_type=JOIN.LEFT_OUTER).join(
            Company, join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, Address, on=Deployment.address == Address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, lpt_address,
            on=Deployment.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER)
