# agents/intent_agent.py

import os
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()


class IntentAgent:

    def execute(self, question):

        prompt = f"""
You are a Jira query classifier.

Classify the user request into one of these intents:

- completed_issues
- open_issues
- blocked_issues
- bugs
- sprint_health
- risk_analysis

Return ONLY JSON.

Question:
{question}

Example:
{{"intent":"completed_issues"}}
"""

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return json.loads(response.text)