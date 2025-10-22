from django.db import models
from django.utils import timezone
import uuid

class Severity(models.TextChoices):
    CRITICAL = 'Critical', 'Critical'
    HIGH = 'High', 'High'
    MEDIUM = 'Medium', 'Medium'
    LOW = 'Low', 'Low'
    INFO = 'Info', 'Info'
    UNKNOWN = 'Unknown', 'Unknown'

class InjectionPointType(models.TextChoices):
    URL_PARAM = 'URL_PARAM', 'URL Parameter'
    POST_PARAM = 'POST_PARAM', 'POST Parameter'
    PATH = 'PATH', 'Path'

class HttpMethod(models.TextChoices):
    GET = 'GET', 'GET'
    POST = 'POST', 'POST'

class VulnerabilityReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    analyzed_target = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.analyzed_target} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class InjectionPoint(models.Model):
    type = models.CharField(max_length=20, choices=InjectionPointType.choices)
    parameter = models.CharField(max_length=100, blank=True, null=True)
    method = models.CharField(max_length=10, choices=HttpMethod.choices, blank=True, null=True)
    
    def __str__(self):
        return f"{self.type} - {self.parameter}"

class Vulnerability(models.Model):
    report = models.ForeignKey(VulnerabilityReport, related_name='vulnerabilities', on_delete=models.CASCADE)
    vulnerability = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.UNKNOWN)
    description = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    vulnerable_code = models.TextField(blank=True, default='')
    injection_point = models.ForeignKey(InjectionPoint, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vulnerability} - {self.severity}"

class HeaderFinding(models.Model):
    class Status(models.TextChoices):
        PRESENT_GOOD = 'Present - Good', 'Present - Good'
        PRESENT_MISCONFIGURED = 'Present - Misconfigured', 'Present - Misconfigured'
        MISSING = 'Missing', 'Missing'

    name = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=Status.choices)
    recommendation = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=[(s, s) for s in ['High', 'Medium', 'Low', 'Info']])
    report = models.ForeignKey('HeadersReport', related_name='findings', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.status}"

class HeadersReport(models.Model):
    class Score(models.TextChoices):
        A_PLUS = 'A+', 'A+'
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        F = 'F', 'F'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    analyzed_url = models.CharField(max_length=512, blank=True, null=True)
    overall_score = models.CharField(max_length=2, choices=Score.choices, blank=True, null=True)
    summary = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.analyzed_url} - {self.overall_score}"

class DomXssConnectedPath(models.Model):
    source = models.CharField(max_length=255)
    sink = models.CharField(max_length=255)
    code_snippet = models.TextField(blank=True, default='')
    explanation = models.TextField(blank=True, null=True)
    report = models.ForeignKey('DomXssAnalysisResult', related_name='connected_paths', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.source} -> {self.sink}"

class DomXssUnconnectedFinding(models.Model):
    class FindingType(models.TextChoices):
        SOURCE = 'source', 'Source'
        SINK = 'sink', 'Sink'
        
    type = models.CharField(max_length=10, choices=FindingType.choices)
    value = models.CharField(max_length=255, blank=True, default='')
    report = models.ForeignKey('DomXssAnalysisResult', related_name='unconnected_findings', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.type}: {self.value}"

class DomXssAnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    analyzed_code = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"DOM XSS Analysis - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ForgedPayload(models.Model):
    technique = models.CharField(max_length=255)
    description = models.TextField()
    payload = models.TextField(blank=True, default='')
    result = models.ForeignKey('ForgedPayloadResult', related_name='payloads', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.technique

class ForgedPayloadResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_payload = models.TextField(blank=True, default='')
    engine = models.CharField(max_length=100, null=True, blank=True)  # For SSTI
    goal = models.CharField(max_length=255, null=True, blank=True)  # For SSTI
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.engine:
            return f"SSTI Forge - {self.engine}"
        return f"Payload Forge - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class XssPayload(models.Model):
    payload = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    mechanism = models.CharField(max_length=255)
    encoding = models.CharField(max_length=255)
    result = models.ForeignKey('XssPayloadResult', related_name='payloads', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.mechanism

class XssPayloadResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    explanation = models.TextField(blank=True, default='')
    vulnerability = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"XSS Payload Result - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class FileUploadAnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    analyzed_url = models.CharField(max_length=512, blank=True, null=True)
    found = models.BooleanField()
    description = models.TextField(blank=True, default='')
    manual_testing_guide = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"File Upload Analysis - {self.analyzed_url}"

class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        MODEL = 'model', 'Model'
        SYSTEM = 'system', 'System'
        
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField(blank=True, default='')
    conversation = models.ForeignKey('Conversation', related_name='messages', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="New Conversation")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title