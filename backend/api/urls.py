import logging
from django.urls import path, include
from rest_framework.routers import DefaultRouter

logger = logging.getLogger(__name__)

from .views import (
    VulnerabilityReportViewSet, HeadersReportViewSet, DomXssAnalysisResultViewSet,
    ForgedPayloadResultViewSet, XssPayloadResultViewSet, FileUploadAnalysisResultViewSet,
    ConversationViewSet,
    analyze_url_api, analyze_code_api, analyze_js_code_api, analyze_dom_xss_api,
    analyze_headers_api, analyze_file_upload_api, find_privesc_exploits_api,
    forge_payloads_api, generate_ssti_payloads_api, analyze_jwt_api,
    generate_xss_payloads_api, generate_sqlmap_command_api,
    ChatMessageAPIView
)
from .views.auth_views import login_view, register_view, verify_token_view, user_view
from .views.admin_views import admin_stats_view
from .views.admin_viewsets import (
    VulnerabilityReportAdminViewSet,
    VulnerabilityAdminViewSet,
    InjectionPointAdminViewSet,
    HeadersReportAdminViewSet,
    HeaderFindingAdminViewSet,
    DomXssAnalysisResultAdminViewSet,
    DomXssConnectedPathAdminViewSet,
    DomXssUnconnectedFindingAdminViewSet,
    ForgedPayloadResultAdminViewSet,
    ForgedPayloadAdminViewSet,
    XssPayloadResultAdminViewSet,
    XssPayloadAdminViewSet,
    FileUploadAnalysisResultAdminViewSet,
    ConversationAdminViewSet,
    ChatMessageAdminViewSet,
)

logger.info("Loading API URLs configuration...")
logger.info(f"Login view function: {login_view}")
logger.info(f"Register view function: {register_view}")

router = DefaultRouter()
router.register(r'reports', VulnerabilityReportViewSet)
router.register(r'headers-reports', HeadersReportViewSet)
router.register(r'dom-xss-results', DomXssAnalysisResultViewSet)
router.register(r'forged-payloads', ForgedPayloadResultViewSet)
router.register(r'xss-payloads', XssPayloadResultViewSet)
router.register(r'file-upload-results', FileUploadAnalysisResultViewSet)
router.register(r'conversations', ConversationViewSet)

# Admin router with restricted CRUD for all models
admin_router = DefaultRouter()
admin_router.register(r'vulnerability-reports', VulnerabilityReportAdminViewSet)
admin_router.register(r'vulnerabilities', VulnerabilityAdminViewSet)
admin_router.register(r'injection-points', InjectionPointAdminViewSet)
admin_router.register(r'headers-reports', HeadersReportAdminViewSet)
admin_router.register(r'header-findings', HeaderFindingAdminViewSet)
admin_router.register(r'dom-xss-results', DomXssAnalysisResultAdminViewSet)
admin_router.register(r'dom-xss-connected-paths', DomXssConnectedPathAdminViewSet)
admin_router.register(r'dom-xss-unconnected-findings', DomXssUnconnectedFindingAdminViewSet)
admin_router.register(r'forged-payload-results', ForgedPayloadResultAdminViewSet)
admin_router.register(r'forged-payloads', ForgedPayloadAdminViewSet)
admin_router.register(r'xss-payload-results', XssPayloadResultAdminViewSet)
admin_router.register(r'xss-payloads', XssPayloadAdminViewSet)
admin_router.register(r'file-upload-results', FileUploadAnalysisResultAdminViewSet)
admin_router.register(r'conversations', ConversationAdminViewSet)
admin_router.register(r'chat-messages', ChatMessageAdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/verify-token/', verify_token_view, name='verify-token'),
    path('auth/user/', user_view, name='user'),
    # Admin endpoints
    path('admin/', include(admin_router.urls)),
    path('admin/stats/', admin_stats_view, name='admin-stats'),
    
    # Analysis endpoints
    path('analyze/url/', analyze_url_api, name='analyze-url'),
    path('analyze/code/', analyze_code_api, name='analyze-code'),
    path('analyze/js-code/', analyze_js_code_api, name='analyze-js-code'),
    path('analyze/dom-xss/', analyze_dom_xss_api, name='analyze-dom-xss'),
    path('analyze/headers/', analyze_headers_api, name='analyze-headers'),
    path('analyze/file-upload/', analyze_file_upload_api, name='analyze-file-upload'),
    path('analyze/privesc/', find_privesc_exploits_api, name='find-privesc-exploits'),
    
    # Payload endpoints
    path('forge/payloads/', forge_payloads_api, name='forge-payloads'),
    path('forge/ssti-payloads/', generate_ssti_payloads_api, name='generate-ssti-payloads'),
    path('analyze/jwt/', analyze_jwt_api, name='analyze-jwt'),
    path('generate/xss-payloads/', generate_xss_payloads_api, name='generate-xss-payloads'),
    path('generate/sqlmap-command/', generate_sqlmap_command_api, name='generate-sqlmap-command'),
    
    # Chat endpoints
    path('chat/messages/', ChatMessageAPIView.as_view(), name='chat-messages'),
]
