from django.db import models
from django.utils import timezone


class CaseStudy(models.Model):
    """Portfolio case studies"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    doctor_name = models.CharField(max_length=100)
    doctor_specialization = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    # Project Details
    project_type = models.CharField(max_length=100)  # e.g., "Website Development", "SEO Campaign"
    duration = models.CharField(max_length=50)  # e.g., "2 Months", "6 Weeks"
    budget_range = models.CharField(max_length=50, blank=True)  # e.g., "₹50,000 - ₹1,00,000"
    
    # Content
    challenge = models.TextField()
    solution = models.TextField()
    results = models.TextField()
    testimonial = models.TextField(blank=True)
    
    # Media
    featured_image = models.ImageField(upload_to='case_studies/')
    before_image = models.ImageField(upload_to='case_studies/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='case_studies/after/', blank=True, null=True)
    
    # Results Metrics
    website_traffic_increase = models.CharField(max_length=50, blank=True)  # e.g., "300%"
    patient_inquiries_increase = models.CharField(max_length=50, blank=True)  # e.g., "250%"
    social_media_growth = models.CharField(max_length=50, blank=True)  # e.g., "500%"
    
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
        ordering = ['order', '-created_at']
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"
    
    def __str__(self):
        return f"{self.doctor_name} - {self.title}"


class CaseStudyImage(models.Model):
    """Additional images for case studies"""
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='case_studies/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Case Study Image"
        verbose_name_plural = "Case Study Images"
    
    def __str__(self):
        return f"{self.case_study.title} - Image {self.order}"


class DoctorWebsite(models.Model):
    """Doctor websites showcase"""
    doctor_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    # Website Details
    website_url = models.URLField()
    website_type = models.CharField(max_length=50)  # e.g., "Clinic Website", "Personal Brand"
    technologies_used = models.CharField(max_length=200, blank=True)  # e.g., "WordPress, Elementor"
    
    # Media
    screenshot = models.ImageField(upload_to='doctor_websites/')
    logo = models.ImageField(upload_to='doctor_websites/logos/', blank=True, null=True)
    
    # Results
    launch_date = models.DateField()
    monthly_visitors = models.PositiveIntegerField(blank=True, null=True)
    patient_inquiries = models.PositiveIntegerField(blank=True, null=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-launch_date']
        verbose_name = "Doctor Website"
        verbose_name_plural = "Doctor Websites"
    
    def __str__(self):
        return f"{self.doctor_name} - {self.clinic_name}"


class Technology(models.Model):
    """Technologies and tools used"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., "Frontend", "Backend", "CMS"
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
    
    def __str__(self):
        return self.name