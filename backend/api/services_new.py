"""
Gemini API services using the new google-genai SDK.
This module provides synchronous wrappers for all security analysis endpoints.
"""
import os
import json
from google import genai
from google.genai import types
from django.conf import settings
from typing import Dict, List, Any, Optional, Union

from .schemas import (
    DAST_RESPONSE_SCHEMA,
    SAST_RESPONSE_SCHEMA,
    JS_RECON_RESPONSE_SCHEMA,
    DOM_XSS_RESPONSE_SCHEMA,
    HEADERS_RESPONSE_SCHEMA,
    FILE_UPLOAD_RESPONSE_SCHEMA,
    PAYLOAD_FORGE_RESPONSE_SCHEMA,
    SSTI_FORGE_RESPONSE_SCHEMA,
    PRIVESC_RESPONSE_SCHEMA,
    XSS_PAYLOADS_RESPONSE_SCHEMA,
    SQLMAP_RESPONSE_SCHEMA,
    CONSOLIDATION_RESPONSE_SCHEMA,
    DEEP_ANALYSIS_RESPONSE_SCHEMA,
    VALIDATION_RESPONSE_SCHEMA,
)

# Configuration
API_KEY = settings.GEMINI_API_KEY or os.environ.get('GEMINI_API_KEY', '')
MODEL = "gemini-2.5-flash"

# Initialize Gemini client
_client = None


def get_client():
    """Get or create Gemini client instance."""
    global _client
    if _client is None:
        if not API_KEY:
            raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY in your environment.")
        _client = genai.Client(api_key=API_KEY)
    return _client


def create_content(prompt: str) -> List[types.Content]:
    """Create content structure from prompt text."""
    return [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]


def create_config(
    response_schema: Optional[genai.types.Schema] = None,
    use_thinking: bool = True,
    temperature: float = 0.2,
    max_output_tokens: int = 8192,
    system_instruction: Optional[str] = None
) -> types.GenerateContentConfig:
    """
    Create generation configuration with optional thinking mode and schema.
    
    Args:
        response_schema: Optional schema for structured JSON output
        use_thinking: Enable extended thinking mode for complex reasoning
        temperature: Generation temperature (0.0-1.0)
        max_output_tokens: Maximum output tokens
        system_instruction: Optional system instruction for the model
    
    Returns:
        GenerateContentConfig instance
    """
    config_params = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": max_output_tokens,
    }
    
    # Add thinking config if enabled
    if use_thinking:
        config_params["thinking_config"] = types.ThinkingConfig(
            thinking_budget=-1  # Extended thinking mode
        )
    
    # Add response schema if provided
    if response_schema:
        config_params["response_mime_type"] = "application/json"
        config_params["response_schema"] = response_schema
    
    # Add system instruction if provided
    if system_instruction:
        config_params["system_instruction"] = [
            types.Part.from_text(text=system_instruction)
        ]
    
    return types.GenerateContentConfig(**config_params)


def call_gemini_api(
    prompt: str,
    response_schema: Optional[genai.types.Schema] = None,
    use_thinking: bool = True,
    response_as_json: bool = True,
    system_instruction: Optional[str] = None
) -> Union[str, Dict]:
    """
    Call the Gemini API with the given prompt (synchronous).
    
    Args:
        prompt: The prompt text
        response_schema: Optional schema for structured output
        use_thinking: Enable thinking mode
        response_as_json: Parse response as JSON
        system_instruction: Optional system instruction
    
    Returns:
        Parsed JSON dict or raw text
    
    Raises:
        ValueError: If API key is not configured
        RuntimeError: If API call fails
    """
    client = get_client()
    
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    try:
        # Create content and config
        contents = create_content(prompt)
        config = create_config(
            response_schema=response_schema if response_as_json else None,
            use_thinking=use_thinking,
            system_instruction=system_instruction
        )
        
        # Generate content synchronously (non-streaming for reliability)
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config
        )
        
        if not response or not response.text:
            raise RuntimeError("Empty response from Gemini API")
        
        response_text = response.text
        
        # Parse response
        if response_as_json:
            # With response_schema, the output should already be valid JSON
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                # Fallback: try to extract JSON from text
                try:
                    return extract_json_fallback(response_text)
                except Exception:
                    raise RuntimeError(f"Failed to parse JSON response: {str(e)}")
        
        return response_text
    
    except ValueError as e:
        raise e
    except RuntimeError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}")


