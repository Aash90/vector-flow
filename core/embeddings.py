"""Embedding service wrapper for both OpenAI and sentence-transformers."""

from typing import List
from enum import Enum


class EmbeddingProvider(Enum):
    OPENAI = "openai"
    SENTENCE_TRANSFORMERS = "sentence-transformers"


class EmbeddingsService:
    """Wrapper for embedding models."""
    
    def __init__(self, provider: str = "sentence-transformers", model_name: str = None):
        """
        Initialize embeddings service.
        
        Args:
            provider: "openai" or "sentence-transformers"
            model_name: specific model to use
        """
        self.provider = provider
        
        if provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI()
                self.model_name = model_name or "text-embedding-3-small"
            except ImportError:
                raise ImportError("OpenAI package required: pip install openai")
        else:
            try:
                from sentence_transformers import SentenceTransformer
                self.model_name = model_name or "all-MiniLM-L6-v2"
                self.model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError("sentence-transformers required: pip install sentence-transformers")
    
    def embed(self, text: str) -> List[float]:
        """Embed a single text."""
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=text,
                model=self.model_name
            )
            return response.data[0].embedding
        else:
            return self.model.encode(text).tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name
            )
            return [item.embedding for item in response.data]
        else:
            return self.model.encode(texts).tolist()
