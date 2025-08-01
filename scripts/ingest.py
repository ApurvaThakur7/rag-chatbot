import os
from dotenv import load_dotenv
from tqdm import tqdm
from chromadb import PersistentClient
from openai import OpenAI
from utils import load_documents, split_text

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "vector_index/chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
DATA_FOLDER = "data/sample_docs"

client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection("rag_collection")

def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text]
    )
    return response.data[0].embedding

def ingest_documents():
    print(f"🔄 Ingesting documents from: {DATA_FOLDER}")
    
    document_count = 0
    chunk_count = 0
    
    for filename, text in tqdm(load_documents(DATA_FOLDER), desc="Processing documents"):
        document_count += 1
        chunks = split_text(text)
        
        for i, chunk in enumerate(chunks):
            try:
                embedding = get_embedding(chunk)
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{"source": filename}],
                    ids=[f"{filename}_{i}"]
                )
                chunk_count += 1
            except Exception as e:
                print(f"❌ Failed on {filename} chunk {i}: {e}")
    
    print(f"✅ Ingestion complete. Processed {document_count} documents, {chunk_count} chunks.")

if __name__ == "__main__":
    ingest_documents()