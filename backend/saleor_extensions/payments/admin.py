from django.contrib import admin
from .models import PaymentGateway, PaymentTransaction, PaymentRefund


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'gateway_type', 'region', 'is_active', 'is_test_mode',
        'supports_card', 'supports_wallet', 'created_at'
    )
    list_filter = ('gateway_type', 'region', 'is_active', 'is_test_mode')
    search_fields = ('name', 'gateway_type', 'merchant_id')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['supported_currencies']
    
    fieldsets = (
        ('Gateway Information', {
            'fields': ('name', 'gateway_type', 'region', 'is_active', 'is_test_mode')
        }),
        ('Credentials', {
            'fields': ('api_key', 'api_secret', 'merchant_id')
        }),
        ('Supported Features', {
            'fields': ('supports_card', 'supports_wallet', 'supports_netbanking', 'supports_upi')
        }),
        ('Supported Currencies', {
            'fields': ('supported_currencies',)
        }),
        ('Settings', {
            'fields': ('settings',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'order_id', 'gateway', 'amount', 'currency',
        'status', 'payment_method', 'initiated_at', 'completed_at'
    )
    list_filter = ('status', 'gateway', 'currency', 'payment_method', 'initiated_at')
    search_fields = ('transaction_id', 'order_id', 'gateway_transaction_id')
    readonly_fields = ('initiated_at', 'completed_at')
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('order_id', 'gateway', 'transaction_id', 'gateway_transaction_id')
        }),
        ('Amount & Currency', {
            'fields': ('amount', 'currency')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'payment_method_details')
        }),
        ('Gateway Response', {
            'fields': ('gateway_response', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('initiated_at', 'completed_at')
        }),
    )


@admin.register(PaymentRefund)
class PaymentRefundAdmin(admin.ModelAdmin):
    list_display = (
        'refund_id', 'payment_transaction', 'amount', 'currency',
        'status', 'requested_at', 'processed_at'
    )
    list_filter = ('status', 'currency', 'requested_at')
    search_fields = ('refund_id', 'gateway_refund_id', 'payment_transaction__transaction_id')
    readonly_fields = ('requested_at', 'processed_at')
    
    fieldsets = (
        ('Refund Information', {
            'fields': ('payment_transaction', 'refund_id', 'gateway_refund_id')
        }),
        ('Amount & Currency', {
            'fields': ('amount', 'currency')
        }),
        ('Status', {
            'fields': ('status', 'reason')
        }),
        ('Gateway Response', {
            'fields': ('gateway_response', 'error_message')
        }),
        ('Request Information', {
            'fields': ('requested_by', 'requested_at', 'processed_at')
        }),
    )


