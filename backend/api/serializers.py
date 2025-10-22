from rest_framework import serializers
from .models import (
    VulnerabilityReport, Vulnerability, InjectionPoint,
    HeadersReport, HeaderFinding, DomXssAnalysisResult,
    DomXssConnectedPath, DomXssUnconnectedFinding,
    ForgedPayloadResult, ForgedPayload, XssPayloadResult,
    XssPayload, FileUploadAnalysisResult, ChatMessage,
    Conversation
)

class InjectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjectionPoint
        fields = ['type', 'parameter', 'method']

class VulnerabilitySerializer(serializers.ModelSerializer):
    injection_point = InjectionPointSerializer(required=False, allow_null=True)
    vulnerable_code = serializers.CharField(required=False, allow_blank=True, default='')
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    impact = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    recommendation = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Vulnerability
        fields = ['vulnerability', 'severity', 'description', 'impact', 
                  'recommendation', 'vulnerable_code', 'injection_point']
    
    def create(self, validated_data):
        injection_point_data = validated_data.pop('injection_point', None)
        vulnerability = Vulnerability.objects.create(**validated_data)
        
        if injection_point_data:
            InjectionPoint.objects.create(vulnerability=vulnerability, **injection_point_data)
        
        return vulnerability

class VulnerabilityReportSerializer(serializers.ModelSerializer):
    vulnerabilities = VulnerabilitySerializer(many=True, required=False)
    analyzed_target = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = VulnerabilityReport
        fields = ['id', 'analyzed_target', 'vulnerabilities', 'created_at']
    
    def create(self, validated_data):
        vulnerabilities_data = validated_data.pop('vulnerabilities', [])
        report = VulnerabilityReport.objects.create(**validated_data)
        
        for vulnerability_data in vulnerabilities_data:
            injection_point_data = vulnerability_data.pop('injection_point', None)
            vulnerability = Vulnerability.objects.create(report=report, **vulnerability_data)
            
            if injection_point_data:
                InjectionPoint.objects.create(vulnerability=vulnerability, **injection_point_data)
        
        return report

class HeaderFindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderFinding
        fields = ['name', 'value', 'status', 'recommendation', 'severity']

class HeadersReportSerializer(serializers.ModelSerializer):
    findings = HeaderFindingSerializer(many=True, required=False)
    analyzed_url = serializers.CharField(required=False, allow_blank=True)
    overall_score = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    summary = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = HeadersReport
        fields = ['id', 'analyzed_url', 'overall_score', 'summary', 'findings', 'created_at']
    
    def create(self, validated_data):
        findings_data = validated_data.pop('findings', [])
        report = HeadersReport.objects.create(**validated_data)
        
        for finding_data in findings_data:
            HeaderFinding.objects.create(report=report, **finding_data)
        
        return report

class DomXssConnectedPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomXssConnectedPath
        fields = ['source', 'sink', 'code_snippet', 'explanation']

class DomXssUnconnectedFindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomXssUnconnectedFinding
        fields = ['type', 'value']

class DomXssAnalysisResultSerializer(serializers.ModelSerializer):
    connected_paths = DomXssConnectedPathSerializer(many=True, required=False)
    unconnected_findings = DomXssUnconnectedFindingSerializer(many=True, required=False)
    analyzed_code = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = DomXssAnalysisResult
        fields = ['id', 'analyzed_code', 'connected_paths', 'unconnected_findings', 'created_at']
    
    def create(self, validated_data):
        connected_paths_data = validated_data.pop('connected_paths', [])
        unconnected_findings_data = validated_data.pop('unconnected_findings', [])
        result = DomXssAnalysisResult.objects.create(**validated_data)
        
        for path_data in connected_paths_data:
            DomXssConnectedPath.objects.create(report=result, **path_data)
        
        for finding_data in unconnected_findings_data:
            DomXssUnconnectedFinding.objects.create(report=result, **finding_data)
        
        return result

class ForgedPayloadSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = ForgedPayload
        fields = ['technique', 'description', 'payload']

class ForgedPayloadResultSerializer(serializers.ModelSerializer):
    payloads = ForgedPayloadSerializer(many=True, required=False)
    base_payload = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = ForgedPayloadResult
        fields = ['id', 'base_payload', 'engine', 'goal', 'payloads', 'created_at']
    
    def create(self, validated_data):
        payloads_data = validated_data.pop('payloads', [])
        result = ForgedPayloadResult.objects.create(**validated_data)
        
        for payload_data in payloads_data:
            ForgedPayload.objects.create(result=result, **payload_data)
        
        return result

class XssPayloadSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = XssPayload
        fields = ['payload', 'description', 'mechanism', 'encoding']

class XssPayloadResultSerializer(serializers.ModelSerializer):
    payloads = XssPayloadSerializer(many=True, required=False)
    explanation = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = XssPayloadResult
        fields = ['id', 'explanation', 'vulnerability', 'payloads', 'created_at']
    
    def create(self, validated_data):
        payloads_data = validated_data.pop('payloads', [])
        result = XssPayloadResult.objects.create(**validated_data)
        
        for payload_data in payloads_data:
            XssPayload.objects.create(result=result, **payload_data)
        
        return result

class FileUploadAnalysisResultSerializer(serializers.ModelSerializer):
    analyzed_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    manual_testing_guide = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = FileUploadAnalysisResult
        fields = ['id', 'analyzed_url', 'found', 'description', 'manual_testing_guide', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = ChatMessage
        fields = ['role', 'content', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'messages', 'created_at']
