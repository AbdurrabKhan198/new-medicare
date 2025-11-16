"""
Django management command to update SiteSettings description and other fields
Use this in production to update existing site settings
"""
from django.core.management.base import BaseCommand
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Update SiteSettings description and other fields to match new defaults'

    def handle(self, *args, **options):
        settings = SiteSettings.objects.first()
        
        if settings:
            # Update description to match footer default
            settings.description = "MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem that grows your clinic automatically. One system, complete clinic growth."
            
            # Update meta_description if it's old
            if not settings.meta_description or "Empowering Doctors Digitally" in settings.meta_description:
                settings.meta_description = "MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors. Get more patients, reduce no-shows, grow reviews automatically. One system, complete clinic growth."
            
            # Update meta_keywords if empty or old
            if not settings.meta_keywords or len(settings.meta_keywords) < 50:
                settings.meta_keywords = "doctor website design, healthcare SEO services, medical practice SEO, doctor website development, healthcare digital marketing agency, medical clinic website, doctor CRM system, Google My Business optimization for doctors, healthcare social media marketing, AI WhatsApp for doctors, appointment reminder system, patient management software, medical practice automation, clinic growth system, healthcare lead generation, doctor online presence, medical website builder, healthcare content marketing, local SEO for doctors, medical reputation management, healthcare PPC advertising, doctor appointment booking system, medical practice management software, healthcare website optimization, doctor digital transformation"
            
            settings.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ SiteSettings updated successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   - Description: {settings.description[:50]}...')
            )
        else:
            # Create new settings if none exists
            SiteSettings.objects.create(
                site_name='Mediwell Care',
                tagline='Empowering Doctors Digitally',
                description='MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem that grows your clinic automatically. One system, complete clinic growth.',
                meta_description='MediWellCare Clinic Growth OS - Complete AI-powered digital ecosystem for doctors. Get more patients, reduce no-shows, grow reviews automatically. One system, complete clinic growth.',
                meta_keywords='doctor website design, healthcare SEO services, medical practice SEO, doctor website development, healthcare digital marketing agency, medical clinic website, doctor CRM system, Google My Business optimization for doctors, healthcare social media marketing, AI WhatsApp for doctors, appointment reminder system, patient management software, medical practice automation, clinic growth system, healthcare lead generation, doctor online presence, medical website builder, healthcare content marketing, local SEO for doctors, medical reputation management, healthcare PPC advertising, doctor appointment booking system, medical practice management software, healthcare website optimization, doctor digital transformation',
                phone='+91-9250757366',
                email='mediwellcare64@gmail.com',
            )
            self.stdout.write(
                self.style.SUCCESS('✅ SiteSettings created successfully!')
            )

