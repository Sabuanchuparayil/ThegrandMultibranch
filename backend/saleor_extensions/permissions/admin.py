from django.contrib import admin
from .models import Role, Permission, RolePermission, UserRole, BranchAccess


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ['permission']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'can_access_all_branches', 'is_active', 'created_at')
    list_filter = ('is_active', 'can_access_all_branches')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['default_branches']
    inlines = [RolePermissionInline]
    
    fieldsets = (
        ('Role Information', {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        ('Branch Access', {
            'fields': ('can_access_all_branches', 'default_branches')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'permission_type', 'module_name', 'menu_path', 'is_active')
    list_filter = ('permission_type', 'is_active', 'module_name')
    search_fields = ('code', 'name', 'menu_path', 'module_name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Permission Information', {
            'fields': ('code', 'name', 'permission_type', 'description', 'is_active')
        }),
        ('Access Details', {
            'fields': ('menu_path', 'module_name')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'allowed', 'created_at')
    list_filter = ('allowed', 'role', 'permission__permission_type')
    search_fields = ('role__name', 'permission__name', 'permission__code')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['role', 'permission']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'role', 'branch', 'can_access_all_branches', 
        'is_active', 'assigned_by', 'assigned_at'
    )
    list_filter = ('role', 'is_active', 'can_access_all_branches', 'branch')
    search_fields = ('user_id', 'role__name', 'branch__name', 'assigned_by')
    readonly_fields = ('assigned_at',)
    
    fieldsets = (
        ('User & Role', {
            'fields': ('user_id', 'role', 'is_active')
        }),
        ('Branch Access', {
            'fields': ('branch', 'can_access_all_branches')
        }),
        ('Assignment', {
            'fields': ('assigned_by', 'assigned_at')
        }),
    )


@admin.register(BranchAccess)
class BranchAccessAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'branch', 'is_active', 'granted_by', 'granted_at')
    list_filter = ('is_active', 'branch')
    search_fields = ('user_id', 'branch__name', 'granted_by')
    readonly_fields = ('granted_at',)
    
    fieldsets = (
        ('Access Information', {
            'fields': ('user_id', 'branch', 'is_active')
        }),
        ('Grant Information', {
            'fields': ('granted_by', 'granted_at')
        }),
    )


