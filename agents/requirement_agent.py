def process(user_input: dict, llm) -> dict:

    system_prompt = """
    You are a Network Requirement Analysis Agent.
    Convert business inputs into structured technical requirements.
    Output STRICT JSON only.
    """

    user_prompt = f"""
    Business Input:
    {user_input}

    Return JSON:
    {{
        "expected_bandwidth_mbps": number,
        "redundancy_required": boolean,
        "compliance_level": "Low/Medium/High",
        "risk_profile": "Low/Medium/High"
    }}
    """

    return llm.call(system_prompt, user_prompt)
