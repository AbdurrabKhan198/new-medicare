#!/usr/bin/env python3
"""
Open the Tailwind CSS pamphlet in browser for easy PDF conversion
"""

import webbrowser
import os
from pathlib import Path

def main():
    print("🏥 Mediwell Care - Tailwind CSS Pamphlet")
    print("=" * 50)
    
    html_file = Path("Mediwell_Care_Tailwind_Pamphlet.html")
    
    if html_file.exists():
        print("🌐 Opening Tailwind CSS pamphlet in your browser...")
        webbrowser.open(f"file://{html_file.absolute()}")
        
        print("\n📄 To create PDF:")
        print("1. Press Ctrl+P (or Cmd+P on Mac)")
        print("2. Select 'Save as PDF'")
        print("3. Choose 'More settings'")
        print("4. Set margins to 'Minimum'")
        print("5. Click 'Save'")
        
        print("\n✨ Features of your Tailwind CSS pamphlet:")
        print("   • 🎨 Beautiful Tailwind CSS design")
        print("   • 📱 Fully responsive (mobile-friendly)")
        print("   • 📄 Perfect 3-page layout")
        print("   • 🚀 Modern gradients and animations")
        print("   • 💎 Premium typography (Inter + Playfair Display)")
        print("   • 🎯 Convincing and attractive design")
        print("   • 📊 Clear pricing and testimonials")
        print("   • 📞 Multiple contact methods")
        
        print("\n💡 This pamphlet will convert prospects into clients!")
        return True
    else:
        print("❌ HTML file not found!")
        return False

if __name__ == "__main__":
    main()
