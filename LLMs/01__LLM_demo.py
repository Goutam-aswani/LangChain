from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = GoogleGenerativeAI(model = "gemini-2.5-pro", temperature=0.1)
response = llm.generate(["What is the capital of France?"])
print(response.generations[0][0].text)