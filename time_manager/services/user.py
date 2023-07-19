from .base import BaseService
from time_manager.db import tables
from time_manager.schemas import user as user_schemas

from sqlalchemy import select
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    def get_list(self):
        query = select(tables.User)
        query = query.order_by(tables.User.id)
        return self.session.scalars(query)

    def get(self, user_id: int):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        return self.session.one(query)

    def create(self, user_schema: user_schemas.UserCreate):
        user = tables.User(**user_schema.dict(exclude={'password'}))
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_schema: user_schemas.UserUpdate):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = self.session.one(query)
        user.first_name = user_schema.first_name or user.first_name
        user.second_name = user_schema.second_name or user.second_name
        user.job_title = user_schema.job_title or user.job_title
        user.password = user_schema.password or user.password
        self.session.add(user)
        return user

    def delete(self, user_id: int):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = self.session.one(query)
        self.session.delete(user)
