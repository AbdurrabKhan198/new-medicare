from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta, time as dtime, date as ddate

from crm.models import Doctor, Clinic, Patient, Appointment
from .forms import PublicAppointmentForm


class DoctorListView(ListView):
    model = Doctor
    template_name = 'directory/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 12

    def get_queryset(self):
        qs = Doctor.objects.select_related('clinic').filter(is_active=True)
        q = self.request.GET.get('q', '').strip()
        specialization = self.request.GET.get('specialization', '').strip()
        city = self.request.GET.get('city', '').strip()

        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(specialization__icontains=q)
            )
        if specialization:
            qs = qs.filter(specialization__icontains=specialization)
        if city:
            qs = qs.filter(clinic__city__icontains=city)
        return qs.order_by('first_name', 'last_name')


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'directory/doctor_detail.html'
    context_object_name = 'doctor'


class PublicAppointmentView(FormView):
    template_name = 'directory/book_appointment.html'
    form_class = PublicAppointmentForm

    def dispatch(self, request, *args, **kwargs):
        self.doctor = get_object_or_404(Doctor, id=kwargs.get('doctor_id'), is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['doctor'] = self.doctor
        return ctx

    def form_valid(self, form):
        # Validate selected time does not conflict with existing appointments
        selected_date = form.cleaned_data['scheduled_date']
        selected_time = form.cleaned_data['scheduled_time']
        clinic = self.doctor.clinic
        duration = clinic.appointment_duration if clinic else 30

        if has_conflict(self.doctor, selected_date, selected_time, duration):
            form.add_error('scheduled_time', 'Selected time is no longer available. Please choose another slot.')
            return self.form_invalid(form)

        # Find or create patient by phone (and optional email)
        phone = form.cleaned_data['phone']
        email = form.cleaned_data.get('email')
        patient = Patient.objects.filter(phone=phone).first()
        if not patient and email:
            patient = Patient.objects.filter(email=email).first()
        if not patient:
            patient = Patient.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                phone=phone,
                email=email or '',
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )

        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=self.doctor,
            clinic=clinic,
            appointment_type=form.cleaned_data['appointment_type'],
            scheduled_date=form.cleaned_data['scheduled_date'],
            scheduled_time=form.cleaned_data['scheduled_time'],
            duration=duration,
            status='scheduled',
            reason=form.cleaned_data['reason'],
            consultation_fee=self.doctor.consultation_fee,
        )

        messages.success(self.request, 'Your appointment request has been submitted successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('directory:booking_success')


class BookingSuccessView(TemplateView):
    template_name = 'directory/booking_success.html'


def has_conflict(doctor, scheduled_date, scheduled_time, duration_minutes):
    """Return True if the proposed slot overlaps any existing appointment for doctor."""
    # Consider only active statuses that reserve time
    active_statuses = ['scheduled', 'confirmed', 'in_progress']
    start_dt = datetime.combine(scheduled_date, scheduled_time)
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    existing = Appointment.objects.filter(
        doctor=doctor,
        scheduled_date=scheduled_date,
        status__in=active_statuses,
    )

    for appt in existing:
        appt_start = datetime.combine(appt.scheduled_date, appt.scheduled_time)
        appt_end = appt_start + timedelta(minutes=appt.duration or duration_minutes)
        # Overlap if start < other_end and end > other_start
        if start_dt < appt_end and end_dt > appt_start:
            return True
    return False


def get_available_slots(request, doctor_id):
    """Return JSON of available time slots for a doctor on a given date."""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    clinic = doctor.clinic
    date_str = request.GET.get('date')
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else ddate.today()
    except ValueError:
        return JsonResponse({'slots': []})

    # Map weekday to clinic hours fields
    weekday = target_date.weekday()  # Monday=0
    day_map = [
        ('monday_start', 'monday_end'),
        ('tuesday_start', 'tuesday_end'),
        ('wednesday_start', 'wednesday_end'),
        ('thursday_start', 'thursday_end'),
        ('friday_start', 'friday_end'),
        ('saturday_start', 'saturday_end'),
        ('sunday_start', 'sunday_end'),
    ]
    start_field, end_field = day_map[weekday]
    start_time = getattr(clinic, start_field)
    end_time = getattr(clinic, end_field)
    if not (start_time and end_time):
        return JsonResponse({'slots': []})

    duration = clinic.appointment_duration or 30
    slots = []
    cursor = datetime.combine(target_date, start_time)
    end_dt = datetime.combine(target_date, end_time)

    # If date is today, avoid past times
    now = datetime.now()
    if target_date == now.date() and cursor < now:
        cursor = (now + timedelta(minutes=5)).replace(second=0, microsecond=0)

    while cursor + timedelta(minutes=duration) <= end_dt:
        t = cursor.time()
        if not has_conflict(doctor, target_date, t, duration):
            slots.append(t.strftime('%H:%M'))
        cursor += timedelta(minutes=duration)

    return JsonResponse({'slots': slots})
