class SelectionValidator:

    def __init__(self, loader):
        self.loader = loader

    def get_highest_capacity(self, devices, key):
        return max(devices, key=lambda x: x[key])["model"]

    def validate_vendor_selection(self, vendor_name, selected_models):

        catalog = self.loader.get_vendor_catalog(vendor_name)

        validated = {}

        # ROUTER
        router_models = [d["model"] for d in catalog["routers"]]
        if selected_models["router_model"] in router_models:
            validated["router_model"] = selected_models["router_model"]
        else:
            validated["router_model"] = self.get_highest_capacity(
                catalog["routers"], "max_users_supported"
            )

        # SWITCH
        switch_models = [d["model"] for d in catalog["switches"]]
        if selected_models["switch_model"] in switch_models:
            validated["switch_model"] = selected_models["switch_model"]
        else:
            validated["switch_model"] = self.get_highest_capacity(
                catalog["switches"], "max_devices_supported"
            )

        # ACCESS POINT
        ap_models = [d["model"] for d in catalog["access_points"]]
        if selected_models["access_point_model"] in ap_models:
            validated["access_point_model"] = selected_models["access_point_model"]
        else:
            validated["access_point_model"] = self.get_highest_capacity(
                catalog["access_points"], "max_users_supported"
            )

        # FIREWALL
        fw_models = [d["model"] for d in catalog["firewalls"]]
        if selected_models["firewall_model"] in fw_models:
            validated["firewall_model"] = selected_models["firewall_model"]
        else:
            validated["firewall_model"] = self.get_highest_capacity(
                catalog["firewalls"], "max_users_supported"
            )

        return validated
