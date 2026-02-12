class SecurityAgent:

    def calculate_risk(self, infra_package):

        infra = infra_package["infrastructure_design"]
        company = infra_package["company_profile"]
        results = {}

        for vendor in infra["selected_models"]:

            risk = 50

            if company["security_level"] == "High":
                risk -= 10
            elif company["security_level"] == "Medium":
                risk -= 5

            if infra["components"]["firewalls"] > 0:
                risk -= 10

            if infra["components"]["ids_systems"] > 0:
                risk -= 10

            if vendor == "cisco":
                risk -= 10
            else:
                risk += 5

            results[vendor] = max(0, min(100, risk))

        return results
