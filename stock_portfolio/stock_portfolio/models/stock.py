from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stock_app'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, unique=True)
    companyName = Column(String, nullable=False)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)

