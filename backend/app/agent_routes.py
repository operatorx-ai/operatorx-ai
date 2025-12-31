from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.agents.base import AgentContext
from app.agents.registry import registry

router = APIRouter(prefix="/agents", tags=["agents"])


class OrchestrateRequest(BaseModel):
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    plan: List[str]


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(request: OrchestrateRequest) -> OrchestrateResponse:
    agent = registry.get("orchestrator")

    ctx = AgentContext(
        tier="personal",
        request_id=None
    )

    result = agent.run(request.model_dump(), ctx)

    return OrchestrateResponse(plan=result["plan"])

