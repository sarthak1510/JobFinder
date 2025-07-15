import os, sys, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_environment
from agents.resume_parser import ResumeParserAgent

load_environment()
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pdf_path = os.path.join(project_root, "data", "sample_resume.pdf")

parser = ResumeParserAgent()
parsed = parser.parse_resume(pdf_path)

print("Resume Parsed:")
print(json.dumps(parsed, indent=2))

os.makedirs(os.path.join(project_root, "data"), exist_ok=True)
with open(os.path.join(project_root, "data", "parsed_resume.json"), "w") as f:
    json.dump(parsed, f, indent=2)
