from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "meta-llama/Llama-3.2-3B-Instruct",
    task= "text-generation",
    temperature=0.1
)

model = ChatHuggingFace(llm = llm)

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt = 18,description="Age of the person")
    city: str = Field(description="City where the person lives")

parser = PydanticOutputParser(pydantic_object=Person)
 
template_str = """
You are an assistant that only responds in JSON.
Provide a JSON object with a fictional person's details from the specified place.
Your response must be a single, valid JSON object and nothing else.

{format_instructions}

Based on the user's query, provide the JSON object.
Query: A fictional person from {place}.

DO NOT output any python code, explanations, or any text other than the JSON object.
"""
template = PromptTemplate(
    # template = "Give me the name, age and city of a fictional {place} person. \n {format_instructions}",
    template = template_str,
    input_variables= ['place'],
    partial_variables= {'format_instructions': parser.get_format_instructions()}
)

chain = template | model | parser
result = chain.invoke({'place': 'New York'})
print(result)


