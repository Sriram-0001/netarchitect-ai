def project(company_profile: dict, infrastructure_design: dict, llm) -> dict:

    system_prompt = """
    You are a Scalability Forecast Agent.
    Predict 3-year user growth and determine if infrastructure upgrade is required.
    Output STRICT JSON only.
    """

    user_prompt = f"""
    Company Profile:
    {company_profile}

    Infrastructure Design:
    {infrastructure_design}

    Forecast user growth for 3 years based on growth_rate_percent.

    Return JSON in this exact format:
    {{
        "year_1_users": integer,
        "year_2_users": integer,
        "year_3_users": integer,
        "upgrade_required": boolean,
        "upgrade_reason": "string"
    }}
    """

    return llm.call(system_prompt, user_prompt)
