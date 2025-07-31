from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "meta-llama/Llama-3.2-3B-Instruct",
    task= "task-generation"
)

model = ChatHuggingFace(llm = llm)

parser = JsonOutputParser()

template = PromptTemplate(
    template = "Give me the name , age and city of a fictional human. \n {format_instruction}",
    input_variables= [],
    partial_variables= {'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

result = chain.invoke({})
print(result)