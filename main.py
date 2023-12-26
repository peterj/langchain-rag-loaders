from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
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

splits = text_splitter.split_documents(md_header_splits)



print(splits)



# print(doc)

# text_splitter = CharacterTextSplitter(
#     # Set a really small chunk size, just to show.
#     chunk_size = 100,
#     chunk_overlap  = 20,
#     length_function = len,
#     add_start_index = True,
#     separator = "\n",
# )

# texts = text_splitter.create_documents([text])

# print(texts[0])
# print(texts[1])

# loader = PyPDFLoader("./book.pdf", extract_images=True)
# pages = loader.load()
# print(pages[14].page_content)

# post_path = "./post.md"

# loader = UnstructuredMarkdownLoader(post_path, mode="elements")

# data = loader.load()

# print(data)


# loader = PythonLoader('./joke.py')
# docs = loader.load()

# print(docs)

# loader = TextLoader("./post.md")
# print(loader.load())