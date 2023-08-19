import calendar
import datetime as dt
import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, func, select

from time_manager import schemas
from time_manager.db import tables
from time_manager.services.base import BaseService


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
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if note_schema.minutes is not None:
            note.minutes = note_schema.minutes
        if note_schema.text is not None:
            note.text = note_schema.text
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

    async def get_summary(self, user_id: int, year: int, month: int, part: str):
        minutes_query = select(func.sum(tables.Note.minutes))
        minutes_query = minutes_query.select_from(tables.User)
        minutes_query = minutes_query.join(tables.Note, tables.User.id == tables.Note.user_id)
        minutes_query = minutes_query.filter_by(user_id=user_id)
        month_start, month_end = self.get_date_range(year, month, part)
        minutes_query = minutes_query.filter(tables.Note.date >= month_start)
        minutes_query = minutes_query.filter(tables.Note.date <= month_end)
        payment_query = select(tables.User.hour_payment).filter_by(id=user_id)
        try:
            hour_payment = await self.session.scalar(payment_query)
            minutes = await self.session.scalar(minutes_query) or 0
            if hour_payment is not None:
                summary_payment = round(hour_payment * minutes / 60)
            else:
                summary_payment = None
            return schemas.note.NoteSummary(minutes=minutes, payment=summary_payment)
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_date_range(year: int, month: int, part: str | None) -> tuple[dt.date, dt.date]:
        if year < 2000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        part = part.lower()
        match part:
            case '1':
                start_day = 1
                end_day = 15
            case '2':
                start_day = 16
                end_day = calendar.monthrange(year, month)[1]
            case 'all':
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
