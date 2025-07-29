from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  
    dimensions=32,
    google_api_key=google_api_key
)

texts = [
    "The capital of France is Paris.",
    "India is a country in South Asia.",
    "The currency of Japan is the Yen.",
    "New Delhi is the capital of India."
]

db = FAISS.from_texts(texts, embeddings)

query = "What is the capital of India?"
results = db.similarity_search(query)
print(f"Query: {query}")
print(f"Most relevant document: '{results[0].page_content}'")
