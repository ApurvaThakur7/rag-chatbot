import os
import fitz  
from docx import Document

def load_documents(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(".pdf"):
            yield filename, extract_text_from_pdf(full_path)
        elif filename.lower().endswith(".docx"):
            yield filename, extract_text_from_docx(full_path)
        elif filename.lower().endswith(".txt"):
            with open(full_path, "r", encoding="utf-8") as f:
                yield filename, f.read()
        else:
            print(f"Unsupported file type: {filename}")
        

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def split_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
