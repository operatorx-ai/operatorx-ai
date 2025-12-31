from __future__ import annotations

from typing import Dict, Type

from app.agents.base import BaseAgent
from app.agents.orchestrator import OrchestratorAgent


class AgentRegistry:
    """
    Simple in-memory registry.
    Later we can extend it for dependency injection, config, tier rules, etc.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        self._agents[name] = agent_cls

    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise ValueError(f"Unknown agent: {name}")
        return self._agents[name]()  # instantiate

    def list(self) -> Dict[str, str]:
        return {k: v.__name__ for k, v in self._agents.items()}


# Global default registry (simple and practical for now)
registry = AgentRegistry()
registry.register("orchestrator", OrchestratorAgent)
