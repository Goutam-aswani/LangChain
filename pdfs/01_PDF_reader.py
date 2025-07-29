from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

loader = PyPDFLoader("D:\Banana Powder Export Business Guide_.pdf")

document = loader.load()

# print("content of first page: " , document[0].page_content[:200])
print("metadata of first page: ", document[0].metadata)