from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    dimensions=300,
    google_api_key=google_api_key
)

document = ["Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
"Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
"MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
"Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
"Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."]

query = "Who is bumrah?"
docs_embedding = embeddings.embed_documents(document)
query_embedding = embeddings.embed_query(query)
score = cosine_similarity([query_embedding], docs_embedding)[0]

index, score = sorted(list(enumerate(score)),key=lambda x:x[1])[-1]

print(document[index])
print(query)
print("similarity score is: " , score)

