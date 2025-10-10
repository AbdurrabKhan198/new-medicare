from .models import SiteSettings


def site_settings(request):
    """Add site settings to all templates"""
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = SiteSettings.objects.create(
                site_name="Mediwell Care",
                tagline="Empowering Doctors Digitally",
                description="Your digital partner for websites, CRM, SEO & patient growth"
            )
    except Exception:
        settings = None
    
    return {
        'site_settings': settings
    }
