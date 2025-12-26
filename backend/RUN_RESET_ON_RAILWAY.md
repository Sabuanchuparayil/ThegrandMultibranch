# Running Reset and Reseed on Railway

## Option 1: Via Railway Shell (Recommended)

1. Go to Railway dashboard → Your backend service
2. Click on "Deployments" → Latest deployment
3. Click "Shell" tab (or use Railway CLI: `railway shell`)
4. Run the reset script:

```bash
python reset_and_reseed.py
```

Or run step by step:

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

## Option 2: Via Railway CLI

If Railway CLI is configured:

```bash
# Link to project
railway link

# Run reset script (if files are accessible)
railway run python reset_and_reseed.py

# Or run via Django shell
railway run python manage.py shell
# Then in the shell:
>>> exec(open('reset_and_reseed.py').read())
```

## Option 3: Create Management Command (Most Reliable)

Create a Django management command for better integration:

```bash
# Create command directory
mkdir -p backend/saleor_extensions/core/management/commands

# Create __init__.py files
touch backend/saleor_extensions/core/management/__init__.py
touch backend/saleor_extensions/core/management/commands/__init__.py

# Then create the command file (see below)
```

Then run:
```bash
railway run python manage.py reset_and_reseed
```

## Troubleshooting

### Files Not Found

If you get "No such file or directory":
- Check that files are in the backend directory
- Verify Railway service root directory is set to `backend`
- Files should be at: `/app/clear_mock_data.py` in the container

### Migration Errors

If migrations fail:
- Check logs: `railway logs --service backend`
- The reset script will prompt whether to continue with seeding
- You can manually fix migrations and then run seeding separately

### Permission Errors

If you get permission errors:
- Ensure you're running in the correct service
- Check that database connection is configured
- Verify environment variables are set

## Manual Step-by-Step (If Scripts Don't Work)

1. **Clear Data Manually:**
   ```python
   python manage.py shell
   >>> from saleor_extensions.regions.models import Region
   >>> Region.objects.all().delete()
   >>> # Repeat for other models...
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Reseed Data:**
   ```python
   python manage.py shell
   >>> exec(open('create_initial_data.py').read())
   ```

