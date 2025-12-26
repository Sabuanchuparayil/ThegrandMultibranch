from django.contrib import admin
from .models import CustomerGroup, CustomerProfile, LoyaltyTransaction, CustomerSupportTicket


class LoyaltyTransactionInline(admin.TabularInline):
    model = LoyaltyTransaction
    extra = 0
    readonly_fields = ('created_at', 'balance_after')


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'discount_percentage', 'is_active', 'created_at')
    list_filter = ('group_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Group Information', {
            'fields': ('name', 'group_type', 'description', 'is_active')
        }),
        ('Benefits', {
            'fields': ('discount_percentage',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'full_name', 'phone', 'customer_group', 'loyalty_points',
        'total_spent', 'total_orders', 'is_active', 'last_order_date'
    )
    list_filter = ('customer_group', 'is_active', 'is_email_verified', 'preferred_branch')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_spent', 'total_orders', 'last_order_date')
    inlines = [LoyaltyTransactionInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Group & Preferences', {
            'fields': ('customer_group', 'preferred_branch', 'preferred_currency', 'preferred_language')
        }),
        ('Loyalty', {
            'fields': ('loyalty_points', 'total_spent', 'total_orders', 'last_order_date')
        }),
        ('Status & Preferences', {
            'fields': ('is_active', 'is_email_verified', 'email_opt_in', 'sms_opt_in')
        }),
        ('Additional Information', {
            'fields': ('notes', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'customer_profile', 'transaction_type', 'points', 'balance_after',
        'reference_type', 'description', 'created_at'
    )
    list_filter = ('transaction_type', 'reference_type', 'created_at')
    search_fields = ('customer_profile__email', 'reference_id', 'description')
    readonly_fields = ('created_at',)


@admin.register(CustomerSupportTicket)
class CustomerSupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number', 'customer_profile', 'subject', 'status', 'priority',
        'assigned_to', 'branch', 'created_at'
    )
    list_filter = ('status', 'priority', 'branch', 'created_at')
    search_fields = ('ticket_number', 'customer_profile__email', 'subject', 'description')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_number', 'customer_profile', 'subject', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'branch')
        }),
        ('Resolution', {
            'fields': ('resolved_at', 'resolution_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


