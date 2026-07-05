import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AIExtractor:

    def extract_candidate(self, resume_text):

        prompt = f"""
You are an expert HR recruiter.

Extract the following information from the resume.

Return ONLY valid JSON.

Fields:
- candidate_name
- email
- phone
- location
- total_experience
- education
- technical_skills
- soft_skills
- certifications
- languages
- projects

Resume:

{resume_text}
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

    def ask_ai(self, prompt):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content
if __name__ == "__main__":
    ai = AIExtractor()

    result = ai.ask_ai("Say only: Groq is working.")

    print(result)