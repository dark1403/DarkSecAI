from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from ..serializers import (
    VulnerabilityReportSerializer, DomXssAnalysisResultSerializer,
    HeadersReportSerializer, FileUploadAnalysisResultSerializer
)
from ..services_new import (
    analyze_url, analyze_code, analyze_js_code, analyze_dom_xss,
    analyze_headers, analyze_file_upload, consolidate_reports,
    perform_deep_analysis, validate_vulnerability, find_privesc_exploits
)
from ..ml_integration import enrich_vulnerability_with_ml, batch_enrich_vulnerabilities


@api_view(['POST'])
def analyze_url_api(request):
    """
    API endpoint to analyze a URL for vulnerabilities.
    
    Performs multi-pass recursive scanning with optional validation and deep analysis.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = data.get('url')
    scan_type = data.get('scanType', 'active')
    depth = data.get('depth', 3)
    validate_findings = data.get('validateFindings', True)
    deep_analysis = data.get('deepAnalysis', False)

    # Validation
    if not url:
        return Response(
            {'error': 'URL is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not isinstance(depth, int) or depth < 1 or depth > 10:
        return Response(
            {'error': 'Depth must be an integer between 1 and 10'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Phase 1: Recursive Scanning
        reports = []
        last_error = None
        
        for i in range(depth):
            try:
                result = analyze_url(url, scan_type, i)
                if result and isinstance(result, dict):
                    reports.append(result)
            except Exception as e:
                last_error = str(e)
                continue

        if not reports:
            error_msg = f'All {depth} analysis attempts failed'
            if last_error:
                error_msg += f': {last_error}'
            return Response(
                {'error': error_msg}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Phase 2: Consolidation
        if len(reports) > 1:
            try:
                base_report = consolidate_reports(reports)
            except Exception as e:
                # If consolidation fails, use the first report
                base_report = reports[0]
        else:
            base_report = reports[0]

        # Phase 3: ML Enrichment (NEW STAGE)
        if base_report.get('vulnerabilities'):
            # Enrich ALL vulnerabilities with ML predictions BEFORE validation/deep analysis
            base_report['vulnerabilities'] = batch_enrich_vulnerabilities(
                base_report['vulnerabilities']
            )
        
        # Phase 4: Validation & Deep Analysis (using ML-enriched data)
        if base_report.get('vulnerabilities'):
            processed_vulnerabilities = []
            
            for vuln in base_report['vulnerabilities']:
                # Validate findings if requested (now with ML context)
                if validate_findings:
                    try:
                        validation_result = validate_vulnerability(vuln)
                        if not validation_result.get('is_valid', True):
                            continue
                    except Exception:
                        pass

                # Perform deep analysis if requested (now with ML context)
                if deep_analysis:
                    try:
                        enriched_vuln = perform_deep_analysis(vuln, url)
                        processed_vulnerabilities.append(enriched_vuln)
                    except Exception:
                        processed_vulnerabilities.append(vuln)
                else:
                    processed_vulnerabilities.append(vuln)

            base_report['vulnerabilities'] = processed_vulnerabilities

        # Create and validate serializer
        serializer = VulnerabilityReportSerializer(data=base_report)

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_code_api(request):
    """
    API endpoint to analyze code for vulnerabilities.
    
    Performs multi-pass static analysis with optional deep analysis.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    code = data.get('code')
    depth = data.get('depth', 3)
    deep_analysis = data.get('deepAnalysis', False)

    # Validation
    if not code:
        return Response(
            {'error': 'Code is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not isinstance(depth, int) or depth < 1 or depth > 10:
        return Response(
            {'error': 'Depth must be an integer between 1 and 10'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Phase 1: Recursive Scanning
        reports = []
        last_error = None
        
        for i in range(depth):
            try:
                result = analyze_code(code, i)
                if result and isinstance(result, dict):
                    reports.append(result)
            except Exception as e:
                last_error = str(e)
                continue

        if not reports:
            error_msg = f'All {depth} analysis attempts failed'
            if last_error:
                error_msg += f': {last_error}'
            return Response(
                {'error': error_msg}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Add ML enrichment before deep analysis
        for i, report in enumerate(reports):
            if report.get('vulnerabilities'):
                reports[i]['vulnerabilities'] = batch_enrich_vulnerabilities(
                    report['vulnerabilities']
                )
        
        # Phase 2: Consolidation
        if len(reports) > 1:
            try:
                base_report = consolidate_reports(reports)
            except Exception:
                # If consolidation fails, use the first report
                base_report = reports[0]
        else:
            base_report = reports[0]

        # Phase 3: Deep Analysis
        if deep_analysis and base_report.get('vulnerabilities'):
            processed_vulnerabilities = []
            
            for vuln in base_report['vulnerabilities']:
                try:
                    enriched_vuln = perform_deep_analysis(vuln, "Code Analysis")
                    processed_vulnerabilities.append(enriched_vuln)
                except Exception:
                    # If deep analysis fails, keep original vulnerability
                    processed_vulnerabilities.append(vuln)

            base_report['vulnerabilities'] = processed_vulnerabilities

        # Create and validate serializer
        serializer = VulnerabilityReportSerializer(data=base_report)

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_js_code_api(request):
    """
    API endpoint to analyze JavaScript code for reconnaissance.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    code = data.get('code')

    if not code:
        return Response(
            {'error': 'Code is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = analyze_js_code(code)

        # Transform JS Recon result into VulnerabilityReport format
        vulnerabilities = []
        
        # Add endpoints as findings
        if result.get('endpoints'):
            endpoints_str = '\n'.join(result['endpoints'])
            vulnerabilities.append({
                'vulnerability': 'API Endpoints Discovered',
                'severity': 'Info',
                'description': f"Found {len(result['endpoints'])} API endpoints in the JavaScript code.",
                'impact': 'These endpoints may expose functionality or data that could be targeted.',
                'recommendation': 'Review each endpoint for proper authentication and authorization.',
                'vulnerable_code': endpoints_str
            })
        
        # Add authentication info
        if result.get('authentication'):
            vulnerabilities.append({
                'vulnerability': 'Authentication Mechanism',
                'severity': 'Info',
                'description': 'Authentication mechanism detected in JavaScript code.',
                'impact': 'Understanding authentication helps identify potential bypasses.',
                'recommendation': 'Ensure authentication is implemented server-side, not just client-side.',
                'vulnerable_code': result['authentication']
            })
        
        # Add data handling info
        if result.get('data_handling'):
            vulnerabilities.append({
                'vulnerability': 'Data Handling',
                'severity': 'Info',
                'description': 'Data handling patterns detected in JavaScript code.',
                'impact': 'Improper data handling could lead to vulnerabilities.',
                'recommendation': 'Validate and sanitize all data on the server-side.',
                'vulnerable_code': result['data_handling']
            })
        
        # Add third-party libraries
        if result.get('third_party_libraries'):
            libs_str = '\n'.join(result['third_party_libraries'])
            vulnerabilities.append({
                'vulnerability': 'Third-Party Libraries',
                'severity': 'Info',
                'description': f"Found {len(result['third_party_libraries'])} third-party libraries.",
                'impact': 'Outdated libraries may contain known vulnerabilities.',
                'recommendation': 'Check each library for known CVEs and update to latest versions.',
                'vulnerable_code': libs_str
            })
        
        # Add security configs
        if result.get('security_configs'):
            vulnerabilities.append({
                'vulnerability': 'Security Configuration',
                'severity': 'Info',
                'description': 'Security configuration detected in JavaScript code.',
                'impact': 'Client-side security configs can be inspected by attackers.',
                'recommendation': 'Move sensitive security configurations to the server-side.',
                'vulnerable_code': result['security_configs']
            })
        
        # Create report structure
        report = {
            'analyzed_target': 'JavaScript Code Analysis',
            'vulnerabilities': vulnerabilities
        }

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_dom_xss_api(request):
    """
    API endpoint to analyze code for DOM XSS vulnerabilities.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    code = data.get('code')

    if not code:
        return Response(
            {'error': 'Code is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = analyze_dom_xss(code)

        # Add the analyzed code to the result
        result['analyzed_code'] = code

        # Create and validate serializer
        serializer = DomXssAnalysisResultSerializer(data=result)

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_headers_api(request):
    """
    API endpoint to analyze security headers of a URL.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = data.get('url')

    if not url:
        return Response(
            {'error': 'URL is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = analyze_headers(url)

        # Create and validate serializer
        serializer = HeadersReportSerializer(data=result)

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def analyze_file_upload_api(request):
    """
    API endpoint to analyze a URL for file upload vulnerabilities.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = data.get('url')

    if not url:
        return Response(
            {'error': 'URL is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = analyze_file_upload(url)

        # Add the analyzed URL to the result
        result['analyzed_url'] = url
        
        # Ensure manual_testing_guide has a default value
        if 'manual_testing_guide' not in result or not result['manual_testing_guide']:
            result['manual_testing_guide'] = ''

        # Create and validate serializer
        serializer = FileUploadAnalysisResultSerializer(data=result)

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def find_privesc_exploits_api(request):
    """
    API endpoint to find privilege escalation exploits for a technology.
    """
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(
            {'error': f'Invalid JSON: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    technology = data.get('technology')
    version = data.get('version')

    if not technology or not version:
        return Response(
            {'error': 'Technology and version are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = find_privesc_exploits(technology, version)

        # Transform PrivEsc result into VulnerabilityReport format
        vulnerabilities = []
        
        # Convert vulnerability strings to proper vulnerability objects
        if result.get('vulnerabilities'):
            for vuln_str in result['vulnerabilities']:
                vulnerabilities.append({
                    'vulnerability': 'Privilege Escalation Vulnerability',
                    'severity': 'High',
                    'description': vuln_str,
                    'impact': result.get('impact', 'Privilege escalation could allow attackers to gain elevated access.'),
                    'recommendation': 'Review mitigation strategies below.',
                    'vulnerable_code': f'{technology} {version}'
                })
        
        # Add exploit techniques as additional findings
        if result.get('exploit_techniques'):
            for technique in result['exploit_techniques']:
                vulnerabilities.append({
                    'vulnerability': 'Exploitation Technique',
                    'severity': 'Medium',
                    'description': technique,
                    'impact': 'This technique could be used to exploit the identified vulnerabilities.',
                    'recommendation': 'Implement security controls to prevent this exploitation method.',
                    'vulnerable_code': technique
                })
        
        # If no vulnerabilities found, add an informational entry
        if not vulnerabilities:
            vulnerabilities.append({
                'vulnerability': 'No Known Vulnerabilities',
                'severity': 'Info',
                'description': f'No publicly known privilege escalation vulnerabilities found for {technology} {version}.',
                'impact': 'This does not guarantee the software is secure.',
                'recommendation': 'Continue monitoring security advisories and conduct manual testing.',
                'vulnerable_code': f'{technology} {version}'
            })
        
        # Add mitigation as a separate finding if available
        if result.get('mitigation'):
            mitigation_str = '\n'.join(result['mitigation']) if isinstance(result['mitigation'], list) else result['mitigation']
            vulnerabilities.append({
                'vulnerability': 'Mitigation Strategies',
                'severity': 'Info',
                'description': 'Recommended mitigation strategies for privilege escalation vulnerabilities.',
                'impact': 'Proper mitigation can prevent successful exploitation.',
                'recommendation': mitigation_str,
                'vulnerable_code': 'N/A'
            })
        
        # Create report structure
        report = {
            'analyzed_target': f'{technology} {version}',
            'vulnerabilities': vulnerabilities
        }

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
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )