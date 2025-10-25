from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import json

from .models import (
    Visitor, PageView, TrafficSource, SessionData, Event, 
    DailyStats, AnalyticsSettings
)
from .utils import generate_analytics_report, get_traffic_source_breakdown

@staff_member_required
def analytics_dashboard(request):
    """Main analytics dashboard"""
    # Date range (default to last 30 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get date range from request
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Get basic metrics
    total_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).count()
    
    unique_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).distinct().count()
    
    total_page_views = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).count()
    
    total_sessions = SessionData.objects.filter(
        start_time__date__range=[start_date, end_date]
    ).count()
    
    # Calculate bounce rate
    single_page_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date],
        total_page_views=1
    ).count()
    bounce_rate = (single_page_visitors / unique_visitors * 100) if unique_visitors > 0 else 0
    
    # Average session duration
    avg_duration = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date],
        time_spent__isnull=False
    ).aggregate(avg_duration=Avg('time_spent'))['avg_duration']
    
    # Top pages
    top_pages = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('path', 'page_title').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Calculate percentages for top pages
    for page in top_pages:
        if total_page_views > 0:
            page['percentage'] = round((page['views'] / total_page_views) * 100, 1)
        else:
            page['percentage'] = 0
    
    # Traffic sources with detailed breakdown
    traffic_sources = TrafficSource.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).values('source_type', 'source_name').annotate(
        visitors=Count('visitor', distinct=True)
    ).order_by('-visitors')
    
    # Calculate percentages for traffic sources
    for source in traffic_sources:
        if unique_visitors > 0:
            source['percentage'] = round((source['visitors'] / unique_visitors) * 100, 1)
        else:
            source['percentage'] = 0
    
    # Dynamic traffic source breakdown
    traffic_breakdown = {
        'direct': 0,
        'google': 0,
        'facebook': 0,
        'instagram': 0,
        'linkedin': 0,
        'whatsapp': 0,
        'referral': 0,
        'other': 0
    }
    
    # Calculate traffic source percentages
    for source in traffic_sources:
        source_type = source['source_type'].lower()
        source_name = source['source_name'].lower()
        percentage = source['percentage']
        
        if source_type == 'direct':
            traffic_breakdown['direct'] = percentage
        elif 'google' in source_name or source_type == 'organic':
            traffic_breakdown['google'] = percentage
        elif 'facebook' in source_name or source_type == 'facebook':
            traffic_breakdown['facebook'] = percentage
        elif 'instagram' in source_name or source_type == 'instagram':
            traffic_breakdown['instagram'] = percentage
        elif 'linkedin' in source_name or source_type == 'linkedin':
            traffic_breakdown['linkedin'] = percentage
        elif 'whatsapp' in source_name or source_type == 'whatsapp':
            traffic_breakdown['whatsapp'] = percentage
        elif source_type == 'referral':
            traffic_breakdown['referral'] = percentage
        else:
            traffic_breakdown['other'] += percentage
    
    # Calculate social media total
    social_media_total = (
        traffic_breakdown['facebook'] + 
        traffic_breakdown['instagram'] + 
        traffic_breakdown['linkedin'] + 
        traffic_breakdown['whatsapp']
    )
    
    # Advanced metrics calculations
    conversion_rate = 2.4  # This would be calculated from actual data
    engagement_score = 8.7  # This would be calculated from actual data
    avg_load_time = 1.2  # This would be calculated from actual data
    mobile_traffic_percentage = 68  # This would be calculated from device breakdown
    
    # Geographic data
    geographic_data = [
        {'country': 'United States', 'percentage': 35, 'visitors': unique_visitors},
        {'country': 'United Kingdom', 'percentage': 20, 'visitors': unique_visitors},
        {'country': 'Canada', 'percentage': 15, 'visitors': unique_visitors},
        {'country': 'Australia', 'percentage': 10, 'visitors': unique_visitors},
        {'country': 'Germany', 'percentage': 8, 'visitors': unique_visitors},
        {'country': 'Others', 'percentage': 12, 'visitors': unique_visitors}
    ]
    
    # Hourly traffic data for charts
    hourly_traffic = []
    for hour in range(24):
        count = PageView.objects.filter(
            timestamp__date__range=[start_date, end_date],
            timestamp__hour=hour
        ).count()
        hourly_traffic.append({'hour': hour, 'count': count})
    
    # Daily traffic data for charts
    daily_traffic = []
    for i in range(7):
        date = end_date - timedelta(days=6-i)
        count = PageView.objects.filter(
            timestamp__date=date
        ).count()
        daily_traffic.append({'date': date.strftime('%Y-%m-%d'), 'count': count})
    
    # Top pages with real data
    top_pages = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('path', 'page_title').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Calculate percentages for top pages
    for page in top_pages:
        if total_page_views > 0:
            page['percentage'] = round((page['views'] / total_page_views) * 100, 1)
        else:
            page['percentage'] = 0
    
    # Device breakdown
    device_breakdown = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Convert to JSON format for JavaScript
    device_breakdown_json = json.dumps(list(device_breakdown))
    
    # Browser breakdown
    browser_breakdown = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).values('browser').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Country breakdown
    country_breakdown = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date],
        country__isnull=False
    ).values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Recent visitors
    recent_visitors = Visitor.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).order_by('-last_visit')[:20]
    
    # Real-time visitors (last 5 minutes)
    real_time_visitors = Visitor.objects.filter(
        last_visit__gte=timezone.now() - timedelta(minutes=5)
    ).count()
    
    # Hourly distribution
    hourly_data = []
    for hour in range(24):
        count = PageView.objects.filter(
            timestamp__date__range=[start_date, end_date],
            timestamp__hour=hour
        ).count()
        hourly_data.append({'hour': hour, 'count': count})
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_visitors': total_visitors,
        'unique_visitors': unique_visitors,
        'total_page_views': total_page_views,
        'total_sessions': total_sessions,
        'bounce_rate': round(bounce_rate, 2),
        'avg_duration': avg_duration,
        'top_pages': top_pages,
        'traffic_sources': traffic_sources,
        'traffic_breakdown': traffic_breakdown,
        'social_media_total': social_media_total,
        'conversion_rate': conversion_rate,
        'engagement_score': engagement_score,
        'avg_load_time': avg_load_time,
        'mobile_traffic_percentage': mobile_traffic_percentage,
        'geographic_data': geographic_data,
        'hourly_traffic': json.dumps(hourly_traffic),
        'daily_traffic': json.dumps(daily_traffic),
        'device_breakdown': device_breakdown,
        'device_breakdown_json': device_breakdown_json,
        'browser_breakdown': browser_breakdown,
        'country_breakdown': country_breakdown,
        'recent_visitors': recent_visitors,
        'real_time_visitors': real_time_visitors,
        'hourly_data': json.dumps(hourly_data),
    }
    
    return render(request, 'analytics/tailwind_dashboard.html', context)

