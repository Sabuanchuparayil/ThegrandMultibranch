"""
Django management command to reset and reseed data.

Usage:
    python manage.py reset_and_reseed
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

# Import scripts
import sys
import os

# Add backend directory to path to import scripts
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from clear_mock_data import clear_all_mock_data
from create_initial_data import run as seed_initial_data


class Command(BaseCommand):
    help = 'Clear all mock data, ensure migrations are complete, and reseed initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-clear',
            action='store_true',
            help='Skip clearing mock data',
        )
        parser.add_argument(
            '--skip-migrate',
            action='store_true',
            help='Skip running migrations',
        )
        parser.add_argument(
            '--skip-seed',
            action='store_true',
            help='Skip seeding initial data',
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("COMPLETE RESET AND RESEED"))
        self.stdout.write("=" * 80)
        
        # Step 1: Clear all mock data
        if not options['skip_clear']:
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("STEP 1: CLEARING MOCK DATA")
            self.stdout.write("=" * 80)
            try:
                clear_all_mock_data()
                self.stdout.write(self.style.SUCCESS("\n✅ Mock data cleared successfully"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n❌ Error clearing mock data: {e}"))
                if not options.get('continue_on_error', False):
                    return
        
        # Step 2: Ensure migrations are complete
        if not options['skip_migrate']:
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("STEP 2: ENSURING MIGRATIONS ARE COMPLETE")
            self.stdout.write("=" * 80)
            try:
                self.stdout.write("\n📦 Running migrations...")
                call_command('migrate', verbosity=1, interactive=False)
                self.stdout.write(self.style.SUCCESS("✅ Migrations complete"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"\n⚠️  Migration error: {e}"))
                self.stdout.write("   Attempting to continue anyway...")
                response = input("\nContinue with seeding? (y/n): ")
                if response.lower() != 'y':
                    self.stdout.write("Aborted.")
                    return
        
        # Step 3: Reseed initial data
        if not options['skip_seed']:
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("STEP 3: RESEEDING INITIAL DATA")
            self.stdout.write("=" * 80)
            try:
                seed_initial_data()
                self.stdout.write(self.style.SUCCESS("\n✅ Initial data seeded successfully"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n❌ Error seeding data: {e}"))
                import traceback
                traceback.print_exc()
                return
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✅ RESET AND RESEED COMPLETE"))
        self.stdout.write("=" * 80)

