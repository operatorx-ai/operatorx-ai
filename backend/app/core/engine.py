from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

# Context object that travels through the system (tier + request_id)
from app.agents.base import AgentContext

# Registry contains agent classes mapped by name (ex: "orchestrator")
from app.agents.registry import registry

# Memory store (Phase 2: in-memory only)
from app.core.memory import memory_store


# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
# Use a named logger so logs are easy to filter later.
logger = logging.getLogger("operatorx.core.engine")


# ------------------------------------------------------------
# Engine Result (structured output)
# ------------------------------------------------------------
@dataclass
class EngineResult:
    """
    Standard result container returned by CoreEngine.

    Why this exists:
    - Keeps outputs consistent across all agents
    - Centralizes success/error reporting
    - Allows future metadata (timing, traces, eval scores, etc.)
    """
    agent: str
    request_id: Optional[str]
    tier: str
    output: Dict[str, Any]

    # True when execution succeeds; False if an error occurs
    ok: bool = True

    # Human-readable error message when ok=False
    error: Optional[str] = None


# ------------------------------------------------------------
# Core Engine
# ------------------------------------------------------------
class CoreEngine:
    """
    Shared execution engine.

    Responsibilities (Phase 2):
    ✅ Resolve an agent by name
    ✅ Run it with input_data + AgentContext
    ✅ Apply consistent logging + error handling
    ✅ Store lightweight memory per request_id (debugging)

    Later phases may add:
    - routing rules
    - policy enforcement
    - retries
    - evaluation hooks
    - persistence (Redis/Postgres/etc.)
    """

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        ctx: AgentContext,
    ) -> EngineResult:
        """
        Main execution path.

        Args:
            agent_name: name of agent (ex: "orchestrator")
            input_data: dict payload to send into the agent
            ctx: AgentContext (tier + request_id)
        """

        # --------------------------------------------
        # Log execution start
        # --------------------------------------------
        logger.info(
            "engine.run_agent start agent=%s tier=%s request_id=%s",
            agent_name,
            ctx.tier,
            ctx.request_id,
        )

        # --------------------------------------------
        # Ensure memory exists for this request_id
        # --------------------------------------------
        # If middleware did not attach a request_id, we skip memory.
        if ctx.request_id:
            memory_store.ensure(request_id=ctx.request_id, tier=ctx.tier)

        # --------------------------------------------
        # Resolve agent
        # --------------------------------------------
        try:
            agent = registry.get(agent_name)
        except Exception as e:
            # Registry couldn't find the agent or failed to build it
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
                error=str(e),
            )

        # --------------------------------------------
        # Run agent safely
        # --------------------------------------------
        try:
            output = agent.run(input_data, ctx)

            # Store last output in memory for debugging (Phase 2)
            if ctx.request_id:
                record = memory_store.get(ctx.request_id)
                if record:
                    record.data["last_agent"] = agent_name
                    record.data["last_output"] = output
                    memory_store.upsert(record)

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
                output=output,
                ok=True,
            )

        except Exception as e:
            # Agent crashed (bug / runtime exception)
            logger.exception(
                "engine.run_agent error agent=%s tier=%s request_id=%s",
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
                error=str(e),
            )


# ------------------------------------------------------------
# Singleton engine instance (simple for Phase 2)
# ------------------------------------------------------------
engine = CoreEngine()
