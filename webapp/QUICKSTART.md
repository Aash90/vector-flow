# 🚀 Vector-Flow Web Portal - Getting Started

A modern, interactive portal to visualize and debug RAG retrieval behavior.

## ⚡ Quick Start (2 minutes)

### 1. Install & Run
```bash
cd webapp
pip install -r ../requirements.txt
python app.py
```

### 2. Open Portal
Visit: **http://localhost:8000**

### 3. Try It Out
- Click **"Load Sample Docs"**
- Click **"Ingest Documents"**
- Enter: `"What are side effects of Aspirin?"`
- Click **"Run Query & Analyze"**
- View the debug analysis

Done! You're now debugging RAG retrieval. 🎉

---

## 🎯 What You'll See

### Query Results
```
[1] Score: 0.89
Text: "Dosage guidelines for Aspirin..."

[2] Score: 0.87  
Text: "History of Aspirin..."
```

### Analysis
```
⚠️ Observations:
  • No chunk contains "side effects"

💡 Possible Issues:
  • Embedding not capturing intent
  • Documents using different terminology

🔍 Detailed Analysis:
  Keyword Coverage: 'side' found in 0/4 chunks
  Chunk Stats: Avg 287 chars per chunk
```

---

## 📁 Portal Structure

```
webapp/
├── app.py              # FastAPI backend
├── start.sh            # Launch script
├── check.py            # Dependency checker
├── static/
│   ├── index.html      # Web UI
│   ├── style.css       # Styling (purple gradient)
│   └── script.js       # Client logic
├── README.md           # Full documentation
├── PORTAL.md           # Architecture guide
└── QUICKSTART.md       # This file
```

---

## 🔧 Core Features

### Document Ingestion
- Load sample pharmaceutical docs
- Paste custom documents
- Automatic chunking & embedding
- ChromaDB vector storage

### Query Analysis
- Real-time retrieval
- Configurable Top-K results
- 3 analysis heuristics:
  1. **Keyword Miss Detection** - Missing query terms
  2. **Similarity-Relevance Gap** - High scores, low relevance  
  3. **Chunk Coverage** - Chunking strategy issues

### Beautiful Results
- Color-coded analysis (🔵 info, 🟡 loading, 🟢 success, 🔴 error)
- Score visualization with gradients
- Expandable analysis sections
- Mobile-responsive design

---

## 🧪 Test Queries (with Sample Data)

Try these to understand analysis:

| Query | Expected Issue | Learning |
|-------|--|--|
| "What are side effects?" | Keyword miss | Shows why embedding doesn't catch semantic intent |
| "How to take Aspirin?" | None | Healthy retrieval - exact match |
| "Best painkiller for stomach?" | Relevance gap | Shows terminology mismatch |

---

## 🚀 Running Options

### Option 1: Quick Start Script
```bash
./start.sh
```
Auto-installs dependencies and launches.

### Option 2: Direct Python
```bash
python app.py
```

### Option 3: Custom Port
```bash
python app.py --port 8001
```

### Option 4: Check Dependencies First
```bash
python check.py
```
Then `python app.py`

---

## 🛠️ API Endpoints

### Ingest Documents
```bash
POST /api/ingest
Content-Type: application/json

{
  "documents": ["Doc 1", "Doc 2", ...]
}
```

### Query & Analyze
```bash
POST /api/query
Content-Type: application/json

{
  "query": "Your question",
  "k": 5
}
```

Response includes:
- Retrieved documents with scores
- Keyword analysis
- Gap detection
- Coverage statistics
- Observations & possible issues

### Get Sample Data
```bash
GET /api/sample-data
```

### System Status
```bash
GET /api/status
```

---

## 🎨 UI Walkthrough

### Left Panel: Documents & Query
1. **Step 1: Ingest**
   - Load sample docs or paste custom
   - Click "Ingest Documents"
   - Wait for success message

2. **Step 2: Query**
   - Enter your search query
   - Adjust Top K if needed
   - Click "Run Query & Analyze"

### Right Panel: Results & Analysis
1. **Top K Results**
   - Ranked by similarity score
   - Full text preview

2. **⚠️ Observations**
   - Issues auto-detected
   - Color-coded warnings

3. **💡 Possible Issues**  
   - Root cause analysis
   - Actionable suggestions

4. **🔍 Detailed Analysis**
   - Keyword coverage breakdown
   - Chunk statistics
   - Similarity-relevance gaps

---

## ⚙️ Configuration

### Use Different Embeddings

In `app.py`, change:
```python
_pipeline = RAGPipeline(
    embedding_provider="sentence-transformers"  # or "openai"
)
```

### Persist Data

Add to `app.py`:
```python
_pipeline = RAGPipeline(
    persist_dir="./chroma_data"
)
```

### Adjust Chunk Size

Edit `core/pipeline.py`:
```python
self.chunk_size = 256  # Increase for bigger chunks
self.chunk_overlap = 50  # Overlap for context
```

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
python app.py --port 8001
```

### "Module not found"
```bash
pip install -r ../requirements.txt --upgrade
```

### "Slow first query"
Normal! Model loads on first query (~2-3 sec).
Use OpenAI embeddings for faster loads.

### "No results returned"
- ✓ Documents are ingested?
- ✓ Query is not empty?
- ✓ Try shorter queries first

---

## 📚 Integration with CLI

The portal uses the **same** components as `run_debugger.py`:
- Same RAG pipeline
- Same vector store (ChromaDB)  
- Same analysis heuristics
- Same embedding service

So insights from CLI also apply to portal!

---

## 🔮 Future Enhancements

- [ ] Multi-query comparison
- [ ] Document Upload UI
- [ ] Export Analysis (PDF/CSV)
- [ ] Query performance metrics
- [ ] LLM-powered suggestions
- [ ] Advanced filtering

---

## 📖 Learn More

- **Portal Architecture**: See [PORTAL.md](PORTAL.md)
- **Full Documentation**: See [README.md](README.md)
- **CLI Tool**: See [experiments/README.md](../experiments/README.md)
- **Core System**: See [top-level README](../README.md)

---

## 🎓 Next Steps

After exploring the portal:

1. **Try Custom Data**
   - Use your own documents
   - Test with real queries
   - Iterate on chunking

2. **Integrate Detection**
   - Use analysis to improve pipeline
   - Adjust chunk size if needed
   - Optimize embedding selection

3. **Production Deployment**
   - Add authentication
   - Set up persistent storage
   - Deploy with gunicorn
   - Add monitoring

---

## 💡 Pro Tips

- **Sample Docs First**: Load samples to understand the system
- **Short Queries**: Easier to debug than complex questions
- **Multiple Runs**: Same query may have different results (try again)
- **Keyword Focus**: Pay attention to keyword miss - often the issue
- **Score Interpretation**: Scores near 1.0 don't always mean relevant

---

**Happy Debugging! 🚀**

Questions? Check [PORTAL.md](PORTAL.md) or [README.md](README.md)
