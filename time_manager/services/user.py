from time_manager.services.base import BaseService
from time_manager.db import tables
from time_manager.schemas import user as user_schemas

from sqlalchemy import select, exc
from fastapi import status
from fastapi.exceptions import HTTPException


class UserService(BaseService):
    async def get_list(self):
        query = select(tables.User)
        query = query.order_by(tables.User.id)
        return await self.session.scalars(query)

    async def get(self, user_id: int):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def create(self, user_schema: user_schemas.UserCreate):
        user = tables.User(**user_schema.model_dump(exclude={'password'}))
        self.session.add(user)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return user

    async def update(self, user_id: int, user_schema: user_schemas.UserUpdate):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user.username = user_schema.username or user.username
        user.first_name = user_schema.first_name or user.first_name
        user.second_name = user_schema.second_name or user.second_name
        user.job_title = user_schema.job_title or user.job_title
        user.hour_payment = user_schema.hour_payment or user.hour_payment
        self.session.add(user)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return user

    async def delete(self, user_id: int):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = await self.session.scalar(query)
        await self.session.delete(user)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
