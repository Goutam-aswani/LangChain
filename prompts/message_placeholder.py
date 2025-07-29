from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

chat_template = ChatPromptTemplate([
    ('system','you are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []
with open("chat_history.txt") as f:
    print(f)
    chat_history.extend(f.readlines())

# chat_history = [
#     """HumanMessage(content="I want to request a refund for my order #12345.")
# AIMessage(content = "Your refund request for order #12345 has been initiated. It will be processed in 3-5 business days.")
# """]

print(chat_history)

prompt = chat_template.invoke({'chat_history' : chat_history,'query': 'where is my refund'})

result = model.invoke(prompt)
print(result.content)

















