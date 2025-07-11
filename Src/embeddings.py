# file: embeddings.py

import os
from langchain.vectorstores import Chroma
from langchain.embeddings import huggingface_hub


def create_vector_store(directory, embedding_model="sentence-transformers/all-MiniLM-L6-v2"):

    if not os.path.exists(directory):
        raise ValueError(f"Directory {directory} does not exist.")
    
    # Initialize the Hugging Face embeddings
    embeddings = huggingface_hub.HuggingFaceEmbeddings(model_name=embedding_model)
    
    # Create a Chroma vector store
    vector_store = Chroma.from_documents(
        directory=directory,
        embedding=embeddings
    )
    
    return vector_store