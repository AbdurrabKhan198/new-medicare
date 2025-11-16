from .models import SiteSettings
from django.db import DatabaseError


def site_settings(request):
    """Add site settings to all templates"""
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            try:
                settings = SiteSettings.objects.create(
                    site_name="Mediwell Care",
                    tagline="Empowering Doctors Digitally",
                    description="Your digital partner for websites, CRM, SEO & patient growth",
                    meta_description="MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors. Get more patients, reduce no-shows, grow reviews automatically.",
                    meta_keywords="doctor website, healthcare digital marketing, medical SEO, doctor CRM, healthcare social media"
                )
            except (DatabaseError, Exception):
                # If creation fails, return a dict with defaults
                settings = {
                    'site_name': 'Mediwell Care',
                    'tagline': 'Empowering Doctors Digitally',
                    'description': 'Your digital partner for websites, CRM, SEO & patient growth',
                    'meta_description': 'MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors',
                    'meta_keywords': 'doctor website, healthcare digital marketing, medical SEO'
                }
    except (DatabaseError, Exception):
        # Return a dict with defaults if database is not available
        settings = {
            'site_name': 'Mediwell Care',
            'tagline': 'Empowering Doctors Digitally',
            'description': 'Your digital partner for websites, CRM, SEO & patient growth',
            'meta_description': 'MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors',
            'meta_keywords': 'doctor website, healthcare digital marketing, medical SEO'
        }
    
    return {
        'site_settings': settings
    }
