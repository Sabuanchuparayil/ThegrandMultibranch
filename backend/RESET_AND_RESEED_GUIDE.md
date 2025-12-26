# Reset and Reseed Guide

## Overview

This guide explains how to clear all mock data, complete migrations, and reseed initial data.

## Scripts Created

### 1. `clear_mock_data.py`
Clears all mock/seed data from extension apps (regions, currencies, branches, inventory, pricing, orders, products, customer groups, tax rules, payment gateways).

**Note:** Does NOT clear Saleor core data (Saleor products, orders, etc.) as that might be production data.

### 2. `reset_and_reseed.py`
Complete automated reset flow:
1. Clears all mock data
2. Ensures migrations are complete
3. Reseeds initial data

### 3. `create_initial_data.py` (existing)
Creates initial seed data (regions, currencies, branches, customer groups).

## Usage

### Option 1: Automated Reset (Recommended)

```bash
# In Django shell
python manage.py shell
>>> exec(open('reset_and_reseed.py').read())
```

Or run directly:
```bash
python reset_and_reseed.py
```

### Option 2: Manual Step-by-Step

```bash
# Step 1: Clear mock data
python manage.py shell
>>> exec(open('clear_mock_data.py').read())

# Step 2: Run migrations
python manage.py migrate

# Step 3: Reseed data
python manage.py shell
>>> exec(open('create_initial_data.py').read())
```

## What Gets Cleared

The `clear_mock_data.py` script clears data in this order (reverse dependency):

1. **Inventory Data**
   - LowStockAlert
   - StockTransfer
   - StockMovement
   - BranchInventory

2. **Pricing Data**
   - PricingOverride
   - MakingCharge
   - GoldRate

3. **Orders**
   - Order (extension app orders)

4. **Products**
   - Product (extension app products)

5. **Branches**
   - Branch

6. **Customer Groups**
   - CustomerGroup

7. **Exchange Rates**
   - ExchangeRate

8. **Currencies**
   - Currency

9. **Regions**
   - Region

10. **Tax Rules**
    - TaxRule

11. **Payment Gateways**
    - PaymentGateway

## What Gets Reseeded

The `create_initial_data.py` script creates:

1. **Regions**
   - UK (United Kingdom)
   - UAE (United Arab Emirates)
   - INDIA (India)

2. **Currencies**
   - GBP (British Pound)
   - AED (UAE Dirham)
   - INR (Indian Rupee)

3. **Branches**
   - London Store (UK)
   - Dubai Mall Store (UAE)
   - Mumbai Store (India)

4. **Customer Groups**
   - Retail Customer
   - Loyalty Customer
   - VIP Customer

## Migration Fix

The migration process has been updated to handle problematic Saleor migrations that try to import GraphQL schema classes:

- **Problem:** Some Saleor migrations (`site.0014`, `site.0015`, `site.0017`, `checkout.0008`) import `ProductFilterInput` from GraphQL schema at import time, causing circular import errors.

- **Solution:** These migrations are now marked as applied directly in the database using `MigrationRecorder.record_applied()` without loading the migration file, avoiding the circular import.

## Important Notes

1. **Saleor Core Data:** The clear script does NOT delete Saleor core data (Saleor products, orders, users, etc.). Only extension app data is cleared.

2. **Migrations:** The reset script ensures migrations are complete before reseeding. If migrations fail, you'll be prompted whether to continue.

3. **Dependencies:** Data is cleared in reverse dependency order to avoid foreign key constraint violations.

4. **Transactions:** All clear operations run in a single database transaction for safety.

## Troubleshooting

### Migration Errors

If migrations fail during reset:

1. Check the error message
2. The script will prompt whether to continue with seeding
3. You can manually fix migrations and then run seeding separately:

```bash
python manage.py migrate
python manage.py shell
>>> exec(open('create_initial_data.py').read())
```

### Foreign Key Errors

If you get foreign key errors during clearing:

- The script clears in reverse dependency order, so this shouldn't happen
- If it does, check that all related data is being cleared
- You may need to manually clear remaining references

### Missing Tables

If tables don't exist when trying to clear:

- This is OK - the script uses `.all().delete()` which is safe on empty querysets
- The script will continue even if some tables don't exist

## Next Steps After Reset

After resetting and reseeding:

1. **Verify Data:**
   ```bash
   python manage.py shell
   >>> from saleor_extensions.regions.models import Region
   >>> Region.objects.count()  # Should be 3
   >>> from saleor_extensions.branches.models import Branch
   >>> Branch.objects.count()  # Should be 3
   ```

2. **Create Superuser (if needed):**
   ```bash
   python manage.py createsuperuser
   ```

3. **Test GraphQL:**
   - Verify GraphQL queries work without 400 errors
   - Test product queries, branch queries, etc.

4. **Add Additional Data:**
   - Create products via admin or GraphQL
   - Add inventory records
   - Create orders
   - etc.

