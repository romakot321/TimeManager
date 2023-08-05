from pydantic import BaseModel


class UserBase(BaseModel):
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
    first_name: str | None = None
    second_name: str | None = None
    job_title: str | None = None

    class Config:
        from_attributes = True
