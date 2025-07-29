from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash"
                               ,google_api_key=os.getenv("GEMINI_API_KEY"))
response = model.invoke("what is the capital of India?")
print(response)