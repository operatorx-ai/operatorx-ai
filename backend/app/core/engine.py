from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.agents.base import AgentContext
from app.agents.registry import registry

# ------------------------------------------------------------
# Logger configuration
# ------------------------------------------------------------
# Uses application-wide logging config set in main.py.
# This logger provides structured, traceable execution logs.
logger = logging.getLogger("operatorx.core.engine")


# ============================================================
# Engine Result Model
# ============================================================

@dataclass
class EngineResult:
    """
    Standardized result returned by the Core Engine.

    This abstraction allows:
    - consistent error handling
    - clean API responses
    - future expansion (metrics, timing, evaluation data)
    """
    agent: str
    request_id: Optional[str]
    tier: str
    output: Dict[str, Any]
    ok: bool = True
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
