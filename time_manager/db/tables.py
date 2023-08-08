from sqlalchemy import Column, Date, ForeignKey, Integer, PrimaryKeyConstraint, String, Text

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
