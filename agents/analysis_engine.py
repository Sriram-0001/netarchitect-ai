from agents.costing_agent import CostingAgent
from agents.performance_agent import PerformanceAgent
from agents.security_agent import SecurityAgent
from agents.optimization_agent import OptimizationAgent


def run_analysis(infra_package):

    cost_agent = CostingAgent()
    performance_agent = PerformanceAgent()
    security_agent = SecurityAgent()
    optimization_agent = OptimizationAgent()

    cost_results = cost_agent.calculate_cost(infra_package)
    performance_scores = performance_agent.calculate_performance(infra_package)
    risk_scores = security_agent.calculate_risk(infra_package)

    optimization = optimization_agent.recommend(
        infra_package,
        cost_results,
        performance_scores,
        risk_scores
    )

    return {
        "cost_analysis": cost_results,
        "performance_scores": performance_scores,
        "security_risk_scores": risk_scores,
        "optimization_recommendation": optimization
    }
