from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentContext:
    """
    Shared request context passed to agents.
    Keep it small and extensible.
    """
    tier: str = "personal"  # personal | business | government
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """
    Common interface for all agents in OperatorX AI.
    """

    name: str = "base-agent"

    @abstractmethod
    def run(self, input_data: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        """
        Execute the agent and return a structured response.
        """
        raise NotImplementedError
