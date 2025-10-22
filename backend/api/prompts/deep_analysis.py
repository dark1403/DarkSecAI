"""
ML Model Integration Layer
Wraps the custom severity/CWE prediction models for use in the Django backend.
"""
import sys
import os
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Add AI model directory to path
AI_DIR = Path(__file__).resolve().parent.parent.parent / 'ai'
sys.path.insert(0, str(AI_DIR))

try:
    from predict_unified import predict_severity, suggest_cwe
    _models_loaded = True
except Exception as e:
    _models_loaded = False
    _load_error = str(e)


def enrich_vulnerability_with_ml(vulnerability: Dict) -> Dict:
    """
    Enrich a vulnerability dict with ML model predictions.
    
    Takes the raw vulnerability from LLM and adds:
    - ML-predicted severity (overrides or supplements LLM severity)
    - Top CWE mappings with similarity scores
    - Industry-standard mitigations from CWE database
    
    Args:
        vulnerability: Dict with keys like 'vulnerability', 'description', 'severity', etc.
        
    Returns:
        Enriched vulnerability dict with ML predictions in 'ml_predictions' key
    """
    if not _models_loaded:
        # Graceful degradation: return original if models not available
        vulnerability['ml_predictions'] = {
            'available': False,
            'error': f'ML models not loaded: {_load_error}'
        }
        return vulnerability
    
    # Extract text for ML model input
    finding_text = _build_finding_text(vulnerability)
    
    try:
        # Stage 1: Predict severity with confidence
        confidence, predicted_severity = predict_severity(finding_text)
        
        # Stage 2: Retrieve top CWEs with mitigations
        cwe_suggestions = suggest_cwe(finding_text, k=3)
        
        # Package ML predictions
        vulnerability['ml_predictions'] = {
            'available': True,
            'severity': {
                'predicted': predicted_severity,
                'confidence': round(float(confidence), 3),
                'original_llm': vulnerability.get('severity', 'Unknown')
            },
            'cwe_mappings': [
                {
                    'cwe_id': cwe.get('CWE-ID', 'Unknown'),
                    'name': cwe.get('Name', ''),
                    'similarity': round(cwe.get('similarity', 0.0), 3),
                    'mitigations': cwe.get('Potential Mitigations', 'Not available'),
                    'description': cwe.get('Description', '')[:300]  # Truncate for token efficiency
                }
                for cwe in cwe_suggestions
            ]
        }
        
        # Optional: Override LLM severity if ML confidence is high
        if confidence > 0.75:
            vulnerability['ml_adjusted_severity'] = predicted_severity
        
    except Exception as e:
        vulnerability['ml_predictions'] = {
            'available': False,
            'error': f'Prediction failed: {str(e)}'
        }
    
    return vulnerability


def _build_finding_text(vulnerability: Dict) -> str:
    """
    Build a comprehensive text representation for ML model input.
    Combines vulnerability name, description, and impact.
    """
    parts = []
    
    if vulnerability.get('vulnerability'):
        parts.append(vulnerability['vulnerability'])
    
    if vulnerability.get('description'):
        parts.append(vulnerability['description'])
    
    if vulnerability.get('impact'):
        parts.append(f"Impact: {vulnerability['impact']}")
    
    return " ".join(parts) if parts else "Unknown vulnerability"


def batch_enrich_vulnerabilities(vulnerabilities: List[Dict]) -> List[Dict]:
    """
    Enrich multiple vulnerabilities with ML predictions.
    
    Args:
        vulnerabilities: List of vulnerability dicts
        
    Returns:
        List of enriched vulnerability dicts
    """
    return [enrich_vulnerability_with_ml(vuln) for vuln in vulnerabilities]


def get_ml_context_summary(vulnerability: Dict) -> str:
    """
    Generate a formatted string of ML predictions for LLM context injection.
    Used in deep analysis prompts.
    
    Args:
        vulnerability: Enriched vulnerability dict with ml_predictions key
        
    Returns:
        Formatted string summarizing ML predictions
    """
    ml_data = vulnerability.get('ml_predictions', {})
    
    if not ml_data.get('available', False):
        return "ML predictions unavailable."
    
    # Build context string
    context_parts = []
    
    # Severity prediction
    sev_info = ml_data.get('severity', {})
    context_parts.append(
        f"ML-Predicted Severity: {sev_info.get('predicted', 'Unknown')} "
        f"(Confidence: {sev_info.get('confidence', 0.0) * 100:.1f}%)"
    )
    
    # CWE mappings
    cwe_list = ml_data.get('cwe_mappings', [])
    if cwe_list:
        context_parts.append("\nRelevant CWE Weaknesses:")
        for i, cwe in enumerate(cwe_list[:3], 1):
            context_parts.append(
                f"{i}. {cwe['cwe_id']}: {cwe['name']} (Similarity: {cwe['similarity'] * 100:.1f}%)"
            )
            if cwe.get('mitigations'):
                context_parts.append(f"   Mitigations: {cwe['mitigations'][:200]}...")
    
    return "\n".join(context_parts)


