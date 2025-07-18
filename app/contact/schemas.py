from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    created_at: datetime
