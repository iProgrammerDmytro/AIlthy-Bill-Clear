from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import SimplifyRequest, SimplifyResponse
from .services import BillService

router = APIRouter(prefix="/bill", tags=["Bill"])


@router.post("/simplify", response_model=SimplifyResponse)
async def simplify(
    request: SimplifyRequest, service: BillService = Depends(BillService)
) -> SimplifyResponse:
    try:
        result = await service.simplify(request)
    except Exception as exc:
        # TODO: log error
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM service unavailable. Try again later.",
        ) from exc
    return SimplifyResponse(result=result)
