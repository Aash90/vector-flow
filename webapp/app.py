"""FastAPI backend for Insight Layer visualization portal."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import RAGPipeline
from debugger.retrieval_debugger import RetrievalDebugger


# Global pipeline and debugger instances
_pipeline = None
_debugger = None
_documents = []


def init_pipeline():
    """Initialize the RAG pipeline and debugger."""
    global _pipeline, _debugger
    
    try:
        _pipeline = RAGPipeline(
            embedding_provider="sentence-transformers",
            collection_name="insight_layer_docs"
        )
        _debugger = RetrievalDebugger(_pipeline)
    except Exception as e:
        print(f"Error initializing pipeline: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifespan - startup and shutdown."""
    # Startup
    init_pipeline()
    yield
    # Shutdown (if needed)
    pass


app = FastAPI(
    title="Vector-Flow Insight Layer Portal",
    version="0.1.0",
    lifespan=lifespan
)

# Request/Response models
class IngestRequest(BaseModel):
    documents: List[str]


class QueryRequest(BaseModel):
    query: str
    k: int = 5


class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    num_results: int


@app.get("/")
async def root():
    """Serve the main HTML page."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Frontend not found")


@app.post("/api/ingest")
async def ingest_documents(request: IngestRequest):
    """Ingest documents into the vector store."""
    global _documents
    
    if not _pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    if not request.documents or len(request.documents) == 0:
        raise HTTPException(status_code=400, detail="No documents provided")
    
    try:
        num_chunks = _pipeline.ingest_documents(request.documents, clear_first=True)
        _documents = request.documents
        
        return {
            "status": "success",
            "num_documents": len(request.documents),
            "num_chunks": num_chunks,
            "message": f"Ingested {len(request.documents)} documents into {num_chunks} chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting documents: {str(e)}")


@app.post("/api/query")
async def query_documents(request: QueryRequest) -> QueryResponse:
    """Query and debug retrieval."""
    
    if not _pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if len(_documents) == 0:
        raise HTTPException(status_code=400, detail="No documents ingested. Please ingest documents first")
    
    try:
        debug_report = _debugger.debug_query(request.query, k=request.k)
        
        return QueryResponse(
            query=debug_report['query'],
            results=debug_report['results'],
            analysis=debug_report['analysis'],
            num_results=len(debug_report['results'])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/status")
async def status():
    """Get system status."""
    return {
        "status": "ready" if _pipeline else "not_initialized",
        "num_documents": len(_documents),
        "pipeline": "initialized" if _pipeline else "not_initialized"
    }


@app.get("/api/sample-data")
async def get_sample_data():
    """Get sample documents for demo."""
    sample_docs = [
        """
        Aspirin Medication Guide
        Active ingredient: Acetylsalicylic acid
        Dosage: 500mg tablets
        Dosage guidelines for Aspirin: Take 1-2 tablets every 4-6 hours as needed for pain relief.
        Do not exceed 8 tablets in 24 hours. Take with food to avoid stomach upset.
        Warnings: May cause stomach irritation and bleeding if used long-term.
        """,
        
        """
        History of Aspirin
        Aspirin was first synthesized in 1897 by German chemist Felix Hoffmann at Bayer.
        It was originally derived from willow bark, used for centuries in traditional medicine.
        The drug was approved by the FDA in 1939 and has been one of the most widely used medications.
        Over 100 years of use and safety data make it one of the most studied drugs.
        """,
        
        """
        Common Pain Relievers Comparison
        Aspirin: Good for inflammation, used for heart attack prevention
        Ibuprofen: Better pain relief, anti-inflammatory properties
        Acetaminophen: Gentle on stomach, no anti-inflammatory effects
        Naproxen: Long-acting, good for arthritis pain
        All pain relievers carry some risks when overused.
        """,
        
        """
        Cardiovascular Benefits of Aspirin
        Low-dose Aspirin (81mg daily) recommended for heart disease prevention.
        Thins blood by inhibiting platelet aggregation.
        Particularly useful after heart attack or stroke.
        Studies show 20-30% reduction in cardiovascular events with regular use.
        Consultation with doctor required before starting regimen.
        """,
    ]
    
    return {
        "documents": sample_docs,
        "count": len(sample_docs)
    }


# Mount static files with correct MIME types
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
