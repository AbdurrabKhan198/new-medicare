#!/usr/bin/env python
"""
Setup script for Mediwell Care Django project
Run this script to set up the project with dummy data
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Mediwell Care Django Project")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediwell_care.settings')
    django.setup()
    
    # Commands to run
    commands = [
        ("python manage.py makemigrations", "Creating database migrations"),
        ("python manage.py migrate", "Running database migrations"),
        ("python manage.py populate_data", "Populating database with dummy data"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    # Run all commands
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
            break
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Create a superuser: python manage.py createsuperuser")
        print("2. Run the development server: python manage.py runserver")
        print("3. Visit http://127.0.0.1:8000 to view the website")
        print("4. Visit http://127.0.0.1:8000/admin to access the admin panel")
        print("\n🔑 Default superuser credentials (if created):")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n📞 For support, contact: info@mediwellcare.com")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
