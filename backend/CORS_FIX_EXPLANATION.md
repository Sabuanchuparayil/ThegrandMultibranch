# CORS Error Fix Explanation

## Error Description

The following CORS error was occurring:
```
Access to fetch at 'https://backend-production-d769.up.railway.app/graphql/' 
from origin 'https://admin-dashboard-production-1924.up.railway.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header 
is present on the requested resource.
```

## Root Cause

The CORS configuration in `grandgold_settings.py` was setting `CORS_ALLOWED_ORIGINS` to a specific list of origins, but when both `CORS_ALLOWED_ORIGINS` and `CORS_ALLOWED_ORIGIN_REGEXES` are used together, django-cors-headers processes them separately. The regex patterns should work, but the configuration needed to be more explicit.

## Solution

Updated the CORS configuration to:

1. **Explicitly set `CORS_ALLOW_ALL_ORIGINS = False`** for security
2. **Use `CORS_ALLOWED_ORIGIN_REGEXES`** to dynamically match all Railway subdomains:
   - `r'^https://.*\.railway\.app$'` - Matches any HTTPS Railway subdomain
   - `r'^http://.*\.railway\.app$'` - Matches any HTTP Railway subdomain (for testing)
   - `r'^http://localhost:\d+$'` - Matches localhost with any port
   - `r'^http://127\.0\.0\.1:\d+$'` - Matches 127.0.0.1 with any port

3. **Include explicit origins as backup** in `CORS_ALLOWED_ORIGINS`:
   - Common Railway URLs are included as a fallback
   - Environment variable `CORS_ALLOWED_ORIGINS` can override defaults

## How It Works

When a request comes from `https://admin-dashboard-production-1924.up.railway.app`:

1. Django CORS middleware checks if the origin matches `CORS_ALLOWED_ORIGINS` (exact match)
2. If not found, it checks if the origin matches any pattern in `CORS_ALLOWED_ORIGIN_REGEXES`
3. The regex pattern `^https://.*\.railway\.app$` matches the origin
4. The middleware adds the `Access-Control-Allow-Origin` header to the response
5. The browser allows the request to proceed

## Configuration Details

```python
CORS_ALLOW_ALL_ORIGINS = False  # Security: Don't allow all origins

CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://.*\.railway\.app$',  # Match any Railway subdomain
    r'^http://.*\.railway\.app$',   # Match HTTP Railway subdomains
    r'^http://localhost:\d+$',      # Localhost with any port
    r'^http://127\.0\.0\.1:\d+$',   # 127.0.0.1 with any port
]

CORS_ALLOWED_ORIGINS = [
    'https://admin-dashboard-production-1924.up.railway.app',
    'https://storefront-app-production-1924.up.railway.app',
    'http://localhost:3000',
    'http://localhost:3001',
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies/auth headers
```

## Deployment Notes

1. **Restart Required**: After deploying this change, the backend service must be restarted for the new CORS configuration to take effect.

2. **Testing**: After deployment, test the GraphQL endpoint from the admin dashboard:
   - The CORS error should no longer appear
   - GraphQL queries should work correctly
   - The browser console should not show CORS errors

3. **Environment Variables**: If you need to add additional origins, you can set the `CORS_ALLOWED_ORIGINS` environment variable in Railway:
   ```
   CORS_ALLOWED_ORIGINS=https://custom-domain.com,https://another-domain.com
   ```

## Benefits

- **Flexible**: Works with any Railway subdomain without code changes
- **Secure**: Only allows Railway subdomains and localhost, not all origins
- **Maintainable**: No need to update code when Railway URLs change
- **Development-friendly**: Supports localhost for local development

## Related Files

- `backend/grandgold_settings.py` - CORS configuration
- `backend/requirements.txt` - django-cors-headers dependency


