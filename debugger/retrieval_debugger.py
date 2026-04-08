"""Retrieval Debugger - Analysis tool for RAG pipeline behavior."""

from typing import List, Dict, Any
from debugger.heuristics import perform_retrieval_analysis


class RetrievalDebugger:
    """Analyze and debug RAG retrieval behavior."""
    
    def __init__(self, pipeline):
        """
        Initialize debugger.
        
        Args:
            pipeline: RAGPipeline instance
        """
        self.pipeline = pipeline
    
    def debug_query(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Debug a single query retrieval.
        
        Args:
            query: Query to debug
            k: Number of results to retrieve
        
        Returns:
            Comprehensive debug report
        """
        # Run retrieval
        results = self.pipeline.retrieve(query, k=k)
        
        # Run analysis heuristics
        analysis = perform_retrieval_analysis(query, results)
        
        return {
            "query": query,
            "num_results": len(results),
            "results": results,
            "analysis": analysis
        }
    
    def format_debug_output(self, debug_report: Dict) -> str:
        """
        Format debug report for human-readable display.
        
        Args:
            debug_report: Output from debug_query()
        
        Returns:
            Formatted string output
        """
        output = []
        query = debug_report['query']
        results = debug_report['results']
        analysis = debug_report['analysis']
        
        # Header
        output.append("\n" + "="*80)
        output.append(f"RETRIEVAL DEBUG REPORT")
        output.append("="*80)
        output.append(f"\nQuery: \"{query}\"")
        output.append(f"Retrieved {len(results)} results\n")
        
        # Results
        output.append("-" * 80)
        output.append("TOP K RESULTS:")
        output.append("-" * 80)
        
        for i, result in enumerate(results, 1):
            score = result['score']
            text = result['text']
            output.append(f"\n[{i}] Score: {score:.2f}")
            # Truncate long text
            if len(text) > 150:
                output.append(f"Text: {text[:150]}...")
            else:
                output.append(f"Text: {text}")
        
        # Observations
        output.append("\n" + "-" * 80)
        output.append("⚠️  OBSERVATIONS:")
        output.append("-" * 80)
        
        if analysis['observations']:
            for obs in analysis['observations']:
                output.append(f"  {obs}")
        else:
            output.append("  ✓ No significant issues detected")
        
        # Possible Issues
        output.append("\n💡 POSSIBLE ISSUES:")
        output.append("-" * 80)
        
        if analysis['possible_issues']:
            for issue in analysis['possible_issues']:
                output.append(f"  • {issue}")
        else:
            output.append("  ✓ Retrieval appears healthy")
        
        # Detailed Recommendations
        output.append("\n🔍 DETAILED ANALYSIS:")
        output.append("-" * 80)
        
        keyword_analysis = analysis['keyword_analysis']
        if keyword_analysis['missed_keywords']:
            output.append(f"\nKeyword Coverage:")
            for kw_info in keyword_analysis['missed_keywords']:
                output.append(f"  • '{kw_info['keyword']}': found in {kw_info['chunks_containing']}/{kw_info['total_chunks']} chunks")
        
        coverage = analysis['coverage_analysis']
        output.append(f"\nChunk Statistics:")
        output.append(f"  • Average chunk length: {coverage['avg_chunk_length']:.0f} chars")
        output.append(f"  • Query length: {coverage['query_length']} chars")
        if coverage['issues']:
            output.append(f"  • Issues: {coverage['issues'][0]}")
        
        output.append("\n" + "="*80 + "\n")
        
        return "\n".join(output)
