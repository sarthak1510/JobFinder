# agents/title_generator.py

import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class TitleGeneratorAgent:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model_name=model_name,
            openai_api_key=os.environ["OPENAI_API_KEY"]
        )

    def generate_titles(self, resume_data: dict) -> list:
        skills = ", ".join(resume_data.get("skills", []))
        roles = ", ".join(resume_data.get("job_preferences", {}).get("roles", []))

        prompt = f"""
        You are a job matching assistant.
        Based on these skills: {skills}
        And these preferred roles: {roles}

        Return a JSON object with:
        "job_titles": list of 5 optimized US job titles.

        ONLY JSON. No explanation.
        """

        response = self.llm.invoke([HumanMessage(content=prompt)])
        try:
            result = json.loads(response.content)
            return result.get("job_titles", [])
        except Exception as e:
            raise ValueError(f"❌ Failed to parse LLM output: {e}")
