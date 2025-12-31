from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import List

from app.agents.base import AgentContext
from app.agents.registry import registry
from app.tier import normalize_tier

router = APIRouter(prefix="/agents", tags=["agents"])


# ----------------------------
# Request / Response Models
# ----------------------------

class OrchestrateRequest(BaseModel):
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    plan: List[str]


# ----------------------------
# Routes
# ----------------------------

@router.get("", summary="List available agents")
def list_agents():
    """
    Returns all agents registered in the AgentRegistry.
    """
    return {"agents": registry.list()}


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(
    request: OrchestrateRequest,
    x_operatorx_tier: str | None = Header(
        default=None,
        alias="X-OperatorX-Tier"
    ),
) -> OrchestrateResponse:
    """
    Orchestrate a plan using a tier-aware agent.
    Tier is provided via the X-OperatorX-Tier header.
    """

    agent = registry.get("orchestrator")

    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=None
    )

    result = agent.run(request.model_dump(), ctx)

    return OrchestrateResponse(plan=result["plan"])



