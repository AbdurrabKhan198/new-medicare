from django.shortcuts import render
from django.views.generic import TemplateView
from .models import HeroSection, FeatureCard, Counter, TeamMember, HomePageSection

from services.models import Service, ServiceCategory
from blog.models import BlogPost, BlogCategory


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Hero section - single query
        context['hero'] = HeroSection.objects.filter(is_active=True).first()
        
        # Feature cards - optimized query
        context['feature_cards'] = FeatureCard.objects.filter(is_active=True).order_by('order')[:3].only('title', 'description', 'icon', 'order')
        
        # Services - optimized query
        context['services'] = Service.objects.filter(is_active=True, is_featured=True).order_by('order')[:6].only('title', 'short_description', 'slug', 'icon', 'order')
        
        # Counters - optimized query
        context['counters'] = Counter.objects.filter(is_active=True).order_by('order').only('title', 'number', 'suffix', 'icon', 'order')
        
        # Recent blog posts - optimized query with select_related
        context['recent_posts'] = BlogPost.objects.filter(status='published').select_related('category', 'author').order_by('-published_at')[:3].only('title', 'excerpt', 'slug', 'featured_image', 'published_at', 'category__name', 'author__username')
        
        # Homepage sections configuration - single query with dict comprehension
        context['homepage_sections'] = {section.section_name: section for section in HomePageSection.objects.filter(is_active=True).only('section_name', 'is_active', 'order')}
        
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Team members - optimized query
        context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order').only('name', 'role', 'bio', 'image', 'order')
        
        # Counters - optimized query
        context['counters'] = Counter.objects.filter(is_active=True).order_by('order').only('title', 'number', 'suffix', 'icon', 'order')
        
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'core/terms_of_service.html'


class CookiePolicyView(TemplateView):
    template_name = 'core/cookie_policy.html'