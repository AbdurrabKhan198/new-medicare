from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortfolioView.as_view(), name='portfolio'),
    path('case-study/<slug:slug>/', views.CaseStudyDetailView.as_view(), name='case_study_detail'),
    path('websites/', views.DoctorWebsiteListView.as_view(), name='doctor_websites'),
]
