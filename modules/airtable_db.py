from pyairtable import Table

import os
from dotenv import load_dotenv

load_dotenv()
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)


def save_candidate(candidate, match_json):

    table.create({
        "Name": candidate.get("candidate_name", ""),
        "Email": candidate.get("email", ""),
        "Phone": candidate.get("phone", ""),
        "Location": candidate.get("location", ""),
        "Current Role": candidate.get("current_role", ""),
        "Current Company": candidate.get("current_company", ""),
        "Experience": str(candidate.get("total_experience", "")),
        "Education": str(candidate.get("education", "")),
        "Technical Skills": ", ".join(candidate.get("technical_skills", [])) if isinstance(candidate.get("technical_skills"), list) else str(candidate.get("technical_skills", "")),
        "Soft Skills": ", ".join(candidate.get("soft_skills", [])),
        "Certifications": ", ".join(candidate.get("certifications", [])),
        "Languages": ", ".join(candidate.get("languages", [])),
        "Projects": str(candidate.get("projects", "")),
        "Match Score": str(match_json.get("match_score", "")),
        "Matching Skills": ", ".join(match_json.get("matching_skills", [])),
        "Missing Skills": ", ".join(match_json.get("missing_skills", [])),
        "AI Summary": match_json.get("summary", ""),
        "Recommendation": match_json.get("recommendation", ""),
        "Recruiter Notes": "",
        "Application Status": "New"
    })