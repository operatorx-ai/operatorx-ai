from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.agents.base import AgentContext
from app.agents.registry import registry

# Basic module-level logger
logger = logging.getLogger("operatorx.core.engine")


@dataclass
class EngineResult:
    agent: str
    request_id: Optional[str]
    tier: str
    output: Dict[str, Any]
    ok: bool = True
    error: Optional[str] = None


class CoreEngine:
    """
    Shared core engine for routing tasks to agents.

    Phase 2: introduce clean execution boundaries:
    - central routing and execution path
    - minimal logging
    - consistent error handling
    """

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        ctx: AgentContext,
    ) -> EngineResult:
        # Log start (keep it lightweight)
        logger.info(
            "engine.run_agent start agent=%s tier=%s request_id=%s",
            agent_name,
            ctx.tier,
            ctx.request_id,
        )

        try:
            agent = registry.get(agent_name)
        except Exception as e:
            # Registry raised an error (unknown agent, etc.)
            logger.warning(
                "engine.run_agent unknown agent=%s tier=%s request_id=%s error=%s",
                agent_name,
                ctx.tier,
                ctx.request_id,
                str(e),
            )
            return EngineResult(
                agent=agent_name,
                request_id=ctx.request_id,
                tier=ctx.tier,
                output={},
                ok=False,
                error=f"Unknown agent: {agent_name}",
            )

        try:
            result = agent.run(input_data, ctx)

            logger.info(
                "engine.run_agent success agent=%s tier=%s request_id=%s",
                agent_name,
                ctx.tier,
                ctx.request_id,
            )

            return EngineResult(
                agent=agent_name,
                request_id=ctx.request_id,
                tier=ctx.tier,
                output=result,
                ok=True,
                error=None,
            )

        except Exception as e:
            # Unexpected runtime error during agent execution
            logger.exception(
                "engine.run_agent failure agent=%s tier=%s request_id=%s",
                agent_name,
                ctx.tier,
                ctx.request_id,
            )
            return EngineResult(
                agent=agent_name,
                request_id=ctx.request_id,
                tier=ctx.tier,
                output={},
                ok=False,
                error="Agent execution failed",
            )


engine = CoreEngine()
