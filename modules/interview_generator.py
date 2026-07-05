import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class InterviewGenerator:

    def generate(self, resume):

        prompt = f"""
You are a senior HR interviewer.

Generate:

- 5 HR Questions
- 5 Technical Questions
- 5 Project Questions

based on this resume.

Resume:

{resume}
"""

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