from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


chat_template = ChatPromptTemplate([
    ('system',"You are a helpful {domain} expert."),
    # ('human',"Explain in simple terms, what is {topic}")
    ('human',"hey")
    ])

initial_prompt = chat_template.invoke({
    "domain": "hip hop",
    # "topic": "Eminem's impact on the genre"
})

chat_history = initial_prompt.to_messages()
initial_response = model.invoke(chat_history)
chat_history.append(AIMessage(content=initial_response.content))
print("AI:", initial_response.content)

while True:
    user_input = input("You:")
    if user_input == 'exit':
        break
    chat_history.append(HumanMessage(content = user_input))
    result = model.invoke(chat_history)
    chat_history.append(result.content)
    print("AI :" , result.content)
# result = model.invoke(prompt)
# print(result.content)
print(chat_history)