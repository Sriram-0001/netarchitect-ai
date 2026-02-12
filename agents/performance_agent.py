import json


class PerformanceAgent:

    def __init__(self, catalog_path="data/vendor_catalog.json"):
        with open(catalog_path, "r") as f:
            self.catalog = json.load(f)

    def calculate_vendor_performance(self, infra_package, vendor):

        selected_models = infra_package["infrastructure_design"]["selected_models"][vendor]
        topology = infra_package["infrastructure_design"]["topology"]
        redundancy = infra_package["infrastructure_design"]["redundancy"]["enabled"]
        cloud_model = infra_package["infrastructure_design"]["cloud_architecture"]["model"]

        vendor_catalog = self.catalog[vendor]

        router_model = selected_models["router_model"]
        switch_model = selected_models["switch_model"]
        ap_model = selected_models["access_point_model"]
        firewall_model = selected_models["firewall_model"]

        router_tp = vendor_catalog["routers"][router_model]["throughput_mbps"]
        switch_tp = vendor_catalog["switches"][switch_model]["throughput_mbps"]
        ap_tp = vendor_catalog["access_points"][ap_model]["throughput_mbps"]
        firewall_tp = vendor_catalog["firewalls"][firewall_model]["throughput_mbps"]

        base_score = (router_tp + switch_tp + ap_tp + firewall_tp) / 4

        # Normalize to 100 scale
        score = min(base_score / 100, 100)

        if redundancy:
            score += 5

        if topology.lower() == "hybrid":
            score += 5

        if cloud_model.lower() == "hybrid":
            score += 5

        return min(score, 100)

    def calculate_performance(self, infra_package):

        return {
            "cisco": round(self.calculate_vendor_performance(infra_package, "cisco"), 2),
            "tplink": round(self.calculate_vendor_performance(infra_package, "tplink"), 2)
        }
