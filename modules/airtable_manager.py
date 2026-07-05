from pyairtable import Table
from dotenv import load_dotenv
import os

load_dotenv()
print("TOKEN:", os.getenv("AIRTABLE_TOKEN"))
print("BASE:", os.getenv("AIRTABLE_BASE_ID"))
print("TABLE:", os.getenv("AIRTABLE_TABLE_NAME"))


class AirtableManager:

    def __init__(self):

        self.table = Table(
            os.getenv("AIRTABLE_TOKEN"),
            os.getenv("AIRTABLE_BASE_ID"),
            os.getenv("AIRTABLE_TABLE_NAME")
        )

    def safe_join(self, value):
        if not value:
            return ""

        if isinstance(value, list):
            result = []

            for item in value:

                if isinstance(item, dict):

                    if "name" in item:
                        result.append(item["name"])

                    elif "title" in item:
                        result.append(item["title"])

                    elif "degree" in item:
                        degree = item.get("degree", "")
                        institution = item.get("institution", "")

                        if institution:
                            result.append(f"{degree} - {institution}")
                        else:
                            result.append(degree)

                    else:
                        result.append(str(item))

                else:
                    result.append(str(item))

            return ", ".join(result)

        return str(value)

    def save_candidate(self, candidate, match, resume_name=""):

        score = match.get("match_score", 0)

        if isinstance(score, str):
            score = score.replace("%", "").strip()

        try:
            score = float(score) / 100
        except:
            score = 0

        record = {

            "Name": candidate.get("candidate_name", ""),

            "Email": candidate.get("email", ""),

            "Phone": candidate.get("phone", ""),

            "Location": candidate.get("location", ""),

            "Current Role": candidate.get("current_role", ""),

            "Current Company": candidate.get("current_company", ""),

            "Experience": candidate.get("total_experience", ""),

            "Education": self.safe_join(
                candidate.get("education", [])
            ),

            "Technical Skills": self.safe_join(
                candidate.get("technical_skills", [])
            ),

            "Soft Skills": self.safe_join(
                candidate.get("soft_skills", [])
            ),

            "Certifications": self.safe_join(
                candidate.get("certifications", [])
            ),

            "Languages": self.safe_join(
                candidate.get("languages", [])
            ),

            "Projects": self.safe_join(
                candidate.get("projects", [])
            ),

            "Match Score": score,

            "Matching Skills": self.safe_join(
                match.get("matching_skills", [])
            ),

            "Missing Skills": self.safe_join(
                match.get("missing_skills", [])
            ),

            "AI Summary": match.get("summary", ""),

            "Recommendation": match.get("recommendation", ""),

            "Recruiter Notes": "",

            "Application Status": match.get(
            "application_status",
            "New"
),

            "Resume Attachment": resume_name,

            "Email Subject": "",

            "Sender Email": ""
        }

        try:
            self.table.create(record)
            print("✅ Candidate saved to Airtable")

        except Exception as e:
            print("❌ Airtable Error")
            print(e)
            print(record)