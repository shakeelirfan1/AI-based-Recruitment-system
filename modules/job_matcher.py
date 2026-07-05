import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


class JobMatcher:

    def match_resume(self, resume_text, job_description):

        prompt = f"""
You are an expert ATS recruiter.

Compare the following resume with the given job description.

Return ONLY valid JSON.

Fields:
{{
    "match_score": "",
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommendation": "",
    "summary": ""
}}

Job Description:
{job_description}

Resume:
{resume_text}
"""

        response = model.generate_content(prompt)

        return response.text


if __name__ == "__main__":

    from resume_parser import ResumeParser
    from file_reader import FileReader

    parser = ResumeParser()
    reader = FileReader()

    resume_path = "data/resumes/88811_1781702817shakeel-resumae.pdf"

    resume = parser.extract_text(resume_path)

    jd = reader.read_job_description()

    matcher = JobMatcher()

    result = matcher.match_resume(resume, jd)

    print(result)