# File: text_cleaner.py

import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def clean_text(text):
    # Hapus icon atau karakter aneh
    text = re.sub(r"[📄📊🟩📷]", "", text)
    text = re.sub(r"\\n{2,}", "\n", text)
    text = re.sub(r"\\s{2,}", " ", text)
    text = text.strip()
    return text

def split_and_format(text, metadata=None, chunk_size=1000, chunk_overlap=100):
    cleaned = clean_text(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(cleaned)

    docs = []
    for i, chunk in enumerate(chunks):
        docs.append(Document(
            page_content=chunk,
            metadata={
                "chunk": i,
                **(metadata or {})
            }
        ))
    return docs
