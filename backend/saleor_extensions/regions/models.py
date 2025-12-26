from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Region(models.Model):
    REGION_CHOICES = [
        ('UK', 'United Kingdom'),
        ('UAE', 'United Arab Emirates'),
        ('INDIA', 'India'),
    ]
    
    code = models.CharField(max_length=10, choices=REGION_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    default_currency = models.CharField(max_length=3)  # GBP, AED, INR
    tax_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    timezone = models.CharField(max_length=50, default='UTC')
    locale = models.CharField(max_length=10, default='en')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'regions'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


