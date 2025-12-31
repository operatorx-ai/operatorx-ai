from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/agents", tags=["agents"])


class OrchestrateRequest(BaseModel):
    goal: str
    constraints: List[str] = []


class OrchestrateResponse(BaseModel):
    plan: List[str]


@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(request: OrchestrateRequest) -> OrchestrateResponse:
    """
    Orchestrator stub.
    This simulates how an agent would break a goal into steps.
    """
    plan = [
        f"Analyze goal: {request.goal}",
        "Evaluate constraints",
        "Generate execution plan",
        "Return structured response",
    ]

    return OrchestrateResponse(plan=plan)
