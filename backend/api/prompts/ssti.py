def create_ssti_forge_prompt(engine: str, goal: str) -> str:
    """Create a prompt for SSTI payload generation."""
    return f"""
    Generate SSTI payloads for {engine} template engine to achieve: {goal}

    Please provide payloads in JSON format with different techniques and bypass methods.
    """

def create_payload_forge_prompt(base_payload: str) -> str:
    """Create a prompt for payload forging."""
    return f"""
    Generate variations of the following payload for security testing:

    Base payload: {base_payload}

    Please provide variations in JSON format with different encoding, obfuscation, and delivery methods.
    """

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