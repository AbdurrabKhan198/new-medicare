#!/usr/bin/env python
"""
Environment setup script for Mediwell Care
Creates .env file with default values
"""

import os

def create_env_file():
    """Create .env file with default values"""
    env_content = """# Mediwell Care Environment Configuration
DEBUG=True
SECRET_KEY=django-insecure-mediwell-care-2024-change-in-production
DB_NAME=mediwell_care
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Optional - for contact forms)
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

# Analytics (Optional)
GOOGLE_ANALYTICS_ID=
GOOGLE_TAG_MANAGER_ID=
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default values")
        print("📝 Please update the database credentials and email settings as needed")
    else:
        print("⚠️  .env file already exists. Skipping creation.")
        print("📝 If you need to reset, delete .env and run this script again")

def main():
    print("🔧 Setting up environment configuration...")
    create_env_file()
    print("\n📋 Environment setup completed!")
    print("\nNext steps:")
    print("1. Update database credentials in .env file")
    print("2. Configure email settings if needed")
    print("3. Run: python run_setup.py")

if __name__ == "__main__":
    main()
