import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import load_environment
from agents.job_search import JobSearchAgent

load_environment()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
titles_path = os.path.join(project_root, "data", "job_titles.json")
resume_path = os.path.join(project_root, "data", "parsed_resume.json")
output_path = os.path.join(project_root, "data", "jobs.json")

print(f"🧪 job_titles.json path: {titles_path}")
print("✅ job_titles.json exists?", os.path.exists(titles_path))

if not os.path.exists(titles_path):
    raise FileNotFoundError(f"❌ job_titles.json not found at {titles_path}")
if not os.path.exists(resume_path):
    raise FileNotFoundError(f"❌ parsed_resume.json not found at {resume_path}")

with open(titles_path) as f:
    job_titles = json.load(f)["job_titles"]

with open(resume_path) as f:
    resume = json.load(f)
    locations = resume["job_preferences"]["locations"]

# 🤖 Run agent
agent = JobSearchAgent()
jobs = agent.search_jobs(job_titles, locations)

# 💾 Save
with open(output_path, "w") as f:
    json.dump(jobs, f, indent=2)

# 🖨️ Show jobs
print("✅ Top Job Listings:")
for job in jobs[:5]:
    title = job.get("title", "Unknown")
    company = job.get("company", {}).get("display_name", "Unknown")
    loc = job.get("location", {}).get("display_name", "Unknown")
    url = job.get("redirect_url", "#")
    print(f"- {title} at {company} ({loc})\n  🔗 {url}")
