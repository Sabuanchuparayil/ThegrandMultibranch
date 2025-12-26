from django.contrib import admin
from .models import ReportDefinition, ReportExecution, ScheduledReport


@admin.register(ReportDefinition)
class ReportDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'report_type', 'is_active', 'updated_at')
    list_filter = ('report_type', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('name', 'code', 'report_type', 'description', 'is_active')
        }),
        ('Configuration', {
            'fields': ('query_config', 'column_config', 'filters_config')
        }),
        ('Access', {
            'fields': ('requires_permission',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    list_display = (
        'report_definition', 'status', 'branch', 'region',
        'date_from', 'date_to', 'executed_by', 'started_at', 'completed_at', 'created_at'
    )
    list_filter = ('status', 'report_definition', 'branch', 'region', 'file_format', 'created_at')
    search_fields = ('report_definition__name', 'executed_by', 'error_message')
    readonly_fields = ('started_at', 'completed_at', 'created_at')
    
    fieldsets = (
        ('Report & Execution', {
            'fields': ('report_definition', 'status', 'executed_by')
        }),
        ('Filters', {
            'fields': ('filters', 'date_from', 'date_to', 'branch', 'region')
        }),
        ('Results', {
            'fields': ('result_data', 'file_url', 'file_format')
        }),
        ('Execution Details', {
            'fields': ('started_at', 'completed_at', 'error_message')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'report_definition', 'frequency', 'is_active',
        'next_run_at', 'last_run_at', 'created_by', 'created_at'
    )
    list_filter = ('frequency', 'is_active', 'file_format', 'report_definition')
    search_fields = ('name', 'report_definition__name', 'email_recipients')
    readonly_fields = ('next_run_at', 'last_run_at', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('name', 'report_definition', 'frequency', 'is_active')
        }),
        ('Default Filters', {
            'fields': ('default_filters', 'default_branch', 'default_region')
        }),
        ('Recipients', {
            'fields': ('email_recipients',)
        }),
        ('Format', {
            'fields': ('file_format',)
        }),
        ('Schedule', {
            'fields': ('next_run_at', 'last_run_at')
        }),
        ('Creation', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


