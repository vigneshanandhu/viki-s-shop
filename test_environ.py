#!/usr/bin/env python
"""
Simple test script to verify django-environ is working correctly
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppingproject.settings')
django.setup()

# Test the environ configuration
from shoppingproject.settings import env

print("Testing django-environ configuration...")
print(f"DEBUG: {env.bool('DEBUG', default=False)}")
print(f"SECRET_KEY: {env('SECRET_KEY', default='not-set')}")
print(f"RAZORPAY_KEY_ID: {env('RAZORPAY_KEY_ID', default='not-set')}")

print("\nEnvironment test completed successfully!")
