import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.apps import apps

print("All installed apps:")
for app_config in apps.get_app_configs():
    print(f"- {app_config.name} (label: {app_config.label})")

print("\nLooking for duplicates...")
app_labels = {}
for app_config in apps.get_app_configs():
    if app_config.label in app_labels:
        print(f"DUPLICATE FOUND: {app_config.label}")
        print(f"  First: {app_labels[app_config.label]}")
        print(f"  Second: {app_config}")
    app_labels[app_config.label] = app_config
