from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from datetime import datetime, timedelta
import json

from .models import (
    Clinic, Doctor, Patient, Appointment, Treatment, 
    Prescription, Payment, MedicalRecord
)
from .forms import (
    PatientForm, AppointmentForm, TreatmentForm, PrescriptionForm, 
    PrescriptionMedicineFormSet, PaymentForm, MedicalRecordForm
)


class CRMDashboardView(LoginRequiredMixin, TemplateView):
    """Main CRM Dashboard"""
    template_name = 'crm/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current user's doctor profile
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            context['doctor'] = doctor
            context['clinic'] = doctor.clinic
        except Doctor.DoesNotExist:
            context['doctor'] = None
            context['clinic'] = None
            return context
        
        # Dashboard Statistics
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        # Today's appointments
        context['today_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date=today,
            status__in=['scheduled', 'confirmed']
        ).order_by('scheduled_time')
        
        # This week's appointments
        context['week_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date__gte=week_start,
            scheduled_date__lte=today + timedelta(days=7)
        ).count()
        
        # This month's appointments
        context['month_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date__gte=month_start
        ).count()
        
        # Total patients
        context['total_patients'] = Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().count()
        
        # Recent appointments
        context['recent_appointments'] = Appointment.objects.filter(
            doctor=doctor
        ).order_by('-scheduled_date', '-scheduled_time')[:5]
        
        # Upcoming appointments
        context['upcoming_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date__gte=today,
            status__in=['scheduled', 'confirmed']
        ).order_by('scheduled_date', 'scheduled_time')[:5]
        
        # Recent patients
        context['recent_patients'] = Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().order_by('-created_at')[:5]
        
        # Revenue statistics
        context['today_revenue'] = Payment.objects.filter(
            appointment__doctor=doctor,
            payment_date__date=today,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context['month_revenue'] = Payment.objects.filter(
            appointment__doctor=doctor,
            payment_date__date__gte=month_start,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return context


class PatientListView(LoginRequiredMixin, ListView):
    """Patient list with search and filters"""
    model = Patient
    template_name = 'crm/patients.html'
    context_object_name = 'patients'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(patient_id__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    """Patient detail view with medical history"""
    model = Patient
    template_name = 'crm/patient_detail.html'
    context_object_name = 'patient'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        
        # Get patient's appointments
        context['appointments'] = Appointment.objects.filter(
            patient=patient
        ).order_by('-scheduled_date', '-scheduled_time')
        
        # Get patient's treatments
        context['treatments'] = Treatment.objects.filter(
            patient=patient
        ).order_by('-treatment_date')
        
        # Get patient's prescriptions
        context['prescriptions'] = Prescription.objects.filter(
            patient=patient
        ).order_by('-prescription_date')
        
        # Get patient's medical records
        context['medical_records'] = MedicalRecord.objects.filter(
            patient=patient
        ).order_by('-record_date')
        
        # Get patient's payments
        context['payments'] = Payment.objects.filter(
            patient=patient
        ).order_by('-payment_date')
        
        return context


class AppointmentListView(LoginRequiredMixin, ListView):
    """Appointment list with filters"""
    model = Appointment
    template_name = 'crm/appointments.html'
    context_object_name = 'appointments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Appointment.objects.all()
        
        # Filter by doctor if user is a doctor
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            pass
        
        # Filter by date
        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(scheduled_date=filter_date)
            except ValueError:
                pass
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-scheduled_date', '-scheduled_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = self.request.GET.get('date', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Appointment.STATUS_CHOICES
        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """Appointment detail view"""
    model = Appointment
    template_name = 'crm/appointment_detail.html'
    context_object_name = 'appointment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        
        # Get related treatments
        context['treatments'] = Treatment.objects.filter(
            appointment=appointment
        ).order_by('-treatment_date')
        
        # Get related payments
        context['payments'] = Payment.objects.filter(
            appointment=appointment
        ).order_by('-payment_date')
        
        return context


class TreatmentListView(LoginRequiredMixin, ListView):
    """Treatment list"""
    model = Treatment
    template_name = 'crm/treatments.html'
    context_object_name = 'treatments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Treatment.objects.all()
        
        # Filter by doctor if user is a doctor
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            pass
        
        # Filter by patient
        patient_id = self.request.GET.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-treatment_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_filter'] = self.request.GET.get('patient', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Treatment.STATUS_CHOICES
        return context


class TreatmentDetailView(LoginRequiredMixin, DetailView):
    """Treatment detail view"""
    model = Treatment
    template_name = 'crm/treatment_detail.html'
    context_object_name = 'treatment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treatment = self.get_object()
        
        # Get related prescriptions
        context['prescriptions'] = Prescription.objects.filter(
            treatment=treatment
        ).order_by('-prescription_date')
        
        # Get related payments
        context['payments'] = Payment.objects.filter(
            treatment=treatment
        ).order_by('-payment_date')
        
        return context


class PrescriptionListView(LoginRequiredMixin, ListView):
    """Prescription list"""
    model = Prescription
    template_name = 'crm/prescriptions.html'
    context_object_name = 'prescriptions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Prescription.objects.all()
        
        # Filter by doctor if user is a doctor
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            pass
        
        # Filter by patient
        patient_id = self.request.GET.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset.order_by('-prescription_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_filter'] = self.request.GET.get('patient', '')
        return context


class PrescriptionDetailView(LoginRequiredMixin, DetailView):
    """Prescription detail view"""
    model = Prescription
    template_name = 'crm/prescription_detail.html'
    context_object_name = 'prescription'


class PaymentListView(LoginRequiredMixin, ListView):
    """Payment list"""
    model = Payment
    template_name = 'crm/payments.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        
        # Filter by doctor if user is a doctor
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = queryset.filter(
                Q(appointment__doctor=doctor) | Q(treatment__doctor=doctor)
            )
        except Doctor.DoesNotExist:
            pass
        
        # Filter by payment status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(payment_status=status)
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(payment_date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(payment_date__date__lte=end_date)
        
        return queryset.order_by('-payment_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['status_choices'] = Payment.PAYMENT_STATUS_CHOICES
        return context


class MedicalRecordListView(LoginRequiredMixin, ListView):
    """Medical records list"""
    model = MedicalRecord
    template_name = 'crm/medical_records.html'
    context_object_name = 'medical_records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.all()
        
        # Filter by doctor if user is a doctor
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            pass
        
        # Filter by patient
        patient_id = self.request.GET.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by record type
        record_type = self.request.GET.get('record_type')
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        
        return queryset.order_by('-record_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_filter'] = self.request.GET.get('patient', '')
        context['record_type'] = self.request.GET.get('record_type', '')
        context['record_type_choices'] = MedicalRecord.RECORD_TYPE_CHOICES
        return context


# AJAX Views for dynamic content
@login_required
def get_patient_appointments(request, patient_id):
    """Get appointments for a specific patient"""
    appointments = Appointment.objects.filter(patient_id=patient_id).order_by('-scheduled_date')
    data = []
    for appointment in appointments:
        data.append({
            'id': appointment.id,
            'date': appointment.scheduled_date.strftime('%Y-%m-%d'),
            'time': appointment.scheduled_time.strftime('%H:%M'),
            'doctor': str(appointment.doctor),
            'status': appointment.get_status_display(),
            'reason': appointment.reason
        })
    return JsonResponse({'appointments': data})


@login_required
def get_patient_treatments(request, patient_id):
    """Get treatments for a specific patient"""
    treatments = Treatment.objects.filter(patient_id=patient_id).order_by('-treatment_date')
    data = []
    for treatment in treatments:
        data.append({
            'id': treatment.id,
            'name': treatment.name,
            'type': treatment.get_treatment_type_display(),
            'date': treatment.treatment_date.strftime('%Y-%m-%d'),
            'status': treatment.get_status_display(),
            'diagnosis': treatment.diagnosis
        })
    return JsonResponse({'treatments': data})


@login_required
def dashboard_stats(request):
    """Get dashboard statistics for AJAX requests"""
    try:
        doctor = Doctor.objects.get(user=request.user)
        today = timezone.now().date()
        
        # Today's appointments
        today_appointments = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date=today,
            status__in=['scheduled', 'confirmed']
        ).count()
        
        # This month's revenue
        month_start = today.replace(day=1)
        month_revenue = Payment.objects.filter(
            appointment__doctor=doctor,
            payment_date__date__gte=month_start,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Total patients
        total_patients = Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().count()
        
        return JsonResponse({
            'today_appointments': today_appointments,
            'month_revenue': float(month_revenue),
            'total_patients': total_patients
        })
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor profile not found'})


# Dynamic Form Views
class PatientCreateView(LoginRequiredMixin, CreateView):
    """Create new patient"""
    model = Patient
    form_class = PatientForm
    template_name = 'crm/patient_form.html'
    success_url = reverse_lazy('crm:patient_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Patient added successfully!')
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """Update patient information"""
    model = Patient
    form_class = PatientForm
    template_name = 'crm/patient_form.html'
    success_url = reverse_lazy('crm:patient_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Patient updated successfully!')
        return super().form_valid(form)


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """Schedule new appointment"""
    model = Appointment
    form_class = AppointmentForm
    template_name = 'crm/appointment_form.html'
    success_url = reverse_lazy('crm:appointment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            kwargs['doctor'] = doctor
        except Doctor.DoesNotExist:
            pass
        return kwargs
    
    def form_valid(self, form):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            form.instance.doctor = doctor
            form.instance.clinic = doctor.clinic
            form.instance.consultation_fee = doctor.consultation_fee
        except Doctor.DoesNotExist:
            pass
        
        messages.success(self.request, 'Appointment scheduled successfully!')
        return super().form_valid(form)


class TreatmentCreateView(LoginRequiredMixin, CreateView):
    """Add new treatment"""
    model = Treatment
    form_class = TreatmentForm
    template_name = 'crm/treatment_form.html'
    success_url = reverse_lazy('crm:treatment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            kwargs['doctor'] = doctor
        except Doctor.DoesNotExist:
            pass
        return kwargs
    
    def form_valid(self, form):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            form.instance.doctor = doctor
        except Doctor.DoesNotExist:
            pass
        
        messages.success(self.request, 'Treatment added successfully!')
        return super().form_valid(form)


class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    """Create new prescription"""
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'crm/prescription_form.html'
    success_url = reverse_lazy('crm:prescription_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            kwargs['doctor'] = doctor
        except Doctor.DoesNotExist:
            pass
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['medicine_formset'] = PrescriptionMedicineFormSet(self.request.POST)
        else:
            context['medicine_formset'] = PrescriptionMedicineFormSet()
        return context
    
    def form_valid(self, form):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            form.instance.doctor = doctor
        except Doctor.DoesNotExist:
            pass
        
        context = self.get_context_data()
        medicine_formset = context['medicine_formset']
        
        if medicine_formset.is_valid():
            response = super().form_valid(form)
            medicine_formset.instance = self.object
            medicine_formset.save()
            messages.success(self.request, 'Prescription created successfully!')
            return response
        else:
            return self.form_invalid(form)


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Record new payment"""
    model = Payment
    form_class = PaymentForm
    template_name = 'crm/payment_form.html'
    success_url = reverse_lazy('crm:payment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            kwargs['doctor'] = doctor
        except Doctor.DoesNotExist:
            pass
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Payment recorded successfully!')
        return super().form_valid(form)


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """Add new medical record"""
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'crm/medical_record_form.html'
    success_url = reverse_lazy('crm:medical_record_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            kwargs['doctor'] = doctor
        except Doctor.DoesNotExist:
            pass
        return kwargs
    
    def form_valid(self, form):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            form.instance.doctor = doctor
        except Doctor.DoesNotExist:
            pass
        
        messages.success(self.request, 'Medical record added successfully!')
        return super().form_valid(form)


# Quick action views
@login_required
def quick_prescription(request, patient_id):
    """Quick prescription for a specific patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, doctor=Doctor.objects.get(user=request.user))
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = Doctor.objects.get(user=request.user)
            prescription.save()
            messages.success(request, f'Prescription created for {patient.full_name}!')
            return redirect('crm:patient_detail', patient_id=patient.id)
    else:
        form = PrescriptionForm(initial={'patient': patient}, doctor=Doctor.objects.get(user=request.user))
    
    return render(request, 'crm/quick_prescription.html', {
        'form': form,
        'patient': patient
    })


@login_required
def quick_appointment(request, patient_id):
    """Quick appointment for a specific patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, doctor=Doctor.objects.get(user=request.user))
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = Doctor.objects.get(user=request.user)
            appointment.clinic = appointment.doctor.clinic
            appointment.consultation_fee = appointment.doctor.consultation_fee
            appointment.save()
            messages.success(request, f'Appointment scheduled for {patient.full_name}!')
            return redirect('crm:patient_detail', patient_id=patient.id)
    else:
        form = AppointmentForm(initial={'patient': patient}, doctor=Doctor.objects.get(user=request.user))
    
    return render(request, 'crm/quick_appointment.html', {
        'form': form,
        'patient': patient
    })