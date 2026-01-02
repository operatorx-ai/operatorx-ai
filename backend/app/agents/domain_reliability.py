from __future__ import annotations

from typing import Any, Dict, List

from app.agents.base import BaseAgent, AgentContext


class DeploymentReliabilityAgent(BaseAgent):
    """
    Domain Agent: Deployment Reliability

    Purpose (Phase 3):
    - Demonstrate a "real" domain agent with a clear responsibility
    - Provide actionable output (recommendations + risks + next steps)
    - Show that the agent behavior can depend on deployment tier

    Why this matters:
    - Recruiters want to see agents that do more than return a stub plan
    - This mirrors real internal tooling / customer success outcomes work
    """

    name = "deployment_reliability"

    def run(self, input_data: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        """
        Create a reliability improvement response based on:
        - goal: what the user wants to improve
        - constraints: limitations that affect recommendations
        - tier: influences logging, oversight, governance patterns

        Returns a structured dictionary so it can be:
        - rendered by a UI later
        - evaluated by an evaluation agent later
        - logged and stored in memory safely
        """
        goal = str(input_data.get("goal", "")).strip()
        constraints: List[str] = input_data.get("constraints", []) or []

        # ------------------------------------------------------------
        # Core recommendations (generic best practices)
        # ------------------------------------------------------------
        recommendations = [
            "Add deployment health checks and rollback strategy",
            "Use progressive delivery (canary / blue-green) for safer releases",
            "Define SLOs/SLIs and alert on error budgets",
            "Automate CI/CD checks (tests, lint, security scans) before deploy",
        ]

        # ------------------------------------------------------------
        # Tier-aware adjustments (shows deployment-sensitive design)
        # ------------------------------------------------------------
        tier_notes: List[str] = []
        if ctx.tier == "personal":
            tier_notes = [
                "Prioritize low-cost monitoring (basic uptime checks, lightweight logs)",
                "Keep setup simple and avoid heavy infrastructure overhead",
            ]
        elif ctx.tier == "business":
            tier_notes = [
                "Use audit-friendly logging and deployment reporting",
                "Integrate with incident workflows (ticketing, on-call, postmortems)",
            ]
        elif ctx.tier == "government":
            tier_notes = [
                "Add human-in-the-loop approvals for releases when required",
                "Enforce traceability: what changed, who approved, and why",
                "Favor explainable controls and documented governance gates",
            ]

        # ------------------------------------------------------------
        # Risk identification (what could go wrong)
        # ------------------------------------------------------------
        risks = [
            "Deployments without rollback increase outage risk",
            "No monitoring/alerts causes slow incident detection",
            "Unvalidated changes increase regression probability",
        ]

        # Add constraint-aware risk notes (simple but realistic)
        if constraints:
            risks.append(f"Constraints may reduce options: {', '.join(constraints)}")

        # ------------------------------------------------------------
        # Next actions (concrete steps a team can execute)
        # ------------------------------------------------------------
        next_actions = [
            "Implement a basic health endpoint and readiness checks",
            "Add CI pipeline gates (unit tests + linting + security scan)",
            "Create a rollback runbook and test rollback in staging",
        ]

        return {
            "agent": self.name,
            "tier": ctx.tier,
            "goal": goal,
            "constraints": constraints,
            "recommendations": recommendations,
            "tier_notes": tier_notes,
            "risks": risks,
            "next_actions": next_actions,
        }
