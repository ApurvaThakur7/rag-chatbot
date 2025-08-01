# RAG AI Assistant 🤖

A Retrieval-Augmented Generation (RAG) chatbot that indexes documents, retrieves relevant context, and generates intelligent answers with source citations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)

## 🚀 Features

- Document processing and vector indexing
- AI-powered responses with source citations
- Modern web interface with real-time interactions
- Structured HTML output for better readability

## 🛠️ Libraries Used

### Backend
- **FastAPI** - Web framework for building APIs
- **OpenAI API** - GPT models and embeddings
- **ChromaDB** - Vector database for document storage
- **PyPDF2** - PDF document processing
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5/CSS3** with Vanilla JavaScript
- **Responsive design** with CSS animations

## 📋 Setup Instructions

### 1. Clone and Install
```bash
git clone https://github.com/ApurvaThakur7/rag-chatbot.git

cd rag-chatbot
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_DIR=vector_index/chroma_db
EMBEDDING_MODEL=text-embedding-3-small
```

### 3. Prepare Documents
- Place PDF files in the `data/` directory
- Run document indexing:
```bash
python scripts/ingest.py
```

### 4. Start Application
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` to use the chatbot.

## 📊 Project Structure

```
rag-chatbot/
├── data/                    # PDF documents
├── frontend/
│   └── index.html          # Web interface
├── scripts/
│   ├── ingest.py           # Document indexing
│   ├── query_engine.py     # RAG processing
│   └── utils.py            # Utilities
├── vector_index/           # Vector database
├── main.py                 # FastAPI app
└── requirements.txt        # Dependencies
```

## 🧪 Sample Queries

Try these example queries:

```
"Which group reported the highest number of domestic violence incidents?"

"What percentage of domestic violence reports were made by Hispanic females?"

"How do domestic violence reports among Hispanic females compare to African American women?"

"What is the percentage decrease in domestic violence cases from Hispanic females to the second-highest group?"
```

## 🔬 Testing

### Console Testing
```bash
python test_query.py
```

### Individual Components
```python
from scripts.query_engine import generate_answer_with_citations
result = generate_answer_with_citations("Your query here")
print(result)
```

## ⚠️ Limitations & Assumptions

### Limitations
- **PDF Only**: Currently supports PDF documents only
- **English Language**: Optimized for English text
- **File Size**: Large PDFs (>50MB) may cause delays
- **Context Limits**: Limited by OpenAI token limits
- **Manual Updates**: Requires re-indexing when documents change

### Assumptions
- PDFs contain extractable text (not scanned images)
- Stable internet connection for OpenAI API
- Queries are in English
- Documents are well-structured

### Security Notes
- Keep OpenAI API key secure
- CORS currently allows all origins (configure for production)
- Basic input sanitization implemented

## 🛠️ Troubleshooting

**ModuleNotFoundError**: `pip install -r requirements.txt`

**OpenAI API Error**: Check API key and credits in `.env`

**No Documents Found**: Place PDFs in `data/` and run `python scripts/ingest.py`

**ChromaDB Error**: Ensure `vector_index/` directory exists

