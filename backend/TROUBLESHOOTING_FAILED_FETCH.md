# Troubleshooting "Failed to fetch" Errors

## Error Description
The frontend is showing "Failed to fetch" errors when trying to connect to the GraphQL endpoint, even after CORS configuration updates.

## Possible Causes

### 1. Backend Service Not Running
The backend service might not be running or may have crashed.

**Check:**
- Go to Railway dashboard → Backend service → Check if status is "Active"
- Check deployment logs for errors
- Verify the service started successfully

**Solution:**
- Restart the backend service in Railway
- Check logs for startup errors

### 2. Backend Not Accessible at URL
The backend URL might be incorrect or the service might be deployed to a different URL.

**Check:**
- Verify the backend URL in Railway dashboard
- Test the GraphQL endpoint directly: `https://backend-production-d769.up.railway.app/graphql/`
- Check if the endpoint returns a GraphQL interface or error page

**Solution:**
- Update the frontend `apollo-client.ts` if the backend URL has changed
- Verify the Railway service domain matches the hardcoded URL

### 3. Backend Not Restarted After CORS Changes
The CORS configuration changes require a backend restart to take effect.

**Solution:**
- Restart the backend service in Railway dashboard
- Or trigger a new deployment by pushing a commit

### 4. GraphQL Endpoint Not Configured
The GraphQL endpoint might not be properly set up or accessible.

**Check:**
- Visit `https://backend-production-d769.up.railway.app/graphql/` in browser
- Should see GraphQL Playground or GraphiQL interface
- If 404, the endpoint is not configured

**Solution:**
- Verify Saleor GraphQL endpoint is enabled
- Check URL routing configuration
- Ensure Saleor URLs are properly included

### 5. Network/Firewall Issues
Network connectivity between frontend and backend might be blocked.

**Check:**
- Test from browser console: `fetch('https://backend-production-d769.up.railway.app/graphql/', {method: 'OPTIONS'})`
- Check browser network tab for detailed error
- Verify SSL certificate is valid

### 6. CORS Preflight Request Failing
The OPTIONS preflight request might be failing.

**Check:**
- Open browser DevTools → Network tab
- Look for OPTIONS request to `/graphql/`
- Check if OPTIONS request returns proper CORS headers

**Solution:**
- Verify CORS middleware is properly configured
- Check that CORS middleware is before other middleware
- Ensure OPTIONS method is allowed in CORS_ALLOW_METHODS

## Diagnostic Steps

### Step 1: Verify Backend is Running
1. Go to Railway dashboard
2. Navigate to backend service
3. Check "Deployments" tab - latest deployment should be "Active"
4. Click "View Logs" to see if service started successfully

### Step 2: Test GraphQL Endpoint Directly
1. Open browser
2. Navigate to: `https://backend-production-d769.up.railway.app/graphql/`
3. Expected: GraphQL Playground/GraphiQL interface
4. If 404 or error: Endpoint is not configured properly

### Step 3: Test CORS Headers
Run this in browser console (from admin dashboard page):

```javascript
fetch('https://backend-production-d769.up.railway.app/graphql/', {
  method: 'OPTIONS',
  headers: {
    'Origin': window.location.origin,
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'content-type,authorization',
  },
})
.then(response => {
  console.log('CORS Headers:', response.headers);
  console.log('Status:', response.status);
})
.catch(error => {
  console.error('CORS Error:', error);
});
```

Check if response includes:
- `Access-Control-Allow-Origin` header
- `Access-Control-Allow-Methods` header
- `Access-Control-Allow-Headers` header

### Step 4: Test GraphQL Query
Run this in browser console:

```javascript
fetch('https://backend-production-d769.up.railway.app/graphql/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Origin': window.location.origin,
  },
  body: JSON.stringify({
    query: '{ __schema { types { name } } }'
  }),
})
.then(response => response.json())
.then(data => console.log('GraphQL Response:', data))
.catch(error => console.error('GraphQL Error:', error));
```

### Step 5: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for detailed error messages
4. Go to Network tab
5. Check failed requests - see status code and response

## Common Error Patterns

### Error: "net::ERR_FAILED"
- **Cause**: Network connectivity issue or backend not responding
- **Solution**: Verify backend is running and accessible

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"
- **Cause**: CORS middleware not working or misconfigured
- **Solution**: Verify CORS configuration and restart backend

### Error: "404 Not Found"
- **Cause**: GraphQL endpoint not configured or wrong URL
- **Solution**: Verify GraphQL URL routing and Saleor configuration

### Error: "500 Internal Server Error"
- **Cause**: Backend error (Django/Saleor issue)
- **Solution**: Check backend logs for error details

## Quick Fixes

### Fix 1: Restart Backend Service
1. Railway dashboard → Backend service
2. Click "..." menu → "Restart"
3. Wait for service to restart
4. Test again

### Fix 2: Verify Environment Variables
Check Railway backend service environment variables:
- `DJANGO_SETTINGS_MODULE` should be set
- `ALLOWED_HOSTS` should include Railway domain
- Database and Redis URLs should be set

### Fix 3: Check Backend Logs
1. Railway dashboard → Backend service → Deployments
2. Click latest deployment → View Logs
3. Look for:
   - Django startup messages
   - CORS middleware loading
   - Any error messages
   - GraphQL endpoint registration

### Fix 4: Verify CORS Middleware Order
The CORS middleware must be before `CommonMiddleware`. Check `grandgold_settings.py`:
```python
MIDDLEWARE = [
    # ... other middleware ...
    'corsheaders.middleware.CorsMiddleware',  # Must be BEFORE CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ... rest of middleware ...
]
```

## Verification Checklist

- [ ] Backend service is "Active" in Railway
- [ ] GraphQL endpoint is accessible: `https://backend-production-d769.up.railway.app/graphql/`
- [ ] Backend has been restarted after CORS changes
- [ ] CORS middleware is in correct position (before CommonMiddleware)
- [ ] CORS_ALLOWED_ORIGIN_REGEXES includes Railway subdomain pattern
- [ ] Browser console shows detailed error (not just "Failed to fetch")
- [ ] Network tab shows request/response details
- [ ] OPTIONS preflight request succeeds
- [ ] POST request to GraphQL returns data or proper error

## Next Steps

If issues persist after following this guide:
1. Share backend logs from Railway
2. Share browser console errors
3. Share Network tab details for failed requests
4. Verify backend URL is correct in frontend configuration


