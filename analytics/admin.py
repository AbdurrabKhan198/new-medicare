from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Visitor, PageView, TrafficSource, SessionData, Event, 
    DailyStats, AnalyticsSettings
)

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_id', 'ip_address', 'country', 'city', 'device_type', 
        'browser', 'total_visits', 'total_page_views', 'last_visit', 'is_bot'
    ]
    list_filter = [
        'device_type', 'browser', 'operating_system', 'country', 
        'is_bot', 'first_visit', 'last_visit'
    ]
    search_fields = ['ip_address', 'visitor_id', 'country', 'city']
    readonly_fields = ['visitor_id', 'first_visit', 'last_visit']
    ordering = ['-last_visit']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_link', 'path', 'page_title', 'timestamp', 
        'time_spent', 'exit_page', 'bounce'
    ]
    list_filter = [
        'timestamp', 'exit_page', 'bounce', 'visitor__device_type',
        'visitor__country'
    ]
    search_fields = ['path', 'page_title', 'visitor__ip_address']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def visitor_link(self, obj):
        url = reverse('admin:analytics_visitor_change', args=[obj.visitor.pk])
        return format_html('<a href="{}">{}</a>', url, obj.visitor.visitor_id)
    visitor_link.short_description = 'Visitor'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('visitor')

@admin.register(TrafficSource)
class TrafficSourceAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_link', 'source_type', 'source_name', 'campaign_name', 
        'first_visit'
    ]
    list_filter = [
        'source_type', 'source_name', 'first_visit'
    ]
    search_fields = [
        'source_name', 'source_url', 'campaign_name', 'visitor__ip_address'
    ]
    readonly_fields = ['first_visit']
    ordering = ['-first_visit']
    
    def visitor_link(self, obj):
        url = reverse('admin:analytics_visitor_change', args=[obj.visitor.pk])
        return format_html('<a href="{}">{}</a>', url, obj.visitor.visitor_id)
    visitor_link.short_description = 'Visitor'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('visitor')

@admin.register(SessionData)
class SessionDataAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_link', 'session_key', 'start_time', 'end_time', 
        'duration', 'page_views_count', 'is_active'
    ]
    list_filter = [
        'start_time', 'is_active', 'visitor__device_type'
    ]
    search_fields = ['session_key', 'visitor__ip_address']
    readonly_fields = ['session_key', 'start_time']
    ordering = ['-start_time']
    
    def visitor_link(self, obj):
        url = reverse('admin:analytics_visitor_change', args=[obj.visitor.pk])
        return format_html('<a href="{}">{}</a>', url, obj.visitor.visitor_id)
    visitor_link.short_description = 'Visitor'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('visitor')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_link', 'event_type', 'event_name', 'event_value', 
        'page_url', 'timestamp'
    ]
    list_filter = [
        'event_type', 'timestamp', 'visitor__device_type'
    ]
    search_fields = [
        'event_name', 'event_value', 'page_url', 'visitor__ip_address'
    ]
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def visitor_link(self, obj):
        url = reverse('admin:analytics_visitor_change', args=[obj.visitor.pk])
        return format_html('<a href="{}">{}</a>', url, obj.visitor.visitor_id)
    visitor_link.short_description = 'Visitor'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('visitor')

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_visitors', 'unique_visitors', 'total_page_views',
        'bounce_rate', 'new_visitors', 'returning_visitors'
    ]
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['date']
    ordering = ['-date']
    
    def has_add_permission(self, request):
        return False

@admin.register(AnalyticsSettings)
class AnalyticsSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'google_analytics_id', 'google_tag_manager_id', 
        'track_user_behavior', 'anonymize_ip'
    ]
    
    def has_add_permission(self, request):
        return not AnalyticsSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
