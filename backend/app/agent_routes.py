from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.agents.base import AgentContext
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/agents", tags=["agents"])


class OrchestrateRequest(BaseModel):
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    plan: List[str]


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(request: OrchestrateRequest) -> OrchestrateResponse:
    agent = OrchestratorAgent()

    ctx = AgentContext(
        tier="personal",  # we’ll make this dynamic later
        request_id=None
    )

    result = agent.run(request.model_dump(), ctx)

    return OrchestrateResponse(plan=result["plan"])
