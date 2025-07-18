from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db.dependencies import AsyncSessionDependency

from .models import Contact
from .schemas import ContactCreate


class ContactService:
    async def upsert_contact(
        self, data: ContactCreate, db: AsyncSessionDependency
    ) -> Contact:
        """
        • Inserts a new contact.
        • If the e-mail already exists, updates phone **only if the caller sent one**.
          (Otherwise keeps the existing phone.)
        • Always returns the contact row in one round‑trip.
        """
        
        insert = pg_insert(Contact).values(**data.model_dump())
        
        # phone := COALESCE(EXCLUDED.phone, contacts.phone)
        stmt = (
            insert.on_conflict_do_update(
                index_elements=[Contact.email],
                set_={
                    "phone": func.coalesce(
                        insert.excluded.phone,  # the new value (may be NULL)
                        Contact.phone,          # the existing value
                    )
                }
            )
            .returning(Contact)
        )

        result = await db.execute(stmt)
        await db.commit()

        return result.scalar_one()
