# Use JSON Schema if:
# You don't want to import extra Python libraries (Pydantic),
# • You need validation but don't need Python objects.
# You want to define structure in a standard JSON format.

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

schema = {
    "title": "Rveiew",
    "description": "A structured representation of a movie review.",
    "type": "object",
    "properties": {
        "key_themes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "write down all the Key themes or elements discussed in the review in a list."
        },
        "summary": {
            "type": "string",
            "description": "A one-sentence summary of the movie."
        },
        "sentiment": {
            "type": "string",
            "enum": ["pos", "neg"],
            "description": "The overall sentiment, e.g., 'Positive', 'Negative', or 'Mixed'."
        },
        "pros": {
            "type": ["array","null"],
            "items": {"type": "string"},
            "description": "List of pros or positive aspects of the movie."
        },
        "cons": {
            "type": ["array","null"],
            "items": {"type": "string"},
            "description": "List of cons or positive aspects of the movie."
        }
    },
    "required": ["key_themes", "summary", "sentiment"]
}

structured_output = model.with_structured_output(schema)

result = structured_output.invoke("Write a review of the movie 'Inception' in one sentence, including its summary and sentiment.")

# print("summary : ", result[0]['args']['summary'])
print(result)