@staff_member_required
def real_time_analytics(request):
    """Real-time analytics view"""
    # Last 5 minutes
    cutoff_time = timezone.now() - timedelta(minutes=5)
    
    # Active visitors
    active_visitors = Visitor.objects.filter(
        last_visit__gte=cutoff_time
    ).order_by('-last_visit')
    
    # Current page views
    current_page_views = PageView.objects.filter(
        timestamp__gte=cutoff_time
    ).order_by('-timestamp')
    
    # Traffic sources in real-time
    real_time_sources = TrafficSource.objects.filter(
        first_visit__gte=cutoff_time
    ).values('source_type', 'source_name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'active_visitors': active_visitors,
        'current_page_views': current_page_views,
        'real_time_sources': real_time_sources,
        'cutoff_time': cutoff_time,
    }
    
    return render(request, 'analytics/real_time.html', context)

@staff_member_required
def visitor_detail(request, visitor_id):
    """Detailed view of a specific visitor"""
    visitor = get_object_or_404(Visitor, visitor_id=visitor_id)
    
    # Get visitor's page views
    page_views = visitor.page_views.all().order_by('-timestamp')
    
    # Get visitor's events
    events = visitor.events.all().order_by('-timestamp')
    
    # Get visitor's traffic sources
    traffic_sources = visitor.traffic_sources.all()
    
    # Get visitor's sessions
    sessions = visitor.sessions.all().order_by('-start_time')
    
    context = {
        'visitor': visitor,
        'page_views': page_views,
        'events': events,
        'traffic_sources': traffic_sources,
        'sessions': sessions,
    }
    
    return render(request, 'analytics/visitor_detail.html', context)

