import json
from agents.analysis_engine import run_analysis

# Load your architecture output JSON
infra_package = {
  "company_profile": {
    "num_employees": 120,
    "office_size_sqft": 6000,
    "security_level": "High",
    "growth_rate_percent": 20,
    "cloud_preference": "Hybrid",
    "budget": 700000
  },
  "infrastructure_design": {
    "topology": "Hybrid",
    "components": {
      "routers": 1,
      "switches": 3,
      "access_points": 4,
      "firewalls": 1,
      "ids_systems": 1
    },
    "cloud_architecture": {
      "model": "Hybrid",
      "cloud_servers": 2,
      "on_prem_servers": 2
    },
    "redundancy": {
      "enabled": True,
      "dual_isp": True
    },
    "selected_models": {
      "cisco": {
        "router_model": "Cisco Catalyst 8300",
        "switch_model": "Cisco Catalyst 9200",
        "access_point_model": "Cisco Catalyst 9120",
        "firewall_model": "Cisco Firepower 1120"
      },
      "tplink": {
        "router_model": "TP-Link ER8411",
        "switch_model": "TP-Link JetStream 48",
        "access_point_model": "TP-Link EAP660 HD",
        "firewall_model": "TP-Link SafeStream TL-R605"
      }
    }
  },
  "scalability_projection": {
    "year_1_users": 144,
    "year_2_users": 172,
    "year_3_users": 207,
    "upgrade_required": True,
    "upgrade_reason": "Insufficient infrastructure to support projected growth"
  }
}

result = run_analysis(infra_package)

print(json.dumps(result, indent=2))
