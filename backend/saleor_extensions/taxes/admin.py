from django.contrib import admin
from .models import TaxRule, TaxExemption


@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'region', 'tax_type', 'rate', 'state', 
        'applies_to', 'is_active', 'effective_from'
    )
    list_filter = ('region', 'tax_type', 'is_active', 'applies_to')
    search_fields = ('name', 'region__code', 'state', 'applies_to')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Tax Rule Details', {
            'fields': ('name', 'region', 'tax_type', 'rate')
        }),
        ('Applicability', {
            'fields': ('state', 'applies_to', 'is_active')
        }),
        ('Validity Period', {
            'fields': ('effective_from', 'effective_until')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(TaxExemption)
class TaxExemptionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'region', 'exemption_type', 'identifier', 
        'exemption_percentage', 'is_active', 'valid_from', 'valid_until'
    )
    list_filter = ('region', 'exemption_type', 'is_active')
    search_fields = ('name', 'identifier', 'region__code')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Exemption Details', {
            'fields': ('name', 'region', 'exemption_type', 'identifier')
        }),
        ('Exemption Rules', {
            'fields': ('min_order_value', 'exemption_percentage', 'is_active')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

