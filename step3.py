from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = Ollama(model="llama3.2", request_timeout=120.0)

docs = SimpleDirectoryReader("data").load_data()
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.get_nodes_from_documents(docs)

index = VectorStoreIndex(chunks)

PROMPT = """Answer the question using ONLY the context below.
If the context does not contain the answer, say exactly: "I cannot answer this from the documents."
Do not use outside knowledge.

Context:
{context_str}

Question: {query_str}
Answer:"""

from llama_index.core import PromptTemplate
engine = index.as_query_engine(
    similarity_top_k=3,
    text_qa_template=PromptTemplate(PROMPT),
)

question = "What is the capital of France?"
response = engine.query(question)

print(response)
print("\n--- Sources ---")
for node in response.source_nodes:
    print(f"score {node.score:.3f} | {node.text[:150]}...")
    
