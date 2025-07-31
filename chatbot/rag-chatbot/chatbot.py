from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=google_api_key)
db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)

custom_prompt_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Helpful Answer:"""

PROMPT = PromptTemplate(
    template=custom_prompt_template,
    input_variables=["context", "question"]     
)

llm = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature=0.2,
    google_api_key=google_api_key
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)


def chat():
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting chatbot. Goodbye!")
            break
        result = qa_chain({"query": user_input})
        print("Chatbot:", result['result'])
    
if __name__ == "__main__":
    chat()
    print("Chatbot session ended.")

