"""
Django management command to initialize SiteSettings
Ensures SiteSettings exists in production database
"""
from django.core.management.base import BaseCommand
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize SiteSettings if they do not exist'

    def handle(self, *args, **options):
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Mediwell Care',
                'tagline': 'Empowering Doctors Digitally',
                'description': 'MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem that grows your clinic automatically. One system, complete clinic growth.',
                'meta_description': 'MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors. Get more patients, reduce no-shows, grow reviews automatically. One system, complete clinic growth.',
                'meta_keywords': 'doctor website design, healthcare SEO services, medical practice SEO, doctor website development, healthcare digital marketing agency, medical clinic website, doctor CRM system, Google My Business optimization for doctors, healthcare social media marketing, AI WhatsApp for doctors, appointment reminder system, patient management software, medical practice automation, clinic growth system, healthcare lead generation, doctor online presence, medical website builder, healthcare content marketing, local SEO for doctors, medical reputation management, healthcare PPC advertising, doctor appointment booking system, medical practice management software, healthcare website optimization, doctor digital transformation',
                'phone': '+91-9250757366',
                'email': 'mediwellcare64@gmail.com',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ SiteSettings created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️  SiteSettings already exists.')
            )

