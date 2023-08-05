from time_manager.services.base import BaseService
from time_manager.db import tables
from time_manager import schemas

import datetime as dt
import calendar
import logging

from sqlalchemy import select, exc, func
from fastapi import status
from fastapi.exceptions import HTTPException


logger = logging.getLogger(__name__)


class NoteService(BaseService):
    async def create(
            self, user_id: int, date: dt.date,
            note_schema: schemas.note.NoteCreate
    ):
        note = tables.Note(
            user_id=user_id, date=date, **note_schema.model_dump()
        )
        self.session.add(note)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            return await self.get(user_id, date)
        return note

    async def update(
            self, user_id: int, date: dt.date,
            note_schema: schemas.note.NoteUpdate
    ):
        query = select(tables.Note).filter_by(user_id=user_id, date=date)
        note: tables.Note = await self.session.scalar(query)
        note.minutes = note_schema.minutes or note.minutes
        note.text = note_schema.text or note.text
        self.session.add(note)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            return await self.get(user_id, date)
        return note

    async def get(self, user_id, date):
        query = select(tables.Note)
        query = query.filter_by(user_id=user_id, date=date)
        try:
            note = await self.session.scalar(query)
            if note is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return note
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    async def get_list(self, user_id: int):
        query = select(tables.Note)
        query = query.filter_by(user_id=user_id)
        try:
            notes = await self.session.scalars(query)
            return notes
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    async def get_summary(self, user_id: int, year: int, month: int, part: int):
        query = select(func.sum(tables.Note.minutes))
        query = query.filter_by(user_id=user_id)
        month_start, month_end = self.get_date_range(year, month, part)
        query = query.filter(tables.Note.date >= month_start)
        query = query.filter(tables.Note.date <= month_end)
        try:
            minutes = await self.session.scalar(query) or 0
            return schemas.note.NoteSummary(minutes=minutes)
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_date_range(year: int, month: int, part: int | None) -> tuple[dt.date, dt.date]:
        if year < 2000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        match part:
            case 1:
                start_day = 1
                end_day = 15
            case 2:
                start_day = 16
                end_day = calendar.monthrange(year, month)[1]
            case None:
                start_day = 1
                end_day = calendar.monthrange(year, month)[1]
            case _:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        try:
            month_start = dt.date(year=year, month=month, day=start_day)
            month_end = dt.date(year=year, month=month, day=end_day)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return month_start, month_end
