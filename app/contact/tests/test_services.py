import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.contact.models import Contact
from app.contact.schemas import ContactCreate
from app.contact.services import ContactService


@pytest.mark.asyncio
class TestContactService:
    async def test_upsert_new_contact(self, db: AsyncSession):
        service = ContactService()
        schema_in = ContactCreate(email="new@example.com", phone="+1234567890")

        out = await service.upsert_contact(schema_in, db)

        assert out.email == schema_in.email
        assert out.phone == schema_in.phone

        db_obj = await db.scalar(
            select(Contact).where(Contact.email == schema_in.email)
        )
        assert db_obj is not None

    async def test_upsert_updates_phone_only_when_provided(self, db: AsyncSession):
        service = ContactService()
        email = "reuse@example.com"
        phone = "+1234567890"

        # 1) initial insert
        await service.upsert_contact(ContactCreate(email=email, phone=phone), db)

        # 2) upsert with phone=NULL should keep "111"
        await service.upsert_contact(ContactCreate(email=email), db)

        kept = await db.scalar(select(Contact).where(Contact.email == email))
        assert kept.phone == phone

        # 3) upsert with new phone overrides
        new_phone = "+0987654321"
        await service.upsert_contact(ContactCreate(email=email, phone=new_phone), db)

        stmt = select(Contact).where(Contact.email == email)
        updated = await db.scalar(stmt.execution_options(populate_existing=True))

        assert updated.phone == new_phone
