import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Suggest me some delicious recipes possible in indian style with tomatoes , onions and olive oil")

print(response.text)
