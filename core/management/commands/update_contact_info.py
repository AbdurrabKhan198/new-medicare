from django.core.management.base import BaseCommand
from core.models import SiteSettings
from contact.models import ContactInfo


class Command(BaseCommand):
    help = 'Update contact information in the database'

    def handle(self, *args, **options):
        self.stdout.write('Updating contact information...')
        
        # Update SiteSettings
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'Mediwell Care',
                'tagline': 'Empowering Doctors Digitally',
                'description': 'Your digital partner for websites, CRM, SEO & patient growth. We specialize in comprehensive digital solutions for doctors and healthcare professionals.',
                'phone': '+91-9250757366',
                'email': 'mediwellcare64@gmail.com',
                'address': 'Lucknow, Uttar Pradesh, India',
                'whatsapp_number': '919250757366',
                'meta_title': 'Mediwell Care - Digital Solutions for Doctors',
                'meta_description': 'Transform your medical practice with our comprehensive digital solutions. Custom websites, CRM systems, SEO optimization, and social media management for healthcare professionals.',
                'meta_keywords': 'doctor website, healthcare digital marketing, medical SEO, doctor CRM, healthcare social media, medical practice management'
            }
        )
        
        if not created:
            # Update existing record
            site_settings.phone = '+91-9250757366'
            site_settings.email = 'mediwellcare64@gmail.com'
            site_settings.address = 'Lucknow, Uttar Pradesh, India'
            site_settings.whatsapp_number = '919250757366'
            site_settings.save()
            self.stdout.write('Updated existing SiteSettings record')
        else:
            self.stdout.write('Created new SiteSettings record')
        
        # Update ContactInfo
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'title': 'Get in Touch',
                'description': 'Ready to transform your practice? Contact us for a free consultation.',
                'phone': '+91-9250757366',
                'email': 'mediwellcare64@gmail.com',
                'address': 'Lucknow, Uttar Pradesh, India',
                'whatsapp_number': '919250757366',
                'office_hours': 'Monday - Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM',
                'is_active': True
            }
        )
        
        if not created:
            # Update existing record
            contact_info.phone = '+91-9250757366'
            contact_info.email = 'mediwellcare64@gmail.com'
            contact_info.address = 'Lucknow, Uttar Pradesh, India'
            contact_info.whatsapp_number = '919250757366'
            contact_info.save()
            self.stdout.write('Updated existing ContactInfo record')
        else:
            self.stdout.write('Created new ContactInfo record')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated contact information!'))
