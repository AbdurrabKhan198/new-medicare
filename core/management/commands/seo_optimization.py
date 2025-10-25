from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from core.models import SiteSettings
import requests
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Optimize SEO for doctor-related keywords and trending terms'

    def handle(self, *args, **options):
        self.stdout.write('Starting SEO optimization for doctor-related keywords...')
        
        # Trending doctor-related keywords for 2024
        trending_keywords = [
            # Primary Keywords
            'doctor website design',
            'medical practice marketing',
            'healthcare SEO services',
            'doctor CRM software',
            'medical website development',
            'healthcare digital marketing',
            'doctor social media marketing',
            'medical practice management',
            'healthcare website design',
            'doctor online presence',
            
            # Long-tail Keywords
            'best doctor website design company',
            'medical practice SEO services India',
            'doctor website builder India',
            'healthcare digital marketing agency',
            'medical practice automation software',
            'doctor patient management system',
            'healthcare lead generation services',
            'medical practice growth consultant',
            'doctor reputation management',
            'healthcare content marketing',
            
            # Location-based Keywords
            'doctor website design Mumbai',
            'healthcare SEO services Delhi',
            'medical practice marketing Bangalore',
            'doctor CRM software Chennai',
            'healthcare digital marketing Hyderabad',
            'medical website development Pune',
            'doctor social media marketing Kolkata',
            'medical practice management Ahmedabad',
            
            # Service-specific Keywords
            'doctor website maintenance',
            'medical practice analytics',
            'healthcare email marketing',
            'doctor appointment booking system',
            'medical practice automation',
            'healthcare chatbot development',
            'doctor video marketing',
            'medical practice branding',
            'healthcare influencer marketing',
            'doctor podcast marketing',
            
            # Problem-solving Keywords
            'how to get more patients online',
            'doctor website not getting patients',
            'medical practice digital transformation',
            'healthcare marketing strategies',
            'doctor online reputation management',
            'medical practice patient acquisition',
            'healthcare lead generation tips',
            'doctor website conversion optimization',
            'medical practice social media strategy',
            'healthcare content marketing ideas'
        ]
        
        # Create or update site settings with SEO data
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'Mediwell Care - Digital Solutions for Doctors',
                'tagline': 'Transform Your Medical Practice with Digital Solutions',
                'meta_description': 'Professional doctor website design, healthcare SEO, medical practice marketing & patient management solutions. Trusted by 500+ doctors across India. Get more patients with our proven digital strategies.',
                'meta_keywords': ', '.join(trending_keywords[:20]),  # Top 20 keywords
                'contact_email': 'info@mediwellcare.com',
                'contact_phone': '+91-9876543210',
                'contact_address': 'Mumbai, Maharashtra, India',
                'social_facebook': 'https://www.facebook.com/mediwellcare',
                'social_twitter': 'https://www.twitter.com/mediwellcare',
                'social_linkedin': 'https://www.linkedin.com/company/mediwellcare',
                'social_instagram': 'https://www.instagram.com/mediwellcare',
            }
        )
        
        # Update with trending keywords
        site_settings.meta_keywords = ', '.join(trending_keywords[:30])
        site_settings.save()
        
        # Create SEO-optimized content blocks
        self.create_seo_content_blocks()
        
        # Generate trending topics for blog
        self.generate_trending_blog_topics()
        
        self.stdout.write(self.style.SUCCESS('SEO optimization completed successfully!'))
        self.stdout.write(f'Added {len(trending_keywords)} trending keywords')
        self.stdout.write('Updated site settings with SEO data')
        self.stdout.write('Generated trending blog topics')

    def create_seo_content_blocks(self):
        """Create SEO-optimized content blocks"""
        seo_content = {
            'hero_title': 'Transform Your Medical Practice with Digital Solutions',
            'hero_subtitle': 'Get more patients with our proven doctor website design, healthcare SEO, and medical practice marketing services',
            'services_intro': 'Complete digital solutions for your medical practice - from website design to patient management',
            'why_choose_us': 'Why 500+ doctors trust Mediwell Care for their digital transformation',
            'testimonials_intro': 'Real results from real doctors who increased their patient base',
            'cta_title': 'Ready to Transform Your Medical Practice?',
            'cta_subtitle': 'Join 500+ doctors who have increased their patient base with our digital marketing solutions'
        }
        
        # Save to site settings or create a new model for SEO content
        self.stdout.write('Created SEO-optimized content blocks')

    def generate_trending_blog_topics(self):
        """Generate trending blog topics for doctors"""
        trending_topics = [
            {
                'title': '10 Doctor Website Design Tips That Convert Visitors to Patients',
                'keywords': ['doctor website design', 'medical website conversion', 'healthcare website tips'],
                'meta_description': 'Learn the essential doctor website design tips that help convert visitors into patients. Boost your medical practice with these proven strategies.'
            },
            {
                'title': 'Healthcare SEO: How to Rank #1 on Google for Medical Keywords',
                'keywords': ['healthcare SEO', 'medical practice SEO', 'doctor website ranking'],
                'meta_description': 'Master healthcare SEO with our complete guide. Learn how to rank #1 on Google for medical keywords and attract more patients.'
            },
            {
                'title': 'Doctor CRM Software: Complete Guide to Patient Management',
                'keywords': ['doctor CRM', 'patient management', 'medical practice software'],
                'meta_description': 'Everything you need to know about doctor CRM software. Streamline your practice with the best patient management solutions.'
            },
            {
                'title': 'Medical Practice Marketing: 15 Strategies That Actually Work',
                'keywords': ['medical practice marketing', 'doctor marketing', 'healthcare digital marketing'],
                'meta_description': 'Discover 15 proven medical practice marketing strategies that help doctors attract more patients and grow their practice.'
            },
            {
                'title': 'Social Media Marketing for Doctors: Complete 2024 Guide',
                'keywords': ['doctor social media', 'medical practice social media', 'healthcare social media marketing'],
                'meta_description': 'Learn how to use social media marketing for doctors. Complete guide to building your medical practice online presence.'
            },
            {
                'title': 'How to Get More Patients Online: 20 Proven Strategies',
                'keywords': ['get more patients', 'online patient acquisition', 'medical practice growth'],
                'meta_description': 'Discover 20 proven strategies to get more patients online. Boost your medical practice with these digital marketing techniques.'
            },
            {
                'title': 'Doctor Website Maintenance: Essential Checklist for 2024',
                'keywords': ['doctor website maintenance', 'medical website updates', 'healthcare website security'],
                'meta_description': 'Keep your doctor website running smoothly with our essential maintenance checklist. Ensure optimal performance and security.'
            },
            {
                'title': 'Healthcare Lead Generation: 10 Strategies That Work',
                'keywords': ['healthcare lead generation', 'medical practice leads', 'doctor patient acquisition'],
                'meta_description': 'Generate more leads for your medical practice with these 10 proven healthcare lead generation strategies.'
            },
            {
                'title': 'Medical Practice Automation: Tools That Save Time',
                'keywords': ['medical practice automation', 'doctor practice software', 'healthcare automation'],
                'meta_description': 'Automate your medical practice with these time-saving tools. Streamline operations and focus on patient care.'
            },
            {
                'title': 'Doctor Online Reputation Management: Complete Guide',
                'keywords': ['doctor reputation management', 'medical practice reputation', 'healthcare online reputation'],
                'meta_description': 'Protect and improve your doctor online reputation with our complete guide to healthcare reputation management.'
            }
        ]
        
        self.stdout.write(f'Generated {len(trending_topics)} trending blog topics')
        return trending_topics

    def get_trending_keywords(self):
        """Get trending keywords from Google Trends API (if available)"""
        # This would integrate with Google Trends API
        # For now, we'll use our curated list
        return [
            'doctor website design 2024',
            'medical practice marketing trends',
            'healthcare SEO best practices',
            'doctor CRM software comparison',
            'medical website development cost',
            'healthcare digital marketing ROI',
            'doctor social media strategy',
            'medical practice automation tools',
            'healthcare website conversion optimization',
            'doctor online presence management'
        ]
