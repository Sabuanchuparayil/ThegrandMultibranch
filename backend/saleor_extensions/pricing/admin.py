from django.contrib import admin
from .models import GoldRate, MakingChargeRule, BranchPricingOverride, RegionPricing


@admin.register(GoldRate)
class GoldRateAdmin(admin.ModelAdmin):
    list_display = (
        'region', 'rate_per_gram', 'currency', 'effective_date', 
        'source', 'created_at'
    )
    list_filter = ('region', 'currency', 'effective_date')
    search_fields = ('region__code', 'region__name', 'source')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Rate Details', {
            'fields': ('region', 'currency', 'rate_per_gram', 'effective_date', 'source')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(MakingChargeRule)
class MakingChargeRuleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'region', 'charge_type', 'value', 
        'min_weight_grams', 'max_weight_grams', 'priority', 'is_active'
    )
    list_filter = ('region', 'charge_type', 'is_active')
    search_fields = ('name', 'region__code', 'region__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Rule Details', {
            'fields': ('name', 'region', 'charge_type', 'value', 'priority', 'is_active')
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
    list_filter = ('branch', 'currency', 'is_active', 'branch__region')
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


@admin.register(RegionPricing)
class RegionPricingAdmin(admin.ModelAdmin):
    list_display = (
        'region', 'product_id', 'base_price', 'currency', 
        'is_active', 'updated_at'
    )
    list_filter = ('region', 'currency', 'is_active')
    search_fields = ('product_id', 'region__code', 'region__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Region Pricing', {
            'fields': ('region', 'product_id', 'base_price', 'currency', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

