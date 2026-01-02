from __future__ import annotations

from typing import Dict, Type

from app.agents.base import BaseAgent
from app.agents.orchestrator import OrchestratorAgent
from app.agents.domain_reliability import DeploymentReliabilityAgent


class AgentRegistry:
    """
    Central registry for all available agents in the system.

    Purpose:
    - Acts as a lightweight dependency registry
    - Decouples agent discovery from agent execution
    - Provides a single source of truth for what agents exist

    Design notes:
    - Agents are registered by name
    - The registry stores agent *classes*, not instances
    - A new agent instance is created per request execution

    In later phases, this can be extended to support:
    - Dependency injection
    - Configuration-based agent loading
    - Tier-based agent availability rules
    """

    def __init__(self) -> None:
        # Internal map: agent_name -> Agent class
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        """
        Register an agent class under a specific name.

        Args:
            name: Public identifier used to reference the agent
            agent_cls: The agent class (not an instance)

        Example:
            registry.register("orchestrator", OrchestratorAgent)
        """
        self._agents[name] = agent_cls

    def get(self, name: str) -> BaseAgent:
        """
        Retrieve and instantiate an agent by name.

        Returns:
            A new instance of the requested agent.

        Raises:
            ValueError if the agent name is not registered.
        """
        if name not in self._agents:
            raise ValueError(f"Unknown agent: {name}")

        # Instantiate a fresh agent per execution
        # This avoids shared state across requests
        return self._agents[name]()

    def list(self) -> Dict[str, str]:
        """
        List all registered agents.

        Returns:
            Dictionary mapping agent names to class names.
        Useful for discovery, debugging, and UI tooling.
        """
        return {name: agent_cls.__name__ for name, agent_cls in self._agents.items()}


# ============================================================
# Global Registry Initialization
# ============================================================
# Agents are registered at import time.
# This keeps bootstrap simple and explicit during early phases.

registry = AgentRegistry()

# Core orchestration agent
registry.register("orchestrator", OrchestratorAgent)

# Phase 3 domain agent (business-focused example)
registry.register("deployment_reliability", DeploymentReliabilityAgent)
