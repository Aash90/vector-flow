# Web Portal - Insight Layer Visualization

Interactive portal to visualize and debug RAG retrieval behavior.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The portal will be available at: **http://localhost:8000**

### 3. Using the Portal

**Step 1: Ingest Documents**
- Click "Load Sample Docs" to use pharmaceutical sample data
- Or paste your own documents in the textarea
- Click "Ingest Documents" to process

**Step 2: Query & Analyze**
- Enter a query in the search box
- Adjust "Top K Results" if needed (default: 5)
- Click "Run Query & Analyze"

**Step 3: Review Analysis**
- View top K retrieval results with similarity scores
- Read observations and possible issues
- Review detailed analysis including:
  - Keyword coverage
  - Chunk statistics
  - Similarity-relevance gaps

## Features

### 📊 Real-time Analysis
- **Keyword Miss Detection**: Identifies missing query keywords in retrieved chunks
- **Similarity-Relevance Gap**: Detects high-scoring results with low semantic relevance
- **Chunk Coverage**: Analyzes chunk size and distribution issues

### 🎯 Query Interface
- Clean, intuitive query input
- Configurable number of results (top-K)
- Real-time feedback on ingestion and queries

### 📈 Visualization
- Color-coded results and analysis
- Score visualization with gradient badges
- Issue categorization (observations vs. possible issues)
- Detailed breakdown of each analysis component

## API Endpoints

The FastAPI backend provides these endpoints:

### `POST /api/ingest`
Ingest documents into the vector store.

Request:
```json
{
  "documents": ["Document 1", "Document 2", ...]
}
```

Response:
```json
{
  "status": "success",
  "num_documents": 2,
  "num_chunks": 8,
  "message": "Ingested 2 documents into 8 chunks"
}
```

### `POST /api/query`
Query and analyze retrieval.

Request:
```json
{
  "query": "Your question here",
  "k": 5
}
```

Response:
```json
{
  "query": "Your question here",
  "num_results": 5,
  "results": [
    {
      "text": "Result text...",
      "score": 0.89,
      "metadata": {...}
    }
  ],
  "analysis": {
    "keyword_analysis": {...},
    "gap_analysis": {...},
    "coverage_analysis": {...},
    "observations": [...],
    "possible_issues": [...]
  }
}
```

### `GET /api/status`
Get system status.

Response:
```json
{
  "status": "ready",
  "num_documents": 2,
  "pipeline": "initialized"
}
```

### `GET /api/sample-data`
Get sample pharmaceutical documents for demo.

## Architecture

```
webapp/
├── app.py                 # FastAPI backend
├── static/
│   ├── index.html        # Frontend UI
│   ├── style.css         # Styling
│   └── script.js         # Client-side logic
└── README.md
```

## Frontend Components

### Document Management
- Sample data loader
- Custom document input
- Document ingestion with progress feedback

### Query Interface
- Real-time query input
- Configurable top-K parameter
- Status indicators

### Results Display
- Retrieved documents with scores
- Color-coded analysis results
- Expandable detailed analysis sections

### Analysis Visualization
- Keyword coverage breakdown
- Chunk statistics
- Gap analysis details
- Issue recommendations

## Styling

The portal uses a professional purple gradient theme with:
- Responsive design (works on mobile/tablet)
- Smooth animations and transitions
- Color-coded status indicators:
  - Blue: Information
  - Yellow: Loading
  - Green: Success
  - Red: Error/Issue

## Integration with Core Pipeline

The portal integrates directly with:
- `core.pipeline.RAGPipeline` - Document processing and retrieval
- `debugger.retrieval_debugger.RetrievalDebugger` - Analysis engine
- `debugger.heuristics` - Analysis heuristics

## Example Queries for Testing

Use the pharmaceutical sample data with these queries:

1. **"What are side effects of Aspirin?"**
   - Tests keyword miss detection (no "side effects" mention)
   - Shows embedding intent capture issues

2. **"How to take Aspirin safely?"**
   - Good query - should retrieve relevant results
   - Demonstrates healthy retrieval

3. **"Best painkiller for stomach?"**
   - Tests relevance gap detection
   - Shows terminology mismatch issues

## Advanced Usage

### Custom Embedding Provider

In `app.py`, change the embedding provider:

```python
_pipeline = RAGPipeline(
    embedding_provider="openai",  # or "sentence-transformers"
    collection_name="documents"
)
```

### Persistent Storage

Enable ChromaDB persistence:

```python
_pipeline = RAGPipeline(
    embedding_provider="sentence-transformers",
    persist_dir="./chroma_data"
)
```

## Performance Notes

- First query may take 2-3 seconds (model loading)
- Subsequent queries typically < 1 second
- Chunk embedding is done during ingestion, not query-time

## Troubleshooting

**Port already in use?**
```bash
python app.py --port 8001
```

**Import errors?**
```bash
pip install -r ../requirements.txt --upgrade
```

**Slow queries?**
- Reduce chunk size in `core/pipeline.py`
- Use OpenAI embeddings (faster but requires API key)

## Future Enhancements

- [ ] Multi-query comparison
- [ ] Query suggestion engine
- [ ] Document upload UI
- [ ] Export analysis reports as PDF
- [ ] Query performance metrics
- [ ] Advanced filtering options
- [ ] Integration with LLM for query rewriting
