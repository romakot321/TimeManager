from pydantic import BaseModel
from datetime import date


class HourNoteBase(BaseModel):
    user_id: int
    date: date
    hours: int

    class Config:
        from_attributes = True


class HourNoteCreate(HourNoteBase):
    pass


class HourNote(HourNoteBase):
    id: int
