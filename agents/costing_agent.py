from utils.catalog_loader import CatalogLoader


class CostingAgent:

    def __init__(self):
        self.loader = CatalogLoader()

    def calculate_vendor_cost(self, vendor, infra_package):

        catalog = self.loader.get_vendor_catalog(vendor)

        design = infra_package["infrastructure_design"]
        components = design["components"]

        normalized_vendor = vendor.lower().replace("-", "").replace(" ", "")
        selected = design["selected_models"][normalized_vendor]

        breakdown = {}
        total_cost = 0

        # Router
        router = next(
            d for d in catalog["routers"]
            if d["model"] == selected["router_model"]
        )
        router_cost = components["routers"] * router["price"]
        breakdown["routers"] = {
            "model": router["model"],
            "quantity": components["routers"],
            "unit_price": router["price"],
            "total": router_cost
        }
        total_cost += router_cost

        # Switch
        switch = next(
            d for d in catalog["switches"]
            if d["model"] == selected["switch_model"]
        )
        switch_cost = components["switches"] * switch["price"]
        breakdown["switches"] = {
            "model": switch["model"],
            "quantity": components["switches"],
            "unit_price": switch["price"],
            "total": switch_cost
        }
        total_cost += switch_cost

        # Access Points
        ap = next(
            d for d in catalog["access_points"]
            if d["model"] == selected["access_point_model"]
        )
        ap_cost = components["access_points"] * ap["price"]
        breakdown["access_points"] = {
            "model": ap["model"],
            "quantity": components["access_points"],
            "unit_price": ap["price"],
            "total": ap_cost
        }
        total_cost += ap_cost

        # Firewall
        if components["firewalls"] > 0:
            fw = next(
                d for d in catalog["firewalls"]
                if d["model"] == selected["firewall_model"]
            )
            fw_cost = components["firewalls"] * fw["price"]
            breakdown["firewalls"] = {
                "model": fw["model"],
                "quantity": components["firewalls"],
                "unit_price": fw["price"],
                "total": fw_cost
            }
            total_cost += fw_cost

        if design["redundancy"]["dual_isp"]:
            total_cost *= 1.1

        return round(total_cost, 2), breakdown

    def calculate_cost(self, infra_package):

        cisco_total, cisco_breakdown = self.calculate_vendor_cost(
            "Cisco", infra_package
        )

        tplink_total, tplink_breakdown = self.calculate_vendor_cost(
            "TP-Link", infra_package
        )

        return {
            "cisco_total_cost": cisco_total,
            "tplink_total_cost": tplink_total,
            "cost_difference": abs(cisco_total - tplink_total),
            "cisco_breakdown": cisco_breakdown,
            "tplink_breakdown": tplink_breakdown
        }
