from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    second_name: str
    job_title: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    job_title: str | None = None

    class Config:
        from_attributes = True
