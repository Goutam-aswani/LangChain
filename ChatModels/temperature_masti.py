from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
#                                temperature=0.1
#                                ,google_api_key=os.getenv("GEMINI_API_KEY"))
# response = model.invoke("tell me a funny dark joke")
# print(response)
response1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                               temperature=0.1
                               ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke")
print(response1.content)
response2 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                               temperature=0.3
                               ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke") 
print(response2.content)
response3 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",    
                               temperature=0.5
                               ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke")
print(response3.content)
response4 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                 temperature=0.7
                                 ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke")
print(response4.content)
response5 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                 temperature=0.9
                                 ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke")
print(response5.content)
response6 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                 temperature=1.0
                                 ,google_api_key=os.getenv("GEMINI_API_KEY")).invoke("tell me a funny dark joke")       
print(response6.content)
