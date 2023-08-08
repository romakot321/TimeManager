import datetime as dt

from pydantic import BaseModel


class NoteSummary(BaseModel):
    minutes: int
    payment: int | None = None

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    minutes: int | None = None
    text: str | None = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    user_id: int
    date: dt.date

    class Config:
        from_attributes = True


class NoteUpdate(BaseModel):
    minutes: int | None = None
    text: str | None = None
