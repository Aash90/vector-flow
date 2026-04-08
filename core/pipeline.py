"""Main RAG Pipeline."""

from typing import List, Dict, Any, Tuple
from core.chunking import chunk_documents
from core.embeddings import EmbeddingsService
from core.retriever import VectorStore


class RAGPipeline:
    """Complete RAG pipeline: Chunk → Embed → Store → Retrieve."""
    
    def __init__(self, embedding_provider: str = "sentence-transformers", 
                 collection_name: str = "documents", persist_dir: str = None):
        """
        Initialize RAG pipeline.
        
        Args:
            embedding_provider: "openai" or "sentence-transformers"
            collection_name: ChromaDB collection name
            persist_dir: Directory for persistent vector storage
        """
        self.embeddings = EmbeddingsService(provider=embedding_provider)
        self.vector_store = VectorStore(collection_name, persist_dir)
        self.chunk_size = 256
        self.chunk_overlap = 50
    
    def ingest_documents(self, documents: List[str], clear_first: bool = False):
        """
        Ingest documents into the pipeline.
        
        Args:
            documents: List of document texts
            clear_first: Clear existing documents before ingesting
        """
        if clear_first:
            self.vector_store.clear()
        
        # Step 1: Chunk documents
        chunks = chunk_documents(documents, self.chunk_size, self.chunk_overlap)
        
        # Extract texts and metadata
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Step 2: Add to vector store (embeddings are handled internally by ChromaDB)
        self.vector_store.add_documents(texts, metadatas, ids)
        
        return len(chunks)
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve documents for a query.
        
        Args:
            query: Query text
            k: Number of results to retrieve
        
        Returns:
            List of result dicts with text, score, and metadata
        """
        results = self.vector_store.retrieve(query, k)
        
        return [
            {
                "text": text,
                "score": score,
                "metadata": metadata
            }
            for text, score, metadata in results
        ]