def extract_json_fallback(text: str) -> Dict:
    """
    Fallback JSON extraction from text.
    
    Args:
        text: Text containing JSON
        
    Returns:
        Extracted JSON as dict
        
    Raises:
        ValueError: If no valid JSON found
    """
    if not text or not text.strip():
        raise ValueError("Empty text provided for JSON extraction")
    
    # Try to find JSON in markdown blocks
    if '```json' in text or '```' in text:
        blocks = text.split('```')
        for block in blocks:
            block = block.replace('json', '').strip()
            if block and len(block) > 0 and block[0] == '{' and block[-1] == '}':
                try:
                    return json.loads(block)
                except json.JSONDecodeError:
                    continue
    
    # Try to find JSON directly
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Could not extract valid JSON from response")


def chat_with_gemini(messages: List[Dict[str, str]]) -> str:
    """
    Chat with Gemini using a list of messages (synchronous).
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        
    Returns:
        AI response text
        
    Raises:
        ValueError: If messages are invalid
        RuntimeError: If chat fails
    """
    client = get_client()
    
    if not messages or len(messages) == 0:
        raise ValueError("Messages list cannot be empty")
    
    # Validate message structure
    for msg in messages:
        if 'role' not in msg or 'content' not in msg:
            raise ValueError("Each message must have 'role' and 'content' keys")
    
    try:
        # Convert messages to content format
        history = []
        for msg in messages[:-1]:  # All but last message
            history.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )
        
        # Last user message
        last_msg = messages[-1]["content"] if messages else ""
        
        # For chat, we'll use simple generation with streaming
        contents = create_content(last_msg)
        config = create_config(use_thinking=False, response_schema=None)
        
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=config
        ):
            if chunk and chunk.text:
                response_text += chunk.text
        
        if not response_text:
            raise RuntimeError("Empty response from chat")
        
        return response_text
    
    except ValueError as e:
        raise e
    except RuntimeError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error in chat with Gemini: {str(e)}")


# Specific analysis functions with proper schemas

def analyze_url(url: str, scan_type: str, iteration: int = 0) -> Dict:
    """
    Analyze a URL using the specified scan type.
    
    Args:
        url: Target URL to analyze
        scan_type: Type of scan (active/passive)
        iteration: Iteration number for multi-pass analysis
        
    Returns:
        Analysis results as dict
    """
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    from .prompts import create_dast_analysis_prompt
    
    prompt = create_dast_analysis_prompt(url, scan_type, iteration)
    return call_gemini_api(
        prompt,
        response_schema=DAST_RESPONSE_SCHEMA,
        use_thinking=True
    )


def analyze_code(code: str, iteration: int = 0) -> Dict:
    """
    Analyze code for vulnerabilities.
    
    Args:
        code: Source code to analyze
        iteration: Iteration number for multi-pass analysis
        
    Returns:
        Analysis results as dict
    """
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    from .prompts import create_sast_analysis_prompt
    
    prompt = create_sast_analysis_prompt(code, iteration)
    return call_gemini_api(
        prompt,
        response_schema=SAST_RESPONSE_SCHEMA,
        use_thinking=True
    )


def analyze_js_code(code: str) -> Dict:
    """
    Analyze JavaScript code for reconnaissance.
    
    Args:
        code: JavaScript code to analyze
        
    Returns:
        Analysis results as dict
    """
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    from .prompts import create_js_recon_prompt
    
    prompt = create_js_recon_prompt(code)
    return call_gemini_api(
        prompt,
        response_schema=JS_RECON_RESPONSE_SCHEMA,
        use_thinking=True
    )


