from django.contrib import admin
from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'default_currency', 'tax_rate', 'is_active', 'created_at')
    list_filter = ('is_active', 'code')
    search_fields = ('code', 'name')
    readonly_fields = ('created_at', 'updated_at')

