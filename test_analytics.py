#!/usr/bin/env python3
"""
Test script to open the beautiful analytics dashboard
"""

import webbrowser
import os
from pathlib import Path

def main():
    print("📊 Mediwell Care - Beautiful Analytics Dashboard")
    print("=" * 50)
    
    # Check if Django server is running
    print("🌐 Opening analytics dashboard...")
    webbrowser.open("http://127.0.0.1:8000/analytics/")
    
    print("\n✨ Features of your new analytics dashboard:")
    print("   • 🎨 Beautiful gradient design")
    print("   • 📱 Fully responsive layout")
    print("   • 📊 Modern metric cards")
    print("   • 🟢 Real-time indicators")
    print("   • 📈 Interactive charts (coming soon)")
    print("   • 🌍 Geographic analytics")
    print("   • 📱 Device breakdown")
    print("   • ⚡ Live activity monitoring")
    
    print("\n💡 If the server isn't running, start it with:")
    print("   python manage.py runserver")
    
    print("\n🔧 To access the dashboard:")
    print("   1. Make sure you're logged in as admin")
    print("   2. Go to http://127.0.0.1:8000/analytics/")
    print("   3. Enjoy the beautiful new design!")

if __name__ == "__main__":
    main()
