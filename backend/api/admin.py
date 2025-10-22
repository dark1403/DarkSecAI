from django.contrib import admin
from django.utils.translation import gettext_lazy as _, ngettext_lazy
from .models import (
    VulnerabilityReport,
    InjectionPoint,
    Vulnerability,
    HeaderFinding,
    HeadersReport,
    DomXssConnectedPath,
    DomXssUnconnectedFinding,
    DomXssAnalysisResult,
    ForgedPayload,
    ForgedPayloadResult,
    XssPayload,
    XssPayloadResult,
    FileUploadAnalysisResult,
    ChatMessage,
    Conversation
)


@admin.register(VulnerabilityReport)
class VulnerabilityReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'analyzed_target', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('analyzed_target',)
    readonly_fields = ('id', 'created_at')


@admin.register(InjectionPoint)
class InjectionPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'parameter', 'method')
    list_filter = ('type', 'method')
    search_fields = ('parameter',)
    # The 'id' field is not explicitly defined in the model, but Django adds it by default for primary keys.
    # If you later define a custom primary key, this might need adjustment.
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('id',) if obj else self.readonly_fields


@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ('vulnerability', 'severity', 'report', 'injection_point')
    list_filter = ('severity', 'report__analyzed_target', 'injection_point__type')
    search_fields = ('vulnerability', 'description', 'recommendation', 'vulnerable_code')
    readonly_fields = ('id',)


@admin.register(HeaderFinding)
class HeaderFindingAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'status', 'severity', 'report')
    list_filter = ('status', 'severity', 'report__analyzed_url')
    search_fields = ('name', 'value', 'recommendation')
    readonly_fields = ('id',)


@admin.register(HeadersReport)
class HeadersReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'analyzed_url', 'overall_score', 'created_at')
    list_filter = ('overall_score', 'created_at')
    search_fields = ('analyzed_url', 'summary')
    readonly_fields = ('id', 'created_at')


@admin.register(DomXssConnectedPath)
class DomXssConnectedPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'sink', 'report')
    list_filter = ('report__created_at',)
    search_fields = ('source', 'sink', 'code_snippet', 'explanation')
    readonly_fields = ('id',)


@admin.register(DomXssUnconnectedFinding)
class DomXssUnconnectedFindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'report')
    list_filter = ('type', 'report__created_at')
    search_fields = ('value',)
    readonly_fields = ('id',)


@admin.register(DomXssAnalysisResult)
class DomXssAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('analyzed_code',)
    readonly_fields = ('id', 'created_at')


@admin.register(ForgedPayload)
class ForgedPayloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'technique', 'result')
    list_filter = ('technique', 'result__engine', 'result__goal')
    search_fields = ('technique', 'description', 'payload')
    readonly_fields = ('id',)


@admin.register(ForgedPayloadResult)
class ForgedPayloadResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_payload', 'engine', 'goal', 'created_at')
    list_filter = ('engine', 'goal', 'created_at')
    search_fields = ('base_payload', 'engine', 'goal')
    readonly_fields = ('id', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.base_payload and obj.payloads.exists():
            obj.base_payload = obj.payloads.first().payload
            obj.save()


@admin.register(XssPayload)
class XssPayloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'mechanism', 'encoding', 'result')
    list_filter = ('mechanism', 'encoding', 'result__vulnerability')
    search_fields = ('payload', 'description', 'mechanism', 'encoding')
    readonly_fields = ('id',)


@admin.register(XssPayloadResult)
class XssPayloadResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'vulnerability', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('explanation', 'vulnerability')
    readonly_fields = ('id', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.vulnerability and obj.payloads.exists():
            obj.vulnerability = obj.payloads.first().description
            obj.save()


@admin.register(FileUploadAnalysisResult)
class FileUploadAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'analyzed_url', 'found', 'created_at')
    list_filter = ('found', 'created_at')
    search_fields = ('analyzed_url', 'description', 'manual_testing_guide')
    readonly_fields = ('id', 'created_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'content', 'created_at')
    list_filter = ('role', 'conversation__title', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('id', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    readonly_fields = ('id', 'created_at')
