from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv
import os


load_dotenv()

os.environ["HF_HOME"] = 'D:/HuggingFace'

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs={
        'max_new_tokens': 128,
    })

response = llm.invoke("write a rap on arpit")
print(response)