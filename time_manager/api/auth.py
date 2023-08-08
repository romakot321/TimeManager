import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from time_manager.schemas.token import Token
from time_manager.services.auth import AuthService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/login',
    tags=["Auth"],
)


@router.post("", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends()
):
    access_token = await auth_service.authenticate_user(form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")
