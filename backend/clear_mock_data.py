#!/usr/bin/env python3
"""
Script to clear all mock/seed data from the database.

Usage:
    python manage.py shell
    >>> exec(open('clear_mock_data.py').read())
    
Or run directly:
    python clear_mock_data.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.db import transaction
from django.core.management import call_command

# Import all models that might have seed data
from saleor_extensions.regions.models import Region
from saleor_extensions.currency.models import Currency, ExchangeRate
from saleor_extensions.branches.models import Branch
from saleor_extensions.customers.models import CustomerGroup
from saleor_extensions.inventory.models import BranchInventory, StockMovement, StockTransfer, LowStockAlert
from saleor_extensions.pricing.models import GoldRate, MakingCharge, PricingOverride
from saleor_extensions.products.models import Product
from saleor_extensions.orders.models import Order
from saleor_extensions.payments.models import PaymentGateway
from saleor_extensions.taxes.models import TaxRule

def clear_all_mock_data():
    """Clear all mock/seed data from custom extensions"""
    print("=" * 80)
    print("CLEARING ALL MOCK DATA")
    print("=" * 80)
    
    with transaction.atomic():
        # Clear in reverse dependency order
        
        # 1. Clear inventory data (depends on branches/products)
        print("\n1. Clearing inventory data...")
        LowStockAlert.objects.all().delete()
        print("   ✅ Cleared LowStockAlert")
        StockTransfer.objects.all().delete()
        print("   ✅ Cleared StockTransfer")
        StockMovement.objects.all().delete()
        print("   ✅ Cleared StockMovement")
        BranchInventory.objects.all().delete()
        print("   ✅ Cleared BranchInventory")
        
        # 2. Clear pricing data
        print("\n2. Clearing pricing data...")
        PricingOverride.objects.all().delete()
        print("   ✅ Cleared PricingOverride")
        MakingCharge.objects.all().delete()
        print("   ✅ Cleared MakingCharge")
        GoldRate.objects.all().delete()
        print("   ✅ Cleared GoldRate")
        
        # 3. Clear orders (depends on products, customers, branches)
        print("\n3. Clearing orders...")
        Order.objects.all().delete()
        print("   ✅ Cleared Order")
        
        # 4. Clear products (depends on branches, regions)
        print("\n4. Clearing products...")
        Product.objects.all().delete()
        print("   ✅ Cleared Product")
        
        # 5. Clear branches (depends on regions)
        print("\n5. Clearing branches...")
        Branch.objects.all().delete()
        print("   ✅ Cleared Branch")
        
        # 6. Clear customer groups
        print("\n6. Clearing customer groups...")
        CustomerGroup.objects.all().delete()
        print("   ✅ Cleared CustomerGroup")
        
        # 7. Clear exchange rates (depends on currencies)
        print("\n7. Clearing exchange rates...")
        ExchangeRate.objects.all().delete()
        print("   ✅ Cleared ExchangeRate")
        
        # 8. Clear currencies
        print("\n8. Clearing currencies...")
        Currency.objects.all().delete()
        print("   ✅ Cleared Currency")
        
        # 9. Clear regions (base dependency)
        print("\n9. Clearing regions...")
        Region.objects.all().delete()
        print("   ✅ Cleared Region")
        
        # 10. Clear tax rules
        print("\n10. Clearing tax rules...")
        TaxRule.objects.all().delete()
        print("   ✅ Cleared TaxRule")
        
        # 11. Clear payment gateways
        print("\n11. Clearing payment gateways...")
        PaymentGateway.objects.all().delete()
        print("   ✅ Cleared PaymentGateway")
        
        # Note: We don't clear Saleor core data (products, orders, etc.)
        # as that might be production data. Only clear our extension data.
        
    print("\n" + "=" * 80)
    print("✅ ALL MOCK DATA CLEARED")
    print("=" * 80)
    print("\nNote: Saleor core data (if any) was NOT cleared.")
    print("Only extension app data was removed.")

if __name__ == '__main__':
    clear_all_mock_data()

