from django.contrib import admin
from .models import IntegrationConfig, WebhookEvent, APILog


@admin.register(IntegrationConfig)
class IntegrationConfigAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'provider_name', 'integration_type', 'region',
        'is_active', 'is_test_mode', 'updated_at'
    )
    list_filter = ('integration_type', 'is_active', 'is_test_mode', 'region')
    search_fields = ('name', 'provider_name', 'api_endpoint')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Integration Information', {
            'fields': ('name', 'integration_type', 'provider_name', 'region', 'is_active', 'is_test_mode')
        }),
        ('API Configuration', {
            'fields': ('api_endpoint', 'api_key', 'api_secret', 'configuration')
        }),
        ('Webhook Configuration', {
            'fields': ('webhook_url', 'webhook_secret')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = (
        'integration', 'event_type', 'status', 'received_at',
        'processed_at', 'ip_address'
    )
    list_filter = ('status', 'integration', 'event_type', 'received_at')
    search_fields = ('event_type', 'integration__provider_name', 'error_message')
    readonly_fields = ('received_at', 'processed_at')
    
    fieldsets = (
        ('Event Information', {
            'fields': ('integration', 'event_type', 'status')
        }),
        ('Payload', {
            'fields': ('payload',)
        }),
        ('Processing', {
            'fields': ('processed_at', 'error_message')
        }),
        ('Request Details', {
            'fields': ('headers', 'ip_address', 'received_at')
        }),
    )


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = (
        'integration', 'request_method', 'endpoint', 'response_status',
        'is_success', 'duration_ms', 'created_at'
    )
    list_filter = ('is_success', 'integration', 'request_method', 'response_status', 'created_at')
    search_fields = ('endpoint', 'integration__provider_name', 'error_message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('integration', 'request_method', 'endpoint', 'request_data')
        }),
        ('Response Information', {
            'fields': ('response_status', 'response_data', 'duration_ms')
        }),
        ('Status', {
            'fields': ('is_success', 'error_message')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


