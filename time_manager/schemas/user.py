from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    second_name: str
    job_title: str
    hour_payment: int | None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    job_title: str | None = None
    hour_payment: int | None = None
    password: str | None = None

    class Config:
        from_attributes = True
