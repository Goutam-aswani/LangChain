from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("Z:/LangChain/pdfs/newpdf.pdf")

document = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=240,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_documents(documents=document)
print(f"Number of documents loaded: {len(document)}")
print(f"Number of chunks created: {len(chunks)}")
print(f"Content of a chunk: {chunks[1].page_content}")
print(f"Metadata of that chunk: {chunks[0].metadata}")
