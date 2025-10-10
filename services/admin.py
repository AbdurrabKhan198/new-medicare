from django.contrib import admin
from .models import ServiceCategory, Service, ServicePackage, ServiceFAQ


class ServicePackageInline(admin.TabularInline):
    model = ServicePackage
    extra = 0
    fields = ['name', 'price', 'duration', 'is_popular', 'is_active', 'order']


class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 0
    fields = ['question', 'answer', 'order', 'is_active']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'starting_price', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServicePackageInline, ServiceFAQInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'short_description', 'description')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Media', {
            'fields': ('icon', 'image')
        }),
        ('Pricing', {
            'fields': ('starting_price', 'price_unit')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    ordering = ['order', 'name']


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'price', 'duration', 'is_popular', 'is_active', 'order']
    list_filter = ['service', 'is_popular', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'service__name']
    list_editable = ['price', 'is_popular', 'is_active', 'order']
    ordering = ['service', 'order', 'name']


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'service', 'order', 'is_active']
    list_filter = ['service', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'service__name']
    list_editable = ['order', 'is_active']
    ordering = ['service', 'order']