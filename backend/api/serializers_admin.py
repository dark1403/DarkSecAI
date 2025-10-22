from rest_framework import serializers

from .models import (
    VulnerabilityReport, Vulnerability, InjectionPoint,
    HeadersReport, HeaderFinding, DomXssAnalysisResult,
    DomXssConnectedPath, DomXssUnconnectedFinding,
    ForgedPayloadResult, ForgedPayload, XssPayloadResult,
    XssPayload, FileUploadAnalysisResult, ChatMessage,
    Conversation
)


class VulnerabilityReportAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulnerabilityReport
        fields = '__all__'


class VulnerabilityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__'


class InjectionPointAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjectionPoint
        fields = '__all__'


class HeadersReportAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadersReport
        fields = '__all__'


class HeaderFindingAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderFinding
        fields = '__all__'


class DomXssAnalysisResultAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomXssAnalysisResult
        fields = '__all__'


class DomXssConnectedPathAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomXssConnectedPath
        fields = '__all__'


class DomXssUnconnectedFindingAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomXssUnconnectedFinding
        fields = '__all__'


class ForgedPayloadResultAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgedPayloadResult
        fields = '__all__'


class ForgedPayloadAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgedPayload
        fields = '__all__'


class XssPayloadResultAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = XssPayloadResult
        fields = '__all__'


class XssPayloadAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = XssPayload
        fields = '__all__'


class FileUploadAnalysisResultAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadAnalysisResult
        fields = '__all__'


class ConversationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class ChatMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

