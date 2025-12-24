from django.contrib import admin
from .models import OrderBranchAssignment, ManualOrder, ManualOrderItem


class ManualOrderItemInline(admin.TabularInline):
    model = ManualOrderItem
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(OrderBranchAssignment)
class OrderBranchAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 'branch', 'region', 'currency', 
        'fulfillment_branch', 'is_click_collect', 'pickup_branch', 'created_at'
    )
    list_filter = ('region', 'currency', 'is_click_collect', 'branch', 'fulfillment_branch')
    search_fields = ('order_id', 'branch__name', 'branch__code')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id',)
        }),
        ('Branch & Region', {
            'fields': ('branch', 'region', 'currency', 'exchange_rate_at_order')
        }),
        ('Fulfillment', {
            'fields': ('fulfillment_branch', 'is_click_collect', 'pickup_branch')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ManualOrder)
class ManualOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'branch', 'customer_name', 'total_amount', 
        'currency', 'status', 'created_by', 'created_at'
    )
    list_filter = ('branch', 'region', 'currency', 'status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ManualOrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'branch', 'region', 'currency', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_id', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ManualOrderItem)
class ManualOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'product_name', 'quantity', 'unit_price', 
        'total_price', 'created_at'
    )
    list_filter = ('created_at',)
    search_fields = ('product_name', 'product_id', 'order__order_number')
    readonly_fields = ('created_at',)

