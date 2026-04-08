"""Vector store and retrieval service using ChromaDB."""

from typing import List, Tuple, Dict, Any
import chromadb
from chromadb.config import Settings


class VectorStore:
    """ChromaDB-based vector store for retrieval."""
    
    def __init__(self, collection_name: str = "documents", persist_dir: str = None):
        """
        Initialize ChromaDB vector store.
        
        Args:
            collection_name: Name of the collection
            persist_dir: Directory for persistent storage (None = in-memory)
        """
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        if persist_dir:
            settings = Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
            self.client = chromadb.Client(settings)
        else:
            self.client = chromadb.Client()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
        """Add documents to the vector store."""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def retrieve(self, query: str, k: int = 5) -> List[Tuple[str, float, Dict]]:
        """
        Retrieve top-k documents for a query.
        
        Returns:
            List of (text, score, metadata) tuples sorted by score (highest first)
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Parse ChromaDB results
        retrieved = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                score = results['distances'][0][i] if results['distances'] else 0
                # ChromaDB returns distances, convert to similarity (1 - distance for cosine)
                similarity = 1 - score if score < 1 else score
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                retrieved.append((doc, similarity, metadata))
        
        return retrieved
    
    def clear(self):
        """Clear the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
