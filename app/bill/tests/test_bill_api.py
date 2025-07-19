import pytest
from fastapi import status
from httpx import AsyncClient

from app.bill.schemas import SimplifyRequest

fake_resp = "Total: $350 - routine office visit."


@pytest.mark.asyncio
class TestSimplifyEndpoint:
    url = "/api/bill/simplify"

    async def test_simplify_success(
        self, client: AsyncClient, monkeypatch: pytest.MonkeyPatch
    ):
        async def fake_simplify(self, request: SimplifyRequest) -> str:
            return fake_resp

        monkeypatch.setattr(
            "app.bill.services.BillService.simplify",
            fake_simplify,
        )

        response = await client.post(
            self.url, json={"text": "CPT 99213 - Office Visit"}
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data == {"result": fake_resp}

    async def test_simplify_upstream_failure(
        self, client: AsyncClient, monkeypatch: pytest.MonkeyPatch
    ):
        async def boom(*_):
            raise RuntimeError

        monkeypatch.setattr("app.bill.services.BillService.simplify", boom)

        response = await client.post(
            self.url, json={"text": "CPT 99213 - Office Visit"}
        )
        assert response.status_code == status.HTTP_502_BAD_GATEWAY

        data = response.json()
        assert "LLM service unavailable" in data["detail"]
