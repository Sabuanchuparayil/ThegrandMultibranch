from django.contrib import admin
from .models import GoldRate, MakingChargeRule, BranchPricingOverride, PricingOverride


@admin.register(GoldRate)
class GoldRateAdmin(admin.ModelAdmin):
    list_display = (
        'rate_per_gram', 'currency', 'effective_date', 
        'source', 'created_at'
    )
    list_filter = ('currency', 'effective_date')
    search_fields = ('source',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Rate Details', {
            'fields': ('currency', 'rate_per_gram', 'effective_date', 'source')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(MakingChargeRule)
class MakingChargeRuleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'charge_type', 'value', 
        'min_weight_grams', 'max_weight_grams', 'priority', 'is_active'
    )
    list_filter = ('charge_type', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Rule Details', {
            'fields': ('name', 'charge_type', 'value', 'priority', 'is_active')
        }),
        ('Weight Constraints', {
            'fields': ('min_weight_grams', 'max_weight_grams')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(BranchPricingOverride)
class BranchPricingOverrideAdmin(admin.ModelAdmin):
    list_display = (
        'branch', 'product_id', 'override_price', 'currency', 
        'override_making_charge', 'is_active', 'valid_from', 'valid_until'
    )
    list_filter = ('branch', 'currency', 'is_active')
    search_fields = ('product_id', 'branch__name', 'branch__code')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Pricing Override', {
            'fields': ('branch', 'product_id', 'override_price', 'currency', 'override_making_charge')
        }),
        ('Validity', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PricingOverride)
class PricingOverrideAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'base_price', 'currency', 
        'is_active', 'updated_at'
    )
    list_filter = ('currency', 'is_active')
    search_fields = ('product__name', 'product__slug')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Pricing Override', {
            'fields': ('product', 'base_price', 'currency', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


