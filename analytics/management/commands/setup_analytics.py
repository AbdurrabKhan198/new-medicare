from django.core.management.base import BaseCommand
from analytics.models import AnalyticsSettings

class Command(BaseCommand):
    help = 'Set up analytics settings and create initial configuration'

    def handle(self, *args, **options):
        # Create analytics settings if they don't exist
        settings, created = AnalyticsSettings.objects.get_or_create(
            defaults={
                'track_user_behavior': True,
                'track_heatmaps': False,
                'track_scroll_depth': True,
                'track_form_interactions': True,
                'track_outbound_links': True,
                'anonymize_ip': True,
                'cookie_consent_required': True,
                'data_retention_days': 365,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Analytics settings created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Analytics settings already exist.')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Analytics setup completed!')
        )
