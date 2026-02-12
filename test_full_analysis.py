from agents.llm_cost_analysis_agent import analyze_infrastructure

infra_input = {
    "architecture": {
        "devices": {
            "router": 2,
            "switch": 4,
            "firewall": 1
        },
        "security_level": "High",
        "redundancy": True,
        "ids": True
    },
    "vendor_options": ["VendorA", "VendorB"],
    "scalability_projection": {},
    "budget": 700000
}

result = analyze_infrastructure(infra_input)
print(result)
