import math


class DeploymentAgent:

    def estimate(self, infra_package, cost_output):

        profile = infra_package["company_profile"]
        design = infra_package["infrastructure_design"]
        components = design["components"]

        sqft = profile["office_size_sqft"]

        # Cable estimation
        avg_cable_per_device = 30  # meters

        total_devices = (
            components["routers"] +
            components["switches"] +
            components["access_points"] +
            components["firewalls"]
        )

        cable_length = total_devices * avg_cable_per_device
        cable_type = "Fiber" if sqft > 10000 else "Cat6"

        # Rack estimation
        rack_units = total_devices * 2
        racks_required = math.ceil(rack_units / 42)

        # Labour estimation
        labour_hours = total_devices * 4
        labour_cost = labour_hours * 1500

        # Power estimation
        estimated_power_kw = total_devices * 0.5

        # Use correct cost_output schema
        cisco_cost = cost_output["cisco_total_cost"]
        tplink_cost = cost_output["tplink_total_cost"]

        total_project_cost = cisco_cost + labour_cost

        return {
            "cable_length_meters": cable_length,
            "cable_type": cable_type,
            "rack_units_required": rack_units,
            "racks_required": racks_required,
            "estimated_labour_hours": labour_hours,
            "labour_cost": labour_cost,
            "estimated_power_kw": estimated_power_kw,
            "cisco_hardware_cost": cisco_cost,
            "tplink_hardware_cost": tplink_cost,
            "total_project_cost_estimate": total_project_cost
        }