@staff_member_required
def traffic_sources(request):
    """Detailed traffic sources analysis"""
    # Date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Traffic sources with detailed metrics
    sources = TrafficSource.objects.filter(
        first_visit__date__range=[start_date, end_date]
    ).values('source_type', 'source_name').annotate(
        visitors=Count('visitor', distinct=True),
        sessions=Count('visitor__sessions', distinct=True),
        page_views=Count('visitor__page_views')
    ).order_by('-visitors')
    
    # UTM campaigns
    utm_campaigns = TrafficSource.objects.filter(
        first_visit__date__range=[start_date, end_date],
        campaign_name__isnull=False
    ).values('campaign_name', 'source_name').annotate(
        visitors=Count('visitor', distinct=True)
    ).order_by('-visitors')
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'sources': sources,
        'utm_campaigns': utm_campaigns,
    }
    
    return render(request, 'analytics/traffic_sources.html', context)

@staff_member_required
def pages_analysis(request):
    """Detailed pages analysis"""
    # Date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Top pages with metrics
    pages = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('path', 'page_title').annotate(
        views=Count('id'),
        unique_visitors=Count('visitor', distinct=True),
        avg_time=Avg('time_spent')
    ).order_by('-views')
    
    # Bounce pages (single page visits)
    bounce_pages = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('path', 'page_title').annotate(
        total_views=Count('id'),
        single_page_visits=Count('visitor', filter=Q(visitor__total_page_views=1))
    ).annotate(
        bounce_rate=F('single_page_visits') * 100.0 / F('total_views')
    ).filter(total_views__gte=5).order_by('-bounce_rate')
    
    # Entry pages
    entry_pages = PageView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('path', 'page_title').annotate(
        entries=Count('id', filter=Q(visitor__page_views__timestamp=F('timestamp')))
    ).order_by('-entries')
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'pages': pages,
        'bounce_pages': bounce_pages,
        'entry_pages': entry_pages,
    }
    
    return render(request, 'analytics/pages_analysis.html', context)

@staff_member_required
def export_data(request):
    """Export analytics data"""
    format_type = request.GET.get('format', 'json')
    data_type = request.GET.get('type', 'visitors')
    
    # Date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    if data_type == 'visitors':
        data = Visitor.objects.filter(
            first_visit__date__range=[start_date, end_date]
        ).values(
            'visitor_id', 'ip_address', 'first_visit', 'last_visit',
            'total_visits', 'total_page_views', 'country', 'city',
            'device_type', 'browser', 'operating_system'
        )
    elif data_type == 'page_views':
        data = PageView.objects.filter(
            timestamp__date__range=[start_date, end_date]
        ).values(
            'visitor__visitor_id', 'url', 'path', 'page_title',
            'timestamp', 'time_spent', 'referrer'
        )
    elif data_type == 'traffic_sources':
        data = TrafficSource.objects.filter(
            first_visit__date__range=[start_date, end_date]
        ).values(
            'visitor__visitor_id', 'source_type', 'source_name',
            'source_url', 'campaign_name', 'first_visit'
        )
    
    if format_type == 'json':
        return JsonResponse(list(data), safe=False)
    elif format_type == 'csv':
        # Implement CSV export
        pass
    
    return JsonResponse({'error': 'Invalid format'}, status=400)

@staff_member_required
def analytics_api(request):
    """API endpoint for analytics data"""
    metric = request.GET.get('metric', 'overview')
    period = request.GET.get('period', '30d')
    
    # Calculate date range based on period
    end_date = timezone.now().date()
    if period == '7d':
        start_date = end_date - timedelta(days=7)
    elif period == '30d':
        start_date = end_date - timedelta(days=30)
    elif period == '90d':
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    if metric == 'overview':
        data = generate_analytics_report(start_date, end_date)
    elif metric == 'traffic_sources':
        data = get_traffic_source_breakdown(start_date, end_date)
    elif metric == 'hourly':
        hourly_data = []
        for hour in range(24):
            count = PageView.objects.filter(
                timestamp__date__range=[start_date, end_date],
                timestamp__hour=hour
            ).count()
            hourly_data.append({'hour': hour, 'count': count})
        data = hourly_data
    else:
        data = {'error': 'Invalid metric'}
    
    return JsonResponse(data)
