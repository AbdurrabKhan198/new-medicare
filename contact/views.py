from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactInfo, ContactInquiry, QuoteRequest, NewsletterSubscriber
from .forms import ContactForm, QuoteRequestForm, NewsletterForm


class ContactView(TemplateView):
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.filter(is_active=True).first()
        context['contact_form'] = ContactForm()
        context['quote_form'] = QuoteRequestForm()
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        
        if 'contact_form' in request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                inquiry = form.save()
                
                # Send email notification
                try:
                    send_mail(
                        f'New Contact Inquiry from {inquiry.name}',
                        f'''
                        Name: {inquiry.name}
                        Email: {inquiry.email}
                        Phone: {inquiry.phone}
                        Clinic: {inquiry.clinic_name}
                        Specialization: {inquiry.specialization}
                        Inquiry Type: {inquiry.get_inquiry_type_display()}
                        Subject: {inquiry.subject}
                        Message: {inquiry.message}
                        ''',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    )
                except Exception as e:
                    pass  # Log error but don't break the flow
                
                messages.success(request, 'Thank you for your inquiry! We will get back to you soon.')
                return redirect('contact')
            else:
                context['contact_form'] = form
        
        elif 'quote_form' in request.POST:
            form = QuoteRequestForm(request.POST)
            if form.is_valid():
                quote = form.save()
                
                # Send email notification
                try:
                    send_mail(
                        f'New Quote Request from {quote.name}',
                        f'''
                        Name: {quote.name}
                        Email: {quote.email}
                        Phone: {quote.phone}
                        Clinic: {quote.clinic_name}
                        Specialization: {quote.specialization}
                        Service Type: {quote.get_service_type_display()}
                        Requirements: {quote.specific_requirements}
                        Budget: {quote.budget_range}
                        Timeline: {quote.timeline}
                        ''',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    )
                except Exception as e:
                    pass  # Log error but don't break the flow
                
                messages.success(request, 'Thank you for your quote request! We will send you a detailed proposal soon.')
                return redirect('contact')
            else:
                context['quote_form'] = form
        
        return render(request, self.template_name, context)


class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    template_name = 'contact/newsletter_success.html'
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data.get('name', '')
        specialization = form.cleaned_data.get('specialization', '')
        location = form.cleaned_data.get('location', '')
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'specialization': specialization,
                'location': location,
            }
        )
        
        if created:
            messages.success(self.request, 'Successfully subscribed to our newsletter!')
        else:
            messages.info(self.request, 'You are already subscribed to our newsletter.')
        
        return redirect('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please check your email address and try again.')
        return redirect('home')