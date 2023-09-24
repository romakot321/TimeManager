import datetime as dt
import logging

from fastapi import APIRouter, Depends

from time_manager import schemas
from time_manager.db import tables
from time_manager.services.auth import AuthService
from time_manager.services.note import NoteService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/notes',
    tags=["Notes"],
)


@router.get(
    '/me',
    response_model=list[schemas.note.Note]
)
async def get_user_note_list(
        service: NoteService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.get_list(user.id)


@router.get(
    '/me/summary/{organization_shortname}/{year}-{month}/{part}',
    response_model=schemas.note.NoteSummary,
    description="""
    Get total user work time and payment for a month
    part: {1, 2} - first or last two weeks of month
    organization: shortname of organization
    """
)
async def get_user_summary(
        year: int,
        month: str,
        part: str,
        organization_shortname: str,
        service: NoteService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.get_summary(user.id, organization_shortname, year, int(month), part)


@router.get(
    '/me/{date}',
    response_model=schemas.note.Note
)
async def get_note(
        date: dt.date,
        service: NoteService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.get(user.id, date)


@router.post(
    '/me/{date}',
    response_model=schemas.note.Note
)
async def create_note(
        date: dt.date,
        schema: schemas.note.NoteCreate,
        service: NoteService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.create(user.id, date, schema)


@router.patch(
    '/me/{date}',
    response_model=schemas.note.Note
)
async def update_note(
        date: dt.date,
        schema: schemas.note.NoteUpdate,
        service: NoteService = Depends(),
        user: tables.User = Depends(AuthService.get_current_user)
):
    return await service.update(user.id, date, schema)
