from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sessions.models import Session
import uuid
import json

class Visitor(models.Model):
    """Track unique visitors to the website"""
    visitor_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    total_visits = models.PositiveIntegerField(default=1)
    total_page_views = models.PositiveIntegerField(default=0)
    total_time_spent = models.DurationField(default=timezone.timedelta(0))
    is_bot = models.BooleanField(default=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-last_visit']
    
    def __str__(self):
        return f"Visitor {self.visitor_id} - {self.ip_address}"

class PageView(models.Model):
    """Track individual page views"""
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views')
    url = models.URLField()
    path = models.CharField(max_length=500)
    page_title = models.CharField(max_length=200, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_spent = models.DurationField(blank=True, null=True)
    exit_page = models.BooleanField(default=False)
    bounce = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.visitor.visitor_id} - {self.path}"

class TrafficSource(models.Model):
    """Track where visitors came from"""
    SOURCE_CHOICES = [
        ('direct', 'Direct'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('bing', 'Bing'),
        ('yahoo', 'Yahoo'),
        ('referral', 'Referral'),
        ('email', 'Email'),
        ('social', 'Social Media'),
        ('organic', 'Organic Search'),
        ('paid', 'Paid Search'),
        ('unknown', 'Unknown'),
    ]
    
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='traffic_sources')
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    source_name = models.CharField(max_length=100)
    source_url = models.URLField(blank=True, null=True)
    campaign_name = models.CharField(max_length=100, blank=True, null=True)
    medium = models.CharField(max_length=50, blank=True, null=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-first_visit']
    
    def __str__(self):
        return f"{self.visitor.visitor_id} - {self.source_name}"

class SessionData(models.Model):
    """Track session-level data"""
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    page_views_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_term = models.CharField(max_length=100, blank=True, null=True)
    utm_content = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Session {self.session_key} - {self.visitor.visitor_id}"

class Event(models.Model):
    """Track custom events (clicks, form submissions, etc.)"""
    EVENT_TYPES = [
        ('click', 'Click'),
        ('form_submit', 'Form Submit'),
        ('download', 'Download'),
        ('video_play', 'Video Play'),
        ('scroll', 'Scroll'),
        ('hover', 'Hover'),
        ('custom', 'Custom'),
    ]
    
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    event_value = models.CharField(max_length=200, blank=True, null=True)
    page_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.visitor.visitor_id} - {self.event_name}"

class AnalyticsSettings(models.Model):
    """Global analytics settings"""
    google_analytics_id = models.CharField(max_length=20, blank=True, null=True)
    google_tag_manager_id = models.CharField(max_length=20, blank=True, null=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True, null=True)
    track_user_behavior = models.BooleanField(default=True)
    track_heatmaps = models.BooleanField(default=False)
    track_scroll_depth = models.BooleanField(default=True)
    track_form_interactions = models.BooleanField(default=True)
    track_outbound_links = models.BooleanField(default=True)
    anonymize_ip = models.BooleanField(default=True)
    cookie_consent_required = models.BooleanField(default=True)
    data_retention_days = models.PositiveIntegerField(default=365)
    
    class Meta:
        verbose_name = "Analytics Settings"
        verbose_name_plural = "Analytics Settings"
    
    def __str__(self):
        return "Analytics Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and AnalyticsSettings.objects.exists():
            return
        super().save(*args, **kwargs)

class DailyStats(models.Model):
    """Daily aggregated statistics"""
    date = models.DateField(unique=True)
    total_visitors = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    total_page_views = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)
    avg_session_duration = models.DurationField(blank=True, null=True)
    bounce_rate = models.FloatField(default=0.0)
    new_visitors = models.PositiveIntegerField(default=0)
    returning_visitors = models.PositiveIntegerField(default=0)
    
    # Traffic sources
    direct_traffic = models.PositiveIntegerField(default=0)
    google_traffic = models.PositiveIntegerField(default=0)
    facebook_traffic = models.PositiveIntegerField(default=0)
    whatsapp_traffic = models.PositiveIntegerField(default=0)
    referral_traffic = models.PositiveIntegerField(default=0)
    organic_traffic = models.PositiveIntegerField(default=0)
    
    # Device breakdown
    desktop_visitors = models.PositiveIntegerField(default=0)
    mobile_visitors = models.PositiveIntegerField(default=0)
    tablet_visitors = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Statistics"
        verbose_name_plural = "Daily Statistics"
    
    def __str__(self):
        return f"Stats for {self.date}"
