from django.contrib import admin
from .models import (
    SiteSettings, TeamMember, Testimonial, Counter, 
    HeroSection, FeatureCard, Specialization, HomePageSection
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['site_name', 'email', 'phone']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline', 'description', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'whatsapp_number')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'google_tag_manager_id')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'order', 'is_active']
    list_filter = ['is_active', 'position', 'created_at']
    search_fields = ['name', 'position', 'specialization']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'clinic_name', 'rating', 'is_featured', 'order', 'is_active']
    list_filter = ['is_featured', 'is_active', 'rating', 'created_at']
    search_fields = ['name', 'title', 'clinic_name', 'content']
    list_editable = ['is_featured', 'order', 'is_active']
    ordering = ['order', '-created_at']


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ['title', 'number', 'suffix', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_editable = ['number', 'suffix', 'order', 'is_active']
    ordering = ['order']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Call to Action', {
            'fields': ('primary_cta_text', 'primary_cta_url', 'secondary_cta_text', 'secondary_cta_url')
        }),
        ('Media', {
            'fields': ('background_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(HomePageSection)
class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ['section_name', 'title', 'is_active', 'order']
    list_filter = ['is_active', 'section_name']
    search_fields = ['title', 'subtitle', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order']