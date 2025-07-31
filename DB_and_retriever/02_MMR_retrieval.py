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

mmr_retriever = db.as_retriever(search_type =  "mmr", search_kwargs={'k': 2, 'fetch_k': 10})
#here k is the final number of documents to return

#fetch_k is the number of documents to consider for MMR to be fetched initially for re-ranking
mmr_query = "Tell me about the capitals of Asian countries."
mmr_docs = mmr_retriever.invoke(mmr_query)


print("\n--- MMR Results ---")
for i, doc in enumerate(mmr_docs):
    print(f"Document {i+1}:\n'{doc.page_content}'\n")
