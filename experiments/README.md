# Running the Retrieval Debugger

## Quick Start

```bash
# Install dependencies
pip install -r ../requirements.txt

# Run the demo
python run_debugger.py
```

## What This Demo Shows

The `run_debugger.py` script demonstrates the core Vector-Flow system:

### 1. Basic RAG Pipeline
- **Chunking**: Splits documents into manageable pieces
- **Embedding**: Converts text to vector representations (using sentence-transformers)
- **Storage**: Stores vectors in ChromaDB for fast retrieval
- **Retrieval**: Finds top-K most similar documents to queries

### 2. Retrieval Debug Analysis (Our Innovation)

For each query, the system outputs:

**Top K Results**
```
[1] Score: 0.89
Text: "Dosage guidelines for Aspirin..."

[2] Score: 0.87
Text: "History of Aspirin..."
```

**Observations & Analysis**
- ⚠️ Keyword miss detection: Identifies when important query words are missing from results
- ⚠️ Similarity-Relevance gap: Detects high-scoring results that lack semantic relevance
- ⚠️ Chunk coverage issues: Identifies if chunking strategy needs adjustment

**Possible Issues**
- Embedding not capturing query intent
- Documents using different terminology
- Chunking may be too broad/narrow

## Core Components

### `core/pipeline.py`
Main RAG pipeline orchestrating the full flow.

### `core/embeddings.py`
Embedding service wrapper supporting:
- sentence-transformers (default, free)
- OpenAI API (requires API key)

### `core/retriever.py`
ChromaDB vector store wrapper for storage and retrieval.

### `debugger/heuristics.py`
Analysis functions:
- `detect_keyword_miss()`: Find missing query keywords
- `detect_similarity_relevance_gap()`: Detect high scores with low relevance
- `detect_chunk_coverage_issue()`: Identify chunking problems

### `debugger/retrieval_debugger.py`
RetrievalDebugger class that ties everything together with formatted output.

## Example Usage in Your Code

```python
from core.pipeline import RAGPipeline
from debugger.retrieval_debugger import RetrievalDebugger

# Initialize
pipeline = RAGPipeline(embedding_provider="sentence-transformers")

# Ingest documents
pipeline.ingest_documents([doc1, doc2, doc3])

# Debug a query
debugger = RetrievalDebugger(pipeline)
report = debugger.debug_query("Your query here", k=5)
print(debugger.format_debug_output(report))
```

## Next Steps (Insight Layer)

Future enhancements:
- Advanced keyword miss strategies
- Semantic relevance scoring
- Query rewriting recommendations
- Multi-step retrieval strategies
