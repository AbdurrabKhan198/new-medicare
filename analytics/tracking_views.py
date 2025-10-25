from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import json
import uuid
from datetime import timedelta

from .models import Visitor, PageView, Event, SessionData
from .utils import get_visitor_info, parse_user_agent, get_geolocation

@csrf_exempt
@require_http_methods(["POST"])
def track_event(request):
    """Track analytics events from JavaScript"""
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        event_data = data.get('data', {})
        
        # Get or create visitor
        visitor = get_or_create_visitor(request)
        if not visitor:
            return JsonResponse({'status': 'error', 'message': 'Could not create visitor'}, status=400)
        
        # Handle different event types
        if event_type == 'page_view':
            handle_page_view(visitor, event_data)
        elif event_type == 'page_unload':
            handle_page_unload(visitor, event_data)
        elif event_type == 'event':
            handle_custom_event(visitor, event_data)
        elif event_type == 'form_submit':
            handle_form_submit(visitor, event_data)
        elif event_type == 'click':
            handle_click(visitor, event_data)
        elif event_type == 'scroll_depth':
            handle_scroll_depth(visitor, event_data)
        elif event_type == 'outbound_click':
            handle_outbound_click(visitor, event_data)
        elif event_type == 'download':
            handle_download(visitor, event_data)
        elif event_type == 'heartbeat':
            handle_heartbeat(visitor, event_data)
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_or_create_visitor(request):
    """Get or create visitor based on session"""
    try:
        # Try to get visitor by session
        if request.session.session_key:
            visitor = Visitor.objects.filter(session_key=request.session.session_key).first()
            if visitor:
                visitor.last_visit = timezone.now()
                visitor.save()
                return visitor
        
        # Get visitor info
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Parse user agent
        device_info = parse_user_agent(user_agent)
        
        # Check if it's a bot
        is_bot = is_bot_user_agent(user_agent)
        
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

def handle_page_view(visitor, data):
    """Handle page view tracking"""
    try:
        page_view = PageView.objects.create(
            visitor=visitor,
            url=data.get('url', ''),
            path=data.get('path', ''),
            page_title=data.get('title', ''),
            referrer=data.get('referrer', ''),
            timestamp=timezone.now()
        )
        
        # Update visitor stats
        visitor.total_page_views += 1
        visitor.save()
        
        # Update session stats
        update_session_stats(visitor, data)
        
    except Exception as e:
        print(f"Error handling page view: {e}")

def handle_page_unload(visitor, data):
    """Handle page unload tracking"""
    try:
        # Find the most recent page view for this visitor
        page_view = PageView.objects.filter(
            visitor=visitor,
            url=data.get('url', '')
        ).order_by('-timestamp').first()
        
        if page_view:
            time_spent = data.get('time_spent', 0)
            page_view.time_spent = timedelta(milliseconds=time_spent)
            page_view.save()
            
            # Update visitor total time
            visitor.total_time_spent += page_view.time_spent
            visitor.save()
        
    except Exception as e:
        print(f"Error handling page unload: {e}")

def handle_custom_event(visitor, data):
    """Handle custom event tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type=data.get('event_type', 'custom'),
            event_name=data.get('event_name', ''),
            event_value=data.get('event_value'),
            page_url=data.get('url', ''),
            metadata=data.get('metadata', {}),
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling custom event: {e}")

def handle_form_submit(visitor, data):
    """Handle form submission tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type='form_submit',
            event_name=f"Form: {data.get('form_id', 'unnamed')}",
            event_value=data.get('form_action', ''),
            page_url=data.get('url', ''),
            metadata={
                'form_method': data.get('form_method'),
                'field_count': data.get('field_count'),
                'field_names': data.get('field_names', [])
            },
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling form submit: {e}")

def handle_click(visitor, data):
    """Handle click tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type='click',
            event_name=f"Click: {data.get('element_tag', 'unknown')}",
            event_value=data.get('element_text', ''),
            page_url=data.get('url', ''),
            metadata={
                'element_id': data.get('element_id'),
                'element_class': data.get('element_class'),
                'element_text': data.get('element_text')
            },
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling click: {e}")

def handle_scroll_depth(visitor, data):
    """Handle scroll depth tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type='scroll',
            event_name='Scroll Depth',
            event_value=data.get('event_value', ''),
            page_url=data.get('url', ''),
            metadata={'scroll_percent': data.get('event_value', '')},
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling scroll depth: {e}")

def handle_outbound_click(visitor, data):
    """Handle outbound link click tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type='outbound_click',
            event_name='Outbound Link Click',
            event_value=data.get('link_url', ''),
            page_url=data.get('source_url', ''),
            metadata={
                'link_text': data.get('link_text'),
                'target_url': data.get('link_url')
            },
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling outbound click: {e}")

def handle_download(visitor, data):
    """Handle file download tracking"""
    try:
        Event.objects.create(
            visitor=visitor,
            event_type='download',
            event_name='File Download',
            event_value=data.get('file_name', ''),
            page_url=data.get('source_url', ''),
            metadata={
                'file_url': data.get('file_url'),
                'file_type': data.get('file_type'),
                'file_name': data.get('file_name')
            },
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error handling download: {e}")

def handle_heartbeat(visitor, data):
    """Handle heartbeat tracking"""
    try:
        # Update visitor last visit
        visitor.last_visit = timezone.now()
        visitor.save()
        
        # Update session if exists
        update_session_stats(visitor, data)
        
    except Exception as e:
        print(f"Error handling heartbeat: {e}")

def update_session_stats(visitor, data):
    """Update session statistics"""
    try:
        if visitor.session_key:
            session_data, created = SessionData.objects.get_or_create(
                session_key=visitor.session_key,
                defaults={
                    'visitor': visitor,
                    'start_time': timezone.now(),
                    'is_active': True
                }
            )
            
            if not created:
                session_data.is_active = True
                session_data.page_views_count += 1
                session_data.save()
                
    except Exception as e:
        print(f"Error updating session stats: {e}")

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_bot_user_agent(user_agent):
    """Check if user agent is a bot"""
    bot_patterns = [
        'bot', 'crawler', 'spider', 'scraper', 'crawler',
        'googlebot', 'bingbot', 'slurp', 'duckduckbot',
        'baiduspider', 'yandexbot', 'facebookexternalhit'
    ]
    user_agent_lower = user_agent.lower()
    return any(pattern in user_agent_lower for pattern in bot_patterns)
