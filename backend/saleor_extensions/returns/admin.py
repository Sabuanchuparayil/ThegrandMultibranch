from django.contrib import admin
from .models import ReturnRequest, ReturnItem, CreditNote


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = (
        'rma_number', 'order_id', 'branch', 'customer_name', 
        'status', 'reason', 'refund_amount', 'currency', 'created_at'
    )
    list_filter = ('status', 'reason', 'branch', 'requires_reverse_pickup', 'created_at')
    search_fields = ('rma_number', 'order_id', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReturnItemInline]
    
    fieldsets = (
        ('Return Information', {
            'fields': ('rma_number', 'order_id', 'branch', 'status', 'reason', 'description')
        }),
        ('Customer Information', {
            'fields': ('customer_id', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Refund Details', {
            'fields': ('refund_amount', 'currency', 'refund_method')
        }),
        ('Pickup Information', {
            'fields': ('requires_reverse_pickup', 'pickup_address', 'pickup_scheduled_at', 'picked_up_at')
        }),
        ('Processing', {
            'fields': ('received_at', 'processed_by', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = (
        'return_request', 'product_name', 'quantity', 'returned_quantity', 
        'unit_price', 'refund_amount', 'condition', 'created_at'
    )
    list_filter = ('condition', 'created_at')
    search_fields = ('product_id', 'product_name', 'return_request__rma_number')
    readonly_fields = ('created_at',)


@admin.register(CreditNote)
class CreditNoteAdmin(admin.ModelAdmin):
    list_display = (
        'credit_note_number', 'return_request', 'total_amount', 'currency', 
        'status', 'issued_at', 'issued_by', 'created_at'
    )
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('credit_note_number', 'return_request__rma_number', 'applied_to_order')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Credit Note Information', {
            'fields': ('credit_note_number', 'return_request', 'status')
        }),
        ('Amount Details', {
            'fields': ('subtotal', 'tax_amount', 'total_amount', 'currency')
        }),
        ('Processing', {
            'fields': ('issued_at', 'issued_by', 'applied_to_order')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

