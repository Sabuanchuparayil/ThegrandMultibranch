from django.contrib import admin
from .models import AuditLog, DataChangeLog


class DataChangeLogInline(admin.TabularInline):
    model = DataChangeLog
    extra = 0
    readonly_fields = ('field_name', 'old_value', 'new_value', 'created_at')
    can_delete = False


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'action', 'username', 'model_name', 'object_repr',
        'branch_id', 'ip_address', 'timestamp'
    )
    list_filter = ('action', 'model_name', 'timestamp', 'branch_id', 'region_code')
    search_fields = ('username', 'user_email', 'action_description', 'object_repr', 'ip_address')
    readonly_fields = ('timestamp',)
    inlines = [DataChangeLogInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_id', 'username', 'user_email')
        }),
        ('Action Details', {
            'fields': ('action', 'action_description')
        }),
        ('Object Information', {
            'fields': ('model_name', 'object_repr', 'content_type', 'object_id', 'changes')
        }),
        ('Context', {
            'fields': ('branch_id', 'region_code')
        }),
        ('Request Information', {
            'fields': ('ip_address', 'user_agent', 'request_path')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Audit logs should only be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Audit logs should be immutable


@admin.register(DataChangeLog)
class DataChangeLogAdmin(admin.ModelAdmin):
    list_display = ('audit_log', 'field_name', 'old_value', 'new_value', 'created_at')
    list_filter = ('field_name', 'created_at')
    search_fields = ('field_name', 'audit_log__object_repr')
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


