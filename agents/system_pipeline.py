import copy

from agents import requirement_agent
from agents import architecture_agent
from agents import scalability_agent
from agents.costing_agent import CostingAgent
from agents.performance_agent import PerformanceAgent
from agents.security_agent import SecurityAgent
from agents.optimization_agent import OptimizationAgent
from agents.deployment_agent import DeploymentAgent
from agents.insight_agent import InsightAgent

from utils.network_diagram import generate_network_diagram
from utils.pdf_report import generate_pdf


def run_full_pipeline(user_input: dict, llm):

    # -------------------------
    # Phase 1: Business Profile
    # -------------------------
    company_profile = {
        "num_employees": user_input["num_employees"],
        "office_size_sqft": user_input["office_size_sqft"],
        "security_level": user_input["security_level"],
        "growth_rate_percent": user_input["growth_rate_percent"],
        "cloud_preference": user_input["cloud_preference"],
        "budget": user_input["budget"],
    }

    # -------------------------
    # Phase 2: Architecture Generation
    # -------------------------
    requirements = requirement_agent.process(user_input, llm)

    architecture = architecture_agent.design(
        requirements,
        company_profile,
        llm,
    )

    scalability = scalability_agent.project(
        company_profile,
        architecture,
        llm,
    )

    infra_package = {
        "company_profile": company_profile,
        "infrastructure_design": {
            "topology": architecture["topology"],
            "components": architecture["components"],
            "cloud_architecture": architecture["cloud_architecture"],
            "redundancy": architecture["redundancy"],
            "selected_models": architecture["selected_models"],
        },
        "scalability_projection": scalability,
    }

    # -------------------------
    # Phase 3: Multi-Agent Analysis
    # -------------------------
    cost_agent = CostingAgent()
    performance_agent = PerformanceAgent()
    security_agent = SecurityAgent()

    cost_output = cost_agent.calculate_cost(infra_package)
    performance_output = performance_agent.evaluate(infra_package)
    security_output = security_agent.evaluate(infra_package)

    initial_analysis = {
        "cost_analysis": cost_output,
        "performance_scores": performance_output,
        "security_scores": security_output,
    }

    initial_design = copy.deepcopy(infra_package)

    # -------------------------
    # Phase 4: Optimization
    # -------------------------
    optimizer = OptimizationAgent()

    decision = optimizer.evaluate(
        infra_package,
        initial_analysis,
    )

    if decision["optimization_needed"]:

        infra_package = optimizer.modify_design(
            infra_package,
            initial_analysis,
        )

        # Re-run analysis after optimization
        cost_output = cost_agent.calculate_cost(infra_package)
        performance_output = performance_agent.evaluate(infra_package)
        security_output = security_agent.evaluate(infra_package)

    optimized_analysis = {
        "cost_analysis": cost_output,
        "performance_scores": performance_output,
        "security_scores": security_output,
    }

    # -------------------------
    # Phase 5: Deployment Estimation
    # -------------------------
    deployment_agent = DeploymentAgent()
    deployment_output = deployment_agent.estimate(
        infra_package,
        cost_output,
    )

        # -------------------------
    # Phase 6: AI Insight Generation
    # -------------------------

    insight_agent = InsightAgent(llm)

    insights = insight_agent.generate(
        infra_package,
        optimized_analysis,
        deployment_output
    )

    # -------------------------
    # Phase 7: Visualization
    # -------------------------

    diagram = generate_network_diagram(infra_package)

    # -------------------------
    # Phase 8: PDF Report Generation
    # -------------------------

    pdf_buffer = generate_pdf(
        infra_package,
        optimized_analysis,
        deployment_output,
        insights,
        diagram
    )


    # -------------------------
    # Final Response Package
    # -------------------------
    return {
        "infra": infra_package,
        "cost": cost_output,
        "performance": performance_output,
        "security": security_output,
        "deployment": deployment_output,
        "diagram": diagram,
        "pdf": pdf_buffer,
        "initial_design": initial_design,
        "initial_analysis": initial_analysis,
        "optimized_analysis": optimized_analysis,
        "optimization_decision": decision,
        "insights": insights,
    }
