def create_file_upload_analysis_prompt(url: str) -> str:
    """Create a prompt for file upload analysis."""
    return f"""
You are a web security expert analyzing file upload functionality. Analyze the target URL for file upload forms.

Target URL: {url}

Your task is to:
1. Detect if the page contains file upload forms/functionality
2. If found, provide security analysis and testing recommendations
3. If not found, provide a clear message

IMPORTANT: You must respond with a JSON object in this EXACT format:
{{
    "found": boolean,
    "description": "string - detailed description of what was found or not found",
    "manual_testing_guide": "string - if found=true, provide comprehensive markdown-formatted manual testing guide with steps, payloads, and expected results. If found=false, provide empty string."
}}

Guidelines for the response:
- Set "found" to true if file upload forms/functionality is detected, false otherwise
- Provide detailed "description" explaining what was analyzed
- If found=true, create a comprehensive "manual_testing_guide" with:
  * Step-by-step testing instructions
  * Example malicious file payloads to test
  * Security checks to perform (file type, size, path traversal, etc.)
  * Expected vulnerable behaviors
  * Use markdown formatting for readability
- If found=false, set "manual_testing_guide" to empty string ""

Return ONLY the JSON object, no other text.
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