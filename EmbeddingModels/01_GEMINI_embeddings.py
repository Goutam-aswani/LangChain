from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  
    dimensions=32,
    google_api_key=google_api_key
)

text = "What is the capital of India?"
embedding = embeddings.embed_query(text)
print(str(embedding))
