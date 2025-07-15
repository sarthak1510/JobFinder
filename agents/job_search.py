import os
import requests

class JobSearchAgent:
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.api_key = os.getenv("ADZUNA_API_KEY")

        if not self.app_id or not self.api_key:
            raise EnvironmentError("Adzuna API credentials not set in .env")

    def search_jobs(self, job_titles, locations=None):
        found_jobs = []

        for title in job_titles:
            print(f"🔎 Searching for: {title} across the United States")
            results = self.call_adzuna(title)
            if results:
                found_jobs.extend(results)
                print(f"✅ Found {len(results)} jobs for '{title}'")
                break
            else:
                print(f"⚠️ No jobs found for '{title}'")

        return found_jobs

    def call_adzuna(self, title):
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "what": title,
            "results_per_page": 15,  
            "content-type": "application/json"
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"⚠️ Adzuna error: {response.status_code} - {response.text}")
                return []
            return response.json().get("results", [])
        except requests.RequestException as e:
            print(f"❌ API call failed: {e}")
            return []
