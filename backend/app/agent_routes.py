from fastapi import APIRouter, Header, Request
from pydantic import BaseModel
from typing import List

# Agent execution context and registry
from app.agents.base import AgentContext
from app.agents.registry import registry

# Tier normalization helper (personal / business / government)
from app.tier import normalize_tier

# Shared core execution engine (single execution path)
from app.core.engine import engine

# Router for all agent-related endpoints
router = APIRouter(prefix="/agents", tags=["agents"])


# ----------------------------
# Request / Response Models
# ----------------------------

class OrchestrateRequest(BaseModel):
    """
    Input payload for orchestration requests.

    Represents a high-level user or system goal along with optional
    constraints that may influence planning or execution behavior.
    """
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    """
    Structured response returned by the orchestrator.

    The plan is intentionally returned as a list to keep the API
    deterministic, readable, and easy to extend in later phases.
    """
    plan: List[str]


# ----------------------------
# Routes
# ----------------------------

@router.get("", summary="List available agents")
def list_agents():
    """
    Returns all agents currently registered in the AgentRegistry.

    This endpoint supports:
    - Debugging and observability
    - Platform introspection
    - Future admin and UI tooling
    """
    return {"agents": registry.list()}


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(
    request_body: OrchestrateRequest,
    request: Request,
    x_operatorx_tier: str | None = Header(
        default=None,
        alias="X-OperatorX-Tier"
    ),
) -> OrchestrateResponse:
    """
    Orchestrates a plan using the shared Core Engine.

    Design notes:
    - The API layer remains thin and declarative
    - All execution logic flows through the CoreEngine
    - Deployment behavior is controlled via tier-aware context
    - Request tracing is supported through request_id propagation
    """

    # Build the execution context for this request.
    # Tier controls deployment-specific behavior.
    # request_id enables tracing across middleware, logs, and agents.
    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=getattr(request.state, "request_id", None),
    )

    # Delegate execution to the core engine.
    # The engine resolves the agent and runs it in a controlled manner.
    engine_result = engine.run_agent(
        "orchestrator",
        request_body.model_dump(),
        ctx
    )

    # Return only the public-facing portion of the result.
    # Internal metadata remains inside the engine layer.
    return OrchestrateResponse(plan=engine_result.output["plan"])


