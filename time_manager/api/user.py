import logging

from fastapi import APIRouter, Depends
from time_manager.services.user import UserService
from time_manager import schemas


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api',
    tags=["Hello"],
)


@router.get('')
async def get_hello_msg():
    return 'Hello from FastAPI and Lawrence'


@router.get(
    '/users',
    response_model=list[schemas.user.User]
)
async def get_list_of_users(
        service: UserService = Depends()
):
    return await service.get_list()


@router.get(
    '/users/{user_id}',
    response_model=schemas.user.User
)
async def create_coffee(
        user_id: int,
        service: UserService = Depends()
):
    return service.get(user_id)
