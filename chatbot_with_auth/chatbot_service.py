# chatbot_service.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings

def get_chatbot_response(prompt: str) -> str:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is not set in the environment.")

    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", google_api_key=settings.google_api_key)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a helpful assistant. Format your responses using GitHub-flavored Markdown. "
            "Use code blocks with language identifiers for all code snippets (e.g., ```python). "
            "Use bold and italics for emphasis. Use bullet points for lists."
        )),
        ("user", "{input}")
    ])
    
    output_parser = StrOutputParser()
    
    chain = prompt_template | llm | output_parser
    
    try:
        print("invoking LangChain with prompt:", prompt)
        response = chain.invoke({"input": prompt})
        return response
    except Exception as e:
        print(f"Error invoking LangChain: {e}")
        return "Sorry, I encountered an error while processing your request."

