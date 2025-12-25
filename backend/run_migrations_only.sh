#!/bin/bash
# Migration-only script for Railway
# This script ONLY runs migrations and exits - no web server

set -e  # Exit on error

echo "=================================================================================="
echo "RUNNING DATABASE MIGRATIONS (Migration Service)"
echo "=================================================================================="
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run migrations
echo "Running migration script..."
python run_migrations.py

# Exit with the migration script's exit code
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=================================================================================="
    echo "✅ Migrations completed successfully!"
    echo "=================================================================================="
    echo ""
    echo "This service can now be stopped/deleted."
    echo "The database tables have been created."
    echo ""
    # Keep container alive for a bit so logs can be viewed, then exit
    echo "Waiting 60 seconds for log review, then exiting..."
    sleep 60
else
    echo ""
    echo "=================================================================================="
    echo "❌ Migrations failed with exit code: $exit_code"
    echo "=================================================================================="
    echo ""
    echo "Check the logs above for error details."
    echo "Keeping container alive for 300 seconds for debugging..."
    sleep 300
fi

exit $exit_code

