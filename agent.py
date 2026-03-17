import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash-lite')

print("----Chat Started (Type 'exit or bye' to stop)-----------")

while True:
    user_input = input("You:")

    if user_input in ["exit","bye","quit"]:
        print("GoodBye! See you tommorow")
        break

    response = model.generate_content(user_input)
    print("Agent:",response.text)

