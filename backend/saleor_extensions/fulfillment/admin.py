from django.contrib import admin
from .models import ClickAndCollectOrder, Shipment, ShipmentItem


class ShipmentItemInline(admin.TabularInline):
    model = ShipmentItem
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(ClickAndCollectOrder)
class ClickAndCollectOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 'branch', 'customer_name', 'customer_phone', 
        'status', 'ready_at', 'picked_up_at', 'created_at'
    )
    list_filter = ('status', 'branch', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'branch', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Pickup Details', {
            'fields': ('ready_at', 'picked_up_at', 'expiry_date', 'prepared_by', 'collected_by')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'fulfillment', 'get_order_id', 'branch', 'shipment_type', 
        'status', 'courier_name', 'tracking_number', 'dispatched_at', 'created_at'
    )
    list_filter = ('status', 'shipment_type', 'branch', 'courier_name', 'created_at')
    search_fields = ('fulfillment__id', 'fulfillment__order__id', 'tracking_number', 'courier_name')
    readonly_fields = ('created_at', 'updated_at', 'get_order_id')
    inlines = [ShipmentItemInline]
    
    def get_order_id(self, obj):
        """Display order ID through fulfillment"""
        return obj.order_id
    get_order_id.short_description = 'Order ID'
    get_order_id.admin_order_field = 'fulfillment__order__id'
    
    fieldsets = (
        ('Shipment Information', {
            'fields': ('fulfillment', 'get_order_id', 'branch', 'shipment_type', 'status')
        }),
        ('Courier Details', {
            'fields': ('courier_name', 'courier_service', 'tracking_number', 'tracking_url')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'shipping_cost')
        }),
        ('Delivery Information', {
            'fields': ('dispatched_at', 'estimated_delivery', 'delivered_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ShipmentItem)
class ShipmentItemAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'product_name', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_id', 'product_name', 'shipment__fulfillment_id')
    readonly_fields = ('created_at',)

