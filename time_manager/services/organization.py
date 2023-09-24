from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, select

from time_manager.db import tables
from time_manager.schemas import organization as org_schemas
from time_manager.services.base import BaseService


class OrganizationService(BaseService):
    async def get_list(self):
        query = select(tables.Organization)
        query = query.order_by(tables.Organization.id)
        return await self.session.scalars(query)

    async def get(self, org_id: int | None = None, name: str | None = None) -> tables.Organization | None:
        query = select(tables.Organization)
        if org_id is not None:
            query = query.filter_by(id=org_id)
        if name is not None:
            query = query.filter_by(name=name)
        org = await self.session.scalar(query)
        if org is None:
            if not raise_exception:
                return
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return org

    async def create(self, org_schema: org_schema.OrganizationCreate) -> tables.Organization:
        org = tables.Organization(**org_schema.model_dump())
        self.session.add(org)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return org

    async def update(self, org_id: int, org_schema: org_schemas.OrganizationUpdate) -> tables.Organization:
        query = select(tables.Organization)
        query = query.filter_by(id=org_id)
        org = await self.session.scalar(query)
        if org is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        org.name = org_schema.name or org.name
        self.session.add(org)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return org

    async def delete(self, org_id: int):
        query = select(tables.Organization)
        query = query.filter_by(id=org_id)
        org = await self.session.scalar(query)
        await self.session.delete(org)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT

    async def attach_user_to_organization(self, org_id: int, user_id: int):
        user_org = tables.UserOrgaization(user_id=user_id, org_id=org_id)
        self.session.add(user_org)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
