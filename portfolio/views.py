from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import CaseStudy, DoctorWebsite, Technology


class PortfolioView(ListView):
    model = CaseStudy
    template_name = 'portfolio/portfolio.html'
    context_object_name = 'case_studies'
    paginate_by = 9
    
    def get_queryset(self):
        return CaseStudy.objects.filter(is_active=True).order_by('order', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor_websites'] = DoctorWebsite.objects.filter(is_active=True, is_featured=True).order_by('order')[:6]
        context['technologies'] = Technology.objects.filter(is_active=True).order_by('order')
        return context


class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = 'portfolio/case_study_detail.html'
    context_object_name = 'case_study'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return CaseStudy.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_study = self.get_object()
        context['images'] = case_study.images.all().order_by('order')
        context['related_case_studies'] = CaseStudy.objects.filter(
            is_active=True
        ).exclude(id=case_study.id).order_by('order')[:3]
        return context


class DoctorWebsiteListView(ListView):
    model = DoctorWebsite
    template_name = 'portfolio/doctor_websites.html'
    context_object_name = 'websites'
    paginate_by = 12
    
    def get_queryset(self):
        return DoctorWebsite.objects.filter(is_active=True).order_by('order', '-launch_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['technologies'] = Technology.objects.filter(is_active=True).order_by('order')
        return context