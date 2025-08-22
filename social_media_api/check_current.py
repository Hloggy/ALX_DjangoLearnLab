import os

print("📋 Contents of current directory:")
print(f"Current directory: {os.getcwd()}")
print("\nItems:")

items = os.listdir('.')
for item in items:
    if os.path.isdir(item):
        print(f"📁 {item}/")
    else:
        print(f"📄 {item}")

print(f"\nTotal items: {len(items)}")
