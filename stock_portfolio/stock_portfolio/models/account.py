from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
