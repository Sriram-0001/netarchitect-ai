class SecurityAgent:

    def evaluate(self, infra_package):

        design = infra_package["infrastructure_design"]
        profile = infra_package["company_profile"]

        risk_score = 50  # base risk

        # Firewall reduces risk
        if design["components"]["firewalls"] > 0:
            risk_score -= 15

        # IDS reduces risk
        if design["components"]["ids_systems"] > 0:
            risk_score -= 10

        # High security requirement reduces tolerance
        if profile["security_level"].lower() == "high":
            risk_score -= 10

        # Redundancy improves resilience
        if design["redundancy"]["dual_isp"]:
            risk_score -= 5

        risk_score = max(risk_score, 5)

        return {
            "cisco": risk_score,
            "tplink": risk_score + 5  # assume slightly higher risk
        }
