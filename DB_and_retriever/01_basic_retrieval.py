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


# mmr_retriever = db.as_retriever(search_type =  "mmr", search_kwargs={'k': 2, 'fetch_k': 10})
# mmr_query = "Tell me about the capitals of Asian countries."
# mmr_docs = mmr_retriever.invoke(mmr_query)


query = "What is the capital of India?"

retriever = db.as_retriever()
retrieved_docs = retriever.invoke(query)


# retriever_top_2 = db.as_retriever(search_kwargs={'k': 2})
# retrieved_docs = retriever_top_2.invoke(query)
# print(f"Retrieved {len(retrieved_docs)} documents.")   

#the kwagrs tell the retriever how many documents to return here it is 2

#default is all line to be returned


print("\n--- Retrieved Content ---")
for i, doc in enumerate(retrieved_docs):
    print(f"Document {i+1}:\n'{doc.page_content}'\n")
