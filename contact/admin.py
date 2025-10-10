from django.contrib import admin
from .models import ContactInquiry, NewsletterSubscriber, QuoteRequest, ContactInfo


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'status', 'priority', 'created_at']
    list_filter = ['inquiry_type', 'status', 'priority', 'created_at']
    search_fields = ['name', 'email', 'clinic_name', 'subject', 'message']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'referrer']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'clinic_name', 'specialization', 'location')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message', 'budget_range', 'timeline')
        }),
        ('Status and Follow-up', {
            'fields': ('status', 'priority', 'admin_notes', 'response_sent', 'response_date')
        }),
        ('Tracking Information', {
            'fields': ('ip_address', 'user_agent', 'referrer', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'specialization', 'location', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'specialization', 'subscribed_at']
    search_fields = ['email', 'name', 'specialization', 'location']
    list_editable = ['is_active']
    ordering = ['-subscribed_at']


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'clinic_name', 'service_type', 'budget_range', 'is_processed', 'quote_sent', 'created_at']
    list_filter = ['service_type', 'is_processed', 'quote_sent', 'created_at']
    search_fields = ['name', 'email', 'clinic_name', 'specialization', 'service_type']
    list_editable = ['is_processed', 'quote_sent']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'clinic_name', 'specialization', 'location')
        }),
        ('Service Requirements', {
            'fields': ('service_type', 'specific_requirements', 'budget_range', 'timeline', 'current_website', 'social_media_handles')
        }),
        ('Additional Information', {
            'fields': ('current_challenges', 'expected_results', 'additional_notes')
        }),
        ('Processing', {
            'fields': ('is_processed', 'quote_sent', 'quote_amount')
        }),
    )
    
    ordering = ['-created_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'phone', 'email', 'address']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address', 'whatsapp_number', 'office_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url')
        }),
        ('Map Information', {
            'fields': ('google_maps_embed', 'latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )