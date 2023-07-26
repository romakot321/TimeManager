import logging

from fastapi import APIRouter, Depends
from time_manager.services.user import UserService
from time_manager import schemas


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/users',
    tags=["Hello"],
)


@router.get(
    '',
    response_model=list[schemas.user.User]
)
async def get_user_list(
        service: UserService = Depends()
):
    return await service.get_list()


@router.get(
    '/{user_id}',
    response_model=schemas.user.User
)
async def get_user(
        user_id: int,
        service: UserService = Depends()
):
    return await service.get(user_id)


@router.post(
    '',
    response_model=schemas.user.User
)
async def create_user(
        user_schema: schemas.user.UserCreate,
        service: UserService = Depends()
):
    return await service.create(user_schema)


@router.patch(
    '/{user_id}',
    response_model=schemas.user.User
)
async def patch_user(
        user_id: int,
        user_schema: schemas.user.UserUpdate,
        service: UserService = Depends()
):
    return await service.update(user_id, user_schema)


@router.delete(
    '/{user_id}'
)
async def delete_user(
        user_id: int,
        service: UserService = Depends()
):
    return await service.delete(user_id)
