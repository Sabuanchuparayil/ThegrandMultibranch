#!/usr/bin/env python3
"""
Generate secret keys and environment variables for Django/Saleor deployment.

This script generates:
- SECRET_KEY (Django)
- RSA_PRIVATE_KEY and RSA_PUBLIC_KEY (Saleor JWT)
- Other recommended environment variables

Usage:
    python generate_secrets.py
"""

import secrets
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Generate Django SECRET_KEY"""
    try:
        # Try using Django's utility
        return get_random_secret_key()
    except ImportError:
        # Fallback if Django not installed
        return secrets.token_urlsafe(50)

def generate_rsa_keys():
    """Generate RSA key pair for Saleor JWT"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')

def main():
    print("=" * 80)
    print("SECRET KEYS GENERATOR FOR GRAND GOLD & DIAMONDS")
    print("=" * 80)
    print()
    
    # Generate SECRET_KEY
    print("1. DJANGO SECRET_KEY:")
    print("-" * 80)
    secret_key = generate_secret_key()
    print(secret_key)
    print()
    
    # Generate RSA keys
    print("2. SALEOR RSA KEYS (for JWT authentication):")
    print("-" * 80)
    private_key, public_key = generate_rsa_keys()
    print("RSA_PRIVATE_KEY:")
    print(private_key)
    print()
    print("RSA_PUBLIC_KEY (optional, for reference):")
    print(public_key)
    print()
    
    # Generate other recommended secrets
    print("3. OTHER RECOMMENDED SECRETS:")
    print("-" * 80)
    print("ALLOWED_HOSTS (comma-separated, add your Railway domain):")
    print("  ALLOWED_HOSTS=your-app.railway.app,localhost,127.0.0.1")
    print()
    print("DATABASE_URL (Railway provides this automatically):")
    print("  DATABASE_URL=postgresql://user:password@host:port/dbname")
    print()
    print("REDIS_URL (if using Redis, Railway provides this):")
    print("  REDIS_URL=redis://host:port")
    print()
    
    # Generate .env file template
    print("4. ENVIRONMENT VARIABLES FILE (.env):")
    print("-" * 80)
    print("Copy these to your Railway environment variables or .env file:")
    print()
    print(f"SECRET_KEY={secret_key}")
    print()
    print("RSA_PRIVATE_KEY=" + private_key.replace('\n', '\\n'))
    print()
    print("# Optional but recommended:")
    print("ALLOWED_HOSTS=your-app.railway.app,localhost,127.0.0.1")
    print("DEBUG=False")
    print("DATABASE_URL=postgresql://user:password@host:port/dbname")
    print("REDIS_URL=redis://host:port")
    print()
    
    print("=" * 80)
    print("IMPORTANT: Keep these keys secure and never commit them to git!")
    print("=" * 80)

if __name__ == '__main__':
    main()

