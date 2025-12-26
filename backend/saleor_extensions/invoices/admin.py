from django.contrib import admin
from .models import Invoice, InvoiceItem, InvoiceTemplate


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'order_id', 'customer_name', 'branch', 'total_amount',
        'currency', 'status', 'payment_status', 'invoice_date', 'due_date'
    )
    list_filter = ('status', 'payment_status', 'region', 'branch', 'currency', 'invoice_date')
    search_fields = ('invoice_number', 'order_id', 'customer_name', 'customer_email')
    readonly_fields = ('created_at', 'updated_at', 'paid_at', 'pdf_generated_at')
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'order_id', 'branch', 'region', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_id', 'customer_name', 'customer_email', 'billing_address')
        }),
        ('Amount Details', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'shipping_amount', 'total_amount', 'currency')
        }),
        ('Payment', {
            'fields': ('payment_status', 'paid_amount', 'paid_at')
        }),
        ('Dates', {
            'fields': ('invoice_date', 'due_date')
        }),
        ('Document', {
            'fields': ('pdf_url', 'pdf_generated_at')
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_conditions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product_name', 'quantity', 'unit_price', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_id', 'product_name', 'invoice__invoice_number')
    readonly_fields = ('created_at',)


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_default', 'is_active', 'updated_at')
    list_filter = ('region', 'is_default', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'region', 'is_default', 'is_active')
        }),
        ('Template Content', {
            'fields': ('template_html',)
        }),
        ('Branding', {
            'fields': ('logo_url', 'company_details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


