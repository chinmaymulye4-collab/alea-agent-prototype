from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = None

docs = SimpleDirectoryReader("data").load_data()
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.get_nodes_from_documents(docs)

index = VectorStoreIndex(chunks)
retriever = index.as_retriever(similarity_top_k=3)

question = "banana"
results = retriever.retrieve(question)

for i, r in enumerate(results, 1):
    print(f"--- Result {i} | score {r.score:.3f} ---")
    print(r.text[:400])
    print()
