from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class JewelleryProductAttribute(models.Model):
    """Extension model for jewellery-specific product attributes"""
    # Link to Saleor Product model
    product = models.OneToOneField(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='jewellery_attributes'
    )
    
    # Metal information
    METAL_TYPE_CHOICES = [
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('PLATINUM', 'Platinum'),
        ('PALLADIUM', 'Palladium'),
        ('DIAMOND', 'Diamond'),
        ('OTHER', 'Other'),
    ]
    
    metal_type = models.CharField(max_length=50, choices=METAL_TYPE_CHOICES, blank=True)
    purity = models.CharField(max_length=50, blank=True)  # e.g., "18K", "22K", "925", "999"
    purity_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Weight information
    weight_grams = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Making charge
    making_charge_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    fixed_making_charge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Certifications
    has_certification = models.BooleanField(default=False)
    certification_type = models.CharField(max_length=100, blank=True)  # e.g., "GIA", "IGI", "BIS"
    certification_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jewellery_product_attributes'
        verbose_name = 'Jewellery Product Attribute'
        verbose_name_plural = 'Jewellery Product Attributes'
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['metal_type', 'purity']),
        ]
    
    def __str__(self):
        product_id = str(self.product.id) if hasattr(self.product, 'id') else 'N/A'
        return f"Jewellery Attributes for Product {product_id}"


class StoneDetail(models.Model):
    """Stone details for jewellery products"""
    STONE_TYPE_CHOICES = [
        ('DIAMOND', 'Diamond'),
        ('RUBY', 'Ruby'),
        ('EMERALD', 'Emerald'),
        ('SAPPHIRE', 'Sapphire'),
        ('PEARL', 'Pearl'),
        ('OTHER', 'Other'),
    ]
    
    jewellery_product = models.ForeignKey(
        JewelleryProductAttribute,
        on_delete=models.CASCADE,
        related_name='stones'
    )
    stone_type = models.CharField(max_length=50, choices=STONE_TYPE_CHOICES)
    carat_weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    stone_count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    shape = models.CharField(max_length=50, blank=True)  # e.g., "Round", "Princess", "Oval"
    color = models.CharField(max_length=50, blank=True)
    clarity = models.CharField(max_length=50, blank=True)  # e.g., "VS1", "VVS2", "SI1"
    
    # Certification
    has_certification = models.BooleanField(default=False)
    certification_type = models.CharField(max_length=100, blank=True)
    certification_number = models.CharField(max_length=100, blank=True)
    
    position = models.IntegerField(default=0)  # For ordering multiple stones
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stone_details'
        verbose_name = 'Stone Detail'
        verbose_name_plural = 'Stone Details'
        ordering = ['position', 'created_at']
        indexes = [
            models.Index(fields=['jewellery_product', 'stone_type']),
        ]
    
    def __str__(self):
        product_id = str(self.jewellery_product.product.id) if hasattr(self.jewellery_product, 'product') and hasattr(self.jewellery_product.product, 'id') else 'N/A'
        return f"{self.stone_type} - {self.carat_weight}ct (Product {product_id})"


class ProductVariantAttribute(models.Model):
    """Variant-specific attributes (size, weight variations, etc.)"""
    # Link to Saleor ProductVariant model
    variant = models.OneToOneField(
        'product.ProductVariant',
        on_delete=models.CASCADE,
        related_name='jewellery_variant_attributes'
    )
    
    # Size information
    size = models.CharField(max_length=50, blank=True)  # Ring size, chain length, etc.
    
    # Weight variations
    weight_grams = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Purity variations (if different from base product)
    purity = models.CharField(max_length=50, blank=True)
    purity_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_variant_attributes'
        verbose_name = 'Product Variant Attribute'
        verbose_name_plural = 'Product Variant Attributes'
        indexes = [
            models.Index(fields=['variant']),
        ]
    
    def __str__(self):
        variant_id = str(self.variant.id) if hasattr(self.variant, 'id') else 'N/A'
        return f"Variant Attributes for {variant_id}"

