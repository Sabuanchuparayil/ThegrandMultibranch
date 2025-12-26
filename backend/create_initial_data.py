"""
Script to create initial data for the system

Usage:
    python manage.py shell
    >>> exec(open('create_initial_data.py').read())

Or run as Django management command (create command if needed):
    python manage.py create_initial_data
"""
from django.utils import timezone
from datetime import datetime

# Regions
from saleor_extensions.regions.models import Region

# Currencies
from saleor_extensions.currency.models import Currency, ExchangeRate

# Branches
from saleor_extensions.branches.models import Branch

# Customer Groups
from saleor_extensions.customers.models import CustomerGroup

# Payment Gateways (will need actual gateway setup later)
from saleor_extensions.payments.models import PaymentGateway

# Taxes
from saleor_extensions.taxes.models import TaxRule


def create_regions():
    """Create initial regions"""
    regions_data = [
        {
            'code': 'UK',
            'name': 'United Kingdom',
            'default_currency': 'GBP',
            'tax_rate': 20.00,  # VAT 20%
            'timezone': 'Europe/London',
            'locale': 'en-GB',
        },
        {
            'code': 'UAE',
            'name': 'United Arab Emirates',
            'default_currency': 'AED',
            'tax_rate': 5.00,  # VAT 5%
            'timezone': 'Asia/Dubai',
            'locale': 'en-AE',
        },
        {
            'code': 'INDIA',
            'name': 'India',
            'default_currency': 'INR',
            'tax_rate': 3.00,  # GST 3%
            'timezone': 'Asia/Kolkata',
            'locale': 'en-IN',
        },
    ]
    
    created = []
    for data in regions_data:
        region, created_flag = Region.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        created.append((region, created_flag))
        print(f"{'Created' if created_flag else 'Exists'}: {region}")
    
    return created


def create_currencies():
    """Create initial currencies"""
    currencies_data = [
        {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'},
        {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'د.إ'},
        {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹'},
    ]
    
    created = []
    for data in currencies_data:
        currency, created_flag = Currency.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        created.append((currency, created_flag))
        print(f"{'Created' if created_flag else 'Exists'}: {currency}")
    
    return created


def create_branches():
    """Create sample branches for each region"""
    try:
        uk_region = Region.objects.get(code='UK')
        uae_region = Region.objects.get(code='UAE')
        india_region = Region.objects.get(code='INDIA')
    except Region.DoesNotExist:
        print("Error: Regions must be created first")
        return
    
    branches_data = [
        {
            'name': 'London Store',
            'code': 'LON-001',
            'region': uk_region,
            'address_line_1': '123 High Street',
            'city': 'London',
            'state': 'England',
            'postal_code': 'SW1A 1AA',
            'country': 'United Kingdom',
            'phone': '+44 20 1234 5678',
            'email': 'london@grandgold.com',
            'operating_hours': {
                'monday': {'open': '09:00', 'close': '18:00'},
                'tuesday': {'open': '09:00', 'close': '18:00'},
                'wednesday': {'open': '09:00', 'close': '18:00'},
                'thursday': {'open': '09:00', 'close': '18:00'},
                'friday': {'open': '09:00', 'close': '18:00'},
                'saturday': {'open': '10:00', 'close': '17:00'},
                'sunday': {'open': '11:00', 'close': '16:00'},
            }
        },
        {
            'name': 'Dubai Mall Store',
            'code': 'DXB-001',
            'region': uae_region,
            'address_line_1': 'Dubai Mall, Ground Floor',
            'city': 'Dubai',
            'state': 'Dubai',
            'postal_code': '00000',
            'country': 'United Arab Emirates',
            'phone': '+971 4 123 4567',
            'email': 'dubai@grandgold.com',
            'operating_hours': {
                'sunday': {'open': '10:00', 'close': '22:00'},
                'monday': {'open': '10:00', 'close': '22:00'},
                'tuesday': {'open': '10:00', 'close': '22:00'},
                'wednesday': {'open': '10:00', 'close': '22:00'},
                'thursday': {'open': '10:00', 'close': '22:00'},
                'friday': {'open': '14:00', 'close': '22:00'},
                'saturday': {'open': '10:00', 'close': '22:00'},
            }
        },
        {
            'name': 'Mumbai Store',
            'code': 'BOM-001',
            'region': india_region,
            'address_line_1': '123 MG Road',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400001',
            'country': 'India',
            'phone': '+91 22 1234 5678',
            'email': 'mumbai@grandgold.com',
            'operating_hours': {
                'monday': {'open': '10:00', 'close': '20:00'},
                'tuesday': {'open': '10:00', 'close': '20:00'},
                'wednesday': {'open': '10:00', 'close': '20:00'},
                'thursday': {'open': '10:00', 'close': '20:00'},
                'friday': {'open': '10:00', 'close': '20:00'},
                'saturday': {'open': '10:00', 'close': '20:00'},
                'sunday': {'open': '11:00', 'close': '19:00'},
            }
        },
    ]
    
    created = []
    for data in branches_data:
        branch, created_flag = Branch.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        created.append((branch, created_flag))
        print(f"{'Created' if created_flag else 'Exists'}: {branch}")
    
    return created


def create_customer_groups():
    """Create initial customer groups"""
    groups_data = [
        {
            'name': 'Retail Customer',
            'group_type': 'RETAIL',
            'description': 'Standard retail customers',
            'discount_percentage': 0,
        },
        {
            'name': 'Loyalty Customer',
            'group_type': 'LOYALTY',
            'description': 'Loyalty program members',
            'discount_percentage': 5.00,
        },
        {
            'name': 'VIP Customer',
            'group_type': 'VIP',
            'description': 'VIP customers',
            'discount_percentage': 10.00,
        },
    ]
    
    created = []
    for data in groups_data:
        group, created_flag = CustomerGroup.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        created.append((group, created_flag))
        print(f"{'Created' if created_flag else 'Exists'}: {group}")
    
    return created


def run():
    """Run all initial data creation"""
    print("=" * 60)
    print("Creating Initial Data")
    print("=" * 60)
    
    print("\n1. Creating Regions...")
    create_regions()
    
    print("\n2. Creating Currencies...")
    create_currencies()
    
    print("\n3. Creating Branches...")
    create_branches()
    
    print("\n4. Creating Customer Groups...")
    create_customer_groups()
    
    print("\n" + "=" * 60)
    print("Initial Data Creation Complete!")
    print("=" * 60)
    print("\nNote: Payment gateways and tax rules should be configured")
    print("via Django admin after Saleor integration is complete.")


# Run if executed directly
if __name__ == '__main__':
    run()


