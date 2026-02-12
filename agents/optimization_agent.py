from utils.catalog_loader import CatalogLoader


class OptimizationAgent:

    def __init__(self):
        self.loader = CatalogLoader()

        self.performance_threshold = 55
        self.risk_threshold = 30

    def evaluate(self, infra_package, analysis):

        budget = infra_package["company_profile"]["budget"]

        cost = analysis["cost_analysis"]
        performance = analysis["performance_scores"]
        risk = analysis["security_scores"]

        cisco_cost = cost["cisco_total_cost"]
        tplink_cost = cost["tplink_total_cost"]

        decision = {
            "optimization_needed": False,
            "reason": None
        }

        # Budget violation
        if cisco_cost > budget and tplink_cost > budget:
            decision["optimization_needed"] = True
            decision["reason"] = "Both vendors exceed budget."

        elif cisco_cost > budget:
            decision["optimization_needed"] = True
            decision["reason"] = "Cisco exceeds budget."

        # Performance issue
        elif performance["cisco"] < self.performance_threshold:
            decision["optimization_needed"] = True
            decision["reason"] = "Performance below threshold."

        # Security risk
        elif risk["cisco"] > self.risk_threshold:
            decision["optimization_needed"] = True
            decision["reason"] = "Security risk too high."

        return decision

    def downgrade_topology(self, topology):
        order = ["Mesh", "Hybrid", "Star"]
        if topology in order:
            idx = order.index(topology)
            if idx < len(order) - 1:
                return order[idx + 1]
        return topology

    def downgrade_router(self, vendor, current_model):

        catalog = self.loader.get_vendor_catalog(vendor)
        devices = sorted(
            catalog["routers"],
            key=lambda x: x["price"]
        )

        models = [d["model"] for d in devices]

        if current_model in models:
            idx = models.index(current_model)
            if idx > 0:
                return models[idx - 1]

        return current_model

    def modify_design(self, infra_package, analysis):

        design = infra_package["infrastructure_design"]

        # Downgrade topology
        design["topology"] = self.downgrade_topology(
            design["topology"]
        )

        # Downgrade Cisco router
        design["selected_models"]["cisco"]["router_model"] = \
            self.downgrade_router(
                "Cisco",
                design["selected_models"]["cisco"]["router_model"]
            )

        # Downgrade TP-Link router
        design["selected_models"]["tplink"]["router_model"] = \
            self.downgrade_router(
                "TP-Link",
                design["selected_models"]["tplink"]["router_model"]
            )

        return infra_package
