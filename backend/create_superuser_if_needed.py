#!/usr/bin/env python3
"""
Auto-create superuser and generate auth token on startup if they don't exist.
This script runs during backend startup to ensure admin user is always available.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction, connection

User = get_user_model()

def create_superuser_if_needed():
    """Create superuser if it doesn't exist"""
    email = os.environ.get('ADMIN_EMAIL', 'mail@jsabu.com')
    password = os.environ.get('ADMIN_PASSWORD', 'Admin@1234')
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ Superuser already exists: {email}")
        return user
    except User.DoesNotExist:
        try:
            user = User.objects.create_superuser(
                email=email,
                password=password,
                is_staff=True,
                is_active=True,
            )
            print(f"✅ Created superuser: {email}")
            return user
        except Exception as e:
            print(f"⚠️  Failed to create superuser: {e}")
            return None

def ensure_permissions(user):
    """Ensure user has all necessary permissions"""
    if not user:
        return
    
    try:
        from django.contrib.auth.models import Permission
        all_permissions = Permission.objects.all()
        user.user_permissions.add(*all_permissions)
        print(f"✅ Added {all_permissions.count()} permissions to user")
    except Exception as e:
        print(f"⚠️  Could not add permissions: {e}")

def generate_token(user):
    """Generate authentication token"""
    if not user:
        return None
    
    try:
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"✅ Created new token for user")
        else:
            print(f"✅ Using existing token for user")
        return token.key
    except ImportError:
        try:
            from saleor.account.models import ServiceAccount
            service_account, created = ServiceAccount.objects.get_or_create(
                name=f"Admin Dashboard - {user.email}",
                user=user,
            )
            if created:
                print(f"✅ Created service account for user")
            else:
                print(f"✅ Using existing service account")
            return service_account.auth_token
        except Exception as e:
            print(f"⚠️  Could not generate token: {e}")
            return None

def main():
    """Main function to create superuser and token"""
    print("=" * 80)
    print("CHECKING/CREATING SUPERUSER AND AUTH TOKEN")
    print("=" * 80)
    
    # Check database connection first
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Skipping superuser creation - will retry on next startup")
        return
    
    with transaction.atomic():
        user = create_superuser_if_needed()
        if user:
            ensure_permissions(user)
            token = generate_token(user)
            
            if token:
                print("\n" + "=" * 80)
                print("AUTHENTICATION TOKEN")
                print("=" * 80)
                print(f"Token: {token}")
                print("\nAdd this to your frontend .env file:")
                print(f"NEXT_PUBLIC_AUTH_TOKEN={token}")
                print("\nOr use it in browser console:")
                print(f"localStorage.setItem('authToken', '{token}')")
                print("=" * 80)
            else:
                print("\n⚠️  Token generation failed. Using session-based authentication.")
        else:
            print("\n⚠️  Could not create superuser. Check database and permissions.")

if __name__ == '__main__':
    main()

