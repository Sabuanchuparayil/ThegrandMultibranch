from django.db import models
from saleor_extensions.branches.models import Branch
from saleor_extensions.currency.models import Currency


class OrderBranchAssignment(models.Model):
    """Extension to link orders with branches"""
    # Link to Saleor Order model
    order = models.OneToOneField(
        'order.Order',
        on_delete=models.CASCADE,
        related_name='branch_assignment'
    )
    
    # Branch assignment
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,
        blank=True
    )
    
    # Currency information
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    exchange_rate_at_order = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True
    )
    
    # Fulfillment information
    fulfillment_branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='fulfilled_orders',
        null=True,
        blank=True
    )
    
    # Click & Collect
    is_click_collect = models.BooleanField(default=False)
    pickup_branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='pickup_orders',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'order_branch_assignments'
        verbose_name = 'Order Branch Assignment'
        verbose_name_plural = 'Order Branch Assignments'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['branch', 'created_at']),
            models.Index(fields=['fulfillment_branch']),
        ]
    
    def __str__(self):
        branch_str = f" - {self.branch.name}" if self.branch else ""
        order_id = str(self.order.id) if hasattr(self.order, 'id') else 'N/A'
        return f"Order {order_id}{branch_str}"


class ManualOrder(models.Model):
    """Manual orders created in-store or via assisted sales"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=100, unique=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='manual_orders'
    )
    country = models.CharField(max_length=100, default='')
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='manual_orders'
    )
    
    # Customer information - link to Saleor's User model (optional for guest orders)
    customer = models.ForeignKey(
        'account.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manual_orders'
    )
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Order details
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True)
    
    created_by = models.CharField(max_length=255, blank=True)  # User ID/username
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'manual_orders'
        verbose_name = 'Manual Order'
        verbose_name_plural = 'Manual Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['branch', 'status', 'created_at']),
            models.Index(fields=['customer']),
        ]
    
    def __str__(self):
        return f"Manual Order {self.order_number} - {self.branch.name}"


class ManualOrderItem(models.Model):
    """Items in manual orders"""
    order = models.ForeignKey(
        ManualOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Jewellery-specific attributes
    metal_type = models.CharField(max_length=100, blank=True)
    purity = models.CharField(max_length=50, blank=True)
    weight_grams = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'manual_order_items'
        verbose_name = 'Manual Order Item'
        verbose_name_plural = 'Manual Order Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} - {self.order.order_number}"

