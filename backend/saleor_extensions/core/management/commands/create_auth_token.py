"""
Django management command to create admin user and generate auth token.
Usage: python manage.py create_auth_token
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin user and generate authentication token for GraphQL API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Admin user email (default: from ADMIN_EMAIL env var or admin@grandgold.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=None,
            help='Admin user password (default: from ADMIN_PASSWORD env var or admin123)',
        )

    def handle(self, *args, **options):
        email = options.get('email') or os.environ.get('ADMIN_EMAIL', 'admin@grandgold.com')
        password = options.get('password') or os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("CREATING ADMIN USER AND AUTH TOKEN"))
        self.stdout.write("=" * 80)
        
        with transaction.atomic():
            # Create or get admin user
            try:
                user = User.objects.get(email=email)
                self.stdout.write(self.style.SUCCESS(f"✅ User already exists: {email}"))
            except User.DoesNotExist:
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    is_staff=True,
                    is_active=True,
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Created admin user: {email}"))
            
            # Ensure user has all necessary permissions
            try:
                from django.contrib.auth.models import Permission
                from django.contrib.contenttypes.models import ContentType
                
                # Get all permissions
                all_permissions = Permission.objects.all()
                user.user_permissions.add(*all_permissions)
                self.stdout.write(self.style.SUCCESS(f"✅ Added {all_permissions.count()} permissions to user"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️  Could not add permissions: {e}"))
            
            # Generate token
            token = self.generate_token(user)
            
            if token:
                self.stdout.write("\n" + "=" * 80)
                self.stdout.write(self.style.SUCCESS("AUTHENTICATION TOKEN"))
                self.stdout.write("=" * 80)
                self.stdout.write(f"Token: {self.style.SUCCESS(token)}")
                self.stdout.write("\nAdd this to your frontend .env file:")
                self.stdout.write(self.style.SUCCESS(f"NEXT_PUBLIC_AUTH_TOKEN={token}"))
                self.stdout.write("\nOr use it in Apollo Client:")
                self.stdout.write(self.style.SUCCESS(f"localStorage.setItem('authToken', '{token}')"))
                self.stdout.write("=" * 80)
            else:
                self.stdout.write(self.style.WARNING("\n⚠️  Token generation failed. Using session-based authentication."))
                self.stdout.write("   Make sure to log in via Django admin first.")

    def generate_token(self, user):
        """Generate authentication token for GraphQL API"""
        import os
        try:
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created new token for user"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ Using existing token for user"))
            return token.key
        except ImportError:
            # If DRF is not installed, try Saleor's token system
            try:
                from saleor.account.models import ServiceAccount
                # Create service account for API access
                service_account, created = ServiceAccount.objects.get_or_create(
                    name=f"Admin Dashboard - {user.email}",
                    user=user,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Created service account for user"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"✅ Using existing service account"))
                return service_account.auth_token
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️  Could not generate token: {e}"))
                return None

