"""
Minimal RAG System Demo with Retrieval Debugger

This script demonstrates:
1. Basic RAG pipeline (Chunk → Embed → Store → Retrieve)
2. Debug analysis of retrieval behavior
3. Our core innovation: Understanding why retrieval fails
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import RAGPipeline
from debugger.retrieval_debugger import RetrievalDebugger


# Sample pharmaceutical documents for testing
SAMPLE_DOCUMENTS = [
    """
    Aspirin Medication Guide
    Active ingredient: Acetylsalicylic acid
    Dosage: 500mg tablets
    Dosage guidelines for Aspirin: Take 1-2 tablets every 4-6 hours as needed for pain relief.
    Do not exceed 8 tablets in 24 hours. Take with food to avoid stomach upset.
    Warnings: May cause stomach irritation and bleeding if used long-term.
    """,
    
    """
    History of Aspirin
    Aspirin was first synthesized in 1897 by German chemist Felix Hoffmann at Bayer.
    It was originally derived from willow bark, used for centuries in traditional medicine.
    The drug was approved by the FDA in 1939 and has been one of the most widely used medications.
    Over 100 years of use and safety data make it one of the most studied drugs.
    """,
    
    """
    Common Pain Relievers Comparison
    Aspirin: Good for inflammation, used for heart attack prevention
    Ibuprofen: Better pain relief, anti-inflammatory properties
    Acetaminophen: Gentle on stomach, no anti-inflammatory effects
    Naproxen: Long-acting, good for arthritis pain
    All pain relievers carry some risks when overused.
    """,
    
    """
    Cardiovascular Benefits of Aspirin
    Low-dose Aspirin (81mg daily) recommended for heart disease prevention.
    Thins blood by inhibiting platelet aggregation.
    Particularly useful after heart attack or stroke.
    Studies show 20-30% reduction in cardiovascular events with regular use.
    Consultation with doctor required before starting regimen.
    """,
]


def main():
    """Run the debugger demonstration."""
    
    print("\n" + "="*80)
    print("MINIMAL RAG SYSTEM WITH RETRIEVAL DEBUGGER")
    print("="*80)
    
    # Step 1: Initialize pipeline
    print("\n[1/3] Initializing RAG Pipeline...")
    try:
        pipeline = RAGPipeline(
            embedding_provider="sentence-transformers",
            collection_name="pharma_docs"
        )
        print("✓ Pipeline initialized with sentence-transformers")
    except Exception as e:
        print(f"✗ Error initializing pipeline: {e}")
        return
    
    # Step 2: Ingest documents
    print("\n[2/3] Ingesting sample documents...")
    try:
        num_chunks = pipeline.ingest_documents(SAMPLE_DOCUMENTS, clear_first=True)
        print(f"✓ Ingested {len(SAMPLE_DOCUMENTS)} documents into {num_chunks} chunks")
    except Exception as e:
        print(f"✗ Error ingesting documents: {e}")
        return
    
    # Step 3: Run retrieval with debug analysis
    print("\n[3/3] Running retrieval with debug analysis...")
    
    try:
        debugger = RetrievalDebugger(pipeline)
        
        # Test queries that showcase different issues
        test_queries = [
            "What are side effects of Aspirin?",  # Missing keywords issue
            "How to take Aspirin?",  # Straightforward query
            "Best painkiller for stomach problems?",  # Relevance gap potential
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'─'*80}")
            print(f"TEST QUERY {i}/{len(test_queries)}")
            print(f"{'─'*80}")
            
            # Run debug
            debug_report = debugger.debug_query(query, k=4)
            
            # Print formatted output
            formatted_output = debugger.format_debug_output(debug_report)
            print(formatted_output)
            
    except Exception as e:
        print(f"✗ Error during retrieval: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n✓ Demo completed successfully!")
    print("This demonstrates our core innovation:")
    print("  • Identifying when retrieval fails")
    print("  • Understanding WHY it fails (keyword miss, relevance gap, chunk coverage)")
    print("  • Providing actionable insights for improvement")
    print()


if __name__ == "__main__":
    main()
