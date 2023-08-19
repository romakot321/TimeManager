import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from time_manager import schemas
from time_manager.db.base import settings
from time_manager.services.base import BaseService, get_session
from time_manager.services.user import UserService


logger = logging.getLogger(__name__)

ALGORITHM = "HS256"


class AuthService(BaseService):
    SECRET_KEY = settings.SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.SESSION_LIFETIME
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/api/login",
        scheme_name="oauth2_schema"
    )

    def __init__(self, user_service: UserService = Depends()):
        super().__init__()
        self.user_service = user_service

    async def create_user(self, user_schema: schemas.user.UserCreate):
        user_schema.password = self.get_password_hash(user_schema.password)
        return await self.user_service.create(user_schema)

    async def update_user(self, user_id: int, user_schema: schemas.user.UserUpdate):
        user_schema.password = self.get_password_hash(user_schema.password)
        return await self.user_service.update(user_id, user_schema)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = schemas.token.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        session = get_session()
        open_session = await anext(session)
        user_service = UserService(open_session)
        try:
            await anext(session)
        except StopAsyncIteration:
            await open_session.close()
        user = await user_service.get(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_service.get(username=username, raise_exception=False)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token
