from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class TaxRule(models.Model):
    """Tax rules"""
    TAX_TYPE_CHOICES = [
        ('VAT', 'VAT (Value Added Tax)'),
        ('GST', 'GST (Goods and Services Tax)'),
        ('SALES_TAX', 'Sales Tax'),
    ]
    
    country = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES)
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    # For India GST: state-level variations
    state = models.CharField(max_length=100, blank=True)
    # Product category or specific product type (e.g., 'GOLD', 'DIAMOND', etc.)
    applies_to = models.CharField(max_length=100, blank=True, default='ALL')
    is_active = models.BooleanField(default=True)
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tax_rules'
        verbose_name = 'Tax Rule'
        verbose_name_plural = 'Tax Rules'
        ordering = ['country', 'tax_type', 'rate']
        indexes = [
            models.Index(fields=['country', 'tax_type', 'is_active']),
            models.Index(fields=['country', 'state']),
        ]
    
    def __str__(self):
        state_str = f" ({self.state})" if self.state else ""
        return f"{self.country}{state_str} - {self.tax_type}: {self.rate}%"


class TaxExemption(models.Model):
    """Tax exemptions for specific products or customers"""
    EXEMPTION_TYPE_CHOICES = [
        ('PRODUCT', 'Product-based'),
        ('CUSTOMER', 'Customer-based'),
        ('ORDER_VALUE', 'Order Value-based'),
    ]
    
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='tax_exemptions'
    )
    exemption_type = models.CharField(max_length=20, choices=EXEMPTION_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    # For PRODUCT: product_id or category
    # For CUSTOMER: customer_id or customer_group
    # For ORDER_VALUE: minimum order value
    identifier = models.CharField(max_length=255, blank=True)
    min_order_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    exemption_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('100'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tax_exemptions'
        verbose_name = 'Tax Exemption'
        verbose_name_plural = 'Tax Exemptions'
        ordering = ['region', 'exemption_type']
        indexes = [
            models.Index(fields=['region', 'exemption_type', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.region.code}) - {self.exemption_type}"


