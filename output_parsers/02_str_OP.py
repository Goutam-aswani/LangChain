from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "meta-llama/Llama-3.2-3B-Instruct",
    task= "task-generation"
)

model = ChatHuggingFace(llm = llm)

#1st prompt

template1 = PromptTemplate(
    template = 'Write a detailed report on {topic}',
    input_variables= ['topic']
)
#2nd prompt
template2 = PromptTemplate(
    template = 'Write a 2 line summary on the following text./n {text}',
    input_variables= ['text']
)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic':'blackhole'})

print(result)