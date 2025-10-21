"""
URL configuration for mediwell_care project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('doctors/', include('directory.urls')),
    path('crm/', include('crm.urls')),
    path('pharmacy/', include('pharmacy.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
