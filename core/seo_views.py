from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import xml.etree.ElementTree as ET


def sitemap_xml(request):
    """Generate dynamic XML sitemap"""
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    # Get current domain
    current_site = Site.objects.get_current()
    base_url = f"https://{current_site.domain}"
    
    # Static pages
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'url': '/services/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/services/website-design/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/services/healthcare-seo/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/services/doctor-crm/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/services/social-media-marketing/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/doctors/', 'priority': '0.7', 'changefreq': 'daily'},
        {'url': '/blog/', 'priority': '0.6', 'changefreq': 'daily'},
        {'url': '/about/', 'priority': '0.5', 'changefreq': 'monthly'},
        {'url': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/privacy-policy/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/terms-of-service/', 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    
    for page in static_pages:
        url_elem = ET.SubElement(root, "url")
        ET.SubElement(url_elem, "loc").text = f"{base_url}{page['url']}"
        ET.SubElement(url_elem, "lastmod").text = timezone.now().strftime("%Y-%m-%d")
        ET.SubElement(url_elem, "changefreq").text = page['changefreq']
        ET.SubElement(url_elem, "priority").text = page['priority']
    
    # Add dynamic content (blog posts, doctors, etc.)
    # This would be populated from your models
    
    # Convert to string
    xml_str = ET.tostring(root, encoding='unicode')
    
    response = HttpResponse(xml_str, content_type='application/xml')
    response['Content-Type'] = 'application/xml; charset=utf-8'
    return response


def robots_txt(request):
    """Generate dynamic robots.txt"""
    content = """User-agent: *
Allow: /

# Important pages for SEO
Allow: /services/
Allow: /doctors/
Allow: /blog/
Allow: /contact/
Allow: /about/

# Disallow admin and private areas
Disallow: /admin/
Disallow: /pharmacy/
Disallow: /crm/
Disallow: /accounts/

# Sitemap location
Sitemap: https://mediwellcare.com/sitemap.xml

# Crawl delay (optional)
Crawl-delay: 1
"""
    return HttpResponse(content, content_type='text/plain')


def seo_analytics(request):
    """SEO analytics dashboard"""
    # This would show SEO metrics, keyword rankings, etc.
    context = {
        'title': 'SEO Analytics Dashboard',
        'keywords_tracked': 50,
        'pages_indexed': 25,
        'backlinks': 150,
        'domain_authority': 45,
    }
    return render(request, 'core/seo_analytics.html', context)
