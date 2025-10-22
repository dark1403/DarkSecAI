"""
Response schemas for Gemini API structured output.
Each schema defines the expected JSON structure for different analysis types.
"""
from google import genai

# DAST Analysis Schema
DAST_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["analyzedTarget", "vulnerabilities"],
    properties={
        "analyzedTarget": genai.types.Schema(type=genai.types.Type.STRING),
        "vulnerabilities": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                required=["vulnerability", "severity", "description", "impact", "vulnerableCode", "recommendation"],
                properties={
                    "vulnerability": genai.types.Schema(type=genai.types.Type.STRING),
                    "severity": genai.types.Schema(type=genai.types.Type.STRING),
                    "description": genai.types.Schema(type=genai.types.Type.STRING),
                    "impact": genai.types.Schema(type=genai.types.Type.STRING),
                    "vulnerableCode": genai.types.Schema(type=genai.types.Type.STRING),
                    "recommendation": genai.types.Schema(type=genai.types.Type.STRING),
                    "injectionPoint": genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        properties={
                            "parameter": genai.types.Schema(type=genai.types.Type.STRING),
                            "method": genai.types.Schema(type=genai.types.Type.STRING),
                            "location": genai.types.Schema(type=genai.types.Type.STRING),
                        }
                    ),
                }
            )
        )
    }
)

# SAST Analysis Schema
SAST_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["vulnerabilities", "overall_risk", "summary"],
    properties={
        "vulnerabilities": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                required=["type", "severity", "description", "recommendation"],
                properties={
                    "type": genai.types.Schema(type=genai.types.Type.STRING),
                    "severity": genai.types.Schema(type=genai.types.Type.STRING),
                    "description": genai.types.Schema(type=genai.types.Type.STRING),
                    "line_number": genai.types.Schema(type=genai.types.Type.INTEGER),
                    "recommendation": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        ),
        "overall_risk": genai.types.Schema(type=genai.types.Type.STRING),
        "summary": genai.types.Schema(type=genai.types.Type.STRING),
    }
)

# JS Recon Schema
JS_RECON_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "endpoints": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "authentication": genai.types.Schema(type=genai.types.Type.STRING),
        "data_handling": genai.types.Schema(type=genai.types.Type.STRING),
        "third_party_libraries": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "security_configs": genai.types.Schema(type=genai.types.Type.STRING),
    }
)

# DOM XSS Schema
DOM_XSS_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "vulnerabilities": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "type": genai.types.Schema(type=genai.types.Type.STRING),
                    "source": genai.types.Schema(type=genai.types.Type.STRING),
                    "sink": genai.types.Schema(type=genai.types.Type.STRING),
                    "attack_vector": genai.types.Schema(type=genai.types.Type.STRING),
                    "prevention": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        )
    }
)

# Headers Analysis Schema
HEADERS_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "missing_headers": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "misconfigured_headers": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "header": genai.types.Schema(type=genai.types.Type.STRING),
                    "issue": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        ),
        "security_implications": genai.types.Schema(type=genai.types.Type.STRING),
        "recommendations": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)

# File Upload Schema
FILE_UPLOAD_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["found", "description"],
    properties={
        "found": genai.types.Schema(type=genai.types.Type.BOOLEAN),
        "description": genai.types.Schema(type=genai.types.Type.STRING),
        "manual_testing_guide": genai.types.Schema(type=genai.types.Type.STRING),
    }
)

# Payload Forge Schema
PAYLOAD_FORGE_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "variations": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "type": genai.types.Schema(type=genai.types.Type.STRING),
                    "payload": genai.types.Schema(type=genai.types.Type.STRING),
                    "description": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        )
    }
)

# SSTI Forge Schema
SSTI_FORGE_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "payloads": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "technique": genai.types.Schema(type=genai.types.Type.STRING),
                    "payload": genai.types.Schema(type=genai.types.Type.STRING),
                    "description": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        )
    }
)

# Privilege Escalation Schema
PRIVESC_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "vulnerabilities": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "exploit_techniques": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "impact": genai.types.Schema(type=genai.types.Type.STRING),
        "mitigation": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)

# XSS Payloads Schema
XSS_PAYLOADS_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "basic_payloads": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "encoded_payloads": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "bypass_payloads": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "context_specific": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)

# SQLMap Schema
SQLMAP_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "command": genai.types.Schema(type=genai.types.Type.STRING),
        "explanation": genai.types.Schema(type=genai.types.Type.STRING),
        "options": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)

# Consolidation Schema
CONSOLIDATION_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["analyzedTarget", "vulnerabilities", "overall_risk", "summary"],
    properties={
        "analyzedTarget": genai.types.Schema(type=genai.types.Type.STRING),
        "vulnerabilities": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "vulnerability": genai.types.Schema(type=genai.types.Type.STRING),
                    "severity": genai.types.Schema(type=genai.types.Type.STRING),
                    "description": genai.types.Schema(type=genai.types.Type.STRING),
                    "impact": genai.types.Schema(type=genai.types.Type.STRING),
                    "recommendation": genai.types.Schema(type=genai.types.Type.STRING),
                    "vulnerableCode": genai.types.Schema(type=genai.types.Type.STRING),
                }
            )
        ),
        "overall_risk": genai.types.Schema(type=genai.types.Type.STRING),
        "summary": genai.types.Schema(type=genai.types.Type.STRING),
    }
)

# Deep Analysis Schema
DEEP_ANALYSIS_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    properties={
        "root_cause": genai.types.Schema(type=genai.types.Type.STRING),
        "attack_vectors": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "impact_assessment": genai.types.Schema(type=genai.types.Type.STRING),
        "remediation": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
        "prevention": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)

# Validation Schema
VALIDATION_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["is_valid", "confidence", "reasoning"],
    properties={
        "is_valid": genai.types.Schema(type=genai.types.Type.BOOLEAN),
        "confidence": genai.types.Schema(type=genai.types.Type.STRING),
        "reasoning": genai.types.Schema(type=genai.types.Type.STRING),
        "false_positive_indicators": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING)
        ),
    }
)
