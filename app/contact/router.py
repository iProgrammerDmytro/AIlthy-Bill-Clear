from fastapi import APIRouter, Depends, HTTPException, status

from app.db.dependencies import AsyncSessionDependency

from .schemas import ContactCreate, ContactRead
from .services import ContactService

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post(
    "/subscribe", response_model=ContactRead, status_code=status.HTTP_201_CREATED
)
async def subscribe(
    payload: ContactCreate,
    db: AsyncSessionDependency,
    service: ContactService = Depends(ContactService),
):
    contact = await service.upsert_contact(payload, db)

    return contact
