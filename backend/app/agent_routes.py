from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import List

# Agent context and registry
from app.agents.base import AgentContext
from app.agents.registry import registry

# Utility for normalizing deployment tier values
from app.tier import normalize_tier

# Create an API router for all agent-related endpoints
router = APIRouter(prefix="/agents", tags=["agents"])


# ----------------------------
# Request / Response Models
# ----------------------------

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


# ----------------------------
# Routes
# ----------------------------

@router.get("", summary="List available agents")
def list_agents():
    """
    Returns all agents currently registered in the AgentRegistry.
    Useful for discovery, debugging, and platform introspection.
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
    Orchestrates a plan using the OrchestratorAgent.

    The deployment tier is provided via the X-OperatorX-Tier HTTP header.
    If no tier is provided, a default is applied by normalize_tier().
    """

    # Retrieve the orchestrator agent from the registry
    agent = registry.get("orchestrator")

    # Build the agent execution context
    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=None  # Request ID support is handled elsewhere (middleware)
    )

    # Execute the agent with structured input and context
    result = agent.run(request.model_dump(), ctx)

    # Return a structured API response
    return OrchestrateResponse(plan=result["plan"])
