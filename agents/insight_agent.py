# agents/insight_agent.py

class InsightAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, infra_package, analysis, deployment):

        system_prompt = """
You are a Senior Enterprise Infrastructure Consultant.
Analyze the structured infrastructure data and generate
executive-grade insights.

Return STRICT JSON only in this format:

{
  "executive_summary": "...",
  "cost_analysis_insight": "...",
  "performance_insight": "...",
  "risk_insight": "...",
  "scalability_insight": "...",
  "deployment_insight": "...",
  "final_recommendation": "..."
}
"""

        user_prompt = f"""
Infrastructure Data:
{infra_package}

Analysis Data:
{analysis}

Deployment Data:
{deployment}

Generate structured strategic insights.
"""

        return self.llm.call(system_prompt, user_prompt)
