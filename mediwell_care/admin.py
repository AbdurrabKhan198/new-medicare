from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from contact.models import ContactInquiry, QuoteRequest, NewsletterSubscriber
from core.models import SiteSettings


class MediwellCareAdminSite(AdminSite):
    site_header = "Mediwell Care Administration"
    site_title = "Mediwell Care Admin"
    index_title = "Welcome to Mediwell Care Administration"
    
    def index(self, request, extra_context=None):
        """
        Display the main admin index page with analytics
        """
        extra_context = extra_context or {}
        
        # Get analytics data
        total_inquiries = ContactInquiry.objects.count()
        total_quotes = QuoteRequest.objects.count()
        total_subscribers = NewsletterSubscriber.objects.count()
        recent_inquiries = ContactInquiry.objects.order_by('-created_at')[:5]
        
        # Get inquiry types distribution
        inquiry_types = ContactInquiry.objects.values('inquiry_type').annotate(
            count=Count('inquiry_type')
        ).order_by('-count')
        
        extra_context.update({
            'total_inquiries': total_inquiries,
            'total_quotes': total_quotes,
            'total_subscribers': total_subscribers,
            'recent_inquiries': recent_inquiries,
            'inquiry_types': inquiry_types,
        })
        
        return super().index(request, extra_context)


# Create custom admin site
admin_site = MediwellCareAdminSite(name='mediwell_care_admin')

# Register models with custom admin site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Register all models
from core.models import SiteSettings, TeamMember, Testimonial, Counter, HeroSection, FeatureCard
from services.models import ServiceCategory, Service, ServicePackage, ServiceFAQ
from portfolio.models import CaseStudy, CaseStudyImage, DoctorWebsite, Technology
from blog.models import BlogCategory, BlogPost, BlogTag, BlogPostTag, BlogComment
from contact.models import ContactInquiry, NewsletterSubscriber, QuoteRequest, ContactInfo

# Core models
admin_site.register(SiteSettings)
admin_site.register(TeamMember)
admin_site.register(Testimonial)
admin_site.register(Counter)
admin_site.register(HeroSection)
admin_site.register(FeatureCard)

# Services models
admin_site.register(ServiceCategory)
admin_site.register(Service)
admin_site.register(ServicePackage)
admin_site.register(ServiceFAQ)

# Portfolio models
admin_site.register(CaseStudy)
admin_site.register(CaseStudyImage)
admin_site.register(DoctorWebsite)
admin_site.register(Technology)

# Blog models
admin_site.register(BlogCategory)
admin_site.register(BlogPost)
admin_site.register(BlogTag)
admin_site.register(BlogPostTag)
admin_site.register(BlogComment)

# Contact models
admin_site.register(ContactInquiry)
admin_site.register(NewsletterSubscriber)
admin_site.register(QuoteRequest)
admin_site.register(ContactInfo)
