#!/usr/bin/env python
"""
Complete setup script for Mediwell Care Django project
This script will set up everything needed to run the project
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the project banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              🏥 MEDIWELL CARE SETUP 🏥                      ║
    ║                                                              ║
    ║         Digital Solutions for Doctors & Healthcare          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_command(command, description, required=True):
    """Run a command and handle the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        if required:
            print("❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
        return False

def check_requirements():
    """Check if required software is installed"""
    print("\n🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if pip is available
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True)
        print("✅ pip is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip is not available. Please install pip first.")
        sys.exit(1)

def setup_environment():
    """Set up the environment"""
    print("\n🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        env_content = """# Mediwell Care Environment Configuration
DEBUG=True
SECRET_KEY=django-insecure-mediwell-care-2024-change-in-production
DB_NAME=mediwell_care
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Social Media URLs (Optional)
FACEBOOK_URL=https://facebook.com/mediwellcare
TWITTER_URL=https://twitter.com/mediwellcare
LINKEDIN_URL=https://linkedin.com/company/mediwellcare
INSTAGRAM_URL=https://instagram.com/mediwellcare
WHATSAPP_NUMBER=919876543210
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default values")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    run_command("pip install -r requirements.txt", "Installing Python packages")

def setup_database():
    """Set up the database"""
    print("\n🗄️ Setting up database...")
    
    commands = [
        ("python manage.py makemigrations", "Creating database migrations"),
        ("python manage.py migrate", "Running database migrations"),
        ("python manage.py populate_data", "Populating database with dummy data"),
    ]
    
    for command, description in commands:
        run_command(command, description)

def create_superuser():
    """Create superuser if it doesn't exist"""
    print("\n👤 Setting up admin user...")
    
    # Check if superuser exists
    try:
        result = subprocess.run(
            "python manage.py shell -c \"from django.contrib.auth.models import User; print('admin' if User.objects.filter(username='admin').exists() else 'no')\"",
            shell=True, capture_output=True, text=True, check=True
        )
        if 'admin' in result.stdout:
            print("✅ Admin user already exists")
            return
    except:
        pass
    
    # Create superuser
    print("Creating superuser (admin/admin123)...")
    try:
        subprocess.run(
            "echo 'from django.contrib.auth.models import User; User.objects.create_superuser(\"admin\", \"admin@mediwellcare.com\", \"admin123\") if not User.objects.filter(username=\"admin\").exists() else None' | python manage.py shell",
            shell=True, check=True, capture_output=True
        )
        print("✅ Admin user created successfully")
    except:
        print("⚠️  Could not create admin user automatically. Please run: python manage.py createsuperuser")

def collect_static():
    """Collect static files"""
    print("\n📁 Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files", required=False)

def main():
    """Main setup function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Run setup steps
    check_requirements()
    setup_environment()
    install_dependencies()
    setup_database()
    create_superuser()
    collect_static()
    
    # Success message
    print("\n" + "="*60)
    print("🎉 MEDIWELL CARE SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Visit the website:")
    print("   http://127.0.0.1:8000")
    print("\n3. Access the admin panel:")
    print("   http://127.0.0.1:8000/admin")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n4. Customize your content:")
    print("   - Update site settings in admin panel")
    print("   - Add your contact information")
    print("   - Customize services and pricing")
    print("   - Add your team members")
    print("\n📞 For support:")
    print("   Email: info@mediwellcare.com")
    print("   Phone: +91 98765 43210")
    print("\n🚀 Ready to empower doctors digitally!")

if __name__ == "__main__":
    main()
