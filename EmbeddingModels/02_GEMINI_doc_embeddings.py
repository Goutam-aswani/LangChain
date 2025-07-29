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

document = [
    "What is the capital of India?",
    "What is the capital of France?",
    "What is the capital of Japan?"
]
text = "What is the capital of India?"
embedding = embeddings.embed_documents(document)
print(str(embedding))
