from django.db import models
from decimal import Decimal


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # GBP, AED, INR
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'currencies'
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        related_name='from_rates'
    )
    to_currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        related_name='to_rates'
    )
    rate = models.DecimalField(max_digits=20, decimal_places=8)
    effective_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exchange_rates'
        unique_together = [['from_currency', 'to_currency', 'effective_date']]
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code}: {self.rate}"

