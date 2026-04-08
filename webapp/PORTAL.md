"""
Vector-Flow: Insight Layer Portal - Complete Documentation

This is the entry point for understanding the full portal system.
"""

# PORTAL ARCHITECTURE

The portal visualizes the core Insight Layer through an interactive web interface.

## Components Overview

### 1. Backend (FastAPI)
**File**: `webapp/app.py`

Provides REST API endpoints:
- `/api/ingest` - Accept documents and ingest into vector store
- `/api/query` - Process queries and return debug analysis
- `/api/status` - System health check
- `/api/sample-data` - Get sample pharmaceutical documents

### 2. Frontend (HTML/CSS/JavaScript)
**Files**: 
- `webapp/static/index.html` - UI structure
- `webapp/static/style.css` - Professional styling
- `webapp/static/script.js` - Client-side logic

Features:
- Document ingestion interface
- Query input with top-K configuration
- Real-time results display
- Interactive analysis visualization

### 3. Core Integration
Connects to:
- `core/pipeline.py` - RAG pipeline orchestration
- `debugger/retrieval_debugger.py` - Analysis engine
- `debugger/heuristics.py` - Analysis heuristics

## User Workflow

```
1. User opens portal
   ↓
2. Load or paste documents
   ↓
3. Click "Ingest Documents"
   ↓ [Backend: Chunk → Embed → Store]
   ↓
4. Enter a query
   ↓
5. Click "Run Query & Analyze"
   ↓ [Backend: Retrieve → Analyze with heuristics]
   ↓
6. View analysis visualization
   - Top K results with scores
   - Observations (warnings/issues found)
   - Possible issues with explanations
   - Detailed analysis breakdown
```

## Analysis Insights Shown

### Keyword Miss Detection
When query keywords are absent from retrieved results:
```
Query: "What are side effects?"
   ↓
Results don't contain: "side", "effects"
   ↓
⚠️ Observation: "No chunk contains 'side effects'"
```

### Similarity-Relevance Gap
When results have high scores but lack relevance:
```
High score (0.85) but:
- No query keywords present
- Different terminology
- Out of context match
   ↓
💡 Issue: "Embedding not capturing intent"
```

### Chunk Coverage
When chunking strategy needs adjustment:
```
- 60% of chunks are too small (<50 chars)
- Documents may lack context
   ↓
💡 Recommendation: "Consider adjusting chunk_size parameter"
```

## Key Files

### Backend
- `webapp/app.py` - FastAPI server with 4 main endpoints
- `webapp/start.sh` - Startup script

### Frontend
- `webapp/static/index.html` - Main page with template definitions
- `webapp/static/style.css` - Gradient theme, responsive design
- `webapp/static/script.js` - API integration and DOM manipulation

### Configuration
- `requirements.txt` - Python dependencies (now includes fastapi, uvicorn)

## Running the Portal

```bash
# Option 1: Using startup script
./webapp/start.sh

# Option 2: Direct execution
cd webapp
python app.py

# Option 3: With custom port
python app.py --port 8001
```

Access at: http://localhost:8000

## Design Highlights

### 🎨 UI/UX
- Two-panel layout: Documents (left) | Analysis (right)
- Purple gradient theme reflecting innovation
- Color-coded status: Blue (info) | Yellow (loading) | Green (success) | Red (error)
- Responsive design works on mobile/tablet
- Smooth animations and transitions

### ⚡ Performance
- Client-side rendering for instant feedback
- Backend processes heavy lifting (embeddings, retrieval)
- Lazy loading of analysis components
- Efficient template cloning in JavaScript

### 🔒 API Design
- Simple, RESTful endpoints
- Request validation with Pydantic
- Proper error handling with detailed messages
- CORS-friendly for future integrations

## Sample Use Cases

### Case 1: Pharmaceutical Documentation
Load medical documents and debug queries like:
- "What are side effects?" → Reveals keyword miss issue
- "How to take Aspirin?" → Healthy retrieval
- "Best painkiller?" → Shows terminology gap

### Case 2: Technical Documentation  
Use API/system docs and test:
- Product-specific queries
- Multi-term searches
- Edge case queries

### Case 3: Customer Support
Debug FAQ and knowledge base:
- Common question retrieval
- Is the KB well-structured?
- Are there keyword gaps?

## Future Enhancements

1. **Query Analytics**
   - Track common query patterns
   - Identify recurring issues

2. **Document Management**
   - Upload files (PDF, TXT)
   - Edit/delete documents
   - Categorize documents

3. **Advanced Analysis**
   - Query rewriting suggestions
   - Multi-step retrieval strategies
   - LLM-powered explanations

4. **Performance Monitoring**
   - Query execution time
   - Cache hit rates
   - Model performance metrics

5. **Export & Reporting**
   - Download analysis reports
   - PDF generation
   - Comparison reports

## Integration Notes

The portal is fully integrated with the core system:

1. **Embeddings**: Uses same service as CLI debugger
2. **Vector Store**: Shared ChromaDB instance
3. **Analysis**: Identical heuristics as `run_debugger.py`
4. **API**: Can be called from other applications

## Troubleshooting

### Port 8000 already in use?
```bash
python webapp/app.py --port 8001
```

### Slow first query?
Normal - model loading takes 2-3 seconds. Use OpenAI embeddings for faster loads.

### Import errors?
```bash
pip install -r requirements.txt --upgrade
```

### No results?
1. Ensure documents are ingested first
2. Check query text is not empty
3. Try sample documents

## Testing the Portal

```bash
# Quick test with sample data
1. Open http://localhost:8000
2. Click "Load Sample Docs"
3. Click "Ingest Documents"
4. Enter query: "What are side effects of Aspirin?"
5. Click "Run Query & Analyze"
6. Review the analysis output
```

Expected for this query:
- Keyword miss detection for "side effects"
- Observations about missing terminology
- Suggestions for improvement
