"""
Django management command to update HeroSection content to match template defaults
Use this in production to update existing hero content
"""
from django.core.management.base import BaseCommand
from core.models import HeroSection


class Command(BaseCommand):
    help = 'Update HeroSection content to match new template defaults'

    def handle(self, *args, **options):
        hero = HeroSection.objects.filter(is_active=True).first()
        
        if hero:
            hero.title = "We Help Doctors Get 20–50 Extra Appointments Every Month Using AI-Powered Clinic Automation."
            hero.subtitle = "While You Sleep, Our AI Systems Book Appointments, Reduce No-Shows by 40%, and Grow Your Google Reviews Automatically."
            hero.description = "Stop wasting money on individual services. One complete Clinic Growth OS. 9 AI-powered systems. Real results. No monthly limits."
            hero.primary_cta_text = "Get Free Demo"
            hero.primary_cta_url = "#contact"
            hero.secondary_cta_text = "See How It Works"
            hero.secondary_cta_url = "#features"
            hero.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ HeroSection updated successfully!')
            )
        else:
            # Create new hero section if none exists
            HeroSection.objects.create(
                title="We Help Doctors Get 20–50 Extra Appointments Every Month Using AI-Powered Clinic Automation.",
                subtitle="While You Sleep, Our AI Systems Book Appointments, Reduce No-Shows by 40%, and Grow Your Google Reviews Automatically.",
                description="Stop wasting money on individual services. One complete Clinic Growth OS. 9 AI-powered systems. Real results. No monthly limits.",
                primary_cta_text="Get Free Demo",
                primary_cta_url="#contact",
                secondary_cta_text="See How It Works",
                secondary_cta_url="#features",
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS('✅ HeroSection created successfully!')
            )

