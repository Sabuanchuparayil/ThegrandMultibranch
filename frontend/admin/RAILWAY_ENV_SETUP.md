# Railway Environment Variable Setup

## Fix "Failed to fetch" / CORS Errors

The frontend is currently using a hardcoded backend URL. To avoid needing to rebuild when the backend URL changes, set an environment variable.

### Step 1: Set Environment Variable in Railway

1. Go to Railway dashboard: https://railway.app
2. Open your **admin dashboard** service (frontend)
3. Click **"Variables"** tab
4. Click **"+ New Variable"**
5. Add:
   - **Name**: `NEXT_PUBLIC_GRAPHQL_URL`
   - **Value**: `https://backend-production-fb5f.up.railway.app/graphql/`
6. Click **"Add"**

### Step 2: Redeploy Frontend

After adding the environment variable, Railway will automatically redeploy. Or manually trigger a redeploy:

1. Go to **"Deployments"** tab
2. Click **"Redeploy"** on the latest deployment

### Step 3: Verify

After redeploy, the frontend will use the environment variable instead of the hardcoded URL. This means:
- ✅ No rebuild needed when backend URL changes
- ✅ Just update the environment variable
- ✅ Frontend automatically picks up the new URL

---

## Alternative: Force Rebuild

If you prefer to keep the hardcoded URL, you can force a rebuild:

1. Make a small change to trigger rebuild (e.g., add a comment)
2. Commit and push
3. Railway will rebuild with the new backend URL

But using environment variables is the recommended approach.

