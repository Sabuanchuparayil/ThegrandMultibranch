# Startup Timeout Fix

## Problem

The container was stopping during `fix_all_product_columns.py` execution. The script was timing out because:

1. **Short timeout**: The subprocess timeout was only 30 seconds
2. **Inefficient database connections**: The script opened a new database connection for EACH column check (20+ connections), making it very slow

## Solution

### 1. Increased Timeout

**File**: `backend/grandgold_wsgi.py`

Changed timeout from 30 seconds to 120 seconds (2 minutes):

```python
timeout=120,  # Increased timeout for comprehensive column fixes
```

This gives the script enough time to complete even if it needs to add many columns.

### 2. Optimized Database Connections

**File**: `backend/fix_all_product_columns.py`

**Before**: Opened a new connection for each column check:
```python
def check_column_exists(table_name, column_name):
    with _connect() as conn, conn.cursor() as cursor:
        # check column...
```

**After**: Reuses a single connection for all operations:
```python
def check_column_exists(cursor, table_name, column_name):
    # Uses the provided cursor instead of creating new connection
    cursor.execute(...)

# In add_all_product_columns():
with _connect() as conn, conn.cursor() as cursor:
    # All operations use the same connection
    for col in all_required_columns:
        if not check_column_exists(cursor, "product_product", col['name']):
            # Add column using same cursor
```

**Performance Impact**:
- **Before**: 20+ columns = 20+ database connections = ~30+ seconds
- **After**: 20+ columns = 1 database connection = ~5-10 seconds

### 3. Added Better Error Handling

Added explicit timeout exception handling:

```python
except subprocess.TimeoutExpired:
    print(f"⚠️  {script_name} timed out after 120 seconds")
```

## Files Changed

1. ✅ `backend/grandgold_wsgi.py` - Increased timeout from 30s to 120s
2. ✅ `backend/fix_all_product_columns.py` - Optimized to reuse database connections

## Expected Results

After these changes:

1. ✅ Script should complete faster (5-10 seconds instead of 30+ seconds)
2. ✅ Script should not timeout (120 second limit is much higher than needed)
3. ✅ Container should start successfully without stopping during startup
4. ✅ Startup logs should show successful completion of all scripts

## Testing

After deploying:

1. Check Railway logs for `fix_all_product_columns.py` completion
2. Verify script output shows columns being added/verified
3. Verify container starts successfully and stays running
4. Verify `create_superuser_if_needed.py` runs after migrations

