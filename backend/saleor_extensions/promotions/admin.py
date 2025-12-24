from django.contrib import admin
from .models import Promotion, Coupon, Campaign, PromotionUsage


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'promotion_type', 'discount_percentage', 'discount_amount',
        'applies_to', 'region', 'valid_from', 'valid_until', 'is_active', 'usage_count'
    )
    list_filter = ('promotion_type', 'applies_to', 'region', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('usage_count', 'created_at', 'updated_at')
    filter_horizontal = ['branches']
    
    fieldsets = (
        ('Promotion Information', {
            'fields': ('name', 'code', 'description', 'promotion_type', 'is_active')
        }),
        ('Discount Details', {
            'fields': ('discount_percentage', 'discount_amount')
        }),
        ('Applicability', {
            'fields': ('applies_to', 'category_id', 'product_ids', 'min_order_value')
        }),
        ('Region & Branches', {
            'fields': ('region', 'branches')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_count', 'per_customer_limit')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'promotion', 'customer_id', 'customer_group_id',
        'usage_count', 'usage_limit', 'is_active', 'valid_from', 'valid_until'
    )
    list_filter = ('is_active', 'promotion', 'valid_from', 'valid_until')
    search_fields = ('code', 'promotion__name', 'customer_id')
    readonly_fields = ('usage_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'promotion', 'is_active')
        }),
        ('Customer Restrictions', {
            'fields': ('customer_id', 'customer_group_id')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_count')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'campaign_type', 'region', 'start_date', 'end_date',
        'is_active', 'created_at'
    )
    list_filter = ('campaign_type', 'region', 'is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['promotions', 'branches']
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('name', 'description', 'campaign_type', 'is_active')
        }),
        ('Promotions', {
            'fields': ('promotions',)
        }),
        ('Region & Branches', {
            'fields': ('region', 'branches')
        }),
        ('Scheduling', {
            'fields': ('start_date', 'end_date')
        }),
        ('Marketing Materials', {
            'fields': ('banner_image_url', 'description_html')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PromotionUsage)
class PromotionUsageAdmin(admin.ModelAdmin):
    list_display = (
        'promotion', 'coupon', 'order_id', 'customer_id',
        'discount_amount', 'currency', 'used_at'
    )
    list_filter = ('currency', 'used_at', 'promotion')
    search_fields = ('order_id', 'customer_id', 'promotion__name', 'coupon__code')
    readonly_fields = ('used_at',)
    
    fieldsets = (
        ('Promotion & Coupon', {
            'fields': ('promotion', 'coupon')
        }),
        ('Usage Details', {
            'fields': ('order_id', 'customer_id', 'discount_amount', 'currency')
        }),
        ('Timestamp', {
            'fields': ('used_at',)
        }),
    )

