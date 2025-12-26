#!/usr/bin/env python3
"""
Create a superuser and generate an authentication token for GraphQL API.
This script creates a user with all necessary permissions for admin dashboard access.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def create_admin_user():
    """Create or get admin user with all permissions"""
    email = os.environ.get('ADMIN_EMAIL', 'admin@grandgold.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ User already exists: {email}")
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            email=email,
            password=password,
            is_staff=True,
            is_active=True,
        )
        print(f"✅ Created admin user: {email}")
    
    # Ensure user has all necessary permissions
    # Saleor uses Django's permission system
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    
    # Get all permissions for account.User model (Saleor's user model)
    try:
        user_content_type = ContentType.objects.get(app_label='account', model='user')
        all_permissions = Permission.objects.filter(content_type=user_content_type)
        user.user_permissions.add(*all_permissions)
        print(f"✅ Added {all_permissions.count()} permissions to user")
    except Exception as e:
        print(f"⚠️  Could not add permissions: {e}")
    
    return user

def generate_token(user):
    """Generate authentication token for GraphQL API"""
    try:
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"✅ Created new token for user")
        else:
            print(f"✅ Using existing token for user")
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
                print(f"✅ Created service account for user")
            else:
                print(f"✅ Using existing service account")
            return service_account.auth_token
        except Exception as e:
            print(f"⚠️  Could not generate token: {e}")
            print("   You may need to authenticate using Django session cookies")
            return None

if __name__ == '__main__':
    print("=" * 80)
    print("CREATING ADMIN USER AND AUTH TOKEN")
    print("=" * 80)
    
    with transaction.atomic():
        user = create_admin_user()
        token = generate_token(user)
        
        if token:
            print("\n" + "=" * 80)
            print("AUTHENTICATION TOKEN")
            print("=" * 80)
            print(f"Token: {token}")
            print("\nAdd this to your frontend .env file:")
            print(f"NEXT_PUBLIC_AUTH_TOKEN={token}")
            print("\nOr use it in Apollo Client:")
            print(f"localStorage.setItem('authToken', '{token}')")
            print("=" * 80)
        else:
            print("\n⚠️  Token generation failed. Using session-based authentication.")
            print("   Make sure to log in via Django admin first.")

