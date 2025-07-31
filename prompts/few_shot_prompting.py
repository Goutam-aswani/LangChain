from langchain.prompts import FewShotPromptTemplate, ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

examples = [
    {
        "input": "My monthly bill is higher than expected.",
        "output": "Billing"
    },
    {
        "input": "I can't log in to my account on your website.",
        "output": "Technical Support"
    },
    {
        "input": "What are your business hours on holidays?",
        "output": "General Inquiry"
    },
    {"input": "I was charged twice for the same order.", "output": "Billing"},
    {"input": "Can you help me reset my password?", "output": "Technical Support"},
    {"input": "Do you offer student discounts?", "output": "General Inquiry"},
    {"input": "My app keeps crashing after the update.", "output": "Technical Support"},
    {"input": "Why was my payment declined?", "output": "Billing"},
    {"input": "Do you ship internationally?", "output": "General Inquiry"},
    {"input": "I'm getting an error message when I try to check out.", "output": "Technical Support"},
    {"input": "Can I get a refund for my purchase?", "output": "Billing"},
    {"input": "Whats your return policy?", "output": "General Inquiry"},
    {"input": "The promo code isnt working.", "output": "Technical Support"},
    {"input": "My invoice is missing for last month.", "output": "Billing"},
    {"input": "Is your customer support available on weekends?", "output": "General Inquiry"},
    {"input": "I'm unable to upload documents to my profile.", "output": "Technical Support"},
    {"input": "Theres an unexplained charge on my credit card.", "output": "Billing"},
    {"input": "Do you have a branch in Mumbai?", "output": "General Inquiry"},
    {"input": "The download link isnt working.", "output": "Technical Support"},
    {"input": "How do I update my billing address?", "output": "Billing"},
    {"input": "What languages does your support team speak?", "output": "General Inquiry"},
    {"input": "I can't access premium features after paying.", "output": "Technical Support"},
    {"input": "Can I change my subscription plan?", "output": "Billing"},
    {"input": "How long is the free trial?", "output": "General Inquiry"},
    {"input": "The website is loading very slowly.", "output": "Technical Support"},
    {"input": "Why was I charged even after cancellation?", "output": "Billing"},
    {"input": "Can I speak to a human agent?", "output": "General Inquiry"},
    {"input": "The confirmation email hasnt arrived.", "output": "Technical Support"},
    {"input": "I received the wrong item.", "output": "Billing"},
    {"input": "Do you have 24/7 chat support?", "output": "General Inquiry"},
    {"input": "The two-factor authentication is not working.", "output": "Technical Support"},
    {"input": "How do I view past invoices?", "output": "Billing"},
    {"input": "Where can I download your mobile app?", "output": "General Inquiry"}
]



example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,example_prompt=example_prompt)   


final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at classifying customer support tickets. You must classify each ticket into one of the following categories: Billing, Technical Support, or General Inquiry."),
    few_shot_prompt,
    ("human", "{input}")
])

new_ticket = "The login page wont load on my phone."
formatted_prompt = final_prompt.invoke({"input": new_ticket})
result = model.invoke(formatted_prompt.to_messages())
# print(formatted_prompt.to_messages())
print("Human query: ", new_ticket)
print(result.content)
