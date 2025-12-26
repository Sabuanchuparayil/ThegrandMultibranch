"""
Script to fix mutation return statements to work with both Saleor BaseMutation and fallback
"""
import re

# Read the schema file
with open('saleor_extensions/inventory/schema.py', 'r') as f:
    content = f.read()

# Pattern to find return cls(...) statements in mutations
pattern = r'return cls\(\s*([^)]+)\s*\)'

# Find all matches
matches = re.finditer(pattern, content)

# We'll need to manually check each one, but for now let's create a helper
# Actually, let's just create a proper fix that handles both cases

print("Found mutation return statements. Creating helper function...")


