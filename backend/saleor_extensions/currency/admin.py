from django.contrib import admin
from .models import Currency, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'rate', 'effective_date', 'created_at')
    list_filter = ('from_currency', 'to_currency', 'effective_date')
    search_fields = ('from_currency__code', 'to_currency__code')
    readonly_fields = ('created_at',)


