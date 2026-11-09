# from openai import OpenAI

# class SummaryAgent:

#     def execute(
#         self,
#         metrics,
#         risk
#     ):

#         prompt = f"""
#         Analyze sprint metrics.

#         Completion Rate:
#         {metrics['completion_rate']}

#         Risk:
#         {risk['risk']}

#         Reasons:
#         {risk['reasons']}
#         """
        
#         client = OpenAI( api_key="YOUR_OPENAI_API_KEY")

#         response = client.chat.completions.create(
#             model="gpt-5",
#             messages=[
#                 {
#                     "role":"user",
#                     "content":prompt
#                 }
#             ]
#         )

#         return response.choices[0].message.content

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class SummaryAgent:

    def execute(self, metrics, risk):

        prompt = f"""
You are an Agile Delivery Manager.

Analyze the following sprint metrics.

Completion Rate: {metrics['completion_rate']}%
Risk Level: {risk['risk']}
Risk Reasons: {risk['reasons']}

Generate:
1. Executive Summary
2. Key Risks
3. Recommendations
4. Sprint Outlook

Keep the response concise and management-friendly.
"""

        try:
            client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Summary generation failed: {str(e)}"