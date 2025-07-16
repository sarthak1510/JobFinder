from fastapi import APIRouter, UploadFile, File
import os, json
from agents.resume_parser import ResumeParserAgent
from agents.title_generator import TitleGeneratorAgent
from agents.job_search import JobSearchAgent
from agents.ranker import RankerAgent

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    agent = ResumeParserAgent()
    contents = await file.read()

    os.makedirs("data", exist_ok=True)
    temp_path = "data/temp_resume.pdf"
    with open(temp_path, "wb") as f:
        f.write(contents)

    parsed = agent.parse_resume(temp_path)

    with open("data/parsed_resume.json", "w") as f:
        json.dump(parsed, f, indent=2)

    return parsed

@router.post("/generate-titles")
def generate_titles():
    with open("data/parsed_resume.json") as f:
        resume = json.load(f)

    agent = TitleGeneratorAgent()
    titles = agent.generate_titles(resume)

    with open("data/job_titles.json", "w") as f:
        json.dump({"job_titles": titles}, f, indent=2)

    return {"titles": titles}

@router.post("/search-jobs")
def search_jobs():
    with open("data/job_titles.json") as f:
        job_titles = json.load(f)["job_titles"]

    with open("data/parsed_resume.json") as f:
        resume = json.load(f)

    locations = resume.get("job_preferences", {}).get("locations", [])

    agent = JobSearchAgent()
    jobs = agent.search_jobs(job_titles, locations)

    with open("data/jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    return {"jobs": jobs[:15]}

@router.post("/rank-jobs")
def rank_jobs():
    try:
        print(" /rank-jobs called")

        with open("data/parsed_resume.json") as f:
            resume = json.load(f)
        print(" Resume loaded with keys:", list(resume.keys()))

        with open("data/jobs.json") as f:
            raw_jobs = json.load(f)
        print(f" Loaded {len(raw_jobs)} raw jobs")

        agent = RankerAgent()
        top_jobs = agent.rank_jobs(resume, raw_jobs)
        print(f"Ranked {len(top_jobs)} jobs")

        ranked_jobs = [job.model_dump(mode="json") for job in top_jobs]

        with open("data/ranked_jobs.json", "w") as f:
            json.dump(ranked_jobs, f, indent=2)

        return {"ranked_jobs": ranked_jobs}

    except Exception as e:
        print(" ERROR in /rank-jobs:", str(e))
        return {"error": str(e)}, 500

