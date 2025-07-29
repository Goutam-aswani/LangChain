from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("D:\Banana Powder Export Business Guide_.pdf")

document = loader.load()

text_splitter =     RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_documents(documents=document)

print(f"Number of documents loaded: {len(document)}")
print(f"Number of chunks created: {len(chunks)}")
# print(f"Content of a chunk: {chunks[10].page_content}")
print(f"Metadata of that chunk: {chunks[10].metadata}")