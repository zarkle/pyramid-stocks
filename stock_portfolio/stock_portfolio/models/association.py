from .meta import Base
from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
)

association_table = Table(
    'association',
    Base.metadata,
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('stock_id', Integer, ForeignKey('stock.id'))
)
