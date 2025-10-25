from django import template
from django.template.loader import render_to_string
from analytics.models import AnalyticsSettings

register = template.Library()

@register.simple_tag
def analytics_tracking():
    """Include analytics tracking code"""
    try:
        analytics_settings = AnalyticsSettings.objects.first()
        if analytics_settings:
            return render_to_string('analytics/google_analytics.html', {
                'analytics_settings': analytics_settings
            })
    except:
        pass
    return ''

@register.simple_tag
def analytics_settings():
    """Get analytics settings"""
    try:
        return AnalyticsSettings.objects.first()
    except:
        return None
