#!/usr/bin/env python3
"""
Build script for Mediwell Care assets
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("🚀 Building Mediwell Care assets...")
    
    # Check if Node.js is installed
    if not run_command("node --version", "Checking Node.js"):
        print("❌ Node.js is not installed. Please install Node.js first.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("npm install", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Build CSS
    if not run_command("npm run build-css-prod", "Building Tailwind CSS"):
        print("❌ Failed to build CSS")
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files")
        sys.exit(1)
    
    print("🎉 All assets built successfully!")
    print("📁 CSS output: static/css/output.css")
    print("📁 Static files: staticfiles/")

if __name__ == "__main__":
    main()
