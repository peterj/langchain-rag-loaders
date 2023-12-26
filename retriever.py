from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

template = """Answer the question based only on the following context:

{context}

Question: {question}
"""

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


# full_text = open("text.txt", "r").read()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# texts = text_splitter.split_text(full_text)

text =""
with open("./post.md") as f:
    text = f.read()

headers_to_split_on = [
      ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
text_splitter =  MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = text_splitter.split_text(text)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=30
)
texts = text_splitter.split_documents(md_header_splits)


embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(documents=texts, embedding=embeddings)
# retriever = db.as_retriever()

model = ChatOpenAI()
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=model
)

prompt = ChatPromptTemplate.from_template(template)
chain = (
    {"context": retriever_from_llm | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke("How to set up statsd-exporter?"))


# retrieved_docs = retriever.invoke(
#     "What did the president say about Ketanji Brown Jackson?"
# )
# print(retrieved_docs[0].page_content)