
from utils.catalog_loader import CatalogLoader


def calculate_vendor_cost(vendor_name, infra_package):

    loader = CatalogLoader()
    catalog = loader.get_vendor_catalog(vendor_name)

    design = infra_package["infrastructure_design"]
    components = design["components"]

    # Normalize vendor name to match architecture keys
    normalized_vendor = (
        vendor_name.lower()
        .replace("-", "")
        .replace(" ", "")
    )

    selected_models = design["selected_models"]

    if normalized_vendor not in selected_models:
        raise KeyError(
            f"Vendor '{normalized_vendor}' not found in selected_models.\n"
            f"Available vendors: {list(selected_models.keys())}"
        )

    selected = selected_models[normalized_vendor]

    total_cost = 0

    # Router
    router_model = selected["router_model"]
    router_data = next(d for d in catalog["routers"] if d["model"] == router_model)
    total_cost += components["routers"] * router_data["price"]

    # Switch
    switch_model = selected["switch_model"]
    switch_data = next(d for d in catalog["switches"] if d["model"] == switch_model)
    total_cost += components["switches"] * switch_data["price"]

    # Access Point
    ap_model = selected["access_point_model"]
    ap_data = next(d for d in catalog["access_points"] if d["model"] == ap_model)
    total_cost += components["access_points"] * ap_data["price"]

    # Firewall
    if components["firewalls"] > 0:
        fw_model = selected["firewall_model"]
        fw_data = next(d for d in catalog["firewalls"] if d["model"] == fw_model)
        total_cost += components["firewalls"] * fw_data["price"]

    # Redundancy multiplier
    if design["redundancy"]["dual_isp"]:
        total_cost *= 1.1

    return round(total_cost, 2)


def run_cost_analysis(infra_package: dict):

    cisco_cost = calculate_vendor_cost("Cisco", infra_package)
    tplink_cost = calculate_vendor_cost("TP-Link", infra_package)

    return {
        "cost_analysis": {
            "cisco_total_cost": cisco_cost,
            "tplink_total_cost": tplink_cost,
            "cost_difference": abs(cisco_cost - tplink_cost)
        },
        "performance_scores": {
            "cisco": 60,
            "tplink": 50
        }
    }

import json


class CostingAgent:

    def __init__(self, catalog_path="data/vendor_catalog.json"):
        with open(catalog_path, "r") as f:
            self.catalog = json.load(f)

    def calculate_vendor_cost(self, infra_package, vendor_key):

        components = infra_package["infrastructure_design"]["components"]
        selected_models = infra_package["infrastructure_design"]["selected_models"][vendor_key]
        cloud_servers = infra_package["infrastructure_design"]["cloud_architecture"]["cloud_servers"]
        dual_isp = infra_package["infrastructure_design"]["redundancy"]["dual_isp"]
        year3_users = infra_package["scalability_projection"]["year_3_users"]

        vendor_catalog = self.catalog[vendor_key]

        total_cost = 0

        # Router
        router_model = selected_models["router_model"]
        router_price = vendor_catalog["routers"][router_model]["price"]
        total_cost += components["routers"] * router_price

        # Switch
        switch_model = selected_models["switch_model"]
        switch_price = vendor_catalog["switches"][switch_model]["price"]
        total_cost += components["switches"] * switch_price

        # Access Point
        ap_model = selected_models["access_point_model"]
        ap_price = vendor_catalog["access_points"][ap_model]["price"]
        total_cost += components["access_points"] * ap_price

        # Firewall
        fw_model = selected_models["firewall_model"]
        fw_price = vendor_catalog["firewalls"][fw_model]["price"]
        total_cost += components["firewalls"] * fw_price

        # Cloud
        cloud_price = vendor_catalog["cloud_server_cost"]
        total_cost += cloud_servers * cloud_price

        # Redundancy
        if dual_isp:
            total_cost *= vendor_catalog["redundancy_multiplier"]

        # Scalability
        if year3_users > 200:
            total_cost *= 1.15

        return total_cost

    def calculate_cost(self, infra_package):
        cisco_cost = self.calculate_vendor_cost(infra_package, "cisco")
        tplink_cost = self.calculate_vendor_cost(infra_package, "tplink")

        return {
            "cisco_total_cost": round(cisco_cost, 2),
            "tplink_total_cost": round(tplink_cost, 2),
            "cost_difference": round(abs(cisco_cost - tplink_cost), 2)
        }

