"""
Model Integration Helper Script

This script helps identify which models need ForeignKey updates.

Run this before updating models to see what needs to be changed.
"""

import os
import re
from pathlib import Path

def find_models_needing_integration():
    """Find models with placeholder ID fields"""
    
    extensions_path = Path(__file__).parent / 'saleor_extensions'
    patterns = [
        r'order_id\s*=\s*models\.CharField',
        r'product_id\s*=\s*models\.CharField',
        r'customer_id\s*=\s*models\.CharField',
        r'user_id\s*=\s*models\.CharField',
    ]
    
    results = {}
    
    for app_dir in extensions_path.iterdir():
        if not app_dir.is_dir() or app_dir.name.startswith('_'):
            continue
            
        models_file = app_dir / 'models.py'
        if not models_file.exists():
            continue
        
        with open(models_file, 'r') as f:
            content = f.read()
        
        matches = []
        for pattern in patterns:
            if re.search(pattern, content):
                field_name = pattern.split('(')[0].split('=')[0].strip()
                matches.append(field_name)
        
        if matches:
            results[app_dir.name] = matches
    
    return results


def print_integration_report():
    """Print a report of models needing integration"""
    
    print("=" * 70)
    print("MODEL INTEGRATION REPORT")
    print("=" * 70)
    print()
    
    results = find_models_needing_integration()
    
    if not results:
        print("✅ No models found with placeholder ID fields!")
        print("All models may already be integrated, or no ID fields exist.")
        return
    
    print(f"Found {len(results)} apps with models needing integration:\n")
    
    for app_name, fields in results.items():
        print(f"📁 {app_name}/models.py")
        for field in fields:
            print(f"   - {field} needs ForeignKey update")
        print()
    
    print("=" * 70)
    print("INTEGRATION STEPS:")
    print("=" * 70)
    print()
    print("1. Review MODEL_UPDATES.md for exact changes needed")
    print("2. Update each model file to use ForeignKeys")
    print("3. Run: python manage.py makemigrations")
    print("4. Run: python manage.py migrate")
    print("5. Test in Django admin")
    print()
    print("=" * 70)


if __name__ == '__main__':
    print_integration_report()


