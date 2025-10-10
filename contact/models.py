from django.db import models
from django.utils import timezone


class ContactInquiry(models.Model):
    """Contact form inquiries"""
    INQUIRY_TYPE_CHOICES = [
        ('website', 'Website Development'),
        ('seo', 'SEO Services'),
        ('social_media', 'Social Media Management'),
        ('crm', 'CRM System'),
        ('google_business', 'Google My Business Setup'),
        ('reputation', 'Reputation Management'),
        ('consultation', 'Free Consultation'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    clinic_name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Inquiry Details
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget_range = models.CharField(max_length=50, blank=True)  # e.g., "₹50,000 - ₹1,00,000"
    timeline = models.CharField(max_length=50, blank=True)  # e.g., "1 Month", "3 Months"
    
    # Status and Follow-up
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    # Response
    admin_notes = models.TextField(blank=True)
    response_sent = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    """Newsletter subscribers"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
    
    def __str__(self):
        return self.email


class QuoteRequest(models.Model):
    """Quote requests for specific services"""
    SERVICE_CHOICES = [
        ('website', 'Website Development'),
        ('seo', 'SEO Services'),
        ('social_media', 'Social Media Management'),
        ('crm', 'CRM System'),
        ('google_business', 'Google My Business Setup'),
        ('reputation', 'Reputation Management'),
        ('package', 'Complete Digital Package'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    clinic_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    # Service Requirements
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    specific_requirements = models.TextField()
    budget_range = models.CharField(max_length=50)
    timeline = models.CharField(max_length=50)
    current_website = models.URLField(blank=True)
    social_media_handles = models.TextField(blank=True)
    
    # Additional Information
    current_challenges = models.TextField(blank=True)
    expected_results = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Status
    is_processed = models.BooleanField(default=False)
    quote_sent = models.BooleanField(default=False)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class ContactInfo(models.Model):
    """Contact information for the website"""
    title = models.CharField(max_length=100, default="Get in Touch")
    description = models.TextField(blank=True)
    
    # Contact Details
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Office Hours
    office_hours = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Map
    google_maps_embed = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return self.title