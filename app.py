import os
import streamlit as st
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
    PromptTemplate,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import time



PERSIST_DIR = "storage"

PROMPT = """Answer the question using ONLY the context below.
If the context does not contain the answer, say exactly: "I cannot answer this from the documents."
Do not use outside knowledge.

Context:
{context_str}

Question: {query_str}
Answer:"""




@st.cache_resource
def build_engine():
   
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Ollama(
        model="llama3.2",
        request_timeout=300.0,
        keep_alive="30m",
        additional_kwargs={"num_predict": 250},
    )

    if os.path.exists(PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    else:
        docs = SimpleDirectoryReader("data").load_data()
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        chunks = splitter.get_nodes_from_documents(docs)
        index = VectorStoreIndex(chunks)
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    return index.as_query_engine(
        similarity_top_k=4,
        text_qa_template=PromptTemplate(PROMPT),
        streaming=True,
   )


st.title("Study Assistant")
st.caption("Answers grounded in the indexed documents. Runs fully offline.")

engine = build_engine()
question = st.text_input("Ask a question about the documents:")

if question:
    t0 = time.time()
    response = engine.query(question)
    st.write_stream(response.response_gen)
    st.caption(f"{time.time() - t0:.1f} seconds")

    with st.expander("Sources"):
        for node in response.source_nodes:
            st.markdown(f"**score {node.score:.3f}**")
            st.text(node.text[:400])