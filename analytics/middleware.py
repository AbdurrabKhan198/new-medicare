from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db import transaction
from django.conf import settings
import uuid
import json
import re
from urllib.parse import urlparse, parse_qs
from .models import Visitor, PageView, TrafficSource, SessionData, Event
from .utils import get_visitor_info, parse_user_agent, get_geolocation

class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to automatically track page views and visitor behavior"""
    
    def process_request(self, request):
        # Skip tracking for certain paths
        skip_paths = ['/admin/', '/static/', '/media/', '/favicon.ico', '/robots.txt']
        if any(request.path.startswith(path) for path in skip_paths):
            return None
        
        # Get or create visitor
        visitor = self.get_or_create_visitor(request)
        if not visitor:
            return None
        
        # Track session
        self.track_session(request, visitor)
        
        # Track traffic source
        self.track_traffic_source(request, visitor)
        
        # Store visitor in request for later use
        request.analytics_visitor = visitor
        
        return None
    
    def process_response(self, request, response):
        # Track page view
        if hasattr(request, 'analytics_visitor'):
            self.track_page_view(request, response)
        
        return response
    
    def get_or_create_visitor(self, request):
        """Get or create visitor based on session or IP"""
        try:
            # Try to get visitor by session
            if request.session.session_key:
                visitor = Visitor.objects.filter(session_key=request.session.session_key).first()
                if visitor:
                    visitor.last_visit = timezone.now()
                    visitor.total_visits += 1
                    visitor.save()
                    return visitor
            
            # Get visitor info
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Parse user agent
            device_info = parse_user_agent(user_agent)
            
            # Check if it's a bot
            is_bot = self.is_bot(user_agent)
            
            # Get geolocation
            geo_info = get_geolocation(ip_address)
            
            # Create new visitor
            visitor = Visitor.objects.create(
                session_key=request.session.session_key,
                ip_address=ip_address,
                user_agent=user_agent,
                is_bot=is_bot,
                country=geo_info.get('country'),
                city=geo_info.get('city'),
                device_type=device_info.get('device_type'),
                browser=device_info.get('browser'),
                operating_system=device_info.get('os')
            )
            
            return visitor
            
        except Exception as e:
            print(f"Error creating visitor: {e}")
            return None
    
    def track_session(self, request, visitor):
        """Track session data"""
        if not request.session.session_key:
            return
        
        session_data, created = SessionData.objects.get_or_create(
            session_key=request.session.session_key,
            defaults={
                'visitor': visitor,
                'start_time': timezone.now(),
                'utm_source': request.GET.get('utm_source'),
                'utm_medium': request.GET.get('utm_medium'),
                'utm_campaign': request.GET.get('utm_campaign'),
                'utm_term': request.GET.get('utm_term'),
                'utm_content': request.GET.get('utm_content'),
            }
        )
        
        if not created:
            session_data.is_active = True
            session_data.save()
    
    def track_traffic_source(self, request, visitor):
        """Track where the visitor came from"""
        referrer = request.META.get('HTTP_REFERER', '')
        utm_source = request.GET.get('utm_source')
        
        # Determine traffic source
        source_info = self.determine_traffic_source(referrer, utm_source, request)
        
        # Check if we already have this traffic source for this visitor
        existing_source = TrafficSource.objects.filter(
            visitor=visitor,
            source_type=source_info['type']
        ).first()
        
        if not existing_source:
            TrafficSource.objects.create(
                visitor=visitor,
                source_type=source_info['type'],
                source_name=source_info['name'],
                source_url=source_info['url'],
                campaign_name=source_info.get('campaign'),
                medium=source_info.get('medium')
            )
    
    def track_page_view(self, request, response):
        """Track page view"""
        try:
            visitor = request.analytics_visitor
            referrer = request.META.get('HTTP_REFERER', '')
            
            # Get page title from response content
            page_title = self.extract_page_title(response.content)
            
            # Create page view
            page_view = PageView.objects.create(
                visitor=visitor,
                url=request.build_absolute_uri(),
                path=request.path,
                page_title=page_title,
                referrer=referrer if referrer else None
            )
            
            # Update visitor stats
            visitor.total_page_views += 1
            visitor.save()
            
            # Update session stats
            if request.session.session_key:
                session_data = SessionData.objects.filter(
                    session_key=request.session.session_key
                ).first()
                if session_data:
                    session_data.page_views_count += 1
                    session_data.save()
            
        except Exception as e:
            print(f"Error tracking page view: {e}")
    
    def determine_traffic_source(self, referrer, utm_source, request):
        """Determine traffic source based on referrer and UTM parameters"""
        if utm_source:
            return {
                'type': 'paid' if request.GET.get('utm_medium') == 'cpc' else 'organic',
                'name': utm_source,
                'url': referrer,
                'campaign': request.GET.get('utm_campaign'),
                'medium': request.GET.get('utm_medium')
            }
        
        if not referrer:
            return {
                'type': 'direct',
                'name': 'Direct',
                'url': None
            }
        
        parsed_referrer = urlparse(referrer)
        domain = parsed_referrer.netloc.lower()
        
        # Social media sources
        social_domains = {
            'facebook.com': ('facebook', 'Facebook'),
            'instagram.com': ('instagram', 'Instagram'),
            'twitter.com': ('twitter', 'Twitter'),
            'linkedin.com': ('linkedin', 'LinkedIn'),
            'youtube.com': ('youtube', 'YouTube'),
            'tiktok.com': ('tiktok', 'TikTok'),
            'snapchat.com': ('snapchat', 'Snapchat'),
        }
        
        for domain_key, (source_type, source_name) in social_domains.items():
            if domain_key in domain:
                return {
                    'type': 'social',
                    'name': source_name,
                    'url': referrer
                }
        
        # Search engines
        search_engines = {
            'google.com': ('google', 'Google'),
            'bing.com': ('bing', 'Bing'),
            'yahoo.com': ('yahoo', 'Yahoo'),
            'duckduckgo.com': ('duckduckgo', 'DuckDuckGo'),
        }
        
        for domain_key, (source_type, source_name) in search_engines.items():
            if domain_key in domain:
                return {
                    'type': 'organic',
                    'name': source_name,
                    'url': referrer
                }
        
        # WhatsApp (special case)
        if 'whatsapp' in domain or 'wa.me' in domain:
            return {
                'type': 'whatsapp',
                'name': 'WhatsApp',
                'url': referrer
            }
        
        # Email
        if 'mail' in domain or 'email' in domain:
            return {
                'type': 'email',
                'name': 'Email',
                'url': referrer
            }
        
        # Referral
        return {
            'type': 'referral',
            'name': parsed_referrer.netloc,
            'url': referrer
        }
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_bot(self, user_agent):
        """Check if user agent is a bot"""
        bot_patterns = [
            'bot', 'crawler', 'spider', 'scraper', 'crawler',
            'googlebot', 'bingbot', 'slurp', 'duckduckbot',
            'baiduspider', 'yandexbot', 'facebookexternalhit'
        ]
        user_agent_lower = user_agent.lower()
        return any(pattern in user_agent_lower for pattern in bot_patterns)
    
    def extract_page_title(self, content):
        """Extract page title from HTML content"""
        try:
            content_str = content.decode('utf-8')
            title_match = re.search(r'<title>(.*?)</title>', content_str, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()
        except:
            pass
        return None
