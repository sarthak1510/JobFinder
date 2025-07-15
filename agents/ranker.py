import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from models.job_model import JobModel
from typing import List
import json

class RankerAgent:
    def __init__(self, api_key: str = None):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def clean_job_text(self, job: dict) -> str:
        title = job.get("title", "")
        description = job.get("description", "")
        return f"{title}\n{description}"

    def validate_jobs(self, raw_jobs: List[dict]) -> List[JobModel]:
        valid = []
        for job in raw_jobs:
            try:
                validated = JobModel(
                    title=job.get("title", "Unknown"),
                    company=job.get("company", {}).get("display_name", "Unknown"),
                    location=job.get("location", {}).get("display_name", "Unknown"),
                    description=job.get("description", ""),
                    url=job.get("redirect_url")
                )
                valid.append(validated)
            except Exception as e:
                print(f"⚠️ Invalid job skipped: {e}")
        return valid

    def rank_jobs(self, resume: dict, raw_jobs: List[dict], k=5) -> List[JobModel]:
        valid_jobs = self.validate_jobs(raw_jobs)
        job_texts = [self.clean_job_text(job.model_dump()) for job in valid_jobs]

        index = FAISS.from_texts(job_texts, embedding=self.embeddings)

        query = ", ".join(resume["skills"]) + ", " + ", ".join(resume["job_preferences"]["roles"])
        results = index.similarity_search(query, k=k)

        top_jobs = []
        for result in results:
            for job in valid_jobs:
                if result.page_content.strip() == self.clean_job_text(job.model_dump()).strip():
                    top_jobs.append(job)
                    break

        return top_jobs
