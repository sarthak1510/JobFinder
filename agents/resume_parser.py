import os
import json
import PyPDF2
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class ResumeParserAgent:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model_name=model_name,
            openai_api_key=os.environ["OPENAI_API_KEY"]
        )

    def parse_pdf_to_text(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            raise RuntimeError(f"❌ PDF parsing failed: {e}")

    def extract_json(self, text: str) -> dict:
        prompt = f"""
        You are a resume parser.
        From the resume text below, extract:
        - skills: list of technical skills
        - job_preferences: roles (list), locations (list)
        - experience_years: total years of experience

        Resume Text:
        {text}

        Return ONLY JSON. No explanation.
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            raise ValueError("❌ LLM returned invalid JSON")

    def parse_resume(self, file_path: str) -> dict:
        resume_text = self.parse_pdf_to_text(file_path)
        return self.extract_json(resume_text)
