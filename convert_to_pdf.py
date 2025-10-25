#!/usr/bin/env python3
"""
Simple script to help convert the premium pamphlet to PDF
"""

import webbrowser
import os
from pathlib import Path

def open_in_browser():
    """Open the HTML file in the default browser for easy PDF conversion"""
    html_file = Path("Mediwell_Care_Premium_Pamphlet.html")
    
    if html_file.exists():
        print("🌐 Opening premium pamphlet in your browser...")
        webbrowser.open(f"file://{html_file.absolute()}")
        
        print("\n📄 To create PDF:")
        print("1. Press Ctrl+P (or Cmd+P on Mac)")
        print("2. Select 'Save as PDF'")
        print("3. Choose 'More settings'")
        print("4. Set margins to 'Minimum'")
        print("5. Click 'Save'")
        print("\n✨ Your premium pamphlet will be ready!")
        
        return True
    else:
        print("❌ HTML file not found!")
        return False

def main():
    print("🏥 Mediwell Care - Premium Pamphlet PDF Converter")
    print("=" * 50)
    
    if open_in_browser():
        print("\n🎉 Premium pamphlet opened successfully!")
        print("📋 Features of your premium pamphlet:")
        print("   • World-class design with premium typography")
        print("   • Professional color scheme and gradients")
        print("   • Easy-to-read layout with perfect spacing")
        print("   • Comprehensive service showcase")
        print("   • Real testimonials and success stories")
        print("   • Clear pricing and contact information")
        print("   • Special offers and CTAs")
        print("\n💡 This pamphlet will impress every doctor who sees it!")
    else:
        print("❌ Failed to open pamphlet")

if __name__ == "__main__":
    main()
