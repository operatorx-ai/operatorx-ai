from fastapi import APIRouter, Header
from app.tier import normalize_tier

router = APIRouter(prefix="/tier", tags=["tier"])


@router.get("")
def get_tier(x_operatorx_tier: str | None = Header(default=None, alias="X-OperatorX-Tier")):
    return {
        "received_header": x_operatorx_tier,
        "normalized_tier": normalize_tier(x_operatorx_tier),
    }