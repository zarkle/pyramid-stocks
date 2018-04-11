from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, unique=True)
    # account_id = Column(Text, ForeignKey='account.id')
    companyName = Column(String, nullable=False)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(Text)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)

