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
import subprocess
import sys

def generate_secret_key():
    """Generate Django SECRET_KEY"""
    try:
        # Try using Django's utility
        from django.core.management.utils import get_random_secret_key
        return get_random_secret_key()
    except ImportError:
        # Fallback if Django not installed
        return secrets.token_urlsafe(50)

def generate_rsa_keys():
    """Generate RSA key pair for Saleor JWT using OpenSSL"""
    try:
        # Try using OpenSSL (usually available on most systems)
        result = subprocess.run(
            ['openssl', 'genrsa', '2048'],
            capture_output=True,
            text=True,
            check=True
        )
        private_key = result.stdout
        
        # Extract public key from private key
        pub_result = subprocess.run(
            ['openssl', 'rsa', '-pubout'],
            input=private_key,
            capture_output=True,
            text=True,
            check=True
        )
        public_key = pub_result.stdout
        
        return private_key, public_key
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: provide instructions
        return None, None

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
    if private_key:
        print("RSA_PRIVATE_KEY:")
        print(private_key)
        print()
        print("RSA_PUBLIC_KEY (optional, for reference):")
        print(public_key)
        print()
    else:
        print("⚠️  OpenSSL not found. Generate RSA keys manually:")
        print()
        print("   Option 1: Using OpenSSL (if installed):")
        print("   openssl genrsa -out private_key.pem 2048")
        print("   cat private_key.pem")
        print()
        print("   Option 2: Using Python cryptography library:")
        print("   pip install cryptography")
        print("   python -c \"from cryptography.hazmat.primitives.asymmetric import rsa;")
        print("   from cryptography.hazmat.primitives import serialization;")
        print("   key = rsa.generate_private_key(public_exponent=65537, key_size=2048);")
        print("   print(key.private_bytes(encoding=serialization.Encoding.PEM,")
        print("   format=serialization.PrivateFormat.PKCS8,")
        print("   encryption_algorithm=serialization.NoEncryption()).decode())\"")
        print()
        private_key = "MANUAL_GENERATION_REQUIRED"
        public_key = None
    
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
    if private_key and private_key != "MANUAL_GENERATION_REQUIRED":
        print("RSA_PRIVATE_KEY=" + private_key.replace('\n', '\\n'))
    else:
        print("RSA_PRIVATE_KEY=<generate-using-openssl-or-cryptography>")
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

