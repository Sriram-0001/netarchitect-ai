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