from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

KNOWLEDGE_BASE_DIR = "knowledge_base"

def ingest_data():
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.txt", show_progress=True,loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {KNOWLEDGE_BASE_DIR}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text = text_splitter.split_documents(documents)
    print(f"Split into {len(text)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=google_api_key)

    db = FAISS.from_documents(text, embeddings)

    db.save_local("faiss_index")
    print("FAISS index saved to faiss_index")

if __name__ == "__main__":
    ingest_data()
    print("Ingestion complete.")
