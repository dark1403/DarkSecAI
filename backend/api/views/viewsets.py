from rest_framework import viewsets

from ..models import (
    VulnerabilityReport, HeadersReport, DomXssAnalysisResult,
    ForgedPayloadResult, XssPayloadResult, FileUploadAnalysisResult,
    Conversation
)
from ..serializers import (
    VulnerabilityReportSerializer, HeadersReportSerializer, 
    DomXssAnalysisResultSerializer, ForgedPayloadResultSerializer,
    XssPayloadResultSerializer, FileUploadAnalysisResultSerializer,
    ConversationSerializer
)

class VulnerabilityReportViewSet(viewsets.ModelViewSet):
    queryset = VulnerabilityReport.objects.all().order_by('-created_at')
    serializer_class = VulnerabilityReportSerializer

class HeadersReportViewSet(viewsets.ModelViewSet):
    queryset = HeadersReport.objects.all().order_by('-created_at')
    serializer_class = HeadersReportSerializer

class DomXssAnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = DomXssAnalysisResult.objects.all().order_by('-created_at')
    serializer_class = DomXssAnalysisResultSerializer

class ForgedPayloadResultViewSet(viewsets.ModelViewSet):
    queryset = ForgedPayloadResult.objects.all().order_by('-created_at')
    serializer_class = ForgedPayloadResultSerializer

class XssPayloadResultViewSet(viewsets.ModelViewSet):
    queryset = XssPayloadResult.objects.all().order_by('-created_at')
    serializer_class = XssPayloadResultSerializer

class FileUploadAnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = FileUploadAnalysisResult.objects.all().order_by('-created_at')
    serializer_class = FileUploadAnalysisResultSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
