# Use pydantic if:
# You need data validation sentiment must be -positive" , "neutral" . or -negative" ).
# You need default values if the LLM misses fields,
# You want automatic type conversion (e.g„


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field
from typing import TypedDict,Annotated,Optional,Literal

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# class Review(BaseModel):
#     key_themes: Annotated[str, "write down all the Key themes or elements discussed in the review in a list."]
#     summary: Annotated[str, "A one-sentence summary of the movie."]
#     sentiment: Annotated[Literal["pos","neg"], "The overall sentiment, e.g., 'Positive', 'Negative', or 'Mixed'."]
#     pros: Annotated[Optional[str], "List of pros or positive aspects of the movie."] = None
#     cons: Annotated[Optional[str], "List of cons or positive aspects of the movie."] = None


class Rveiew(BaseModel):
    key_themes: list[str] = Field(
        description="write down all the Key themes or elements discussed in the review in a list."
    )
    summary: str = Field(
        description="A one-sentence summary of the movie."
    )   
    sentiment: Literal["pos","neg"] = Field(
        description="The overall sentiment, e.g., 'Positive', 'Negative', or 'Mixed'."
    )
    pros: Optional[list[str]] = Field(
        default=None,
        description="List of pros or positive aspects of the movie."
    )
    cons: Optional[list[str]] = Field(
        default=None,
        description="List of cons or positive aspects of the movie."
    )
    



structured_output = model.with_structured_output(Rveiew)

result = structured_output.invoke("""Christopher Nolan\'s "Inception" attempts to immerse viewers in a convoluted world where experts infiltrate dreams to steal or plant ideas, following Cobb\'s quest to return home by performing one last impossible "inception." However, for all its visual grandeur and ambitious premise, the film crumbles under its own weight of excessive exposition and a clinical, detached narrative. What begins as a fascinating concept quickly devolves into an exhausting series of rules and explanations, leaving little room for genuine character development or emotional investment. The intricate multi-layered dreamscapes, while visually inventive, often feel more like a complex puzzle to be solved than a thrilling, immersive experience, making the stakes feel curiously low despite the constant peril. Ultimately, "Inception" is a meticulously constructed intellectual exercise that prioritizes cerebral gymnastics over human connection, resulting in a cold, over-explained spectacle that leaves one more bewildered than moved.""")

print(result)