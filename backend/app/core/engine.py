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
# This logger name matches what we used earlier so logs show up clean.
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
    - Supports error handling in one place
    - Allows future metadata (timing, traces, eval scores, etc.)
    """
    agent: str
    request_id: Optional[str]
    tier: str
    output: Dict[str, Any]
    ok: bool = True
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
    ✅ Optionally store lightweight memory per request_id

    Later phases:
    - routing rules
    - policy enforcement
    - retries
    - evaluation hooks
    - persistence
    """

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        ctx: AgentContext,
    ) -> EngineResult:
        """
        Main execution path.

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
                output={},        # ✅ correct indentation
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
                output={},        # ✅ correct indentation
                ok=False,
                error=str(e),
            )


# ------------------------------------------------------------
# Singleton engine instance (simple for Phase 2)
# ------------------------------------------------------------
engine = CoreEngine()
    error: Optional[str] = None


# ============================================================
# Core Engine
# ============================================================

class CoreEngine:
    """
    Shared core engine responsible for agent execution.

    Architectural responsibilities:
    - Central routing and execution control
    - Isolation of execution logic from API layer
    - Consistent logging and error handling
    - Tier-aware execution boundaries

    Phase 2 intentionally keeps this lightweight while
    establishing strong structural foundations.
    """

    def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        ctx: AgentContext,
    ) -> EngineResult:
        """
        Executes a single agent within a controlled environment.

        Args:
            agent_name: Name of the agent to execute
            input_data: Structured input payload
            ctx: Execution context (tier, request_id)

        Returns:
            EngineResult with success flag and output/error
        """

        # ----------------------------------------------------
        # Log execution start
        # ----------------------------------------------------
        logger.info(
            "engine.run_agent start agent=%s tier=%s request_id=%s",
            agent_name,
            ctx.tier,
            ctx.request_id,
        )

        # ----------------------------------------------------
        # Resolve agent from registry
        # ----------------------------------------------------
        try:
            agent = registry.get(agent_name)
        except Exception:
            # Unknown or unregistered agent
            logger.warning(
                "engine.run_agent unknown agent=%s tier=%s request_id=%s",
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
                error=f"Unknown agent: {agent_name}",
            )

        # ----------------------------------------------------
        # Execute agent safely
        # ----------------------------------------------------
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

        except Exception:
            # Catch unexpected runtime errors to protect the system
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


# Singleton engine instance used across the application
engine = CoreEngine()
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
