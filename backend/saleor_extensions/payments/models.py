from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from saleor_extensions.regions.models import Region
from saleor_extensions.currency.models import Currency


class PaymentGateway(models.Model):
    """Payment gateway configurations per region"""
    GATEWAY_TYPE_CHOICES = [
        ('STRIPE', 'Stripe'),
        ('PAYPAL', 'PayPal'),
        ('RAZORPAY', 'Razorpay'),
        ('PAYU', 'PayU'),
        ('CASHFREE', 'Cashfree'),
        ('PAYTABS', 'PayTabs'),
        ('NETWORK_INTERNATIONAL', 'Network International'),
        ('TABBY', 'Tabby'),
        ('SQUARE', 'Square'),
    ]
    
    name = models.CharField(max_length=100)
    gateway_type = models.CharField(max_length=50, choices=GATEWAY_TYPE_CHOICES)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='payment_gateways'
    )
    
    # Credentials (encrypted in production)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    merchant_id = models.CharField(max_length=200, blank=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    is_test_mode = models.BooleanField(default=False)
    
    # Supported features
    supports_card = models.BooleanField(default=True)
    supports_wallet = models.BooleanField(default=False)
    supports_netbanking = models.BooleanField(default=False)
    supports_upi = models.BooleanField(default=False)  # For India
    
    # Supported currencies
    supported_currencies = models.ManyToManyField(
        Currency,
        related_name='payment_gateways'
    )
    
    # Settings
    settings = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_gateways'
        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'
        unique_together = [['gateway_type', 'region']]
        indexes = [
            models.Index(fields=['region', 'is_active']),
            models.Index(fields=['gateway_type']),
        ]
    
    def __str__(self):
        return f"{self.get_gateway_type_display()} - {self.region.code}"


class PaymentTransaction(models.Model):
    """Payment transaction records"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('PARTIALLY_REFUNDED', 'Partially Refunded'),
    ]
    
    # Order information
    order_id = models.CharField(max_length=255)
    
    # Gateway information
    gateway = models.ForeignKey(
        PaymentGateway,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    
    # Transaction details
    transaction_id = models.CharField(max_length=255, unique=True)  # Gateway transaction ID
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    
    # Amount
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='payments')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Payment method
    payment_method = models.CharField(max_length=50, blank=True)  # card, wallet, netbanking, etc.
    payment_method_details = models.JSONField(default=dict, blank=True)
    
    # Response from gateway
    gateway_response = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payment_transactions'
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-initiated_at']
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['gateway', 'status', 'initiated_at']),
            models.Index(fields=['status', 'initiated_at']),
        ]
    
    def __str__(self):
        return f"{self.transaction_id} - {self.amount} {self.currency.code} ({self.status})"


class PaymentRefund(models.Model):
    """Payment refund records"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    
    payment_transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name='refunds'
    )
    
    refund_id = models.CharField(max_length=255, unique=True)
    gateway_refund_id = models.CharField(max_length=255, blank=True)
    
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='refunds')
    
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    gateway_response = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    requested_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'payment_refunds'
        verbose_name = 'Payment Refund'
        verbose_name_plural = 'Payment Refunds'
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['refund_id']),
            models.Index(fields=['payment_transaction', 'status']),
        ]
    
    def __str__(self):
        return f"Refund {self.refund_id} - {self.amount} {self.currency.code}"

