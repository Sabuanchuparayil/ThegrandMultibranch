from django.contrib import admin
from .models import BranchInventory, StockMovement, StockTransfer, LowStockAlert


@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'branch', 'quantity', 'reserved_quantity', 
        'available_quantity', 'is_low_stock', 'last_updated'
    )
    list_filter = ('branch', 'is_low_stock', 'branch__region')
    search_fields = ('product_id', 'branch__name', 'branch__code')
    readonly_fields = ('available_quantity', 'is_low_stock', 'last_updated', 'created_at')
    
    fieldsets = (
        ('Product & Branch', {
            'fields': ('product_id', 'branch')
        }),
        ('Stock Levels', {
            'fields': ('quantity', 'reserved_quantity', 'available_quantity', 'low_stock_threshold', 'is_low_stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated')
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'branch', 'movement_type', 'quantity', 
        'reference_number', 'created_by', 'created_at'
    )
    list_filter = ('movement_type', 'branch', 'created_at')
    search_fields = ('product_id', 'reference_number', 'branch__name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Movement Details', {
            'fields': ('branch', 'product_id', 'movement_type', 'quantity')
        }),
        ('Reference', {
            'fields': ('reference_number', 'notes', 'created_by')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = (
        'transfer_number', 'product_id', 'from_branch', 'to_branch', 
        'quantity', 'status', 'created_at'
    )
    list_filter = ('status', 'from_branch', 'to_branch', 'created_at')
    search_fields = ('transfer_number', 'product_id', 'from_branch__name', 'to_branch__name')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Transfer Details', {
            'fields': ('transfer_number', 'from_branch', 'to_branch', 'product_id', 'quantity', 'status')
        }),
        ('Information', {
            'fields': ('requested_by', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(LowStockAlert)
class LowStockAlertAdmin(admin.ModelAdmin):
    list_display = (
        'branch_inventory', 'current_quantity', 'threshold', 
        'status', 'acknowledged_by', 'created_at'
    )
    list_filter = ('status', 'created_at', 'branch_inventory__branch')
    search_fields = ('branch_inventory__product_id', 'branch_inventory__branch__name')
    readonly_fields = ('created_at', 'acknowledged_at')
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('branch_inventory', 'current_quantity', 'threshold', 'status')
        }),
        ('Acknowledgment', {
            'fields': ('acknowledged_by', 'acknowledged_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

