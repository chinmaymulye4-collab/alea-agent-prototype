from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

docs = SimpleDirectoryReader("data").load_data()
print(f"Loaded {len(docs)} pages")

splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.get_nodes_from_documents(docs)
print(f"Created {len(chunks)} chunks")

print("--- First chunk ---")
print(chunks[0].text)