from .meta import Base
from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

association_table = Table(
    'association',
    Base.metadata,
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('stock_id', Integer, ForeignKey('stock.id'))
)
