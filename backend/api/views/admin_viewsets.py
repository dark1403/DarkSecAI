from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import (
    VulnerabilityReport, Vulnerability, InjectionPoint,
    HeadersReport, HeaderFinding, DomXssAnalysisResult,
    DomXssConnectedPath, DomXssUnconnectedFinding,
    ForgedPayloadResult, ForgedPayload, XssPayloadResult,
    XssPayload, FileUploadAnalysisResult, Conversation, ChatMessage
)
from ..serializers_admin import (
    VulnerabilityReportAdminSerializer, VulnerabilityAdminSerializer, InjectionPointAdminSerializer,
    HeadersReportAdminSerializer, HeaderFindingAdminSerializer, DomXssAnalysisResultAdminSerializer,
    DomXssConnectedPathAdminSerializer, DomXssUnconnectedFindingAdminSerializer,
    ForgedPayloadResultAdminSerializer, ForgedPayloadAdminSerializer, XssPayloadResultAdminSerializer,
    XssPayloadAdminSerializer, FileUploadAnalysisResultAdminSerializer, ConversationAdminSerializer,
    ChatMessageAdminSerializer
)


class BaseAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]


class VulnerabilityReportAdminViewSet(BaseAdminViewSet):
    queryset = VulnerabilityReport.objects.all().order_by('-created_at')
    serializer_class = VulnerabilityReportAdminSerializer


class VulnerabilityAdminViewSet(BaseAdminViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilityAdminSerializer


class InjectionPointAdminViewSet(BaseAdminViewSet):
    queryset = InjectionPoint.objects.all()
    serializer_class = InjectionPointAdminSerializer


class HeadersReportAdminViewSet(BaseAdminViewSet):
    queryset = HeadersReport.objects.all().order_by('-created_at')
    serializer_class = HeadersReportAdminSerializer


class HeaderFindingAdminViewSet(BaseAdminViewSet):
    queryset = HeaderFinding.objects.all()
    serializer_class = HeaderFindingAdminSerializer


class DomXssAnalysisResultAdminViewSet(BaseAdminViewSet):
    queryset = DomXssAnalysisResult.objects.all().order_by('-created_at')
    serializer_class = DomXssAnalysisResultAdminSerializer


class DomXssConnectedPathAdminViewSet(BaseAdminViewSet):
    queryset = DomXssConnectedPath.objects.all()
    serializer_class = DomXssConnectedPathAdminSerializer


class DomXssUnconnectedFindingAdminViewSet(BaseAdminViewSet):
    queryset = DomXssUnconnectedFinding.objects.all()
    serializer_class = DomXssUnconnectedFindingAdminSerializer


class ForgedPayloadResultAdminViewSet(BaseAdminViewSet):
    queryset = ForgedPayloadResult.objects.all().order_by('-created_at')
    serializer_class = ForgedPayloadResultAdminSerializer


class ForgedPayloadAdminViewSet(BaseAdminViewSet):
    queryset = ForgedPayload.objects.all()
    serializer_class = ForgedPayloadAdminSerializer


class XssPayloadResultAdminViewSet(BaseAdminViewSet):
    queryset = XssPayloadResult.objects.all().order_by('-created_at')
    serializer_class = XssPayloadResultAdminSerializer


class XssPayloadAdminViewSet(BaseAdminViewSet):
    queryset = XssPayload.objects.all()
    serializer_class = XssPayloadAdminSerializer


class FileUploadAnalysisResultAdminViewSet(BaseAdminViewSet):
    queryset = FileUploadAnalysisResult.objects.all().order_by('-created_at')
    serializer_class = FileUploadAnalysisResultAdminSerializer


class ConversationAdminViewSet(BaseAdminViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationAdminSerializer


class ChatMessageAdminViewSet(BaseAdminViewSet):
    queryset = ChatMessage.objects.all().order_by('-created_at')
    serializer_class = ChatMessageAdminSerializer

