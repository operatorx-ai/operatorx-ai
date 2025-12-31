from __future__ import annotations

from typing import Any, Dict, List

from app.agents.base import BaseAgent, AgentContext


class OrchestratorAgent(BaseAgent):
    name = "orchestrator"

    def run(self, input_data: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        goal = str(input_data.get("goal", "")).strip()
        constraints: List[str] = input_data.get("constraints", []) or []

        plan = [
            f"Analyze goal: {goal}",
            f"Tier: {ctx.tier}",
            "Evaluate constraints",
            "Generate execution plan",
            "Return structured response",
        ]

        if constraints:
            plan.insert(3, f"Constraints: {', '.join(constraints)}")

        return {"plan": plan}
