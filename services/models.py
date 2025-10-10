from django.db import models
from django.utils import timezone


class ServiceCategory(models.Model):
    """Service categories for organization"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Services offered by Mediwell Care"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    features = models.TextField(help_text="List features separated by new lines")
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # Pricing
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=20, default="Starting from")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.name


class ServicePackage(models.Model):
    """Service packages with pricing"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, blank=True)  # e.g., "1 Month", "3 Months"
    features = models.TextField(help_text="List features separated by new lines")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service Package"
        verbose_name_plural = "Service Packages"
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ServiceFAQ(models.Model):
    """Frequently Asked Questions for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"
    
    def __str__(self):
        return self.question