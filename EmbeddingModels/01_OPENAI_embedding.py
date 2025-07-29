from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv  

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3",dimensions=32)
text = "What is the capital of India?"
embedding = embeddings.embed_query(text)
print(str(embedding))
