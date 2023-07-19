from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    second_name: str
    job_title: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserUpdate(BaseModel):
    first_name: str | None
    second_name: str | None
    job_title: str | None
    password: str | None

    class Config:
        from_attributes = True
