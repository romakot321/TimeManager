from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Text
from time_manager.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True,
                index=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    password = Column(String, nullable=False)


class HourNote(Base):
    __tablename__ = "hours"

    id = Column(Integer, autoincrement=True, primary_key=True,
                index=True)
    user_id = Column(ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    hours = Column(Integer, nullable=False)


class TaskNote(Base):
    __tablename__ = "tasks"

    id = Column(Integer, autoincrement=True, primary_key=True,
                index=True)
    user_id = Column(ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    text = Column(Text, nullable=False)
