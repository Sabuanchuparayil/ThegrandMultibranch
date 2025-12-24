# Saleor Integration Checklist

Use this checklist to track your progress through the integration process.

## Phase 1: Saleor Installation & Setup

- [ ] Saleor 3.20+ installed (`pip install saleor>=3.20.0`)
- [ ] Saleor project structure initialized
- [ ] PostgreSQL database configured
- [ ] Redis configured
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Saleor migrations run successfully (`python manage.py migrate`)
- [ ] Django admin accessible (`python manage.py createsuperuser`)

## Phase 2: Settings Configuration

- [ ] `saleor/settings/base.py` or `local.py` created/updated
- [ ] All 20 extension apps added to `INSTALLED_APPS`
- [ ] Audit middleware added to `MIDDLEWARE`
- [ ] Environment variables configured (`.env` file)
- [ ] Database connection verified
- [ ] Redis connection verified
- [ ] Settings file loads without errors

## Phase 3: Model Updates

### Orders Module
- [ ] `OrderBranchAssignment.order_id` → `ForeignKey('order.Order')`
- [ ] `ManualOrder.customer_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Products Module
- [ ] `JewelleryProductAttribute.product_id` → `OneToOneField('product.Product')`
- [ ] `ProductMakingCharge.product_id` → `ForeignKey('product.Product')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Customers Module
- [ ] `CustomerProfile.customer_id` → `OneToOneField('account.User')`
- [ ] `CustomerGroup.customer_ids` → `ManyToManyField(User)`
- [ ] `LoyaltyPoints.customer_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Inventory Module
- [ ] `BranchInventory.product_id` → `ForeignKey('product.ProductVariant')`
- [ ] `StockMovement.product_id` → `ForeignKey('product.ProductVariant')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Invoices Module
- [ ] `Invoice.order_id` → `ForeignKey('order.Order')`
- [ ] `Invoice.customer_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Payments Module
- [ ] `PaymentTransaction.order_id` → `ForeignKey('order.Order')` or `ForeignKey('payment.Payment')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Fulfillment Module
- [ ] `Shipment.order_id` → `ForeignKey('order.Order')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Returns Module
- [ ] `ReturnRequest.order_id` → `ForeignKey('order.Order')`
- [ ] `ReturnRequest.customer_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Audit Module
- [ ] `AuditLog.user_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

### Permissions Module
- [ ] `UserRole.user_id` → `ForeignKey('account.User')`
- [ ] Migration created
- [ ] Migration applied
- [ ] Tested in admin

## Phase 4: Initial Data Setup

- [ ] Create initial regions (UK, UAE, India)
- [ ] Create initial currencies (GBP, AED, INR)
- [ ] Create at least one branch per region
- [ ] Create initial customer groups
- [ ] Create payment gateways per region
- [ ] Set up tax rules per region
- [ ] Verify all relationships work correctly

## Phase 5: GraphQL API Development

- [ ] `graphene-django` installed
- [ ] Branches schema activated and tested
- [ ] Products schema implemented
- [ ] Orders schema implemented
- [ ] Inventory schema implemented
- [ ] Pricing schema implemented
- [ ] Customers schema implemented
- [ ] GraphQL playground accessible
- [ ] Queries tested
- [ ] Mutations tested
- [ ] Authentication working

## Phase 6: Service Implementation

- [ ] Payment gateway SDKs installed (stripe, razorpay, etc.)
- [ ] Payment gateway implementations completed
- [ ] Invoice PDF generation working
- [ ] Currency API integration working
- [ ] Gold rate API integration working
- [ ] Logistics integrations working
- [ ] Notification services working

## Phase 7: Celery Tasks

- [ ] Celery configured in settings
- [ ] `tasks.py` created
- [ ] Celery beat schedule configured
- [ ] Worker service running
- [ ] Beat service running
- [ ] Test tasks execute successfully
- [ ] Currency rate updates working
- [ ] Gold rate updates working
- [ ] Scheduled reports working

## Phase 8: Testing

- [ ] All models can be created via admin
- [ ] ForeignKey relationships work correctly
- [ ] GraphQL queries return correct data
- [ ] GraphQL mutations create/update correctly
- [ ] Celery tasks execute on schedule
- [ ] Services work as expected
- [ ] No critical errors in logs

## Phase 9: Frontend Integration (Next Phase)

- [ ] Admin dashboard connects to GraphQL API
- [ ] Storefront connects to GraphQL API
- [ ] Authentication flow working
- [ ] Data displays correctly
- [ ] Forms submit correctly

## Phase 10: Deployment (Final Phase)

- [ ] Railway services configured
- [ ] Environment variables set
- [ ] Database migrations run on production
- [ ] All services running
- [ ] Health checks passing
- [ ] Monitoring set up

---

## Notes

- Work through each phase systematically
- Test after each model update
- Don't skip migration testing
- Keep backups before major changes
- Document any customizations

## Troubleshooting

If you encounter issues:
1. Check error logs
2. Verify Saleor installation
3. Confirm all migrations applied
4. Test ForeignKey relationships
5. Review Django admin for errors

---

**Current Phase**: _______________

**Last Updated**: _______________

