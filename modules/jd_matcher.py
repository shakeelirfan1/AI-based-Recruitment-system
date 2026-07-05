import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class JDMatcher:

    def compare(self, resume, jd):

        prompt = f"""
You are an expert HR recruiter.

Compare the resume with the job description.

Return ONLY valid JSON.

Fields:
- match_score
- matching_skills
- missing_skills
- strengths
- weaknesses
- recommendation
- summary

Resume:

{resume}

Job Description:

{jd}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content