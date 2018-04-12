from .meta import Base
from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt
from sqlalchemy.orm import relationship
from .association import association_table
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)

manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    stock_id = relationship('Stock', secondary=association_table, back_populates='account_id')

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)
        self.registered_on = dt.now()
        self.admin = admin

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        if request.dbsession is None:
            raise DBAPIError

        is_authenicated = False

        query = request.dbsession.query(cls).filter(cls.username == username).one_or_none()

        if query is not None:
            if manager.check(query.password, password):
                is_authenicated = True

        return (is_authenicated, username)

