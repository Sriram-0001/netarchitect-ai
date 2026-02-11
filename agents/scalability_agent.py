def project(company_profile: dict, infrastructure_design: dict, llm) -> dict:

    system_prompt = """
    You are a Scalability Forecast Agent.
    Predict 3-year growth and infrastructure expansion.
    Output STRICT JSON only.
    """

    user_prompt = f"""
    Company Profile:
    {company_profile}

    Infrastructure Design:
    {infrastructure_design}

    Return JSON:
    {{
        "year_1_users": number,
        year_2 = int(year_2),
        year_3 = int(year_3),
        "upgrade_required": boolean,
        "upgrade_reason": "text"
    }}
    """

    return llm.call(system_prompt, user_prompt)
