from utils.catalog_loader import CatalogLoader
import math
from utils.selection_validator import SelectionValidator


def design(requirements: dict, company_profile: dict, llm) -> dict:

    loader = CatalogLoader()

    num_users = company_profile["num_employees"]
    office_sqft = company_profile["office_size_sqft"]
    security_level = company_profile["security_level"]
    cloud_pref = company_profile["cloud_preference"]

    # -----------------------------
    # 1️⃣ Deterministic Quantity Logic
    # -----------------------------

    router_count = max(1, math.ceil(num_users / 150))
    switch_count = max(1, math.ceil(num_users / 48))
    ap_count = max(2, math.ceil(office_sqft / 1500))
    firewall_count = 1 if security_level in ["Medium", "High"] else 0
    ids_count = 1 if security_level == "High" else 0

    # -----------------------------
    # 2️⃣ Filter Catalog Options
    # -----------------------------

    cisco_routers = loader.filter_routers("Cisco", num_users, office_sqft)
    tplink_routers = loader.filter_routers("TP-Link", num_users, office_sqft)

    cisco_switches = loader.get_vendor_catalog("Cisco")["switches"]
    tplink_switches = loader.get_vendor_catalog("TP-Link")["switches"]

    cisco_aps = loader.get_vendor_catalog("Cisco")["access_points"]
    tplink_aps = loader.get_vendor_catalog("TP-Link")["access_points"]

    cisco_firewalls = loader.filter_firewalls("Cisco", num_users)
    tplink_firewalls = loader.filter_firewalls("TP-Link", num_users)

    # -----------------------------
    # 3️⃣ LLM Selects Models Only
    # -----------------------------

    system_prompt = """
    You are a Network Architecture Model Selection Agent.
    Select the best device models from provided options.
    You must choose ONLY from provided catalog lists.
    Output STRICT JSON only.
    You must select a valid model for every category.
    Empty strings are not allowed.

    """

    user_prompt = f"""
    Company Profile:
    {company_profile}

    Required Quantities (PRE-CALCULATED):
    Routers: {router_count}
    Switches: {switch_count}
    Access Points: {ap_count}
    Firewalls: {firewall_count}

    Cisco Router Options:
    {cisco_routers}

    TP-Link Router Options:
    {tplink_routers}

    Cisco Switch Options:
    {cisco_switches}

    TP-Link Switch Options:
    {tplink_switches}

    Cisco Access Point Options:
    {cisco_aps}

    TP-Link Access Point Options:
    {tplink_aps}

    Cisco Firewall Options:
    {cisco_firewalls}

    TP-Link Firewall Options:
    {tplink_firewalls}

    Return JSON:
    {{
        "topology": one of ["Star", "Hybrid", "Mesh"],
        "cisco_models": {{
            "router_model": "...",
            "switch_model": "...",
            "access_point_model": "...",
            "firewall_model": "..."
        }},
        "tplink_models": {{
            "router_model": "...",
            "switch_model": "...",
            "access_point_model": "...",
            "firewall_model": "..."
        }}
    }}
    """

    selection = llm.call(system_prompt, user_prompt)
    validator = SelectionValidator(loader)
    validated_cisco = validator.validate_vendor_selection(
        "Cisco", selection["cisco_models"]
    )

    validated_tplink = validator.validate_vendor_selection(
        "TP-Link", selection["tplink_models"]
    )

    # -----------------------------
    # 4️⃣ Final Structured Output
    # -----------------------------

    architecture = {
        "topology": selection["topology"],
        "components": {
            "routers": router_count,
            "switches": switch_count,
            "access_points": ap_count,
            "firewalls": firewall_count,
            "ids_systems": ids_count
        },
        "redundancy": {
            "enabled": True if security_level in ["Medium", "High"] else False,
            "dual_isp": True if security_level == "High" else False
        },
        "cloud_architecture": {
            "model": cloud_pref,
            "cloud_servers": 2 if cloud_pref in ["Cloud", "Hybrid"] else 0,
            "on_prem_servers": 2 if cloud_pref in ["On-Prem", "Hybrid"] else 0
        },
        "selected_models": {
        "cisco": validated_cisco,
        "tplink": validated_tplink
        }

    }

    return architecture
