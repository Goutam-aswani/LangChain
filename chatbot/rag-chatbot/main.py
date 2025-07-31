from fastapi import FastAPI
from pydantic import BaseModel
from chain import get_qa_chain
from fastapi.middleware.cors import CORSMiddleware 

class Query(BaseModel):
    question: str

app = FastAPI(title = "Indori Brews Chatbot API")

origins = ["*"] # In production, you should restrict this to your frontend's domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qa_chain = get_qa_chain()

@app.post("/chat")
async def chat(query: Query):
    result = qa_chain.invoke({"question": query.question})

    answer = result.get('answer', 'No answer found.')
    return {
        "answer": answer
        }
