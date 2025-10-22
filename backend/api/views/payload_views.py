from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from ..serializers import (
    ForgedPayloadResultSerializer, XssPayloadResultSerializer,
    VulnerabilityReportSerializer
)
from ..services_new import (
    forge_payloads, generate_ssti_payloads, analyze_jwt,
    generate_xss_payloads, generate_sqlmap_command
)

import json
import base64


@api_view(['POST'])
def forge_payloads_api(request):
    """
    API endpoint to generate variations of a payload.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    base_payload = data.get('basePayload')

    if not base_payload:
        return Response(
            {'error': 'Base payload is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = forge_payloads(base_payload)

        # Transform AI response to serializer format
        # AI returns: {"variations": [{"type": "...", "payload": "...", "description": "..."}]}
        # Serializer expects: {"base_payload": "...", "payloads": [{"technique": "...", "payload": "...", "description": "..."}]}
        
        payloads = []
        if result.get('variations'):
            for variation in result['variations']:
                payloads.append({
                    'technique': variation.get('type', 'Unknown'),
                    'payload': variation.get('payload', ''),
                    'description': variation.get('description', '')
                })
        
        # If no variations returned, add a default one
        if not payloads:
            payloads.append({
                'technique': 'Original',
                'payload': base_payload,
                'description': 'Original payload (no variations generated)'
            })
        
        # Create the data structure for the serializer
        forge_data = {
            'base_payload': base_payload,
            'payloads': payloads
        }

        # Create and validate serializer
        serializer = ForgedPayloadResultSerializer(data=forge_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Payload generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def generate_ssti_payloads_api(request):
    """
    API endpoint to generate SSTI payloads for a template engine.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    engine = data.get('engine')
    goal = data.get('goal')

    if not engine or not goal:
        return Response(
            {'error': 'Engine and goal are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = generate_ssti_payloads(engine, goal)

        # Transform AI response to serializer format
        # AI returns: {"payloads": [{"technique": "...", "payload": "...", "description": "..."}]}
        # Serializer expects: {"engine": "...", "goal": "...", "payloads": [{"technique": "...", "payload": "...", "description": "..."}]}
        
        payloads = result.get('payloads', [])
        
        # If no payloads returned, add a default one
        if not payloads:
            payloads.append({
                'technique': 'Basic Detection',
                'payload': '{{ 7*7 }}',
                'description': f'Default detection payload for {engine}'
            })
        
        # Create the data structure for the serializer
        ssti_data = {
            'engine': engine,
            'goal': goal,
            'base_payload': '',  # SSTI doesn't have a base payload
            'payloads': payloads
        }

        # Create and validate serializer
        serializer = ForgedPayloadResultSerializer(data=ssti_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'SSTI payload generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_jwt_api(request):
    """
    API endpoint to analyze a JWT token.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token = data.get('token')
    mode = data.get('mode', 'blue_team')  # Default to blue_team

    if not token:
        return Response(
            {'error': 'Token is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if mode not in ['blue_team', 'red_team']:
        return Response(
            {'error': 'Mode must be either "blue_team" or "red_team"'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Parse the token
        parts = token.split('.')
        if len(parts) != 3:
            return Response(
                {'error': 'Invalid JWT format. Expected format: header.payload.signature'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Decode header and payload
        try:
            # Add padding if needed for base64 decoding
            header_str = base64.urlsafe_b64decode(parts[0] + '==').decode('utf-8')
            payload_str = base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8')

            header = json.loads(header_str)
            payload = json.loads(payload_str)
        except (ValueError, UnicodeDecodeError) as e:
            return Response(
                {'error': f'Invalid JWT encoding: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except json.JSONDecodeError as e:
            return Response(
                {'error': f'Invalid JWT JSON structure: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Analyze the JWT
        analysis_result = analyze_jwt(header, payload, mode)

        # Create a report
        report = {
            'analyzedTarget': f'JWT Analysis - {mode}',
            'vulnerabilities': []
        }

        # Add the analysis result as a vulnerability
        vulnerability = {
            'vulnerability': 'JWT Analysis',
            'severity': 'Info',
            'description': analysis_result,
            'impact': 'See description for details',
            'recommendation': 'See description for details',
            'vulnerableCode': token
        }

        report['vulnerabilities'].append(vulnerability)

        # Create and validate serializer
        serializer = VulnerabilityReportSerializer(data=report)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'JWT analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def generate_xss_payloads_api(request):
    """
    API endpoint to generate XSS payloads for a vulnerability.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    vulnerability = data.get('vulnerability')
    sample_payloads = data.get('samplePayloads')

    if not vulnerability:
        return Response(
            {'error': 'Vulnerability is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate sample_payloads if provided
    if sample_payloads is not None and not isinstance(sample_payloads, list):
        return Response(
            {'error': 'samplePayloads must be a list'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = generate_xss_payloads(vulnerability, sample_payloads)

        # Add the vulnerability to the result
        result['vulnerability'] = json.dumps(vulnerability)

        # Create and validate serializer
        serializer = XssPayloadResultSerializer(data=result)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'XSS payload generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def generate_sqlmap_command_api(request):
    """
    API endpoint to generate a SQLMap command for a SQL injection vulnerability.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    vulnerability = data.get('vulnerability')
    url = data.get('url')

    if not vulnerability or not url:
        return Response(
            {'error': 'Vulnerability and URL are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = generate_sqlmap_command(vulnerability, url)
        return Response(result, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'SQLMap command generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )