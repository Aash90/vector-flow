# Vector-Flow

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![Built with ❤️](https://img.shields.io/badge/Built%20with-%E2%9D%A4%EF%B8%8F-red.svg)](#)

**Understanding why RAG systems fail — not just when they appear to work.**

> A debugging and observability layer for analyzing failure modes in RAG pipelines with an interactive web portal and CLI tools.

---

## ⚡ Features at a Glance

🌐 **Web Portal** - Modern, beautiful UI for interactive debugging  
🔍 **Root Cause Analysis** - Understand WHY retrieval fails  
📊 **Three Analysis Heuristics** - Keyword miss, relevance gap, chunk coverage  
🚀 **Zero Configuration** - Works out of the box with sample data  
📚 **Well Documented** - Multiple entry points for different use cases  
🔧 **Flexible Integration** - Web portal, CLI tool, Python API  

---

## ⚡ Quick Start (2 Minutes)

```bash
# Install
pip install -r requirements.txt

# Run web portal
cd webapp && python app.py

# Open browser
# http://localhost:8000
```

Then:
1. Click "Load Sample Docs"
2. Enter query: "What are side effects?"
3. See analysis with keyword miss detection and insights

**That's it!** 🎉

---

## ❗ Problem

RAG (Retrieval-Augmented Generation) systems often fail silently.

- Irrelevant chunks are retrieved despite high similarity scores
- Important context is missed due to chunking or embedding issues
- LLMs hallucinate when retrieval quality is low

Existing tools show *what* was retrieved.  
They don’t explain *why it failed*.

## 💡 Solution

Vector-Flow is a debugging and observability layer for RAG pipelines.

It helps analyze:

- How queries are embedded
- What chunks are retrieved and why
- Where retrieval breaks down
- How context impacts LLM outputs


## 🏗️ Architecture

![Vector-Flow Architecture](./architecture.png)

### Pipeline

Query → Embedding → Vector Search → Retrieved Chunks → LLM → Response

### Observability Layer (Vector-Flow)

Vector-Flow instruments each stage of the pipeline:

- **Embedding Stage**
  - Vector inspection
  - Embedding comparison across queries

- **Retrieval Stage**
  - Similarity score breakdown
  - Top-K analysis

- **Chunk Analysis**
  - Chunk relevance vs ranking
  - Missed relevant chunks

- **LLM Output**
  - Grounding vs hallucination detection


## 📌 Example: Retrieval Failure Analysis

**Query:**  
"What are the side effects of Drug X?"

**Top Retrieved Chunks:**
1. "Drug X dosage guidelines..." (Score: 0.89)
2. "History of Drug X development..." (Score: 0.87)
3. "Drug X interactions..." (Score: 0.85)

**Issue:**
- High similarity scores
- But missing the chunk containing actual side effects

**Diagnosis:**
- Embedding failed to capture intent ("side effects")
- Chunking diluted critical medical information

**Impact:**
- LLM generates incomplete or hallucinated answer

**Insight:**
High similarity does not guarantee task relevance

## 🔍 Debugging Scenarios

### 1. High similarity, low relevance
- Retrieved chunks have high cosine similarity
- But are semantically irrelevant

→ Indicates embedding limitations

---

### 2. Missing critical context
- Relevant chunks exist but are not retrieved

→ Indicates chunking or indexing issue

---

### 3. Hallucinated answers
- Retrieval quality is low
- Model fills gaps with parametric knowledge

→ Indicates weak grounding

## 🧠 Key Insights

- High cosine similarity ≠ semantic relevance
- Chunk size significantly impacts retrieval quality
- Embedding models behave differently across domains
- Retrieval failures are the root cause of most hallucinations

---

## 🌐 Web Portal - Interactive Insight Layer

Vector-Flow includes a modern web portal for visual debugging and analysis of RAG retrieval behavior.

### Portal Features

✨ **Beautiful, Interactive UI**
- Professional design with real-time analysis
- Purple gradient theme with responsive layout
- Color-coded results and insights (mobile/tablet/desktop friendly)

🔍 **Three Analysis Heuristics**
- **Keyword Miss Detection**: Identifies missing query keywords in retrieved results
- **Similarity-Relevance Gap**: Detects high-scoring results lacking semantic relevance
- **Chunk Coverage Analysis**: Identifies chunking strategy issues

📊 **Real-time Debugging**
- Load documents and run queries instantly
- View top-K results with similarity scores
- Get root cause analysis for retrieval failures
- Actionable insights for improvement

🧪 **Sample Data Included**
- Pre-loaded pharmaceutical dataset
- Test queries demonstrating all analysis types
- Learn by example

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the portal
cd webapp
python app.py

# 3. Open in browser
# http://localhost:8000
```

### Portal Usage

**Step 1: Ingest Documents**
```
Click "Load Sample Docs" → Click "Ingest Documents"
```

**Step 2: Query**
```
Enter query: "What are side effects of Aspirin?"
Click "Run Query & Analyze"
```

**Step 3: Review Analysis**
```
✓ Top K results with scores
✓ Observations (what went wrong)
✓ Possible issues (why it failed)
✓ Detailed analysis breakdown
```

### Example Analysis Output

```
Query: "What are side effects of Aspirin?"

[1] Score: 0.89
Text: "Dosage guidelines for Aspirin..."

[2] Score: 0.87
Text: "History of Aspirin..."

⚠️ Observations:
  • No chunk contains "side effects"
  • High similarity but missing key terms

💡 Possible Issues:
  • Embedding not capturing query intent
  • Documents using different terminology

🔍 Detailed Analysis:
  Keyword Coverage: 'side' found in 0/4 chunks
  Chunk Stats: Avg 287 chars per chunk
```

### Portal Architecture

**Backend**
- FastAPI for high-performance async web server
- ChromaDB vector storage
- Embedding service (sentence-transformers or OpenAI)

**Frontend**
- Modern HTML5/CSS3/JavaScript (vanilla, no frameworks)
- Real-time API integration
- Beautiful gradient UI with smooth animations

**API Endpoints**
```
POST /api/ingest         ← Ingest documents
POST /api/query          ← Query and analyze
GET  /api/status         ← System health
GET  /api/sample-data    ← Sample documents
GET  /static/*           ← Static files (CSS, JS)
```

### API Integration

**Python Client Example:**
```python
import requests

# Ingest documents
response = requests.post('http://localhost:8000/api/ingest', json={
    'documents': ['Doc 1', 'Doc 2', 'Doc 3']
})

# Query with analysis
response = requests.post('http://localhost:8000/api/query', json={
    'query': 'Your question here',
    'k': 5
})

# Get detailed analysis
analysis = response.json()['analysis']
print(analysis['observations'])
print(analysis['possible_issues'])
```

### Documentation

| Resource | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | 2-minute quick start |
| [webapp/QUICKSTART.md](webapp/QUICKSTART.md) | Detailed setup guide |
| [webapp/README.md](webapp/README.md) | Full portal documentation |
| [webapp/PORTAL.md](webapp/PORTAL.md) | Technical architecture |
| [PORTAL_SUMMARY.md](PORTAL_SUMMARY.md) | Complete overview |

---

## 🚀 Roadmap

**Completed ✅**
- [x] Core RAG pipeline (chunk → embed → store → retrieve)
- [x] Three analysis heuristics (keyword miss, gap, coverage)
- [x] CLI debugging tool (run_debugger.py)
- [x] Web portal with beautiful UI
- [x] REST API for integration
- [x] Sample data & documentation

**Planned**
- [ ] Advanced heuristics (semantic scoring, LLM evaluation)
- [ ] Query rewriting suggestions
- [ ] Multi-step retrieval strategies
- [ ] Performance metrics dashboard
- [ ] Document upload interface
- [ ] Export analysis reports (PDF/CSV)
- [ ] User authentication & teams
- [ ] Cloud deployment templates

---

## 🛠️ Tools & Components

### CLI Tool (Command-line Debugger)
Located in `experiments/run_debugger.py`

```bash
cd experiments
python run_debugger.py
```

Demonstrates the full pipeline with:
- Sample pharmaceutical dataset
- Multiple test queries
- Console-based analysis output
- Good for batch processing and automation

### Web Portal (Interactive Debugger)
Located in `webapp/`

```bash
cd webapp
python app.py
# Open http://localhost:8000
```

Features:
- Real-time web interface
- Interactive query testing
- Beautiful result visualization
- Perfect for exploration and learning

### Core System
Located in `core/` and `debugger/`

Reusable components:
- `RAGPipeline` - Main orchestrator
- `EmbeddingsService` - Text→Vector conversion
- `VectorStore` - ChromaDB wrapper
- `RetrievalDebugger` - Analysis engine
- Analysis heuristics

---

## 📦 Project Structure

```
vector-flow/
├── core/                       # RAG Pipeline Components
│   ├── pipeline.py            # Main orchestrator
│   ├── embeddings.py          # Embedding service
│   ├── retriever.py           # Vector store (ChromaDB)
│   └── chunking.py            # Document chunking
│
├── debugger/                   # Analysis & Insight Layer
│   ├── heuristics.py          # 3 analysis functions
│   └── retrieval_debugger.py  # Analysis orchestrator
│
├── webapp/                     # 🌐 WEB PORTAL (NEW!)
│   ├── app.py                 # FastAPI backend
│   ├── static/                # HTML/CSS/JS frontend
│   ├── README.md              # Portal documentation
│   ├── QUICKSTART.md          # Quick setup
│   └── PORTAL.md              # Technical guide
│
├── experiments/               # Demos & Examples
│   ├── run_debugger.py        # CLI tool
│   └── README.md              # CLI documentation
│
├── START_HERE.md              # 👉 Start here! (2 min setup)
├── PORTAL_SUMMARY.md          # Portal overview
└── requirements.txt           # Python dependencies
```

---

## 🎯 Typical Workflow

### Option 1: Web Portal (Visual Debugging)
```
1. pip install -r requirements.txt
2. cd webapp && python app.py
3. Open http://localhost:8000
4. Click "Load Sample Docs"
5. Enter queries and explore analysis
```

### Option 2: CLI Tool (Batch Processing)
```
1. pip install -r requirements.txt
2. cd experiments
3. python run_debugger.py
4. See analysis of multiple queries
```

### Option 3: Python API (Programmatic Access)
```python
from core.pipeline import RAGPipeline
from debugger.retrieval_debugger import RetrievalDebugger

pipeline = RAGPipeline()
pipeline.ingest_documents(['Doc1', 'Doc2'])

debugger = RetrievalDebugger(pipeline)
report = debugger.debug_query("Your question")
print(debugger.format_debug_output(report))
```

---

## 💻 System Requirements

- Python 3.8+
- pip (Python package manager)
- 500MB+ disk space (for ML models)
- 2GB+ RAM recommended

### Dependencies

```
# Core
chromadb>=0.3.21              # Vector database
sentence-transformers>=2.2.0  # Embeddings
openai>=1.0.0                 # Optional: LLM

# Web Portal
fastapi>=0.95.0               # Web framework
uvicorn>=0.21.0               # ASGI server
pydantic>=1.10.0              # Data validation
```

---

## 🧪 Quick Test

```bash
# 1. Install & setup
pip install -r requirements.txt

# 2. Run web portal
cd webapp && python app.py

# 3. Test in browser
# - Open http://localhost:8000
# - Click "Load Sample Docs" 
# - Query: "What are side effects?"
# - See keyword miss detection in action!
```

---

## 📖 Documentation

**Entry Points:**
- **[START_HERE.md](START_HERE.md)** - Quick 2-minute start
- **[PORTAL_SUMMARY.md](PORTAL_SUMMARY.md)** - Complete overview
- **[webapp/](webapp/)** - Web portal docs & guides
- **[experiments/](experiments/)** - CLI tool docs

**Deep Dives:**
- [webapp/QUICKSTART.md](webapp/QUICKSTART.md) - Portal setup
- [webapp/README.md](webapp/README.md) - Full portal guide
- [webapp/PORTAL.md](webapp/PORTAL.md) - Technical architecture
- [experiments/README.md](experiments/README.md) - CLI guide

---

## 🎯 Why Vector-Flow?

### The Problem With Existing Solutions

❌ **Traditional RAG Debugging:**
- Shows what was retrieved
- Returns results ranked by score
- Stops there

❌ **The Reality:**
- High similarity scores don't mean relevance
- You have no idea WHY retrieval failed
- Debugging requires deep diving into code

✅ **Vector-Flow Approach:**
- Shows what was retrieved AND why
- Analyzes root causes of failures
- Provides actionable insights
- Beautiful interactive interface

### Our Competitive Advantages

**🔍 Root Cause Analysis**
- Don't just know retrieval failed—understand WHY
- Three complementary heuristics catch different failure modes
- Actionable recommendations for fixing issues

**📊 Visual Debugging**
- Modern web portal with real-time analysis
- Beautiful, intuitive interface
- No terminal/command-line required
- Works on any device (mobile/tablet/desktop)

**🚀 Easy to Use**
- 2-minute setup
- Sample data included
- No configuration needed
- Try it immediately

**🔧 Flexible Integration**
- Use as web portal
- Use as CLI tool
- Use as Python library
- Deploy to cloud
- REST API for third-party integration

**📚 Well Documented**
- Multiple entry points for different use cases
- Comprehensive guides and examples
- Clear architecture documentation
- Active community support

---

## 📋 Use Cases

### 1. **Business Intelligence & Search**
Debug why important documents are being missed in search results.

### 2. **Customer Support**
Analyze why FAQ search isn't finding relevant answers for support teams.

### 3. **Legal/Compliance**
Ensure critical legal documents are being retrieved for contract analysis.

### 4. **Medical/Healthcare**
Verify retrieval accuracy for medical knowledge retrieval systems.

### 5. **Technical Documentation**
Optimize API documentation retrieval for developer support.

### 6. **E-commerce**
Debug product search and recommendation retrieval quality.

### 7. **Academic Research**
Analyze paper retrieval systems for literature reviews.

### 8. **Production Monitoring**
Monitor RAG system health and detect degradation early.

---

## 🔗 Integration Examples

### As FastAPI Dependency
```python
from fastapi import Depends
from core.pipeline import RAGPipeline

def get_pipeline():
    return RAGPipeline()

@app.get("/search")
async def search(query: str, pipeline = Depends(get_pipeline)):
    results = pipeline.retrieve(query)
    return results
```

### With LangChain
```python
from core.pipeline import RAGPipeline
from langchain.chains import RetrievalQA

pipeline = RAGPipeline()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=pipeline.vector_store,
    chain_type="stuff"
)
```

### With LlamaIndex
```python
from core.pipeline import RAGPipeline
from llama_index.indices.vector_store import VectorStoreIndex

pipeline = RAGPipeline()
index = VectorStoreIndex(vector_store=pipeline.vector_store)
query_engine = index.as_query_engine()
```

---

## 🌟 Key Features at a Glance

| Feature | CLI | Web Portal | Python API |
|---------|-----|-----------|-----------|
| Batch Processing | ✅ | ❌ | ✅ |
| Interactive Debugging | ❌ | ✅ | ✅ |
| Web UI | ❌ | ✅ | ❌ |
| Beautiful Visualization | ❌ | ✅ | ❌ |
| Custom Integration | ❌ | ❌ | ✅ |
| Zero Configuration | ✅ | ✅ | ❌ |
| REST API | ❌ | ✅ | ❌ |

---

## 🚢 Deployment

### Local Development
```bash
cd webapp && python app.py
```

### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "webapp/app.py"]
```

### Cloud Platforms
- **Heroku**: Deploy directly with Procfile
- **AWS Lambda**: Container or function deployment
- **Google Cloud Run**: Containerized
- **Azure App Service**: Python runtime

---

## 💡 Tips & Best Practices

### Query Selection
- Use diverse queries to test different scenarios
- Include edge cases and ambiguous queries
- Test both simple and complex questions

### Document Preparation
- Use consistent formatting
- Include metadata where relevant
- Avoid very short or very long documents
- Test with real-world data

### Chunk Optimization
- Start with default size (256 chars)
- Adjust based on your domain
- Monitor keyword coverage in analysis
- Iterate based on insights

### Embedding Selection
- Use sentence-transformers for free, fast results
- Use OpenAI for better semantic understanding
- Test across different domains
- Compare results between models

---

## 🤝 Contributing & Community

We welcome contributions! Areas for help:

- 🐛 Bug reports and fixes
- ✨ New analysis heuristics
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 📦 Integration examples

### Development Setup
```bash
git clone https://github.com/Aash90/vector-flow.git
cd vector-flow
pip install -r requirements.txt
# Make changes and test
python experiments/run_debugger.py
cd webapp && python app.py
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

This project builds on excellent open-source libraries:
- **ChromaDB** - Vector storage
- **sentence-transformers** - Embeddings
- **FastAPI** - Web framework
- **Pydantic** - Data validation

---

## 📞 Support & Feedback

- 📖 **Documentation**: Check [START_HERE.md](START_HERE.md)
- 💬 **Questions**: Open an issue or discussion
- 🐛 **Bugs**: Report with reproducible example
- 💡 **Ideas**: Share your use cases!

---

**Made with ❤️ to make RAG systems more understandable and debuggable.**

*Vector-Flow: Understanding why RAG systems fail* 🚀

---