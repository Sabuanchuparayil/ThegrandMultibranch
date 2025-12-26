from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from saleor_extensions.branches.models import Branch
from saleor_extensions.currency.models import Currency


class GoldRate(models.Model):
    """Gold rate"""
    rate_per_gram = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='gold_rates'
    )
    effective_date = models.DateTimeField()
    source = models.CharField(max_length=100, blank=True)  # API source name
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'gold_rates'
        verbose_name = 'Gold Rate'
        verbose_name_plural = 'Gold Rates'
        ordering = ['-effective_date']
        indexes = [
            models.Index(fields=['effective_date']),
        ]
    
    def __str__(self):
        return f"Gold Rate: {self.rate_per_gram} {self.currency.code} per gram ({self.effective_date.date()})"


class MakingChargeRule(models.Model):
    """Making charge calculation rules"""
    CHARGE_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage of gold value'),
        ('FIXED_PER_GRAM', 'Fixed amount per gram'),
        ('FIXED_TOTAL', 'Fixed total amount'),
    ]
    
    name = models.CharField(max_length=200)
    charge_type = models.CharField(max_length=20, choices=CHARGE_TYPE_CHOICES)
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    min_weight_grams = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    max_weight_grams = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Lower number = higher priority
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'making_charge_rules'
        verbose_name = 'Making Charge Rule'
        verbose_name_plural = 'Making Charge Rules'
        ordering = ['priority', 'name']
        indexes = [
            models.Index(fields=['is_active', 'priority']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.charge_type}"


class BranchPricingOverride(models.Model):
    """Branch-specific pricing overrides"""
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='pricing_overrides'
    )
    # Link to Saleor Product
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='branch_pricing_overrides'
    )
    override_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='branch_pricing_overrides'
    )
    override_making_charge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'branch_pricing_overrides'
        verbose_name = 'Branch Pricing Override'
        verbose_name_plural = 'Branch Pricing Overrides'
        unique_together = [['branch', 'product']]
        indexes = [
            models.Index(fields=['branch', 'product', 'is_active']),
        ]
    
    def __str__(self):
        product_id = str(self.product.id) if hasattr(self.product, 'id') else 'N/A'
        return f"{self.branch.name} - Product {product_id}: {self.override_price} {self.currency.code}"


class PricingOverride(models.Model):
    """Product pricing overrides"""
    # Link to Saleor Product
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='pricing_overrides'
    )
    base_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='product_pricing_overrides'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pricing_overrides'
        verbose_name = 'Pricing Override'
        verbose_name_plural = 'Pricing Overrides'
        unique_together = [['product', 'currency']]
        indexes = [
            models.Index(fields=['product', 'is_active']),
        ]
    
    def __str__(self):
        product_id = str(self.product.id) if hasattr(self.product, 'id') else 'N/A'
        return f"Product {product_id}: {self.base_price} {self.currency.code}"

