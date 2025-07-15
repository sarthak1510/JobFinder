
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import load_environment
from agents.ranker import RankerAgent

load_environment()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parsed_resume_path = os.path.join(project_root, "data", "parsed_resume.json")
jobs_path = os.path.join(project_root, "data", "jobs.json")
output_path = os.path.join(project_root, "data", "ranked_jobs.json")

if not os.path.exists(parsed_resume_path):
    raise FileNotFoundError(f"❌ parsed_resume.json not found at {parsed_resume_path}")
if not os.path.exists(jobs_path):
    raise FileNotFoundError(f"❌ jobs.json not found at {jobs_path}")

with open(parsed_resume_path, "r") as f:
    resume = json.load(f)

with open(jobs_path, "r") as f:
    raw_jobs = json.load(f)

agent = RankerAgent()
top_jobs = agent.rank_jobs(resume, raw_jobs, k=5)


print(" Top Ranked Jobs:")
for i, job in enumerate(top_jobs, 1):
    print(f"{i}. {job.title} at {job.company} ({job.location})\n   🔗 {job.redirect_url}")

with open(output_path, "w") as f:
    json.dump([job.model_dump(mode="json") for job in top_jobs], f, indent=2)

