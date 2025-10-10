from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory, ServicePackage, ServiceFAQ


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order')
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        context['packages'] = ServicePackage.objects.filter(service=service, is_active=True).order_by('order')
        context['faqs'] = ServiceFAQ.objects.filter(service=service, is_active=True).order_by('order')
        context['related_services'] = Service.objects.filter(
            category=service.category, 
            is_active=True
        ).exclude(id=service.id).order_by('order')[:3]
        return context


class ServiceCategoryView(ListView):
    model = Service
    template_name = 'services/service_category.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(ServiceCategory, slug=self.kwargs['slug'], is_active=True)
        return Service.objects.filter(category=self.category, is_active=True).order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order')
        return context