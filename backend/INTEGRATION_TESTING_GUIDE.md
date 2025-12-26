# GraphQL Integration Testing Guide

## Quick Start Testing

### Step 1: Install Missing Dependencies

```bash
cd backend
source venv/bin/activate
pip install setuptools  # Fixes pkg_resources issue
```

### Step 2: Configure Database

Ensure `saleor/settings/local.py` has database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'grandgold_dev',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Test Schema Import

```bash
python test_graphql_standalone.py
```

This will test if the schema can be imported and introspected.

### Step 5: Start Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000/graphql/`

## Testing Queries

### Using GraphQL Playground

1. Open browser to `http://localhost:8000/graphql/`
2. Try the introspection query to see available queries/mutations
3. Try example queries from `GRAPHQL_INTEGRATION_COMPLETE.md`

### Using Python Script

Create a test script:

```python
import requests

url = "http://localhost:8000/graphql/"
query = """
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}
"""

response = requests.post(url, json={'query': query})
print(response.json())
```

## Integration Status

✅ **Schema Implementation**: Complete  
✅ **Integration Structure**: Complete  
✅ **BaseMutation Fallback**: Complete  
⏳ **Database Setup**: Required  
⏳ **Testing**: Pending database setup  

---

For detailed examples, see `GRAPHQL_INTEGRATION_COMPLETE.md`


