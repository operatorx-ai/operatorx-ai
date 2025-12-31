from __future__ import annotations

from typing import Any, Dict, List

from app.agents.base import BaseAgent, AgentContext


class OrchestratorAgent(BaseAgent):
    name = "orchestrator"

    def run(self, input_data: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        goal = str(input_data.get("goal", "")).strip()
        constraints: List[str] = input_data.get("constraints", []) or []

        # Shared core steps (all tiers)
        plan: List[str] = [
            f"Analyze goal: {goal}",
            f"Tier: {ctx.tier}",
        ]

        # Tier-specific behavior
        if ctx.tier == "personal":
            plan += [
                "Keep data local when possible",
                "Minimize logging (privacy-first)",
                "Generate a simple execution plan",
            ]

        elif ctx.tier == "business":
            plan += [
                "Confirm scope + stakeholders",
                "Enable audit-friendly logging",
                "Check integration touchpoints (APIs, dashboards, workflows)",
                "Generate an execution plan with measurable outcomes",
            ]

        elif ctx.tier == "government":
            plan += [
                "Require human-in-the-loop approval for key decisions",
                "Capture traceability (inputs, outputs, rationale)",
                "Run policy + compliance checks (privacy, security, accountability)",
                "Generate an execution plan with governance gates",
            ]

        # Constraint handling (all tiers)
        plan.append("Evaluate constraints")
        if constraints:
            plan.append(f"Constraints: {', '.join(constraints)}")

        # Closing steps (all tiers)
        plan += [
            "Generate execution plan",
            "Return structured response",
        ]

        return {"plan": plan}

