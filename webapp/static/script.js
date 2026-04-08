/**
 * Vector-Flow Insight Layer Portal - Frontend Logic
 */

const API_URL = '/api';

// DOM Elements
const loadSampleBtn = document.getElementById('loadSampleBtn');
const loadCustomBtn = document.getElementById('loadCustomBtn');
const docsInput = document.getElementById('docsInput');
const ingestBtn = document.getElementById('ingestBtn');
const ingestStatus = document.getElementById('ingestStatus');

const queryInput = document.getElementById('queryInput');
const kInput = document.getElementById('kInput');
const queryBtn = document.getElementById('queryBtn');
const queryStatus = document.getElementById('queryStatus');

const resultsContainer = document.getElementById('resultsContainer');
const resultsTemplate = document.getElementById('resultsTemplate');
const resultItemTemplate = document.getElementById('resultItemTemplate');

// State
let documentsIngested = false;

/**
 * Initialize event listeners
 */
function initEventListeners() {
    loadSampleBtn.addEventListener('click', loadSampleDocuments);
    loadCustomBtn.addEventListener('click', () => {
        docsInput.focus();
    });
    ingestBtn.addEventListener('click', ingestDocuments);
    queryBtn.addEventListener('click', queryAndAnalyze);
    
    // Allow Enter key to submit query
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            queryAndAnalyze();
        }
    });
}

/**
 * Show status message
 */
function showStatus(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `status-message status-${type}`;
}

/**
 * Load sample pharmaceutical documents
 */
async function loadSampleDocuments() {
    showStatus('ingestStatus', 'Loading sample documents...', 'loading');
    
    try {
        const response = await fetch(`${API_URL}/sample-data`);
        const data = await response.json();
        
        docsInput.value = data.documents.map(doc => doc.trim()).join('\n\n---\n\n');
        showStatus('ingestStatus', `Loaded ${data.count} sample documents`, 'success');
    } catch (error) {
        showStatus('ingestStatus', `Error loading sample data: ${error.message}`, 'error');
    }
}

/**
 * Parse documents from textarea
 */
function parseDocuments(docText) {
    // Split by --- if present, otherwise by double newline
    const docs = docText.split(/\n\s*---\s*\n|\n\s*\n{2,}/).filter(doc => doc.trim().length > 0);
    return docs.map(doc => doc.trim());
}

/**
 * Ingest documents into the vector store
 */
async function ingestDocuments() {
    const docText = docsInput.value.trim();
    
    if (!docText) {
        showStatus('ingestStatus', 'Please provide documents', 'error');
        return;
    }
    
    const documents = parseDocuments(docText);
    
    if (documents.length === 0) {
        showStatus('ingestStatus', 'No valid documents found', 'error');
        return;
    }
    
    showStatus('ingestStatus', 'Ingesting documents...', 'loading');
    ingestBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/ingest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ documents })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        documentsIngested = true;
        showStatus('ingestStatus', 
            `✓ ${data.num_documents} documents ingested into ${data.num_chunks} chunks`, 
            'success');
        
        // Enable query button
        queryBtn.disabled = false;
    } catch (error) {
        showStatus('ingestStatus', `Error: ${error.message}`, 'error');
        documentsIngested = false;
    } finally {
        ingestBtn.disabled = false;
    }
}

/**
 * Query and analyze retrieval
 */
async function queryAndAnalyze() {
    if (!documentsIngested) {
        showStatus('queryStatus', 'Please ingest documents first', 'error');
        return;
    }
    
    const query = queryInput.value.trim();
    if (!query) {
        showStatus('queryStatus', 'Please enter a query', 'error');
        return;
    }
    
    const k = parseInt(kInput.value) || 5;
    
    showStatus('queryStatus', 'Processing query...', 'loading');
    queryBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, k })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        showStatus('queryStatus', `✓ Retrieved ${data.num_results} results`, 'success');
        displayResults(data);
    } catch (error) {
        showStatus('queryStatus', `Error: ${error.message}`, 'error');
    } finally {
        queryBtn.disabled = false;
    }
}

/**
 * Display query results and analysis
 */
