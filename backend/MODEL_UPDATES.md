# Model Updates for Saleor Integration

This document shows exactly what needs to be changed in each model file.

## Orders Module

**File**: `saleor_extensions/orders/models.py`

### OrderBranchAssignment

**FIND:**
```python
order_id = models.CharField(max_length=255, unique=True)  # Temporary until Saleor integration
```

**REPLACE WITH:**
```python
from saleor.order.models import Order

order = models.OneToOneField(
    Order,
    on_delete=models.CASCADE,
    related_name='branch_assignment',
    primary_key=False  # We'll use an id field as primary key
)
```

### ManualOrder

**FIND:**
```python
order_id = models.CharField(max_length=255, unique=True)
```

**REPLACE WITH:**
```python
from saleor.order.models import Order

order = models.OneToOneField(
    Order,
    on_delete=models.CASCADE,
    related_name='manual_order'
)
```

---

## Products Module

**File**: `saleor_extensions/products/models.py`

### JewelleryProductAttribute

**FIND:**
```python
product_id = models.CharField(max_length=255, unique=True)
```

**REPLACE WITH:**
```python
from saleor.product.models import Product

product = models.OneToOneField(
    Product,
    on_delete=models.CASCADE,
    related_name='jewellery_attributes'
)
```

### ProductMakingCharge

**FIND:**
```python
product_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.product.models import Product

product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    related_name='making_charges'
)
```

---

## Customers Module

**File**: `saleor_extensions/customers/models.py`

### CustomerProfile

**FIND:**
```python
customer_id = models.CharField(max_length=255, unique=True)
```

**REPLACE WITH:**
```python
from saleor.account.models import User

customer = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='customer_profile'
)
```

### CustomerGroup

**FIND:**
```python
customer_ids = models.JSONField(default=list)  # List of customer IDs
```

**REPLACE WITH:**
```python
from saleor.account.models import User

customers = models.ManyToManyField(
    User,
    related_name='customer_groups',
    blank=True
)
```

### LoyaltyPoints

**FIND:**
```python
customer_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.account.models import User

customer = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='loyalty_points'
)
```

---

## Inventory Module

**File**: `saleor_extensions/inventory/models.py`

### BranchInventory

**FIND:**
```python
product_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.product.models import ProductVariant

product_variant = models.ForeignKey(
    ProductVariant,
    on_delete=models.CASCADE,
    related_name='branch_inventory'
)
```

### StockMovement

**FIND:**
```python
product_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.product.models import ProductVariant

product_variant = models.ForeignKey(
    ProductVariant,
    on_delete=models.CASCADE,
    related_name='stock_movements'
)
```

---

## Invoices Module

**File**: `saleor_extensions/invoices/models.py`

### Invoice

**FIND:**
```python
order_id = models.CharField(max_length=255)
customer_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.order.models import Order
from saleor.account.models import User

order = models.ForeignKey(
    Order,
    on_delete=models.PROTECT,
    related_name='invoices'
)
customer = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='invoices'
)
```

---

## Payments Module

**File**: `saleor_extensions/payments/models.py`

### PaymentTransaction

**FIND:**
```python
order_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.payment.models import Payment

payment = models.ForeignKey(
    Payment,  # Or link to Order if you prefer
    on_delete=models.PROTECT,
    related_name='branch_transactions'
)

# OR if you want to link to Order directly:
from saleor.order.models import Order

order = models.ForeignKey(
    Order,
    on_delete=models.PROTECT,
    related_name='payment_transactions'
)
```

---

## Fulfillment Module

**File**: `saleor_extensions/fulfillment/models.py`

### Shipment

**FIND:**
```python
order_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.order.models import Order

order = models.ForeignKey(
    Order,
    on_delete=models.CASCADE,
    related_name='shipments'
)
```

---

## Returns Module

**File**: `saleor_extensions/returns/models.py`

### ReturnRequest

**FIND:**
```python
order_id = models.CharField(max_length=255)
customer_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.order.models import Order
from saleor.account.models import User

order = models.ForeignKey(
    Order,
    on_delete=models.PROTECT,
    related_name='return_requests'
)
customer = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='return_requests'
)
```

---

## Audit Module

**File**: `saleor_extensions/audit/models.py`

### AuditLog

**FIND:**
```python
user_id = models.CharField(max_length=255, blank=True)
```

**REPLACE WITH:**
```python
from saleor.account.models import User

user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='audit_logs'
)
```

---

## Permissions Module

**File**: `saleor_extensions/permissions/models.py`

### UserRole

**FIND:**
```python
user_id = models.CharField(max_length=255)
```

**REPLACE WITH:**
```python
from saleor.account.models import User

user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='user_roles'
)
```

---

## Important Notes

1. **Run Saleor migrations first** before creating your own migrations
2. **Test each model** after updating to ensure ForeignKeys work
3. **Consider data migration** if you have existing data with string IDs
4. **Use `on_delete=models.PROTECT`** for critical relationships (orders, invoices)
5. **Use `on_delete=models.CASCADE`** for dependent data (inventory, movements)
6. **Use `on_delete=models.SET_NULL`** for optional relationships (user in audit logs)

## Migration Strategy

If you have existing data:

1. Create a data migration script
2. Map string IDs to actual ForeignKey objects
3. Update records in batches
4. Verify data integrity
5. Then update model fields

## Testing Checklist

After updating each model:
- [ ] Migration created successfully
- [ ] Migration applied successfully
- [ ] Can create new records via admin
- [ ] Can access related objects
- [ ] ForeignKey relationships work correctly
- [ ] No data loss occurred

