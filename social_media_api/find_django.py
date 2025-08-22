import os
import sys

print("🔍 Searching for Django project structure...")

# Look for manage.py in current directory and subdirectories
manage_py_found = False
project_root = None

for root, dirs, files in os.walk('.'):
    if 'manage.py' in files:
        manage_py_path = os.path.join(root, 'manage.py')
        project_root = os.path.abspath(root)
        print(f"✅ Found manage.py at: {manage_py_path}")
        print(f"📁 Project root: {project_root}")
        manage_py_found = True
        break

if not manage_py_found:
    print("❌ No manage.py found in current directory or subdirectories.")
    print("💡 Try navigating to your project directory first.")
    sys.exit(1)

# Check for apps in the project root
print("\n📦 Looking for Django apps:")
apps_found = []
if project_root:
    for item in os.listdir(project_root):
        item_path = os.path.join(project_root, item)
        if (os.path.isdir(item_path) and 
            os.path.exists(os.path.join(item_path, '_init_.py')) and 
            os.path.exists(os.path.join(item_path, 'apps.py'))):
            apps_found.append(item)
            print(f"   ✅ App found: {item}")

print(f"\n🎯 Total apps found: {len(apps_found)}")
if apps_found:
    for app in apps_found:
        print(f"   - {app}")

print(f"\n💡 Your project is at: {project_root}")
print("   Navigate to this directory to run Django commands.")
