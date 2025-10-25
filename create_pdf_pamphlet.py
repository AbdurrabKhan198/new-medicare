#!/usr/bin/env python3
"""
Script to convert the HTML marketing pamphlet to PDF format
Requires: pip install weasyprint
"""

import os
import sys
from pathlib import Path

def create_pdf():
    """Convert HTML pamphlet to PDF"""
    try:
        import weasyprint
        
        # Read the HTML file
        html_file = Path("Mediwell_Care_Marketing_Pamphlet.html")
        if not html_file.exists():
            print("❌ HTML file not found!")
            return False
            
        # Create PDF
        pdf_file = Path("Mediwell_Care_Marketing_Pamphlet.pdf")
        
        print("🔄 Converting HTML to PDF...")
        
        # Convert HTML to PDF with proper page sizing
        html_doc = weasyprint.HTML(filename=str(html_file))
        css = weasyprint.CSS(string='''
            @page {
                size: A4;
                margin: 0;
            }
            .page {
                min-height: 297mm;
                padding: 20mm;
                page-break-after: always;
            }
            .page:last-child {
                page-break-after: avoid;
            }
        ''')
        
        html_doc.write_pdf(str(pdf_file), stylesheets=[css])
        
        print(f"✅ PDF created successfully: {pdf_file}")
        print(f"📄 File size: {pdf_file.stat().st_size / 1024:.1f} KB")
        
        return True
        
    except ImportError:
        print("❌ WeasyPrint not installed!")
        print("📦 Install it with: pip install weasyprint")
        return False
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

def install_requirements():
    """Install required packages"""
    try:
        import subprocess
        import sys
        
        print("📦 Installing WeasyPrint...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint"])
        print("✅ WeasyPrint installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error installing WeasyPrint: {e}")
        return False

def main():
    """Main function"""
    print("🏥 Mediwell Care - Marketing Pamphlet PDF Generator")
    print("=" * 50)
    
    # Check if weasyprint is installed
    try:
        import weasyprint
        print("✅ WeasyPrint is already installed")
    except ImportError:
        print("📦 WeasyPrint not found. Installing...")
        if not install_requirements():
            print("❌ Failed to install WeasyPrint. Please install manually:")
            print("   pip install weasyprint")
            return False
    
    # Create PDF
    if create_pdf():
        print("\n🎉 Marketing pamphlet PDF created successfully!")
        print("📁 File: Mediwell_Care_Marketing_Pamphlet.pdf")
        print("\n📋 The pamphlet includes:")
        print("   • Company overview and value proposition")
        print("   • Comprehensive service offerings")
        print("   • Success stories and testimonials")
        print("   • Pricing packages")
        print("   • Contact information and CTAs")
        print("\n💡 You can now use this PDF for:")
        print("   • Email marketing campaigns")
        print("   • Social media sharing")
        print("   • Client presentations")
        print("   • Print distribution")
        return True
    else:
        print("❌ Failed to create PDF")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
