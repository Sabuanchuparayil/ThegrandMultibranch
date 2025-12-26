from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'region', 'city', 'country', 
        'can_ship', 'can_click_collect', 'is_active', 'created_at'
    )
    list_filter = ('region', 'is_active', 'can_ship', 'can_click_collect', 'can_cross_border')
    search_fields = ('name', 'code', 'city', 'country', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'region')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Capabilities', {
            'fields': ('can_ship', 'can_click_collect', 'can_cross_border', 'operating_hours')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


