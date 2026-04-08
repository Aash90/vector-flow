"""Document chunking utilities."""

from typing import List


def chunk_text(text: str, chunk_size: int = 256, overlap: int = 50) -> List[str]:
    """
    Simple chunking strategy: split by sentences/paragraphs.
    
    Args:
        text: Input text to chunk
        chunk_size: Approximate size of each chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to break at a sentence boundary
        if end < len(text):
            # Find last period, question mark, or newline before end
            last_break = max(
                text.rfind('.', start, end),
                text.rfind('?', start, end),
                text.rfind('\n', start, end)
            )
            if last_break > start:
                end = last_break + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap if end - overlap > start else end
    
    return chunks


def chunk_documents(documents: List[str], chunk_size: int = 256, overlap: int = 50) -> List[dict]:
    """
    Chunk multiple documents.
    
    Returns:
        List of dicts with 'text' and 'doc_id' keys
    """
    chunks = []
    
    for doc_id, doc in enumerate(documents):
        doc_chunks = chunk_text(doc, chunk_size, overlap)
        for chunk_idx, chunk in enumerate(doc_chunks):
            chunks.append({
                "text": chunk,
                "doc_id": doc_id,
                "chunk_id": chunk_idx,
                "metadata": {
                    "source": f"doc_{doc_id}",
                    "chunk_index": chunk_idx
                }
            })
    
    return chunks
