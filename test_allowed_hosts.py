#!/usr/bin/env python
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test with different ALLOWED_HOSTS values
test_cases = [
    ('.onrender.com', "Render deployment"),
    ('localhost,127.0.0.1', "Local development"),
    ('*', "Wildcard (should work but not recommended for production)"),
]

print("Testing ALLOWED_HOSTS configuration...\n")

for hosts_value, description in test_cases:
    print(f"Testing: {description}")
    print(f"Setting ALLOWED_HOSTS='{hosts_value}'")
    
    # Set the environment variable
    os.environ['ALLOWED_HOSTS'] = hosts_value
    
    try:
        # Import settings after setting environment variable
        from shoppingproject.settings import ALLOWED_HOSTS, DEBUG
        
        print(f"  ALLOWED_HOSTS: {ALLOWED_HOSTS}")
        print(f"  DEBUG: {DEBUG}")
        print(f"  ✅ Configuration loaded successfully")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("-" * 50)

print("\nTest completed. The ALLOWED_HOSTS configuration should now work correctly for Render deployment.")
