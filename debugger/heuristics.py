"""Heuristics for retrieval analysis and debugging."""

from typing import List, Dict, Set
import re


def detect_keyword_miss(query: str, retrieved_texts: List[str], threshold: float = 0.5) -> Dict:
    """
    Detect if important query keywords are missing from retrieved chunks.
    
    Args:
        query: Original query
        retrieved_texts: List of retrieved document texts
        threshold: Percentage of chunks (0-1) that must contain keyword for it to not be "missed"
    
    Returns:
        Dict with missed keywords and analysis
    """
    # Extract keywords (simple: words > 3 chars, excluding common words)
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'with', 'has', 'have', 'this', 'that'}
    keywords = set()
    
    for word in re.findall(r'\b\w+\b', query.lower()):
        if len(word) > 3 and word not in stop_words:
            keywords.add(word)
    
    if not keywords:
        return {"missed_keywords": [], "analysis": "No significant keywords found in query"}
    
    # Check which keywords appear in retrieved texts
    missed = []
    for keyword in keywords:
        count = sum(1 for text in retrieved_texts if keyword.lower() in text.lower())
        coverage = count / len(retrieved_texts) if retrieved_texts else 0
        
        if coverage < threshold:
            missed.append({
                "keyword": keyword,
                "coverage": coverage,
                "chunks_containing": count,
                "total_chunks": len(retrieved_texts)
            })
    
    return {
        "missed_keywords": missed,
        "total_keywords": len(keywords),
        "analysis": f"Found {len(missed)} keywords with low coverage (<{int(threshold*100)}%)"
    }


def detect_similarity_relevance_gap(retrieved_results: List[Dict], 
                                    query_keywords: Set[str] = None,
                                    score_threshold: float = 0.75) -> Dict:
    """
    Detect gap between high similarity scores and low semantic relevance.
    
    Args:
        retrieved_results: List of result dicts with score and text
        query_keywords: Optional set of keywords expected in relevant results
        score_threshold: Minimum score to consider "high similarity"
    
    Returns:
        Dict with gap analysis
    """
    gaps = []
    
    for i, result in enumerate(retrieved_results):
        score = result.get('score', 0)
        text = result.get('text', '')
        
        # High score but no query keywords
        if score >= score_threshold and query_keywords:
            found_keywords = sum(1 for kw in query_keywords if kw.lower() in text.lower())
            
            if found_keywords == 0:
                gaps.append({
                    "rank": i + 1,
                    "score": score,
                    "text_preview": text[:80] + "..." if len(text) > 80 else text,
                    "issue": "High similarity but no query keywords detected"
                })
    
    return {
        "gaps": gaps,
        "analysis": f"Detected {len(gaps)} high-scoring results with potential relevance gaps"
    }


def detect_chunk_coverage_issue(query: str, retrieved_texts: List[str]) -> Dict:
    """
    Detect if chunks are too broad or narrow (chunk coverage issues).
    
    Args:
        query: Original query
        retrieved_texts: Retrieved chunk texts
    
    Returns:
        Dict with coverage analysis
    """
    if not retrieved_texts:
        return {"issue": "No chunks retrieved", "avg_chunk_length": 0}
    
    avg_length = sum(len(t) for t in retrieved_texts) / len(retrieved_texts)
    query_length = len(query)
    
    issues = []
    
    # Chunks too small (< 50 chars) might lack context
    small_chunks = sum(1 for t in retrieved_texts if len(t) < 50)
    if small_chunks / len(retrieved_texts) > 0.5:
        issues.append("Over 50% of chunks are very small (<50 chars) - may lack context")
    
    # Chunks too large (> 500 chars) might be too broad
    large_chunks = sum(1 for t in retrieved_texts if len(t) > 500)
    if large_chunks / len(retrieved_texts) > 0.5:
        issues.append("Over 50% of chunks are very large (>500 chars) - may contain noise")
    
    return {
        "avg_chunk_length": avg_length,
        "query_length": query_length,
        "small_chunks": small_chunks,
        "large_chunks": large_chunks,
        "issues": issues,
        "recommendation": "Consider adjusting chunk_size parameter" if issues else "Chunk size looks reasonable"
    }


def perform_retrieval_analysis(query: str, 
                               retrieved_results: List[Dict]) -> Dict:
    """
    Comprehensive retrieval analysis combining all heuristics.
    
    Args:
        query: Original query
        retrieved_results: List of retrieval results
    
    Returns:
        Comprehensive analysis dict
    """
    texts = [r.get('text', '') for r in retrieved_results]
    
    # Extract query keywords
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'with', 'has', 'have', 'this', 'that'}
    keywords = set()
    for word in re.findall(r'\b\w+\b', query.lower()):
        if len(word) > 3 and word not in stop_words:
            keywords.add(word)
    
    # Run all heuristics
    keyword_analysis = detect_keyword_miss(query, texts)
    gap_analysis = detect_similarity_relevance_gap(retrieved_results, keywords)
    coverage_analysis = detect_chunk_coverage_issue(query, texts)
    
    # Aggregate observations
    observations = []
    if keyword_analysis['missed_keywords']:
        observations.append(f"⚠️  {len(keyword_analysis['missed_keywords'])} keywords have low coverage in results")
    if gap_analysis['gaps']:
        observations.append(f"⚠️  {len(gap_analysis['gaps'])} high-scoring results may have relevance gaps")
    if coverage_analysis['issues']:
        observations.append(f"⚠️  Chunk coverage issue: {coverage_analysis['issues'][0]}")
    
    # Possible issues
    possible_issues = []
    if keyword_analysis['missed_keywords']:
        possible_issues.append("Embedding not capturing query intent or important keywords")
    if gap_analysis['gaps']:
        possible_issues.append("Documents may be using different terminology than the query")
    if coverage_analysis['issues']:
        possible_issues.append("Chunking strategy needs adjustment")
    
    return {
        "keyword_analysis": keyword_analysis,
        "gap_analysis": gap_analysis,
        "coverage_analysis": coverage_analysis,
        "observations": observations,
        "possible_issues": possible_issues
    }
