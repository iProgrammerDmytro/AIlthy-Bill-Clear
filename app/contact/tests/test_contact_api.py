import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.contact.models import Contact


@pytest.mark.asyncio
class TestSubscribeEndpoint:
    url = "/api/contact/subscribe"

    async def test_contract_create_success(self, client: AsyncClient, db: AsyncSession):
        payload = {"email": "alice@example.com", "phone": "+1234567890"}

        response = await client.post(self.url, json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        for key, value in payload.items():
            assert data[key] == value

        # DB round-trip → prove persistence
        contact = await db.scalar(
            select(Contact).where(Contact.email == payload["email"])
        )

        assert contact is not None
        assert contact.phone == payload["phone"]

    async def test_upsert_keeps_existing_phone(self, client: AsyncClient, db):
        """Second call with same e-mail but no phone keeps old phone."""
        first = {"email": "bob@example.com", "phone": "+1234567890"}
        second = {"email": "bob@example.com"}  # <- phone ommited

        await client.post(self.url, json=first)
        response = await client.post(self.url, json=second)

        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data["phone"] == first["phone"]  # unchanged

    async def test_validation_error_on_bad_email(self, client: AsyncClient):
        bad_payload = {"email": "not-an-email", "phone": "123"}
        response = await client.post(self.url, json=bad_payload)

        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        )  # FastAPI / Pydantic validation error
