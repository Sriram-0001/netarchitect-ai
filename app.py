import os
import copy
from dotenv import load_dotenv

from agents.optimization_agent import OptimizationAgent
from agents.costing_agent import run_cost_analysis
from models.llm_handler import LLMHandler
from agents import requirement_agent
from agents import architecture_agent
from agents import vendor_agent
from agents import scalability_agent


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise Exception("GROQ_API_KEY not found in environment variables.")

MODEL = "llama-3.1-8b-instant"

llm = LLMHandler(API_KEY, MODEL)


def run_pipeline(user_input: dict):
    """
    Runs the complete infrastructure planning pipeline:
    1. Requirements Analysis
    2. Architecture Design
    3. Scalability Projection
    4. Cost Analysis
    5. Optimization (if needed)
    """

    company_profile = {
        "num_employees": user_input["num_employees"],
        "office_size_sqft": user_input["office_size_sqft"],
        "security_level": user_input["security_level"],
        "growth_rate_percent": user_input["growth_rate_percent"],
        "cloud_preference": user_input["cloud_preference"],
        "budget": user_input["budget"]
    }

    # 1️⃣ Requirements
    requirements = requirement_agent.process(user_input, llm)

    # 2️⃣ Architecture
    architecture = architecture_agent.design(
        requirements,
        company_profile,
        llm
    )
    print(architecture["selected_models"].keys())

    # 3️⃣ Scalability
    scalability = scalability_agent.project(
        company_profile,
        architecture,
        llm
    )

    # Infrastructure package
    infra_package = {
        "company_profile": company_profile,
        "infrastructure_design": {
            "topology": architecture["topology"],
            "components": architecture["components"],
            "cloud_architecture": architecture["cloud_architecture"],
            "redundancy": architecture["redundancy"],
            "selected_models": architecture["selected_models"]
        },
        "scalability_projection": scalability
    }
    
    # 4️⃣ Cost Analysis
    cost_output = run_cost_analysis(infra_package)

    # Save initial state (deep copy to prevent mutation)
    initial_design = copy.deepcopy(infra_package)
    initial_cost = copy.deepcopy(cost_output)

    # 5️⃣ Optimization Agent
    optimization_agent = OptimizationAgent()
    decision = optimization_agent.evaluate(infra_package, cost_output)

    if decision.get("optimization_needed"):
        infra_package = optimization_agent.modify_design(infra_package)
        cost_output = run_cost_analysis(infra_package)

        return {
            "initial_design": initial_design,
            "initial_cost": initial_cost,
            "optimized_design": infra_package,
            "optimized_cost": cost_output,
            "optimization_decision": decision
        }
    
    # If no optimization required
    return {
        "design": infra_package,
        "cost": cost_output,
        "optimization_decision": decision
    }


# TEST RUN
if __name__ == "__main__":

    test_input = {
        "num_employees": 120,
        "office_size_sqft": 6000,
        "security_level": "High",
        "growth_rate_percent": 20,
        "cloud_preference": "Hybrid",
        "budget": 700000
    }

    result = run_pipeline(test_input)
    print(result)
