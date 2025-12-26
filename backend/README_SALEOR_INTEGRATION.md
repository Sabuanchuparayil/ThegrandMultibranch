# Saleor Integration - Quick Start

## Current Status

✅ All 20 Django extension apps created  
✅ Models, services, and admin interfaces complete  
⏳ Saleor integration needed  

## Quick Integration Steps

### Step 1: Install Saleor

```bash
cd backend
source venv/bin/activate  # or your virtual env

# Option 1: Use installation script
./install_saleor.sh

# Option 2: Manual installation
pip install saleor>=3.20.0
```

### Step 2: Check Setup

```bash
# Run integration checker
./integration_steps.sh
```

This will verify:
- Saleor is installed
- Saleor directory exists
- Extensions are present

### Step 3: Update Settings

1. Open `saleor/settings/base.py` (or create `local.py`)
2. Add your apps to `INSTALLED_APPS`:
   ```python
   # See: saleor_settings_integration.py for exact code
   ```
3. Add middleware:
   ```python
   'saleor_extensions.audit.middleware.AuditLogMiddleware',
   ```

### Step 4: Update Models

Follow `MODEL_UPDATES.md` to update each model with ForeignKeys.

**Start with these key models:**
1. `orders/models.py` - OrderBranchAssignment
2. `products/models.py` - JewelleryProductAttribute  
3. `customers/models.py` - CustomerProfile

### Step 5: Create Migrations

```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 6: Create Initial Data

```bash
python manage.py shell
>>> exec(open('create_initial_data.py').read())
```

Or as a management command:
```bash
python manage.py shell < create_initial_data.py
```

### Step 7: Test Integration

1. Start server: `python manage.py runserver`
2. Visit admin: `http://localhost:8000/admin`
3. Verify:
   - All extension apps visible
   - Can create records
   - ForeignKey relationships work

## Files Reference

### Documentation
- **`SALEOR_INTEGRATION_GUIDE.md`** - Complete step-by-step guide
- **`MODEL_UPDATES.md`** - Exact model changes needed
- **`INTEGRATION_CHECKLIST.md`** - Progress tracker

### Configuration
- **`saleor_settings_integration.py`** - Settings to add
- **`saleor_settings_template.py`** - Full template

### Scripts
- **`install_saleor.sh`** - Install Saleor
- **`integration_steps.sh`** - Check setup
- **`integrate_models.py`** - Find models needing updates
- **`create_initial_data.py`** - Create initial data

## Common Issues

### Issue: "No module named 'saleor'"
**Solution**: Install Saleor - `pip install saleor>=3.20.0`

### Issue: "Saleor directory not found"
**Solution**: Initialize Saleor project structure
- Follow: https://docs.saleor.io/docs/3.x/developer/installation

### Issue: "ForeignKey doesn't exist"
**Solution**: 
1. Make sure Saleor migrations are run first: `python manage.py migrate`
2. Check app name in ForeignKey is correct: `'order.Order'` not `'saleor.order.Order'`

### Issue: "Migration conflicts"
**Solution**:
1. Always run Saleor migrations first
2. Then create your extension migrations
3. Review migration files if conflicts occur

## Next Steps After Integration

1. ✅ Test all models in Django admin
2. ✅ Build GraphQL APIs (see `branches/schema.py` for example)
3. ✅ Complete service implementations
4. ✅ Set up Celery tasks
5. ✅ Build frontend interfaces

## Need Help?

- **Saleor Docs**: https://docs.saleor.io/
- **Integration Guide**: `SALEOR_INTEGRATION_GUIDE.md`
- **Model Updates**: `MODEL_UPDATES.md`
- **Checklist**: `INTEGRATION_CHECKLIST.md`

---

**Status**: Ready for Saleor Integration 🚀


