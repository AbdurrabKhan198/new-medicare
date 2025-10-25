import re
import requests
import json
from django.conf import settings
from django.utils import timezone

def parse_user_agent(user_agent):
    """Parse user agent string to extract device, browser, and OS info"""
    device_type = 'desktop'
    browser = 'Unknown'
    os = 'Unknown'
    
    user_agent_lower = user_agent.lower()
    
    # Detect device type
    if any(mobile in user_agent_lower for mobile in ['mobile', 'android', 'iphone']):
        device_type = 'mobile'
    elif any(tablet in user_agent_lower for tablet in ['tablet', 'ipad']):
        device_type = 'tablet'
    
    # Detect browser
    if 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
        browser = 'Chrome'
    elif 'firefox' in user_agent_lower:
        browser = 'Firefox'
    elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
        browser = 'Safari'
    elif 'edg' in user_agent_lower:
        browser = 'Edge'
    elif 'opera' in user_agent_lower:
        browser = 'Opera'
    
    # Detect operating system
    if 'windows' in user_agent_lower:
        os = 'Windows'
    elif 'mac' in user_agent_lower:
        os = 'macOS'
    elif 'linux' in user_agent_lower:
        os = 'Linux'
    elif 'android' in user_agent_lower:
        os = 'Android'
    elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
        os = 'iOS'
    
    return {
        'device_type': device_type,
        'browser': browser,
        'os': os
    }

def get_geolocation(ip_address):
    """Get geolocation information for IP address"""
    try:
        # Skip private IPs
        if ip_address.startswith(('127.', '192.168.', '10.', '172.')):
            return {'country': 'Local', 'city': 'Local'}
        
        # Use a free geolocation service
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown')
            }
    except:
        pass
    
    return {'country': 'Unknown', 'city': 'Unknown'}

def get_visitor_info(request):
    """Extract visitor information from request"""
    return {
        'ip_address': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'referrer': request.META.get('HTTP_REFERER', ''),
        'accept_language': request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
    }

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_mobile_device(user_agent):
    """Check if the device is mobile"""
    mobile_patterns = [
        'mobile', 'android', 'iphone', 'ipod', 'blackberry',
        'windows phone', 'opera mini', 'iemobile'
    ]
    user_agent_lower = user_agent.lower()
    return any(pattern in user_agent_lower for pattern in mobile_patterns)

def get_screen_resolution(request):
    """Extract screen resolution from request (if available)"""
    # This would typically come from JavaScript tracking
    return request.session.get('screen_resolution', 'Unknown')

def track_event(visitor, event_type, event_name, event_value=None, page_url=None, metadata=None):
    """Track a custom event"""
    from .models import Event
    
    try:
        Event.objects.create(
            visitor=visitor,
            event_type=event_type,
            event_name=event_name,
            event_value=event_value,
            page_url=page_url or '',
            metadata=metadata or {}
        )
    except Exception as e:
        print(f"Error tracking event: {e}")

def calculate_bounce_rate(visitor):
    """Calculate bounce rate for a visitor"""
    page_views = visitor.page_views.count()
    if page_views <= 1:
        return 100.0
    return 0.0

def get_traffic_source_breakdown(start_date, end_date):
    """Get traffic source breakdown for a date range"""
    from .models import TrafficSource
    from django.db import models
    
    sources = TrafficSource.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).values('source_type').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    return sources

def generate_analytics_report(start_date, end_date):
    """Generate comprehensive analytics report"""
    from .models import Visitor, PageView, DailyStats
    from django.db.models import Avg
    
    # Get basic metrics
    total_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).count()
    
    total_page_views = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).count()
    
    # Get unique visitors
    unique_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).distinct().count()
    
    # Calculate average session duration
    avg_duration = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date],
        time_spent__isnull=False
    ).aggregate(avg_duration=Avg('time_spent'))['avg_duration']
    
    return {
        'total_visitors': total_visitors,
        'unique_visitors': unique_visitors,
        'total_page_views': total_page_views,
        'avg_session_duration': avg_duration,
        'bounce_rate': calculate_bounce_rate_period(start_date, end_date),
    }

def calculate_bounce_rate_period(start_date, end_date):
    """Calculate bounce rate for a specific period"""
    from .models import Visitor, PageView
    
    visitors_with_single_page = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date],
        total_page_views=1
    ).count()
    
    total_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).count()
    
    if total_visitors == 0:
        return 0.0
    
    return (visitors_with_single_page / total_visitors) * 100