function displayResults(data) {
    const query = data.query;
    const results = data.results;
    const analysis = data.analysis;
    
    // Clone the template
    const resultsHTML = resultsTemplate.content.cloneNode(true);
    
    // Set query text
    resultsHTML.getElementById('queryText').textContent = query;
    
    // Display top K results
    const topResultsList = resultsHTML.getElementById('topResultsList');
    topResultsList.innerHTML = '';
    results.forEach((result, index) => {
        const resultItem = resultItemTemplate.content.cloneNode(true);
        resultItem.querySelector('.rank-num').textContent = index + 1;
        resultItem.querySelector('.score-value').textContent = result.score.toFixed(2);
        resultItem.querySelector('.result-text').textContent = result.text;
        topResultsList.appendChild(resultItem);
    });
    
    // Display observations
    const observationsList = resultsHTML.getElementById('observationsList');
    observationsList.innerHTML = '';
    if (analysis.observations.length > 0) {
        analysis.observations.forEach(obs => {
            const div = document.createElement('div');
            div.className = 'observation-item';
            div.textContent = obs;
            observationsList.appendChild(div);
        });
    } else {
        const div = document.createElement('div');
        div.className = 'observation-item';
        div.textContent = '✓ No significant issues detected';
        observationsList.appendChild(div);
    }
    
    // Display possible issues
    const issuesList = resultsHTML.getElementById('issuesList');
    issuesList.innerHTML = '';
    if (analysis.possible_issues.length > 0) {
        analysis.possible_issues.forEach(issue => {
            const div = document.createElement('div');
            div.className = 'issue-item';
            div.textContent = '• ' + issue;
            issuesList.appendChild(div);
        });
    } else {
        const div = document.createElement('div');
        div.className = 'issue-item';
        div.style.background = '#e8f8f5';
        div.style.borderLeftColor = '#27ae60';
        div.style.color = '#0b5345';
        div.textContent = '✓ Retrieval appears healthy';
        issuesList.appendChild(div);
    }
    
    // Display keyword analysis
    displayKeywordAnalysis(resultsHTML, analysis.keyword_analysis);
    
    // Display coverage analysis
    displayCoverageAnalysis(resultsHTML, analysis.coverage_analysis);
    
    // Display gap analysis
    displayGapAnalysis(resultsHTML, analysis.gap_analysis);
    
    // Replace results container content
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(resultsHTML);
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Display keyword analysis
 */
function displayKeywordAnalysis(templateClone, analysis) {
    const keywordAnalysis = templateClone.getElementById('keywordAnalysis');
    keywordAnalysis.innerHTML = '';
    
    if (analysis.missed_keywords.length === 0) {
        const div = document.createElement('div');
        div.className = 'keyword-item';
        div.style.borderLeftColor = '#27ae60';
        div.innerHTML = '<span style="color: #27ae60;">✓ All keywords well-represented</span>';
        keywordAnalysis.appendChild(div);
    } else {
        analysis.missed_keywords.forEach(kw => {
            const div = document.createElement('div');
            div.className = 'keyword-item';
            div.innerHTML = `
                <span class="keyword-name">'${kw.keyword}'</span>
                <span class="keyword-coverage">Found in ${kw.chunks_containing}/${kw.total_chunks} chunks (${(kw.coverage * 100).toFixed(0)}%)</span>
            `;
            keywordAnalysis.appendChild(div);
        });
    }
}

/**
 * Display coverage analysis
 */
function displayCoverageAnalysis(templateClone, analysis) {
    const coverageAnalysis = templateClone.getElementById('coverageAnalysis');
    coverageAnalysis.innerHTML = '';
    
    const stats = [
        { label: 'Average chunk length', value: `${analysis.avg_chunk_length.toFixed(0)} chars` },
        { label: 'Query length', value: `${analysis.query_length} chars` },
        { label: 'Small chunks (<50 chars)', value: `${analysis.small_chunks}` },
        { label: 'Large chunks (>500 chars)', value: `${analysis.large_chunks}` }
    ];
    
    stats.forEach(stat => {
        const div = document.createElement('div');
        div.className = 'coverage-stat';
        div.innerHTML = `
            <span class="coverage-stat-label">${stat.label}</span>
            <span class="coverage-stat-value">${stat.value}</span>
        `;
        coverageAnalysis.appendChild(div);
    });
    
    if (analysis.issues.length > 0) {
        const divider = document.createElement('div');
        divider.style.borderBottom = '2px solid #667eea';
        divider.style.margin = '10px 0';
        coverageAnalysis.appendChild(divider);
        
        const issueDiv = document.createElement('div');
        issueDiv.style.color = '#e74c3c';
        issueDiv.style.fontWeight = '600';
        issueDiv.textContent = '⚠️ ' + analysis.issues[0];
        coverageAnalysis.appendChild(issueDiv);
    }
    
    const recommendation = document.createElement('div');
    recommendation.style.marginTop = '10px';
    recommendation.style.paddingTop = '10px';
    recommendation.style.borderTop = '1px solid #eee';
    recommendation.style.color = '#666';
    recommendation.style.fontStyle = 'italic';
    recommendation.textContent = '💡 ' + analysis.recommendation;
    coverageAnalysis.appendChild(recommendation);
}

/**
 * Display gap analysis
 */
function displayGapAnalysis(templateClone, analysis) {
    const gapAnalysis = templateClone.getElementById('gapAnalysis');
    gapAnalysis.innerHTML = '';
    
    if (analysis.gaps.length === 0) {
        const div = document.createElement('div');
        div.className = 'gap-item';
        div.style.borderLeftColor = '#27ae60';
        div.style.background = '#e8f8f5';
        div.innerHTML = '<span style="color: #27ae60;">✓ No relevance gaps detected</span>';
        gapAnalysis.appendChild(div);
    } else {
        analysis.gaps.forEach(gap => {
            const div = document.createElement('div');
            div.className = 'gap-item';
            div.innerHTML = `
                <div><span class="gap-rank">Rank ${gap.rank}</span> (Score: ${gap.score.toFixed(2)})</div>
                <div class="gap-issue">${gap.issue}</div>
                <div style="color: #999; font-size: 0.8em; margin-top: 4px;">Preview: ${gap.text_preview}</div>
            `;
            gapAnalysis.appendChild(div);
        });
    }
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    
    // Check API status
    fetch(`${API_URL}/status`)
        .then(r => r.json())
        .then(data => {
            if (data.status === 'not_initialized') {
                showStatus('ingestStatus', 'Note: Pipeline initializing...', 'info');
                setTimeout(() => {
                    showStatus('ingestStatus', '', 'info');
                }, 2000);
            }
        })
        .catch(err => console.log('Health check:', err));
});
