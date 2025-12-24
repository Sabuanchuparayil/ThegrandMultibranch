from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from saleor_extensions.regions.models import Region
from saleor_extensions.branches.models import Branch


class Promotion(models.Model):
    """Promotions and campaigns"""
    PROMOTION_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage Discount'),
        ('FIXED_AMOUNT', 'Fixed Amount Discount'),
        ('BUY_X_GET_Y', 'Buy X Get Y'),
        ('FREE_SHIPPING', 'Free Shipping'),
        ('GIFT', 'Free Gift'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    
    promotion_type = models.CharField(max_length=50, choices=PROMOTION_TYPE_CHOICES)
    
    # Discount details
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    discount_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Applicability
    applies_to = models.CharField(
        max_length=50,
        choices=[
            ('ALL', 'All Products'),
            ('CATEGORY', 'Category'),
            ('PRODUCT', 'Specific Product'),
            ('ORDER_TOTAL', 'Order Total'),
        ],
        default='ALL'
    )
    category_id = models.CharField(max_length=255, blank=True)
    product_ids = models.JSONField(default=list, blank=True)
    min_order_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Region and branch
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='promotions',
        null=True,
        blank=True
    )
    branches = models.ManyToManyField(
        Branch,
        related_name='promotions',
        blank=True
    )
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Usage limits
    usage_limit = models.IntegerField(null=True, blank=True)  # Total usage limit
    usage_count = models.IntegerField(default=0)
    per_customer_limit = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'promotions'
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['region', 'is_active', 'valid_from', 'valid_until']),
            models.Index(fields=['is_active', 'valid_from', 'valid_until']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code or 'No Code'})"


class Coupon(models.Model):
    """Coupon codes"""
    code = models.CharField(max_length=100, unique=True)
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='coupons'
    )
    
    # Customer restrictions - link to Saleor User (optional)
    customer = models.ForeignKey(
        'account.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_coupons'
    )
    customer_group_id = models.CharField(max_length=255, blank=True)
    
    # Usage tracking
    usage_limit = models.IntegerField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['promotion']),
        ]
    
    def __str__(self):
        return f"Coupon {self.code} - {self.promotion.name}"


class Campaign(models.Model):
    """Marketing campaigns (festivals, seasonal, etc.)"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Campaign type
    CAMPAIGN_TYPE_CHOICES = [
        ('FESTIVAL', 'Festival Campaign'),
        ('SEASONAL', 'Seasonal Campaign'),
        ('LAUNCH', 'Product Launch'),
        ('CLEARANCE', 'Clearance Sale'),
        ('LOYALTY', 'Loyalty Program'),
        ('OTHER', 'Other'),
    ]
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPE_CHOICES)
    
    # Promotions in campaign
    promotions = models.ManyToManyField(
        Promotion,
        related_name='campaigns',
        blank=True
    )
    
    # Region and branch
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='campaigns',
        null=True,
        blank=True
    )
    branches = models.ManyToManyField(
        Branch,
        related_name='campaigns',
        blank=True
    )
    
    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Marketing materials
    banner_image_url = models.URLField(blank=True)
    description_html = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'campaigns'
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['campaign_type', 'is_active', 'start_date', 'end_date']),
            models.Index(fields=['region', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.campaign_type})"


class PromotionUsage(models.Model):
    """Track promotion/coupon usage"""
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='usage_history'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usage_history'
    )
    
    # Link to Saleor Order and User
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.PROTECT,
        related_name='promotion_usages'
    )
    customer = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='promotion_usages'
    )
    
    # Discount applied
    discount_amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=3)
    
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'promotion_usage'
        verbose_name = 'Promotion Usage'
        verbose_name_plural = 'Promotion Usage'
        ordering = ['-used_at']
        indexes = [
            models.Index(fields=['promotion', 'used_at']),
            models.Index(fields=['customer', 'used_at']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        order_id = str(self.order.id) if hasattr(self.order, 'id') else 'N/A'
        return f"{self.promotion.name} used in order {order_id}"

