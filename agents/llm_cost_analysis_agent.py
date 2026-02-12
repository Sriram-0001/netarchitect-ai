import os
import json
from openai import OpenAI

from agents.costing_agent import CostingAgent
from agents.performance_agent import PerformanceAgent
from agents.security_agent import SecurityAgent
from agents.optimization_agent import OptimizationAgent

import os
from openai import OpenAI

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)


def transform_input_schema(raw_input: dict) -> dict:

    company = raw_input.get("company_profile", {})
    infra = raw_input.get("infrastructure_design", {})
    vendors_raw = raw_input.get("vendor_options", [])

    components = infra.get("components", {})

    devices = {
        "router_basic": components.get("routers", 0),
        "switch_24": components.get("switches", 0),
        "access_point": components.get("access_points", 0),
        "firewall": components.get("firewalls", 0),
        "ids": components.get("ids_systems", 0)
    }

    return {
        "architecture": {
            "devices": devices,
            "security_level": company.get("security_level", "Medium"),
            "redundancy": infra.get("redundancy", {}).get("enabled", False),
            "ids": devices.get("ids", 0) > 0
        },
        "vendor_options": vendors_raw,
        "budget": company.get("budget", 0)
    }


def generate_llm_explanation(result_dict, budget):

    system_prompt = """
You are a senior enterprise IT infrastructure financial consultant.
Return ONLY valid JSON.
"""

    user_prompt = f"""
Network Infrastructure Analysis:

{json.dumps(result_dict, indent=2)}

Budget: {budget}

Return JSON:

{{
  "summary": "...",
  "cost_reasoning": "...",
  "performance_tradeoff_analysis": "...",
  "risk_consideration": "...",
  "final_recommendation_justification": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.strip("```json").strip("```").strip()

        return json.loads(content)

    except Exception as e:
        return {
            "error": "LLM processing failed",
            "details": str(e)
        }


def analyze_infrastructure(infra_input: dict) -> dict:

    infra_input = transform_input_schema(infra_input)

    architecture = infra_input.get("architecture", {})
    vendors = infra_input.get("vendor_options", [])
    budget = infra_input.get("budget", 0)

    cost_agent = CostingAgent()
    performance_agent = PerformanceAgent()
    security_agent = SecurityAgent()
    optimization_agent = OptimizationAgent()

    cost_analysis = cost_agent.calculate_cost(architecture, vendors)
    performance_scores = performance_agent.calculate_performance(architecture, vendors)
    security_risk_scores = security_agent.calculate_security_risk(architecture, vendors)

    optimization = optimization_agent.optimize_vendor(
        cost_analysis,
        performance_scores,
        security_risk_scores,
        budget
    )

    result = {
        "cost_analysis": cost_analysis,
        "performance_scores": performance_scores,
        "security_risk_scores": security_risk_scores,
        "optimization_suggestion": optimization
    }

    result["strategic_explanation"] = generate_llm_explanation(result, budget)

    return result
