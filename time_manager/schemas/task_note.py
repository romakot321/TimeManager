from pydantic import BaseModel
from datetime import date


class TaskNoteBase(BaseModel):
    user_id: int
    date: date
    text: str

    class Config:
        from_attributes = True


class TaskNoteCreate(TaskNoteBase):
    pass


class HourNote(TaskNoteBase):
    id: int
