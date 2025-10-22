from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from ..models import (
    VulnerabilityReport,
    Vulnerability,
    HeadersReport,
    DomXssAnalysisResult,
    ForgedPayloadResult,
    XssPayloadResult,
    FileUploadAnalysisResult,
    Conversation,
)


User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_stats_view(request):
    """
    Return aggregate admin statistics. Admins only.
    """
    user = request.user
    if not user.is_staff:
        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    # Core counts
    users_total = User.objects.count()
    admins_total = User.objects.filter(is_staff=True).count()

    reports_total = VulnerabilityReport.objects.count()
    vulnerabilities_total = Vulnerability.objects.count()
    headers_reports_total = HeadersReport.objects.count()
    domxss_results_total = DomXssAnalysisResult.objects.count()
    payload_results_total = ForgedPayloadResult.objects.count()
    xss_payload_results_total = XssPayloadResult.objects.count()
    file_upload_results_total = FileUploadAnalysisResult.objects.count()
    conversations_total = Conversation.objects.count()

    # API keys configured (do not expose values)
    api_keys_configured = 0
    api_keys = {
        "GEMINI_API_KEY": bool(getattr(settings, "GEMINI_API_KEY", None)),
    }
    api_keys_configured = sum(1 for v in api_keys.values() if v)

    # Build a simple last event timestamp across entities with created_at
    timestamps = []
    def take_latest(qs, field="created_at"):
        item = qs.order_by(f"-{field}").values_list(field, flat=True).first()
        if item:
            timestamps.append(item)

    take_latest(VulnerabilityReport.objects.all())
    take_latest(HeadersReport.objects.all())
    take_latest(DomXssAnalysisResult.objects.all())
    take_latest(ForgedPayloadResult.objects.all())
    take_latest(XssPayloadResult.objects.all())
    take_latest(FileUploadAnalysisResult.objects.all())
    take_latest(Conversation.objects.all())

    last_event = max(timestamps).isoformat() if timestamps else None

    # A simple aggregate of activity as an "audit events" proxy
    audit_events = (
        reports_total
        + headers_reports_total
        + domxss_results_total
        + payload_results_total
        + xss_payload_results_total
        + file_upload_results_total
        + conversations_total
    )

    # Severity breakdown for discovered vulnerabilities
    severity_qs = Vulnerability.objects.values('severity').annotate(count=Count('id'))
    severity_breakdown = {row['severity']: row['count'] for row in severity_qs}

    return Response({
        "users_total": users_total,
        "admins_total": admins_total,
        "reports_total": reports_total,
        "vulnerabilities_total": vulnerabilities_total,
        "headers_reports_total": headers_reports_total,
        "domxss_results_total": domxss_results_total,
        "payload_results_total": payload_results_total,
        "xss_payload_results_total": xss_payload_results_total,
        "file_upload_results_total": file_upload_results_total,
        "conversations_total": conversations_total,
        "api_keys_configured": api_keys_configured,
        "api_keys": api_keys,
        "last_event": last_event,
        "audit_events": audit_events,
        "severity_breakdown": severity_breakdown,
    })
