import os
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "vector_index/chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection("rag_collection")

def get_query_embedding(query):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    )
    return response.data[0].embedding

def retrieve_relevant_chunks(query, k=3):
    query_embedding = get_query_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )
    
    # Debug: Print what we're actually retrieving
    print(f"\n🔍 DEBUG: Retrieved {len(results['documents'][0])} chunks for query: '{query}'")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"Chunk {i+1}: Source = {meta.get('source', 'Unknown')}")
        print(f"Content preview: {doc[:100]}...")
        print()
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return documents, metadatas

def generate_answer_with_citations(query, k=3, format_for_web=False):
    documents, metadatas = retrieve_relevant_chunks(query, k)

    context = ""
    sources = []
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        source = meta.get('source', 'Unknown')
        context += f"{i+1}. (source: {source})\n{doc}\n\n"
        if source not in sources and source != 'Unknown':
            sources.append(source)

    if format_for_web:
        
        prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question in a well-structured format suitable for web display.

IMPORTANT FORMATTING RULES FOR WEB:
1. Structure your response with clear sections using HTML tags:
   - Use <h3> for main section headings
   - Use <h4> for subsections  
   - Use <strong> for emphasis
   - Use <p> for paragraphs
   - Use <ul> and <li> for bullet points
   - Use <ol> and <li> for numbered lists
2. Include source references in parentheses after relevant information
3. Keep the response scannable and well-organized
4. Use proper HTML structure for better readability
5. Separate different concepts with clear section breaks

Context:
{context}

Question: {query}

Answer (use HTML formatting):
        """.strip()
    else:
        
        prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question in a well-structured format.

IMPORTANT FORMATTING RULES:
1. Use clear headings and subheadings
2. Use bullet points or numbered lists for multiple items
3. Separate different concepts with line breaks
4. Include source references in parentheses after relevant information
5. Make the response easy to scan and read

Context:
{context}

Question: {query}

Answer:
        """.strip()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    
    if format_for_web:
        return {
            "answer": answer,
            "sources": sources,
            "context": context,
            "raw_documents": documents
        }
    else:
        return answer