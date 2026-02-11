def generate(infrastructure_design: dict, llm) -> dict:

    system_prompt = """
    You are a Vendor Evaluation Agent.
    Provide two vendor options: Premium and Budget.
    Output STRICT JSON only.
    """

    user_prompt = f"""
    Infrastructure Design:
    {infrastructure_design}

    Return JSON:
    {{
        "vendor_options": [
            {{
                "vendor_name": "Vendor_A_Premium",
                "quality_score": number,
                "pricing_multiplier": number,
                "warranty_years": number
            }},
            {{
                "vendor_name": "Vendor_B_Budget",
                "quality_score": number,
                "pricing_multiplier": number,
                "warranty_years": number
            }}
        ]
    }}
    """

    return llm.call(system_prompt, user_prompt)