def analyze_dom_xss(code: str) -> Dict:
    """
    Analyze code for DOM XSS vulnerabilities.
    
    Args:
        code: Code to analyze for DOM XSS
        
    Returns:
        Analysis results as dict
    """
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    from .prompts import create_dom_xss_pathfinder_prompt
    
    prompt = create_dom_xss_pathfinder_prompt(code)
    return call_gemini_api(
        prompt,
        response_schema=DOM_XSS_RESPONSE_SCHEMA,
        use_thinking=True
    )


def analyze_headers(url: str) -> Dict:
    """
    Analyze security headers of a URL.
    
    Args:
        url: Target URL to analyze headers
        
    Returns:
        Analysis results as dict
    """
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    from .prompts import create_headers_analysis_prompt
    
    prompt = create_headers_analysis_prompt(url)
    return call_gemini_api(
        prompt,
        response_schema=HEADERS_RESPONSE_SCHEMA,
        use_thinking=False
    )


def forge_payloads(base_payload: str) -> Dict:
    """
    Generate variations of a payload.
    
    Args:
        base_payload: Base payload to generate variations from
        
    Returns:
        Generated payloads as dict
    """
    if not base_payload or not base_payload.strip():
        raise ValueError("Base payload cannot be empty")
    
    from .prompts import create_payload_forge_prompt
    
    prompt = create_payload_forge_prompt(base_payload)
    return call_gemini_api(
        prompt,
        response_schema=PAYLOAD_FORGE_RESPONSE_SCHEMA,
        use_thinking=True
    )


def generate_ssti_payloads(engine: str, goal: str) -> Dict:
    """
    Generate SSTI payloads for the specified template engine.
    
    Args:
        engine: Template engine name
        goal: Goal for the payload (RCE, file read, etc.)
        
    Returns:
        Generated SSTI payloads as dict
    """
    if not engine or not engine.strip():
        raise ValueError("Engine cannot be empty")
    if not goal or not goal.strip():
        raise ValueError("Goal cannot be empty")
    
    from .prompts import create_ssti_forge_prompt
    
    prompt = create_ssti_forge_prompt(engine, goal)
    return call_gemini_api(
        prompt,
        response_schema=SSTI_FORGE_RESPONSE_SCHEMA,
        use_thinking=True
    )


def analyze_jwt(header: Dict, payload: Dict, mode: str) -> str:
    """
    Analyze a JWT token.
    
    Args:
        header: JWT header as dict
        payload: JWT payload as dict
        mode: Analysis mode (blue_team/red_team)
        
    Returns:
        Analysis result as plain text
    """
    if not header:
        raise ValueError("JWT header cannot be empty")
    if not payload:
        raise ValueError("JWT payload cannot be empty")
    if mode not in ['blue_team', 'red_team']:
        raise ValueError("Mode must be 'blue_team' or 'red_team'")
    
    from .prompts import create_jwt_blue_team_prompt, create_jwt_red_team_prompt
    
    if mode == 'blue_team':
        prompt = create_jwt_blue_team_prompt(
            json.dumps(header, indent=2),
            json.dumps(payload, indent=2)
        )
    else:
        prompt = create_jwt_red_team_prompt(
            json.dumps(header, indent=2),
            json.dumps(payload, indent=2)
        )
    
    return call_gemini_api(
        prompt,
        response_schema=None,  # Text response
        use_thinking=True,
        response_as_json=False
    )


def analyze_file_upload(url: str) -> Dict:
    """
    Analyze a URL for file upload vulnerabilities.
    
    Args:
        url: Target URL with file upload functionality
        
    Returns:
        Analysis results as dict
    """
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    from .prompts import create_file_upload_analysis_prompt
    
    prompt = create_file_upload_analysis_prompt(url)
    return call_gemini_api(
        prompt,
        response_schema=FILE_UPLOAD_RESPONSE_SCHEMA,
        use_thinking=True
    )


