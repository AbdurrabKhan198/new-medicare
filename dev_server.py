#!/usr/bin/env python3
"""
Development server script for Mediwell Care
"""
import subprocess
import sys
import os
import time
import threading

def run_command(command, description, background=False):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if background:
            process = subprocess.Popen(command, shell=True)
            return process
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} completed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main development process"""
    print("🚀 Starting Mediwell Care development server...")
    
    # Build assets first
    print("📦 Building assets...")
    if not run_command("npm run build-css-prod", "Building Tailwind CSS"):
        print("❌ Failed to build CSS")
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files")
        sys.exit(1)
    
    print("🎉 Assets built successfully!")
    print("🌐 Starting Django development server...")
    print("📍 Server will be available at: http://127.0.0.1:8008")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Start Django server
    try:
        subprocess.run("python manage.py runserver 8008", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
