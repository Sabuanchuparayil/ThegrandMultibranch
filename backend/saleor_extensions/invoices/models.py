from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from saleor_extensions.currency.models import Currency
from saleor_extensions.branches.models import Branch


class Invoice(models.Model):
    """Invoice generation and management"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('ISSUED', 'Issued'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=100, unique=True)
    
    # Link to Saleor Order
    # Use unique related_name to avoid conflict with Saleor's invoice app (if it exists)
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.PROTECT,
        related_name='extension_invoices'  # Changed from 'invoices' to avoid conflict
    )
    
    # Branch
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Link to Saleor User (customer)
    customer = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True)
    billing_address = models.JSONField(default=dict)
    
    # Amount details
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='invoices')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    # Payment
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('UNPAID', 'Unpaid'),
            ('PARTIAL', 'Partially Paid'),
            ('PAID', 'Paid'),
        ],
        default='UNPAID'
    )
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    # Dates
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # PDF
    pdf_url = models.URLField(blank=True)
    pdf_generated_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-invoice_date', '-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['order']),
            models.Index(fields=['branch', 'status', 'invoice_date']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['status', 'invoice_date']),
        ]
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.total_amount} {self.currency.code}"


class InvoiceItem(models.Model):
    """Items in an invoice"""
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoice_items'
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} - {self.invoice.invoice_number}"


class InvoiceTemplate(models.Model):
    """Invoice templates for different countries"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, default='')
    
    # Template content (HTML)
    template_html = models.TextField()
    
    # Settings
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Logo and branding
    logo_url = models.URLField(blank=True)
    company_details = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoice_templates'
        verbose_name = 'Invoice Template'
        verbose_name_plural = 'Invoice Templates'
        indexes = [
            models.Index(fields=['country', 'is_active', 'is_default']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.country})"