def create_deep_analysis_prompt(vulnerability: dict, target: str) -> str:
    """
    Create a prompt for deep vulnerability analysis with ML context.
    
    If the vulnerability dict contains ml_predictions, they are injected
    as structured context to ground the LLM's analysis.
    """
    from ..ml_integration import get_ml_context_summary
    
    # Extract ML context if available
    ml_context = get_ml_context_summary(vulnerability)
    
    # Format vulnerability for prompt
    vuln_str = f"""
Vulnerability Name: {vulnerability.get('vulnerability', 'Unknown')}
LLM-Assessed Severity: {vulnerability.get('severity', 'Unknown')}
Description: {vulnerability.get('description', 'N/A')}
Impact: {vulnerability.get('impact', 'N/A')}
    """.strip()
    
    return f"""
You are a security expert performing deep analysis on a detected vulnerability.

**Target System:** {target}

**Detected Vulnerability:**
{vuln_str}

**ML Model Predictions (Industry-Standard Context):**
{ml_context}

**Your Task:**
Provide a comprehensive, context-aware analysis that:
1. **Validates Severity**: Compare the LLM-assessed severity with the ML-predicted severity. If there's a discrepancy, explain which is more accurate based on the CWE mappings and your security expertise.

2. **Root Cause Analysis**: Explain the underlying weakness using the CWE context provided. Reference specific CWE IDs where relevant.

3. **Attack Vectors**: Detail realistic exploitation scenarios, considering the ML-identified weakness patterns.

4. **Enhanced Impact Assessment**: Expand on the initial impact using the CWE consequence data and industry knowledge.

5. **Remediation Strategy**: Synthesize the CWE-suggested mitigations with custom recommendations for this specific vulnerability and target.

6. **Prevention Methods**: Long-term architectural/process changes to prevent this class of vulnerability.

**Output Format (JSON):**
{{
    "validated_severity": "Critical|High|Medium|Low",
    "severity_justification": "explanation comparing LLM vs ML predictions",
    "root_cause": "detailed root cause with CWE references",
    "attack_vectors": ["vector1", "vector2", ...],
    "enhanced_impact": "detailed impact assessment",
    "remediation_steps": ["step1", "step2", ...],
    "prevention_methods": ["method1", "method2", ...],
    "cwe_analysis": "how the identified CWEs relate to this vulnerability"
}}
    """


def create_validation_prompt(vulnerability: dict) -> str:
    """
    Create a prompt for vulnerability validation with ML context.
    """
    from ..ml_integration import get_ml_context_summary
    
    ml_context = get_ml_context_summary(vulnerability)
    
    vuln_str = f"""
{vulnerability.get('vulnerability', 'Unknown')} (Severity: {vulnerability.get('severity', 'Unknown')})
Description: {vulnerability.get('description', 'N/A')}
    """.strip()
    
    return f"""
Validate if this vulnerability is likely to be a true positive:

{vuln_str}

**ML Model Analysis:**
{ml_context}

Consider:
- Does the ML severity confidence support this finding?
- Do the CWE mappings align with the described vulnerability?
- Are there indicators of false positives?

Provide validation in JSON format:
{{
    "is_valid": true/false,
    "confidence": "High|Medium|Low",
    "reasoning": "detailed explanation using ML context",
    "false_positive_indicators": ["indicator1", ...],
    "alignment_score": "how well LLM and ML predictions align (0-100)"
}}
    """

def create_file_upload_analysis_prompt(url: str) -> str:
    """Create a prompt for file upload analysis."""
    return f"""
    Analyze the file upload functionality at: {url}

    Please provide security analysis in JSON format covering:
    - File type restrictions
    - Size limitations
    - Path traversal vulnerabilities
    - Malicious file detection
    - Recommendations
    """

def create_privesc_pathfinder_prompt(technology: str, version: str) -> str:
    """Create a prompt for privilege escalation analysis."""
    return f"""
    Find privilege escalation exploits for:

    Technology: {technology}
    Version: {version}

    Please provide analysis in JSON format with:
    - Known vulnerabilities
    - Exploit techniques
    - Impact assessment
    - Mitigation strategies
    """

def create_xss_payload_generation_prompt(vulnerability: str, sample_payloads=None) -> str:
    """Create a prompt for XSS payload generation."""
    return f"""
    Generate XSS payloads for this vulnerability:

    {vulnerability}

    Please provide payloads in JSON format with different techniques:
    - Basic payloads
    - Encoded payloads
    - Filter bypass payloads
    - Context-specific payloads
    """

def create_sqlmap_command_generation_prompt(vulnerability: str, url: str) -> str:
    """Create a prompt for SQLMap command generation."""
    return f"""
    Generate SQLMap command for:

    Vulnerability: {vulnerability}
    URL: {url}

    Please provide the command and explanation in JSON format.
    """