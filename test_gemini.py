import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API Key:", api_key[:15] + "...")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

try:
    response = model.generate_content("Say hello")
    print("SUCCESS")
    print(response.text)
except Exception as e:
    print("ERROR")
    print(e)