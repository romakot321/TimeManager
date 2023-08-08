from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import PrimaryKeyConstraint
from time_manager.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    hour_payment = Column(Integer)


class Note(Base):
    __tablename__ = "notes"

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    minutes = Column(Integer, nullable=False, default=0)
    text = Column(Text, nullable=False, default="")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
        {},
    )
