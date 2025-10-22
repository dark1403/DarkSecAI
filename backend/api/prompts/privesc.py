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

def create_deep_analysis_prompt(vulnerability: str, target: str) -> str:
    """Create a prompt for deep vulnerability analysis."""
    return f"""
    Perform deep analysis on this vulnerability:

    Vulnerability: {vulnerability}
    Target: {target}

    Please provide detailed analysis in JSON format covering:
    - Root cause analysis
    - Attack vectors
    - Impact assessment
    - Remediation strategies
    - Prevention methods
    """

def create_validation_prompt(vulnerability: str) -> str:
    """Create a prompt for vulnerability validation."""
    return f"""
    Validate if this vulnerability is likely to be real:

    {vulnerability}

    Please provide validation analysis in JSON format with:
    - is_valid: boolean
    - confidence: High|Medium|Low
    - reasoning: explanation
    - false_positive_indicators: list of indicators
    """

def create_consolidation_prompt(reports: str) -> str:
    """Create a prompt for report consolidation."""
    return f"""
    Consolidate the following vulnerability reports:

    {reports}

    Please provide a consolidated analysis in JSON format.
    """