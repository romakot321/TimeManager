import logging
import datetime as dt

from fastapi import APIRouter, Depends
from time_manager.services.note import NoteService
from time_manager import schemas


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api',
    tags=["Hello"],
)


@router.get(
    '/{user_id}',
    response_model=list[schemas.note.Note]
)
async def get_user_note_list(
        user_id: int,
        service: NoteService = Depends()
):
    return await service.get_list(user_id)


@router.get(
    '/{user_id}/summary',
    response_model=schemas.note.NoteSummary
)
async def get_user_summary(
        user_id: int,
        service: NoteService = Depends()
):
    return await service.get_summary(user_id)


@router.get(
    '/{user_id}/{date}',
    response_model=schemas.note.Note
)
async def get_note(
        user_id: int,
        date: dt.date,
        service: NoteService = Depends()
):
    return await service.get(user_id, date)


@router.post(
    '/{user_id}/{date}',
    response_model=schemas.note.Note
)
async def create_note(
        user_id: int,
        date: dt.date,
        schema: schemas.note.NoteCreate,
        service: NoteService = Depends()
):
    return await service.create(user_id, date, schema)


@router.patch(
    '/{user_id}/{date}',
    response_model=schemas.note.Note
)
async def update_note(
        user_id: int,
        date: dt.date,
        schema: schemas.note.NoteUpdate,
        service: NoteService = Depends()
):
    return await service.update(user_id, date, schema)
