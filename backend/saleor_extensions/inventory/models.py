from django.db import models
from django.core.validators import MinValueValidator
from saleor_extensions.branches.models import Branch


class BranchInventory(models.Model):
    """Branch-level inventory for products"""
    # Link to Saleor ProductVariant (inventory is tracked at variant level)
    product_variant = models.ForeignKey(
        'product.ProductVariant',
        on_delete=models.CASCADE,
        related_name='branch_inventory'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    low_stock_threshold = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'branch_inventory'
        verbose_name = 'Branch Inventory'
        verbose_name_plural = 'Branch Inventory'
        unique_together = [['product_variant', 'branch']]
        indexes = [
            models.Index(fields=['product_variant', 'branch']),
            models.Index(fields=['branch', 'quantity']),
        ]
    
    @property
    def available_quantity(self):
        return max(0, self.quantity - self.reserved_quantity)
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
    
    def __str__(self):
        variant_id = str(self.product_variant.id) if hasattr(self.product_variant, 'id') else 'N/A'
        return f"Variant {variant_id} at {self.branch.name}: {self.quantity} units"


class StockMovement(models.Model):
    """Track stock movements (in/out)"""
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUSTMENT', 'Adjustment'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('TRANSFER_IN', 'Transfer In'),
        ('RETURN', 'Return'),
    ]
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    product_variant = models.ForeignKey(
        'product.ProductVariant',
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)  # User ID/username
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['branch', 'created_at']),
            models.Index(fields=['product_variant', 'created_at']),
        ]
    
    def __str__(self):
        variant_id = str(self.product_variant.id) if hasattr(self.product_variant, 'id') else 'N/A'
        return f"{self.movement_type} - Variant {variant_id} at {self.branch.name}: {self.quantity}"


class StockTransfer(models.Model):
    """Stock transfers between branches"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    transfer_number = models.CharField(max_length=100, unique=True)
    from_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='transfers_out'
    )
    to_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='transfers_in'
    )
    product_id = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_by = models.CharField(max_length=255, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stock_transfers'
        verbose_name = 'Stock Transfer'
        verbose_name_plural = 'Stock Transfers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['from_branch', 'status']),
            models.Index(fields=['to_branch', 'status']),
            models.Index(fields=['transfer_number']),
        ]
    
    def __str__(self):
        return f"Transfer {self.transfer_number}: {self.from_branch.name} → {self.to_branch.name}"


class LowStockAlert(models.Model):
    """Alerts for low stock items"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
    ]
    
    branch_inventory = models.ForeignKey(
        BranchInventory,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    current_quantity = models.IntegerField()
    threshold = models.IntegerField()
    acknowledged_by = models.CharField(max_length=255, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'low_stock_alerts'
        verbose_name = 'Low Stock Alert'
        verbose_name_plural = 'Low Stock Alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"Low Stock Alert: {self.branch_inventory.product_id} at {self.branch_inventory.branch.name}"

