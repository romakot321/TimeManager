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
