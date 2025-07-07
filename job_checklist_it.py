import streamlit as st
import json
import os
from datetime import date

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("📋 Job Application Tracker")

# --- File to store state ---
DATA_FILE = "job_tracker_data.json"

# --- Load data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        job_data = json.load(f)
else:
    job_data = {}

# --- Jobs list ---
jobs = {
    "Trainee Data analyst": "https://www.adzuna.co.uk/jobs/details/4986013048?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
    "Graduate Scheme - HO Digital": "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=b3duZXJ0eXBlPWZhaXImam9ibGlzdF92aWV3X3ZhYz0xOTU4MTIyJnVzZXJzZWFyY2hjb250ZXh0PTEzODQzNTMwMiZzZWFyY2hzb3J0PXNjb3JlJm93bmVyPTUwNzAwMDAmcGFnZWFjdGlvbj12aWV3dmFjYnlqb2JsaXN0JnNlYXJjaHBhZ2U9MSZwYWdlY2xhc3M9Sm9icw==",
    "IT Support Apprentice": "https://www.linkedin.com/jobs/view/4255199263",
    "Data Center Technician, Microsoft": "https://jobs.careers.microsoft.com/us/en/job/1829145/Data-Center-Technician?jobsource=linkedin/jobs/6952538?gh_src=00bdd2ae1",
    "IT Support Technician": "https://www.linkedin.com/jobs/view/4256882186",
    "Customer Support Technician, Hybrid": "https://alcumus.pinpointhq.com/postings/fe62f351-946a-4958-b9aa-431874242c78/applications/new?utm_medium=job_board&utm_source=linkedIn",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4255764277",
    "IT Service Desk Analyst": "https://www.linkedin.com/jobs/view/4252816741",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4251786334",
    "Service Desk Analyst, Hays": "https://www.linkedin.com/jobs/view/4255988653",
    "IT Service Desk Engineer": "https://www.linkedin.com/jobs/view/4242590705",
    "IT Support Officer, Welsh Rugby": "https://www.linkedin.com/jobs/view/4257017155",
    "AI Analyst": "https://www.linkedin.com/jobs/view/4250266675"   
}

status_colors = {
    "Not Applied": "white",
    "Applied": "#e6f7ff",
    "Interview": "#fffbe6",
    "Rejected": "#ffe6e6",
    "Offered": "#e6ffe6"
}

status_options = list(status_colors.keys())
filter_option = st.selectbox("Filter jobs by status:", ["All"] + status_options)

for job, link in jobs.items():
    data = job_data.get(job, {
        "applied": False,
        "notes": "",
        "date": "",
        "status": "Not Applied"
    })

    if filter_option != "All" and data["status"] != filter_option:
        continue

    bg_color = status_colors.get(data["status"], "white")
    display_job = f"~~{job}~~" if data["status"] == "Rejected" else job

    st.markdown(f"<div style='background-color:{bg_color}; padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
    with st.expander(f"🔗 [{display_job}]({link})"):
        applied = st.checkbox("Mark as applied", key=job, value=data["applied"])
        status = st.selectbox("Application status", status_options, index=status_options.index(data["status"]), key=f"{job}-status")
        notes = st.text_area("Notes", value=data["notes"], key=f"{job}-notes")
        app_date = st.date_input("Application date", key=f"{job}-date", value=date.fromisoformat(data["date"]) if data["date"] else date.today())

        job_data[job] = {
            "applied": applied,
            "notes": notes,
            "date": app_date.isoformat(),
            "status": status
        }
    st.markdown("</div>", unsafe_allow_html=True)

# --- Save to file ---
with open(DATA_FILE, "w") as f:
    json.dump(job_data, f, indent=2)

st.success("Progress saved locally. Relaunch the app to continue where you left off.")

