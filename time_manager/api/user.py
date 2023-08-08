import logging

from fastapi import APIRouter, Depends

from time_manager import schemas
from time_manager.db import tables
from time_manager.services.auth import AuthService
from time_manager.services.user import UserService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/users',
    tags=["Users"],
)


@router.get(
    '/me',
    response_model=schemas.user.User
)
async def get_user(
        service: UserService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.get(user.id)


@router.post(
    '',
    response_model=schemas.user.User
)
async def create_user(
        user_schema: schemas.user.UserCreate,
        service: AuthService = Depends()
):
    return await service.create_user(user_schema)


@router.patch(
    '/me',
    response_model=schemas.user.User
)
async def patch_user(
        user_schema: schemas.user.UserUpdate,
        service: AuthService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.update_user(user.id, user_schema)


@router.delete(
    '/me'
)
async def delete_user(
        service: UserService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.delete(user.id)
