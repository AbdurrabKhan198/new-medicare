from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SiteSettings(models.Model):
    """Site-wide settings and configuration"""
    site_name = models.CharField(max_length=100, default="Mediwell Care")
    tagline = models.CharField(max_length=200, default="Empowering Doctors Digitally")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True)
    google_tag_manager_id = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name


class TeamMember(models.Model):
    """Team members for About page"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Client testimonials"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)  # Doctor's title/specialization
    clinic_name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class Counter(models.Model):
    """Animated counters for homepage"""
    title = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True)  # e.g., "+", "%", "K"
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Counter"
        verbose_name_plural = "Counters"
    
    def __str__(self):
        return self.title


class HeroSection(models.Model):
    """Homepage hero section content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    description = models.TextField()
    primary_cta_text = models.CharField(max_length=50, default="Get Free Consultation")
    primary_cta_url = models.CharField(max_length=200, default="#contact")
    secondary_cta_text = models.CharField(max_length=50, default="View Our Work")
    secondary_cta_url = models.CharField(max_length=200, default="#portfolio")
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
    
    def __str__(self):
        return self.title


class FeatureCard(models.Model):
    """Feature cards for homepage"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # FontAwesome icon class
    cta_text = models.CharField(max_length=50, blank=True)
    cta_url = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Feature Card"
        verbose_name_plural = "Feature Cards"
    
    def __str__(self):
        return self.title


class HomePageSection(models.Model):
    """Configurable sections for homepage"""
    SECTION_CHOICES = [
        ('hero', 'Hero Section'),
        ('features', 'Features'),
        ('services', 'Services'),
        ('case_studies', 'Case Studies'),
        ('testimonials', 'Testimonials'),
        ('websites', 'Doctor Websites'),
        ('blog', 'Blog Posts'),
        ('counters', 'Statistics'),
    ]
    
    section_name = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Homepage Section"
        verbose_name_plural = "Homepage Sections"
    
    def __str__(self):
        return self.title