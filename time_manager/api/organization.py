import logging

from fastapi import APIRouter, Depends

from time_manager import schemas
from time_manager.db import tables
from time_manager.services.auth import AuthService
from time_manager.services.organization import OrganizationService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/organizations',
    tags=["Organizations"],
)


@router.get(
    '',
    response_model=schemas.organization.Organization
)
async def get_organization(
        service: OrganizationService = Depends(),
        organization: tables.Organization = Depends(AuthService.get_current_organization)
):
    return await service.get(organization.id)


@router.post(
    '',
    response_model=schemas.organization.Organization
)
async def create_organization(
        organization_schema: schemas.organization.OrganizationCreate,
        service: AuthService = Depends()
):
    return await service.create_organization(organization_schema)


@router.patch(
    '/me',
    response_model=schemas.organization.Organization
)
async def patch_organization(
        organization_schema: schemas.organization.OrganizationUpdate,
        service: AuthService = Depends(),
        organization: tables.Organization = Depends(AuthService.get_current_organization)
):
    return await service.update_organization(organization.id, organization_schema)


@router.delete(
    '/me'
)
async def delete_organization(
        service: OrganizationService = Depends(),
        organization: tables.Organization = Depends(get_organization)
):
    return await service.delete(organization.id)
