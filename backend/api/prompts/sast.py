def create_sast_analysis_prompt(code: str, iteration: int = 0) -> str:
    """Create a prompt for SAST analysis."""
    return f"""
    Analyze the following code for security vulnerabilities:

    {code}

    Please provide a detailed security analysis in JSON format with the following structure:
    {{
        "vulnerabilities": [
            {{
                "type": "vulnerability_type",
                "severity": "High|Medium|Low",
                "description": "detailed description",
                "line_number": 123,
                "recommendation": "how to fix"
            }}
        ],
        "overall_risk": "High|Medium|Low",
        "summary": "brief summary"
    }}
    """

def create_js_recon_prompt(code: str) -> str:
    """Create a prompt for JavaScript reconnaissance."""
    return f"""
    Analyze the following JavaScript code for reconnaissance purposes:

    {code}

    Please provide analysis in JSON format covering:
    - Endpoints and API calls
    - Authentication mechanisms
    - Data handling patterns
    - Third-party libraries
    - Security configurations
    """

def create_dom_xss_pathfinder_prompt(code: str) -> str:
    """Create a prompt for DOM XSS analysis."""
    return f"""
    Analyze the following code for DOM XSS vulnerabilities:

    {code}

    Please provide a detailed analysis in JSON format with potential attack vectors and prevention methods.
    """

def create_headers_analysis_prompt(url: str) -> str:
    """Create a prompt for security headers analysis."""
    return f"""
    Analyze the security headers for the following URL: {url}

    Please provide a comprehensive security headers analysis in JSON format.
    """

def create_payload_forge_prompt(base_payload: str) -> str:
    """Create a prompt for payload forging."""
    return f"""
    Generate variations of the following payload for security testing:

    Base payload: {base_payload}

    Please provide variations in JSON format with different encoding, obfuscation, and delivery methods.
    """

def create_ssti_forge_prompt(engine: str, goal: str) -> str:
    """Create a prompt for SSTI payload generation."""
    return f"""
    Generate SSTI payloads for {engine} template engine to achieve: {goal}

    Please provide payloads in JSON format with different techniques and bypass methods.
    """

def create_jwt_blue_team_prompt(header: str, payload: str) -> str:
    """Create a prompt for JWT blue team analysis."""
    return f"""
    Analyze this JWT for security from a defensive perspective:

    Header: {header}
    Payload: {payload}

    Please provide security analysis and recommendations.
    """

def create_jwt_red_team_prompt(header: str, payload: str) -> str:
    """Create a prompt for JWT red team analysis."""
    return f"""
    Analyze this JWT for attack opportunities:

    Header: {header}
    Payload: {payload}

    Please provide attack vectors and exploitation methods.
    """

def create_file_upload_analysis_prompt(url: str) -> str:
    """Create a prompt for file upload analysis."""
    return f"""
    Analyze the file upload functionality at: {url}

    Please provide security analysis in JSON format covering vulnerabilities and recommendations.
    """

def create_consolidation_prompt(reports: str) -> str:
    """Create a prompt for report consolidation."""
    return f"""
    Consolidate the following vulnerability reports:

    {reports}

    Please provide a consolidated analysis in JSON format.
    """

def create_deep_analysis_prompt(vulnerability: str, target: str) -> str:
    """Create a prompt for deep vulnerability analysis."""
    return f"""
    Perform deep analysis on this vulnerability:

    Vulnerability: {vulnerability}
    Target: {target}

    Please provide detailed analysis in JSON format.
    """

def create_validation_prompt(vulnerability: str) -> str:
    """Create a prompt for vulnerability validation."""
    return f"""
    Validate if this vulnerability is likely to be real:

    {vulnerability}

    Please provide validation analysis in JSON format.
    """

def create_privesc_pathfinder_prompt(technology: str, version: str) -> str:
    """Create a prompt for privilege escalation analysis."""
    return f"""
    Find privilege escalation exploits for:

    Technology: {technology}
    Version: {version}

    Please provide analysis in JSON format.
    """

def create_xss_payload_generation_prompt(vulnerability: str, sample_payloads=None) -> str:
    """Create a prompt for XSS payload generation."""
    return f"""
    Generate XSS payloads for this vulnerability:

    {vulnerability}

    Please provide payloads in JSON format.
    """

def create_sqlmap_command_generation_prompt(vulnerability: str, url: str) -> str:
    """Create a prompt for SQLMap command generation."""
    return f"""
    Generate SQLMap command for:

    Vulnerability: {vulnerability}
    URL: {url}

    Please provide the command and explanation.
    """

def create_sast_deep_analysis_prompt(vulnerability: str, target: str) -> str:
    """Create a prompt for SAST deep analysis."""
    return f"""
    Perform deep SAST analysis on this vulnerability:

    Vulnerability: {vulnerability}
    Target: {target}

    Please provide detailed analysis in JSON format.
    """