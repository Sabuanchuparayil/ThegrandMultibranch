from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from saleor_extensions.branches.models import Branch
from saleor_extensions.currency.models import Currency


class ReturnRequest(models.Model):
    """Return Merchandise Authorization (RMA) requests"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PICKUP_SCHEDULED', 'Pickup Scheduled'),
        ('PICKED_UP', 'Picked Up'),
        ('RECEIVED', 'Received at Branch'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    REASON_CHOICES = [
        ('DEFECTIVE', 'Defective/Not Working'),
        ('WRONG_ITEM', 'Wrong Item Received'),
        ('SIZE_ISSUE', 'Size/Size Issue'),
        ('QUALITY_ISSUE', 'Quality Issue'),
        ('NOT_AS_DESCRIBED', 'Not as Described'),
        ('DAMAGED', 'Damaged in Transit'),
        ('CHANGE_MIND', 'Changed Mind'),
        ('OTHER', 'Other'),
    ]
    
    rma_number = models.CharField(max_length=100, unique=True)
    
    # Order information
    # Note: order will be linked to Saleor's Order model once Saleor is initialized
    # order = models.ForeignKey('order.Order', on_delete=models.PROTECT, related_name='returns')
    order_id = models.CharField(max_length=255)
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='returns'
    )
    
    # Link to Saleor User (customer)
    customer = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='return_requests'
    )
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Return details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    
    # Refund information
    refund_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='returns'
    )
    refund_method = models.CharField(max_length=50, blank=True)  # e.g., "ORIGINAL_PAYMENT", "STORE_CREDIT"
    
    # Pickup information
    requires_reverse_pickup = models.BooleanField(default=False)
    pickup_address = models.JSONField(default=dict, blank=True)
    pickup_scheduled_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    
    # Processing
    received_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.CharField(max_length=255, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'return_requests'
        verbose_name = 'Return Request'
        verbose_name_plural = 'Return Requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rma_number']),
            models.Index(fields=['order_id']),
            models.Index(fields=['branch', 'status', 'created_at']),
            models.Index(fields=['customer', 'status']),
        ]
    
    def __str__(self):
        return f"RMA {self.rma_number} - Order {self.order_id} ({self.status})"


class ReturnItem(models.Model):
    """Items in a return request"""
    return_request = models.ForeignKey(
        ReturnRequest,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    returned_quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Condition assessment
    condition = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('NEW', 'New/Unused'),
            ('LIKE_NEW', 'Like New'),
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('POOR', 'Poor'),
        ]
    )
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'return_items'
        verbose_name = 'Return Item'
        verbose_name_plural = 'Return Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} - RMA {self.return_request.rma_number}"


class CreditNote(models.Model):
    """Credit notes for refunds"""
    credit_note_number = models.CharField(max_length=100, unique=True)
    
    return_request = models.OneToOneField(
        ReturnRequest,
        on_delete=models.CASCADE,
        related_name='credit_note'
    )
    
    # Amount information
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='credit_notes'
    )
    
    # Status
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ISSUED', 'Issued'),
        ('APPLIED', 'Applied'),
        ('REFUNDED', 'Refunded'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Processing
    issued_at = models.DateTimeField(null=True, blank=True)
    issued_by = models.CharField(max_length=255, blank=True)
    applied_to_order = models.CharField(max_length=255, blank=True)  # Order ID if applied
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'credit_notes'
        verbose_name = 'Credit Note'
        verbose_name_plural = 'Credit Notes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['credit_note_number']),
            models.Index(fields=['return_request', 'status']),
        ]
    
    def __str__(self):
        return f"Credit Note {self.credit_note_number} - {self.total_amount} {self.currency.code}"

