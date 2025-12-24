from django.db import models
from saleor_extensions.regions.models import Region


class Branch(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(
        Region, 
        on_delete=models.PROTECT, 
        related_name='branches'
    )
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Fulfillment capabilities
    can_ship = models.BooleanField(default=True)
    can_click_collect = models.BooleanField(default=True)
    can_cross_border = models.BooleanField(default=False)
    
    # Operating hours
    operating_hours = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.region.code})"

