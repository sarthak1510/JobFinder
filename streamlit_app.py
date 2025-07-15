import streamlit as st
import requests
import json

"BACKEND_URL = "https://jobfinder-production-331e.up.railway.app"


st.set_page_config(page_title="JobFinder", layout="centered")
st.markdown("<h1 style='text-align: center; color: #000000;'>🔍 JobFinder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA;'>Match your resume to the best jobs using AI + Adzuna</p>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    if st.button("🚀 Find Matching Jobs"):
        with st.spinner("⏳ Uploading and parsing resume..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }
            response = requests.post(f"{BACKEND_URL}/upload-resume", files=files)
            if response.status_code != 200:
                st.error(f"❌ Resume upload failed: {response.status_code}")
                st.text(response.text)
            else:
                st.success("✅ Resume parsed successfully!")

                
                title_res = requests.post(f"{BACKEND_URL}/generate-titles")
                if title_res.status_code != 200:
                    st.error(" Failed to generate job titles")
                    st.stop()

                
                search_res = requests.post(f"{BACKEND_URL}/search-jobs")
                if search_res.status_code != 200:
                    st.error("❌ Failed to fetch job listings")
                    st.stop()

                
                rank_res = requests.post(f"{BACKEND_URL}/rank-jobs")
                if rank_res.status_code != 200:
                    st.error("❌ Failed to rank jobs")
                    st.stop()

                top_jobs = rank_res.json().get("ranked_jobs", [])
                st.markdown("### 💼 Top Job Matches")
                for i, job in enumerate(top_jobs, 1):
                    st.markdown(f"""
                        <div style='padding: 10px; border: 1px solid #444; border-radius: 8px; margin-bottom: 10px; background-color: #1e1e1e;'>
                            <b style='color: #00FFCC;'>{i}. {job['title']}</b><br>
                            <span style='color: #CCCCCC;'>🏢 {job['company']}<br>
                            📍 {job['location']}</span><br>
                            🔗 <a href='{job['redirect_url']}' target='_blank'>Apply Now</a>
                        </div>
                    """, unsafe_allow_html=True)
