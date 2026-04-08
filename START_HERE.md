# 🚀 Vector-Flow: Insight Layer Portal

**A web-based platform to visualize and debug Retrieval-Augmented Generation (RAG) systems**

## ⚡ Get Started in 2 Minutes

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Run
```bash
cd webapp
python app.py
```

### 3. Open
Visit: **http://localhost:8000**

### 4. Try
- Click "Load Sample Docs"
- Enter query: `"What are side effects?"`
- Click "Run Query & Analyze"
- See the magic ✨

---

## 🎯 What This Does

Visualizes **why** RAG retrieval works or fails with three analysis heuristics:

### 1. ⚠️ Keyword Miss Detection
Finds when important query words are missing from results.

### 2. 💡 Similarity-Relevance Gap  
Detects high-scoring results that aren't actually relevant.

### 3. 🔍 Chunk Coverage Analysis
Identifies if chunking strategy needs adjustment.

---

## 📚 Documentation

| Document | Purpose |
|---|---|
| [PORTAL_SUMMARY.md](PORTAL_SUMMARY.md) | Complete overview & architecture |
| [webapp/QUICKSTART.md](webapp/QUICKSTART.md) | 5-minute setup guide |
| [webapp/README.md](webapp/README.md) | Full portal documentation |
| [webapp/PORTAL.md](webapp/PORTAL.md) | Technical architecture |
| [experiments/README.md](experiments/README.md) | CLI tool documentation |

---

## 🏗️ Project Structure

```
vector-flow/
├── webapp/              ← 🌐 WEB PORTAL (START HERE!)
│   ├── app.py          ← FastAPI backend
│   ├── static/         ← HTML/CSS/JS frontend
│   ├── QUICKSTART.md   ← 2-minute setup
│   └── README.md       ← Full docs
│
├── core/               ← 🔧 RAG Pipeline
│   ├── pipeline.py     ← Main orchestrator
│   ├── embeddings.py   ← Text→Vector
│   ├── chunking.py     ← Document splitting
│   └── retriever.py    ← ChromaDB storage
│
├── debugger/           ← 🔍 Analysis Engine
│   ├── heuristics.py   ← 3 analysis functions
│   └── retrieval_debugger.py ← Orchestrator
│
└── experiments/        ← 🧪 CLI Demo
    └── run_debugger.py ← Command-line tool
```

---

## 🚀 Quick Commands

```bash
# Port 8000 in use? Try 8001
python webapp/app.py --port 8001

# Check dependencies first
python webapp/check.py

# Use the startup script
cd webapp && ./start.sh

# Run CLI version  
cd experiments && python run_debugger.py
```

---

## 🎓 Features

✅ **Beautiful Web UI**
- Professional design with purple gradient
- Real-time query analysis
- Color-coded results

✅ **Advanced Analysis**
- 3 retrieval heuristics
- Root cause detection
- Actionable insights

✅ **Easy Integration**
- RESTful API
- Sample data included
- Decorator patterns

✅ **Production Ready**
- FastAPI backend
- Error handling
- Request validation

---

## 🧪 Test it Out

Sample query to understand the analysis:

```
Load: Pharmaceutical documents
Query: "What are side effects of Aspirin?"

Result: Keyword miss detection
Reason: No "side effects" in retrieval results
Issue: Embedding didn't capture intent
Solution: Adjust chunking or improve docs
```

---

## 🎯 Next Steps

1. **Try the portal** → 2 min setup above
2. **Load sample data** → Click button in UI
3. **Run test queries** → See analysis
4. **Review insights** → Understand what's detected
5. **Iterate** → Improve your RAG system

---

## 📖 Learning Path

- Beginner: [webapp/QUICKSTART.md](webapp/QUICKSTART.md)
- Intermediate: [webapp/README.md](webapp/README.md)  
- Advanced: [PORTAL_SUMMARY.md](PORTAL_SUMMARY.md)
- Technical: [webapp/PORTAL.md](webapp/PORTAL.md)

---

## 💡 Key Innovation

The portal's superpower is **explanation**, not just results:

```
❌ Traditional: "Here are 5 results"
✅ Vector-Flow: "Here are 5 results AND why they might fail"
```

We tell you:
- What's wrong (keyword miss? gap? coverage?)
- Why it's wrong (root cause analysis)
- How to improve (actionable suggestions)

---

## 🚀 Ready?

```bash
cd webapp
python app.py
# Open http://localhost:8000
```

**That's it! You're debugging RAG systems now.** 🎉

---

## 📞 Need Help?

1. **Quick Start**: See [webapp/QUICKSTART.md](webapp/QUICKSTART.md)
2. **Full Docs**: See [webapp/README.md](webapp/README.md)
3. **Architecture**: See [PORTAL_SUMMARY.md](PORTAL_SUMMARY.md)
4. **Issues**: Check error messages in browser console

---

**Happy debugging! 🚀**

Made with ❤️ for better RAG systems.
