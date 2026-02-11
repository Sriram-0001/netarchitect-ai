import json
import os


class CatalogLoader:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "data")

        with open(os.path.join(base_path, "cisco_catalog.json"), "r") as f:
            self.cisco = json.load(f)

        with open(os.path.join(base_path, "tplink_catalog.json"), "r") as f:
            self.tplink = json.load(f)

    # ---------------------------
    # Basic Accessors
    # ---------------------------

    def get_vendor_catalog(self, vendor_name: str):
        if vendor_name.lower() == "cisco":
            return self.cisco
        elif vendor_name.lower() == "tp-link":
            return self.tplink
        else:
            raise ValueError("Unsupported vendor")

    def get_all_vendors(self):
        return {
            "Cisco": self.cisco,
            "TP-Link": self.tplink
        }

    # ---------------------------
    # Filtering Helpers
    # ---------------------------

    def filter_routers(self, vendor: str, min_users: int, min_sqft: int):
        catalog = self.get_vendor_catalog(vendor)
        return [
            r for r in catalog["routers"]
            if r["max_users_supported"] >= min_users
            and r["coverage_sqft"] >= min_sqft
        ]

    def filter_switches(self, vendor: str, min_devices: int):
        catalog = self.get_vendor_catalog(vendor)
        return [
            s for s in catalog["switches"]
            if s["max_devices_supported"] >= min_devices
        ]

    def filter_access_points(self, vendor: str, min_users: int, min_sqft: int):
        catalog = self.get_vendor_catalog(vendor)
        return [
            ap for ap in catalog["access_points"]
            if ap["max_users_supported"] >= min_users
            and ap["coverage_sqft"] >= min_sqft
        ]

    def filter_firewalls(self, vendor: str, min_users: int):
        catalog = self.get_vendor_catalog(vendor)
        return [
            fw for fw in catalog["firewalls"]
            if fw["max_users_supported"] >= min_users
        ]

    # ---------------------------
    # Budget-aware filtering
    # ---------------------------

    def filter_by_budget(self, devices: list, max_price: int):
        return [
            d for d in devices
            if d["price"] <= max_price
        ]

    # ---------------------------
    # Utility
    # ---------------------------

    def summarize_vendor(self, vendor: str):
        catalog = self.get_vendor_catalog(vendor)
        return {
            "routers": len(catalog["routers"]),
            "switches": len(catalog["switches"]),
            "access_points": len(catalog["access_points"]),
            "firewalls": len(catalog["firewalls"])
        }
