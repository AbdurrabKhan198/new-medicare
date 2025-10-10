from django.contrib import admin
from .models import CaseStudy, CaseStudyImage, DoctorWebsite, Technology


class CaseStudyImageInline(admin.TabularInline):
    model = CaseStudyImage
    extra = 0
    fields = ['image', 'caption', 'order']


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'doctor_name', 'doctor_specialization', 'project_type', 'is_featured', 'is_active', 'order']
    list_filter = ['project_type', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'doctor_name', 'clinic_name', 'doctor_specialization']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CaseStudyImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'doctor_name', 'doctor_specialization', 'clinic_name', 'location')
        }),
        ('Project Details', {
            'fields': ('project_type', 'duration', 'budget_range')
        }),
        ('Content', {
            'fields': ('challenge', 'solution', 'results', 'testimonial')
        }),
        ('Media', {
            'fields': ('featured_image', 'before_image', 'after_image')
        }),
        ('Results Metrics', {
            'fields': ('website_traffic_increase', 'patient_inquiries_increase', 'social_media_growth')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    ordering = ['order', '-created_at']


@admin.register(CaseStudyImage)
class CaseStudyImageAdmin(admin.ModelAdmin):
    list_display = ['case_study', 'caption', 'order']
    list_filter = ['case_study']
    search_fields = ['case_study__title', 'caption']
    list_editable = ['order']
    ordering = ['case_study', 'order']


@admin.register(DoctorWebsite)
class DoctorWebsiteAdmin(admin.ModelAdmin):
    list_display = ['doctor_name', 'specialization', 'clinic_name', 'website_type', 'is_featured', 'is_active', 'order']
    list_filter = ['website_type', 'is_featured', 'is_active', 'launch_date']
    search_fields = ['doctor_name', 'specialization', 'clinic_name', 'location']
    list_editable = ['is_featured', 'is_active', 'order']
    
    fieldsets = (
        ('Doctor Information', {
            'fields': ('doctor_name', 'specialization', 'clinic_name', 'location')
        }),
        ('Website Details', {
            'fields': ('website_url', 'website_type', 'technologies_used')
        }),
        ('Media', {
            'fields': ('screenshot', 'logo')
        }),
        ('Results', {
            'fields': ('launch_date', 'monthly_visitors', 'patient_inquiries')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    ordering = ['order', '-launch_date']


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']