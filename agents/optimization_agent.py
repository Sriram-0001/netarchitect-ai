
from utils.catalog_loader import CatalogLoader


class OptimizationAgent:

    def __init__(self):
        self.loader = CatalogLoader()

    def evaluate(self, infra_package, cost_output):

        budget = infra_package["company_profile"]["budget"]
        cisco_cost = cost_output["cost_analysis"]["cisco_total_cost"]
        tplink_cost = cost_output["cost_analysis"]["tplink_total_cost"]

        if cisco_cost > budget and tplink_cost > budget:
            return {"optimization_needed": True, "reason": "Both vendors exceed budget."}

        if cisco_cost > budget:
            return {"optimization_needed": True, "reason": "Cisco exceeds budget."}

        return {"optimization_needed": False, "reason": "Within budget."}

    def downgrade_topology(self, topology):

        order = ["Mesh", "Hybrid", "Star"]

        if topology in order:
            idx = order.index(topology)
            if idx < len(order) - 1:
                return order[idx + 1]

        return topology

    def downgrade_model(self, vendor, category, current_model):

        catalog = self.loader.get_vendor_catalog(vendor)

        devices = catalog[category]

        # sort by price ascending
        devices_sorted = sorted(devices, key=lambda x: x["price"])

        models = [d["model"] for d in devices_sorted]

        if current_model in models:
            idx = models.index(current_model)
            if idx > 0:
                return models[idx - 1]

        return current_model

    def modify_design(self, infra_package):

        design = infra_package["infrastructure_design"]

        # downgrade topology first
        design["topology"] = self.downgrade_topology(design["topology"])

        # downgrade Cisco router
        design["selected_models"]["cisco"]["router_model"] = self.downgrade_model(
            "Cisco", "routers",
            design["selected_models"]["cisco"]["router_model"]
        )

        # downgrade TP-Link router
        design["selected_models"]["tplink"]["router_model"] = self.downgrade_model(
            "TP-Link", "routers",
            design["selected_models"]["tplink"]["router_model"]
        )

        return infra_package
class OptimizationAgent:

    def recommend(self, infra_package, cost_results, performance_scores, risk_scores):

        budget = infra_package["company_profile"]["budget"]

        vendors = infra_package["infrastructure_design"]["selected_models"].keys()

        best_vendor = None
        best_score = float("inf")

        for vendor in vendors:

            cost = cost_results[f"{vendor}_total_cost"]
            performance = performance_scores[vendor]
            risk = risk_scores[vendor]

            composite = cost - (performance * 1000) + (risk * 500)

            if composite < best_score:
                best_score = composite
                best_vendor = vendor

        selected_cost = cost_results[f"{best_vendor}_total_cost"]

        if selected_cost > budget:
            return {
                "recommended_vendor": best_vendor,
                "reason": "Exceeds budget. Optimization required.",
                "optimization_needed": True
            }

        return {
            "recommended_vendor": best_vendor,
            "reason": "Best cost-performance-risk balance within budget.",
            "optimization_needed": False
        }
