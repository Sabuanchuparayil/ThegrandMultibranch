from django.contrib import admin
from .models import JewelleryProductAttribute, StoneDetail, ProductVariantAttribute


class StoneDetailInline(admin.TabularInline):
    model = StoneDetail
    extra = 0
    ordering = ['position']
    fields = (
        'stone_type', 'carat_weight', 'stone_count', 'shape', 
        'color', 'clarity', 'has_certification', 'certification_type', 
        'certification_number', 'position'
    )


@admin.register(JewelleryProductAttribute)
class JewelleryProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'metal_type', 'purity', 'weight_grams', 
        'making_charge_percentage', 'has_certification', 'updated_at'
    )
    list_filter = ('metal_type', 'purity', 'has_certification')
    search_fields = ('product_id', 'certification_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StoneDetailInline]
    
    fieldsets = (
        ('Product', {
            'fields': ('product_id',)
        }),
        ('Metal Information', {
            'fields': ('metal_type', 'purity', 'purity_percentage')
        }),
        ('Weight', {
            'fields': ('weight_grams',)
        }),
        ('Making Charge', {
            'fields': ('making_charge_percentage', 'fixed_making_charge')
        }),
        ('Certification', {
            'fields': ('has_certification', 'certification_type', 'certification_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(StoneDetail)
class StoneDetailAdmin(admin.ModelAdmin):
    list_display = (
        'jewellery_product', 'stone_type', 'carat_weight', 'stone_count', 
        'shape', 'color', 'has_certification', 'position'
    )
    list_filter = ('stone_type', 'has_certification', 'shape', 'color')
    search_fields = ('jewellery_product__product_id', 'certification_number')
    readonly_fields = ('created_at',)


@admin.register(ProductVariantAttribute)
class ProductVariantAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'variant_id', 'size', 'weight_grams', 'purity', 'updated_at'
    )
    list_filter = ('purity',)
    search_fields = ('variant_id', 'size')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Variant', {
            'fields': ('variant_id',)
        }),
        ('Size', {
            'fields': ('size',)
        }),
        ('Weight', {
            'fields': ('weight_grams',)
        }),
        ('Purity', {
            'fields': ('purity', 'purity_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

