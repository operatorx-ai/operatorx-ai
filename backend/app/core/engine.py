from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.agents.base import AgentContext
from app.agents.registry import registry


@dataclass
class EngineResult:
    agent: str
    request_id: Optional[str]
    tier: str
    output: Dict[str, Any]


class CoreEngine:
    """
    Shared core engine for routing tasks to agents.
    Phase 2 focus: clean boundaries + simple execution flow.
    """

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        ctx: AgentContext,
    ) -> EngineResult:
        agent = registry.get(agent_name)
        result = agent.run(input_data, ctx)

        return EngineResult(
            agent=agent_name,
            request_id=ctx.request_id,
            tier=ctx.tier,
            output=result,
        )


engine = CoreEngine()
