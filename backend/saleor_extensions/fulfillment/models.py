from django.db import models
from saleor_extensions.branches.models import Branch


class ClickAndCollectOrder(models.Model):
    """Click & Collect order management"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY_FOR_PICKUP', 'Ready for Pickup'),
        ('PICKED_UP', 'Picked Up'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]
    
    # Link to Saleor Order
    order = models.OneToOneField(
        'order.Order',
        on_delete=models.CASCADE,
        related_name='click_collect'
    )
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='click_collect_orders'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Pickup information
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    
    # Timestamps
    ready_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    # Staff information
    prepared_by = models.CharField(max_length=255, blank=True)
    collected_by = models.CharField(max_length=255, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'click_collect_orders'
        verbose_name = 'Click & Collect Order'
        verbose_name_plural = 'Click & Collect Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['branch', 'status', 'created_at']),
            models.Index(fields=['status', 'ready_at']),
        ]
    
    def __str__(self):
        order_id = str(self.order.id) if hasattr(self.order, 'id') else 'N/A'
        return f"Click & Collect - Order {order_id} at {self.branch.name}"


class Shipment(models.Model):
    """Shipment tracking and dispatch"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready for Dispatch'),
        ('DISPATCHED', 'Dispatched'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    SHIPMENT_TYPE_CHOICES = [
        ('FULL', 'Full Shipment'),
        ('PARTIAL', 'Partial Shipment'),
    ]
    
    # Link to Saleor Fulfillment
    fulfillment = models.ForeignKey(
        'order.Fulfillment',
        on_delete=models.CASCADE,
        related_name='shipments'
    )
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='shipments'
    )
    
    shipment_type = models.CharField(max_length=20, choices=SHIPMENT_TYPE_CHOICES, default='FULL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Courier information
    courier_name = models.CharField(max_length=100, blank=True)  # e.g., "Royal Mail", "DHL", "Aramex"
    courier_service = models.CharField(max_length=100, blank=True)  # Service type
    tracking_number = models.CharField(max_length=100, blank=True, unique=True)
    tracking_url = models.URLField(blank=True)
    
    # Shipping details
    shipping_address = models.JSONField(default=dict)
    shipping_cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shipments'
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['fulfillment']),
            models.Index(fields=['branch', 'status', 'created_at']),
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status', 'dispatched_at']),
        ]
    
    @property
    def order_id(self):
        """Get order ID through fulfillment relationship"""
        if self.fulfillment and hasattr(self.fulfillment, 'order'):
            return self.fulfillment.order.id if self.fulfillment.order else None
        return None
    
    def __str__(self):
        tracking = f" - {self.tracking_number}" if self.tracking_number else ""
        return f"Shipment {self.fulfillment_id}{tracking} ({self.status})"


class ShipmentItem(models.Model):
    """Items in a shipment"""
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'shipment_items'
        verbose_name = 'Shipment Item'
        verbose_name_plural = 'Shipment Items'
        ordering = ['created_at']
    
    def __str__(self):
        fulfillment_id = str(self.shipment.fulfillment.id) if hasattr(self.shipment, 'fulfillment') and hasattr(self.shipment.fulfillment, 'id') else 'N/A'
        return f"{self.product_name} x{self.quantity} - Shipment {fulfillment_id}"

