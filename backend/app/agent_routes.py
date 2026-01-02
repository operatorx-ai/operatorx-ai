from fastapi import APIRouter, Header, Request
from pydantic import BaseModel
from typing import List

from app.agents.base import AgentContext
from app.agents.registry import registry
from app.tier import normalize_tier
from app.core.engine import engine

router = APIRouter(prefix="/agents", tags=["agents"])


# ============================================================
# Request / Response Models
# ============================================================

class OrchestrateRequest(BaseModel):
    """
    Input payload for orchestration requests.
    Represents a high-level goal and optional constraints.
    """
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    """
    Structured response returned by the orchestrator.
    Contains a step-by-step execution plan.
    """
    plan: List[str]


# ============================================================
# Routes
# ============================================================

@router.get("", summary="List available agents")
def list_agents():
    """
    Returns all agents currently registered in the AgentRegistry.
    """
    return {"agents": registry.list()}


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(
    request_body: OrchestrateRequest,
    request: Request,
    x_operatorx_tier: str | None = Header(default=None, alias="X-OperatorX-Tier"),
) -> OrchestrateResponse:
    """
    Orchestrates a plan using the shared Core Engine.
    """

    # Build execution context (tier + request_id)
    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=getattr(request.state, "request_id", None),
    )

    # Execute via core engine
    engine_result = engine.run_agent(
        "orchestrator",
        request_body.model_dump(),
        ctx
    )

    # Handle errors gracefully
    if not engine_result.ok:
        return OrchestrateResponse(
            plan=[f"ERROR: {engine_result.error}"]
        )

    return OrchestrateResponse(
        plan=engine_result.output["plan"]
    )
