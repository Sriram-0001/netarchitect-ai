import requests
import json
import re


class LLMHandler:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def extract_json(self, text: str):
        """
        Safely extract first valid JSON object from LLM response.
        """

        # Remove markdown blocks
        text = text.replace("```json", "").replace("```", "").strip()

        # Find first '{'
        start = text.find("{")
        if start == -1:
            raise Exception("No JSON object found in response.")

        # Track bracket balance
        bracket_count = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                bracket_count += 1
            elif text[i] == "}":
                bracket_count -= 1

                if bracket_count == 0:
                    json_str = text[start:i+1]
                    return json.loads(json_str)

        raise Exception("Incomplete JSON object in response.")

    def call(self, system_prompt: str, user_prompt: str) -> dict:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Groq API Error: {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        return self.extract_json(content)
