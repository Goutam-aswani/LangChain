from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-3.5", openai_api_key=os.getenv("OPENAI_API_KEY"))
response = model.invoke("What is the capital of India?")
print(response.content)
