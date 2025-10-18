from django.shortcuts import render
from django.views.generic import TemplateView
from .models import HeroSection, FeatureCard, Testimonial, Counter, TeamMember
from crm.models import Doctor

from services.models import Service, ServiceCategory
from portfolio.models import CaseStudy, DoctorWebsite
from blog.models import BlogPost, BlogCategory


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Hero section
        context['hero'] = HeroSection.objects.filter(is_active=True).first()
        
        # Feature cards
        context['feature_cards'] = FeatureCard.objects.filter(is_active=True).order_by('order')[:3]
        
        # Services
        context['services'] = Service.objects.filter(is_active=True, is_featured=True).order_by('order')[:6]
        
        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')[:6]
        
        # Counters
        context['counters'] = Counter.objects.filter(is_active=True).order_by('order')
        
        # Case studies
        context['case_studies'] = CaseStudy.objects.filter(is_active=True, is_featured=True).order_by('order')[:3]
        
        # Doctor websites
        context['doctor_websites'] = DoctorWebsite.objects.filter(is_active=True, is_featured=True).order_by('order')[:6]
        
        # Recent blog posts
        context['recent_posts'] = BlogPost.objects.filter(status='published').order_by('-published_at')[:3]
        
        # Featured doctors (public directory preview)
        context['featured_doctors'] = Doctor.objects.filter(is_active=True, is_available=True).select_related('clinic').order_by('-experience_years')[:6]
        
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Team members
        context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order')
        
        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')[:6]
        
        # Counters
        context['counters'] = Counter.objects.filter(is_active=True).order_by('order')
        
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'core/terms_of_service.html'


class CookiePolicyView(TemplateView):
    template_name = 'core/cookie_policy.html'