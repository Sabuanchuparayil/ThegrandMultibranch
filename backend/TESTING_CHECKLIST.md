# GraphQL Testing Checklist

## Pre-Testing Setup

### ✅ Completed
- [x] GraphQL schema implemented
- [x] Integration structure created
- [x] BaseMutation fallback implemented
- [x] Dependencies installed (setuptools)
- [x] Documentation created

### ⏳ Required Before Testing
- [ ] Database configured in `saleor/settings/local.py`
- [ ] Migrations run: `python manage.py migrate`
- [ ] Test data created:
  - [ ] At least one Branch
  - [ ] At least one Product/ProductVariant
  - [ ] At least one BranchInventory record (optional, can create via mutation)

## Testing Steps

### 1. Basic Schema Test
```bash
python test_graphql_standalone.py
```
**Expected**: Should show available queries and mutations

### 2. Start Server
```bash
python manage.py runserver
```
**Expected**: Server starts on http://localhost:8000

### 3. Test GraphQL Endpoint
Visit: `http://localhost:8000/graphql/`

**Test Introspection:**
```graphql
{
  __schema {
    queryType {
      fields {
        name
      }
    }
    mutationType {
      fields {
        name
      }
    }
  }
}
```

**Expected**: Should list all inventory queries and mutations

### 4. Test Queries (require data)

#### Query: Branch Inventory
- Requires: Branch ID
- Returns: Inventory list for branch

#### Query: Stock Movements
- Requires: Branch ID (optional)
- Returns: Movement history

### 5. Test Mutations (require data)

#### Mutation: Stock Adjustment
- Requires: Branch ID, Product Variant ID
- Creates: Inventory record if doesn't exist
- Updates: Stock quantity

#### Mutation: Create Transfer
- Requires: From/To Branch IDs, Product Variant ID
- Creates: Transfer request

## Success Criteria

✅ Schema can be imported  
✅ All queries are accessible  
✅ All mutations are accessible  
✅ Queries return data (with test data)  
✅ Mutations create/update data correctly  
✅ Error handling works  

## Troubleshooting

### Issue: Import Errors
**Solution**: Check Django settings module path

### Issue: No Data Returned
**Solution**: Create test data in Django admin

### Issue: Mutation Fails
**Solution**: Check foreign key relationships exist

---

For detailed examples, see `GRAPHQL_INTEGRATION_COMPLETE.md`

