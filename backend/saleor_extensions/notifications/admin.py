from django.contrib import admin
from .models import EmailTemplate, SMSTemplate, WhatsAppTemplate, NotificationLog, NotificationTrigger


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'subject', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'subject', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'code', 'category', 'description', 'is_active')
        }),
        ('Content', {
            'fields': ('subject', 'body_text', 'body_html')
        }),
        ('Variables', {
            'fields': ('available_variables',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'message_preview', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'code', 'category', 'description', 'is_active')
        }),
        ('Content', {
            'fields': ('message',)
        }),
        ('Variables', {
            'fields': ('available_variables',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(WhatsAppTemplate)
class WhatsAppTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'template_id', 'category', 'language', 'is_active', 'updated_at'
    )
    list_filter = ('category', 'language', 'is_active', 'created_at')
    search_fields = ('name', 'template_id', 'body')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_id', 'category', 'language', 'description', 'is_active')
        }),
        ('Content', {
            'fields': ('header', 'body', 'footer', 'buttons_config')
        }),
        ('Variables', {
            'fields': ('available_variables',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        'notification_type', 'template_code', 'recipient_email', 'recipient_phone',
        'status', 'triggered_by', 'sent_at', 'created_at'
    )
    list_filter = ('notification_type', 'status', 'triggered_by', 'created_at')
    search_fields = (
        'recipient_email', 'recipient_phone', 'recipient_name',
        'template_code', 'reference_id', 'provider_message_id'
    )
    readonly_fields = ('sent_at', 'delivered_at', 'created_at')
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('notification_type', 'template_code', 'status')
        }),
        ('Recipient', {
            'fields': ('recipient_email', 'recipient_phone', 'recipient_name')
        }),
        ('Content', {
            'fields': ('subject', 'message')
        }),
        ('Status & Response', {
            'fields': ('provider_message_id', 'provider_response', 'error_message')
        }),
        ('Context', {
            'fields': ('triggered_by', 'reference_type', 'reference_id')
        }),
        ('Timestamps', {
            'fields': ('sent_at', 'delivered_at', 'created_at')
        }),
    )


@admin.register(NotificationTrigger)
class NotificationTriggerAdmin(admin.ModelAdmin):
    list_display = (
        'trigger_event', 'send_email', 'send_sms', 'send_whatsapp',
        'email_template', 'sms_template', 'whatsapp_template', 'is_active'
    )
    list_filter = ('is_active', 'send_email', 'send_sms', 'send_whatsapp')
    search_fields = ('trigger_event',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Trigger Configuration', {
            'fields': ('trigger_event', 'is_active')
        }),
        ('Notification Channels', {
            'fields': ('send_email', 'send_sms', 'send_whatsapp')
        }),
        ('Templates', {
            'fields': ('email_template', 'sms_template', 'whatsapp_template')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

