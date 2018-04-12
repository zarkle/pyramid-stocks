from .meta import Base
from sqlalchemy.orm import relationship
from .association import association_table
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, unique=True)
    companyName = Column(String, nullable=False)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(Text)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)
    account_id = relationship('Account', secondary=association_table, back_populates='stock_id')

