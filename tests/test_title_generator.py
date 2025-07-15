import os, sys, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_environment
from agents.title_generator import TitleGeneratorAgent

load_environment()

parsed_resume_path = os.path.join(os.path.dirname(__file__), "..", "data", "parsed_resume.json")

if not os.path.exists(parsed_resume_path):
    raise FileNotFoundError(f"Resume JSON not found at: {parsed_resume_path}")

with open(parsed_resume_path, "r") as f:
    resume_json = json.load(f)

agent = TitleGeneratorAgent()
titles = agent.generate_titles(resume_json)

print("Generated Job Titles:")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

with open(os.path.join(os.path.dirname(__file__), "..", "data", "job_titles.json"), "w") as f:
    json.dump({"job_titles": titles}, f, indent=2)
