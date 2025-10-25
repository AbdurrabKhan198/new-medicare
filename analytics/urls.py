from django.urls import path
from . import views
from . import tracking_views

app_name = 'analytics'

urlpatterns = [
    # Main dashboard
    path('', views.analytics_dashboard, name='dashboard'),
    path('real-time/', views.real_time_analytics, name='real_time'),
    
    # Detailed views
    path('visitor/<uuid:visitor_id>/', views.visitor_detail, name='visitor_detail'),
    path('traffic-sources/', views.traffic_sources, name='traffic_sources'),
    path('pages/', views.pages_analysis, name='pages_analysis'),
    
    # API endpoints
    path('api/', views.analytics_api, name='api'),
    path('export/', views.export_data, name='export'),
    
    # Tracking endpoints
    path('track/', tracking_views.track_event, name='track'),
]
