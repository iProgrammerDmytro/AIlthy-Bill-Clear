import pytest

from app.bill.schemas import SimplifyRequest
from app.bill.services import BillService


@pytest.mark.asyncio
class TestBillService:
    async def test_simplify_calls_llm(self, monkeypatch: pytest.MonkeyPatch):
        """BillService should forward the text to the LLM and return its answer."""
        captured = {}

        class StubLLM:
            async def simplify_bill(self, text: str) -> str:
                captured["text"] = text
                return "Plain english"

        # inject stub → no network call
        service = BillService(llm=StubLLM())

        result = await service.simplify(SimplifyRequest(text="RAW BILL"))

        assert result == "Plain english"
        assert captured["text"] == "RAW BILL"

    async def test_simplify_propagates_error(self, monkeypatch: pytest.MonkeyPatch):
        """If the LLM wrapper raises, the service should re-raise (endpoint handles)."""

        class BoomLLM:
            async def simplify_bill(self, text: str) -> str:  # pragma: no cover
                raise RuntimeError("LLM down")

        service = BillService(llm=BoomLLM())

        with pytest.raises(RuntimeError, match="LLM down"):
            await service.simplify(SimplifyRequest(text="RAW BILL"))
