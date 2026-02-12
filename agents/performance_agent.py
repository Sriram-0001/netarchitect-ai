from utils.catalog_loader import CatalogLoader


class PerformanceAgent:

    def __init__(self):
        self.loader = CatalogLoader()

    def evaluate_vendor(self, vendor, infra_package):

        catalog = self.loader.get_vendor_catalog(vendor)

        design = infra_package["infrastructure_design"]
        components = design["components"]

        normalized_vendor = vendor.lower().replace("-", "").replace(" ", "")
        selected = design["selected_models"][normalized_vendor]

        score = 0

        # Router performance
        router = next(
            d for d in catalog["routers"]
            if d["model"] == selected["router_model"]
        )

        throughput = router.get("throughput_mbps", 0)
        score += throughput * 0.4

        # Switch performance (use ports if max_devices not present)
        switch = next(
            d for d in catalog["switches"]
            if d["model"] == selected["switch_model"]
        )

        switch_capacity = (
            switch.get("max_devices")
            or switch.get("ports")
            or 0
        )

        score += switch_capacity * 0.1

        # Access Point performance
        ap = next(
            d for d in catalog["access_points"]
            if d["model"] == selected["access_point_model"]
        )

        ap_capacity = ap.get("max_devices", 0)
        score += ap_capacity * 0.05

        # Normalize score
        score = min(score / 10, 100)

        return round(score, 2)

    def evaluate(self, infra_package):

        return {
            "cisco": self.evaluate_vendor("Cisco", infra_package),
            "tplink": self.evaluate_vendor("TP-Link", infra_package)
        }
