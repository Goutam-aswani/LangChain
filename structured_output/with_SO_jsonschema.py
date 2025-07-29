from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import TypedDict,Annotated

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)
review_schema = {
    "title": "Review",
    "description": "A movie review with a summary and sentiment analysis.",
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "A one-sentence summary of the movie."
        },
        "sentiment": {
            "type": "string",
            "description": "The overall sentiment, e.g., 'Positive', 'Negative', or 'Mixed'."
        }
    },
    "required": ["summary", "sentiment"]
}


structured_output = model.with_structured_output(review_schema)

result = structured_output.invoke("Write a review of the movie 'Inception' in one sentence, including its summary and sentiment.")

print(result)