def consolidate_reports(reports: List[Dict]) -> Dict:
    """
    Consolidate multiple vulnerability reports.
    
    Args:
        reports: List of vulnerability report dicts
        
    Returns:
        Consolidated report as dict
    """
    if not reports or len(reports) == 0:
        raise ValueError("Reports list cannot be empty")
    
    from .prompts import create_consolidation_prompt
    
    prompt = create_consolidation_prompt(json.dumps(reports))
    return call_gemini_api(
        prompt,
        response_schema=CONSOLIDATION_RESPONSE_SCHEMA,
        use_thinking=True
    )


def perform_deep_analysis(vulnerability: Dict, target: str) -> Dict:
    """
    Perform deep analysis on a vulnerability.
    
    Args:
        vulnerability: Vulnerability details as dict
        target: Target system/URL
        
    Returns:
        Deep analysis results as dict
    """
    if not vulnerability:
        raise ValueError("Vulnerability cannot be empty")
    if not target or not target.strip():
        raise ValueError("Target cannot be empty")
    
    from .prompts import create_deep_analysis_prompt
    
    prompt = create_deep_analysis_prompt(vulnerability, target)
    return call_gemini_api(
        prompt,
        response_schema=DEEP_ANALYSIS_RESPONSE_SCHEMA,
        use_thinking=True
    )


def validate_vulnerability(vulnerability: Dict) -> Dict:
    """
    Validate if a vulnerability is likely to be real.
    
    Args:
        vulnerability: Vulnerability details as dict
        
    Returns:
        Validation results as dict
    """
    if not vulnerability:
        raise ValueError("Vulnerability cannot be empty")
    
    from .prompts import create_validation_prompt
    
    prompt = create_validation_prompt(vulnerability)
    return call_gemini_api(
        prompt,
        response_schema=VALIDATION_RESPONSE_SCHEMA,
        use_thinking=True
    )


def find_privesc_exploits(technology: str, version: str) -> Dict:
    """
    Find privilege escalation exploits for a technology.
    
    Args:
        technology: Technology name (e.g., 'sudo', 'polkit')
        version: Version string
        
    Returns:
        Exploit information as dict
    """
    if not technology or not technology.strip():
        raise ValueError("Technology cannot be empty")
    if not version or not version.strip():
        raise ValueError("Version cannot be empty")
    
    from .prompts import create_privesc_pathfinder_prompt
    
    prompt = create_privesc_pathfinder_prompt(technology, version)
    return call_gemini_api(
        prompt,
        response_schema=PRIVESC_RESPONSE_SCHEMA,
        use_thinking=True
    )


def generate_xss_payloads(vulnerability: Dict, sample_payloads: Optional[List[str]] = None) -> Dict:
    """
    Generate XSS payloads for a vulnerability.
    
    Args:
        vulnerability: Vulnerability details as dict
        sample_payloads: Optional list of sample payloads to build upon
        
    Returns:
        Generated XSS payloads as dict
    """
    if not vulnerability:
        raise ValueError("Vulnerability cannot be empty")
    
    from .prompts import create_xss_payload_generation_prompt
    
    prompt = create_xss_payload_generation_prompt(vulnerability, sample_payloads)
    return call_gemini_api(
        prompt,
        response_schema=XSS_PAYLOADS_RESPONSE_SCHEMA,
        use_thinking=True
    )


def generate_sqlmap_command(vulnerability: Dict, url: str) -> Dict:
    """
    Generate a SQLMap command for a SQL injection vulnerability.
    
    Args:
        vulnerability: SQL injection vulnerability details
        url: Target URL
        
    Returns:
        SQLMap command and options as dict
    """
    if not vulnerability:
        raise ValueError("Vulnerability cannot be empty")
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    from .prompts import create_sqlmap_command_generation_prompt
    
    prompt = create_sqlmap_command_generation_prompt(vulnerability, url)
    return call_gemini_api(
        prompt,
        response_schema=SQLMAP_RESPONSE_SCHEMA,
        use_thinking=False
    )