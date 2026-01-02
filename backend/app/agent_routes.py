from fastapi import APIRouter, Header, Request
from pydantic import BaseModel
from typing import List

# Agent execution context object passed through the system
from app.agents.base import AgentContext

# Registry used only for discovery (not execution)
from app.agents.registry import registry

# Helper to normalize deployment tier values (personal/business/government)
from app.tier import normalize_tier

# Shared core engine responsible for routing + execution
from app.core.engine import engine

# Router grouping all agent-related endpoints
router = APIRouter(prefix="/agents", tags=["agents"])


# ============================================================
# Request / Response Models
# ============================================================

class OrchestrateRequest(BaseModel):
    """
    Input payload for orchestration requests.

    Represents a high-level goal plus optional constraints.
    Keeping this small makes the API stable while we iterate.
    """
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    """
    Public-facing response returned by the orchestrator.

    We return a simple list of steps:
    - easy to debug
    - easy to display in a UI later
    - easy to extend (add metadata later without breaking clients)
    """
    plan: List[str]


# ============================================================
# Routes
# ============================================================

@router.get("", summary="List available agents")
def list_agents():
    """
    Lists all agents registered in the system.

    Purpose:
    - Debugging and observability
    - Platform introspection
    - Future admin tooling / dashboards
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

    Architecture:
    - API layer stays thin (no business logic here)
    - CoreEngine is the only execution entry point
    - Tier controls behavior via AgentContext
    - request_id supports traceability end-to-end
    """

    # --------------------------------------------------------
    # 1) Build execution context
    # --------------------------------------------------------
    # normalize_tier() ensures we always have a safe tier value:
    #   personal / business / government (fallback handled inside normalize_tier)
    #
    # request_id is injected by RequestIdMiddleware and stored on request.state
    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=getattr(request.state, "request_id", None),
    )

    # --------------------------------------------------------
    # 2) Execute agent through Core Engine
    # --------------------------------------------------------
    # The engine:
    # - resolves the agent by name
    # - runs it safely
    # - applies consistent logging + error handling
    engine_result = engine.run_agent(
        agent_name="orchestrator",
        input_data=request_body.model_dump(),
        ctx=ctx,
    )

    # --------------------------------------------------------
    # 3) Handle errors (simple Phase 2 approach)
    # --------------------------------------------------------
    if not engine_result.ok:
        # Keep error response deterministic and readable
        return OrchestrateResponse(plan=[f"ERROR: {engine_result.error}"])

    # --------------------------------------------------------
    # 4) Return public-facing response only
    # --------------------------------------------------------
    # We only expose the plan; internal metadata stays inside EngineResult
    return OrchestrateResponse(plan=engine_result.output.get("plan", []))
class OrchestrateResponse(BaseModel):
    """
    Public-facing response returned by the orchestrator.

    The plan is intentionally a list of steps to ensure:
    - deterministic output
    - easy inspection/debugging
    - future compatibility with UI rendering
    """
    plan: List[str]


# ============================================================
# Routes
# ============================================================

@router.get("", summary="List available agents")
def list_agents():
    """
    Lists all agents registered in the system.

    This endpoint supports:
    - Debugging and observability
    - Platform introspection
    - Admin tooling and dashboards (future)
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

    Architectural intent:
    - The API layer remains thin and declarative
    - All execution flows through the CoreEngine
    - Deployment-specific behavior is controlled via tier context
    - Request tracing is preserved using request_id propagation
    """

    # --------------------------------------------------------
    # Build execution context
    # --------------------------------------------------------
    # Tier controls how the system behaves (personal/business/gov).
    # request_id enables end-to-end tracing across middleware,
    # engine logs, agents, and future observability tooling.
    ctx = AgentContext(
        tier=normalize_tier(x_operatorx_tier),
        request_id=getattr(request.state, "request_id", None),
    )

    # --------------------------------------------------------
    # Delegate execution to the Core Engine
    # --------------------------------------------------------
    # The engine is the single execution entry point.
    # It resolves the agent, runs it, and handles errors/logging.
    engine_result = engine.run_agent(
        "orchestrator",
        request_body.model_dump(),
        ctx
    )

    # --------------------------------------------------------
    # Handle execution errors gracefully
    # --------------------------------------------------------
    # Phase 2 keeps error handling simple and consistent.
    if not engine_result.ok:
        return OrchestrateResponse(
            plan=[f"ERROR: {engine_result.error}"]
        )

    # --------------------------------------------------------
    # Return structured response
    # --------------------------------------------------------
    # Only return public output — internal metadata stays
    # inside the engine layer.
    return OrchestrateResponse(
        plan=engine_result.output["plan"]
    )
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


