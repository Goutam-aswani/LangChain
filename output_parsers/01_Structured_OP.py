from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "meta-llama/Llama-3.2-3B-Instruct",
    task= "text-generation"
)

model = ChatHuggingFace(llm = llm)

schema = [
    ResponseSchema(name = "fact1",description="fact 1 about the Topic"),
    ResponseSchema(name = "fact2",description="fact 2 about the topic"),
    ResponseSchema(name = "fact3",description="fact 3 about the Topic")
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template = "Write 3 facts about {topic} \n {format_instructions}",
    input_variables= ['topic'],
    partial_variables= {'format_instructions': parser.get_format_instructions()}
)

# prompt = template.invoke({'topic': 'blackhole'})
# result = model.invoke(prompt)
# print(result.content)
# final_result = parser.parse(result.content)
# print(final_result)


chain = template | model | parser
result = chain.invoke({'topic':'blackhole'})
print(result)
