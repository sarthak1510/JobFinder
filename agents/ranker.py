import os
from models.job_model import JobModel
from typing import List
import json
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


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
    print(" RankerAgent.rank_jobs()")

    valid_jobs = self.validate_jobs(raw_jobs)
    print(f"{len(valid_jobs)} jobs validated")

    job_texts = [self.clean_job_text(job.model_dump()) for job in valid_jobs]
    print(f"Created {len(job_texts)} job texts for FAISS")

    try:
        index = FAISS.from_texts(job_texts, embedding=self.embeddings)
        print(" FAISS index created")
    except Exception as e:
        print("FAISS init failed:", e)
        raise

    query = ", ".join(resume.get("skills", [])) + ", " + ", ".join(resume.get("job_preferences", {}).get("roles", []))
    print("Query:", query)

    try:
        results = index.similarity_search(query, k=k)
        print(f"Found {len(results)} matching jobs")
    except Exception as e:
        print("Similarity search failed:", e)
        raise

    ...

