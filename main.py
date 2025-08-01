import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts.query_engine import generate_answer_with_citations
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        result = generate_answer_with_citations(request.query, k=3, format_for_web=True)
        
        if isinstance(result, dict):
            sources = result.get("sources", [])
            answer = result.get("answer", "")
        else:
            sources = []
            answer = str(result).replace('\n\n', '</p><p>').replace('\n', '<br>')
            answer = f"<p>{answer}</p>"
        
        return {
            "question": request.query,
            "answer": answer,
            "sources": sources,
            "context": result.get("context", "") if isinstance(result, dict) else ""
        }
        
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="frontend"), name="static")