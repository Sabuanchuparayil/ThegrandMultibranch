#!/bin/bash
# Quick Migration Commands for Railway
# Run these commands one by one in your terminal

echo "=========================================="
echo "Railway Database Migration Commands"
echo "=========================================="
echo ""
echo "Step 1: Link to Railway project"
echo "  cd backend"
echo "  railway link"
echo "  (Select 'Grand Multibranch' from the list)"
echo ""
echo "Step 2: Verify database connection"
echo "  railway run python verify_and_migrate.py"
echo ""
echo "Step 3: Run migrations"
echo "  railway run python manage.py migrate"
echo ""
echo "Step 4: Verify migrations completed"
echo "  railway run python manage.py showmigrations --plan | grep '\[ \]'"
echo "  (Should show no unapplied migrations)"
echo ""
echo "=========================================="
echo "Alternative: If Railway CLI doesn't work,"
echo "use Railway Dashboard method (see RUN_MIGRATIONS_NOW.md)"
echo "=========================================="

