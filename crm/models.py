from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Clinic(models.Model):
    """Clinic information and settings"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Clinic Settings
    registration_number = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    established_date = models.DateField(blank=True, null=True)
    
    # Business Hours
    monday_start = models.TimeField(blank=True, null=True)
    monday_end = models.TimeField(blank=True, null=True)
    tuesday_start = models.TimeField(blank=True, null=True)
    tuesday_end = models.TimeField(blank=True, null=True)
    wednesday_start = models.TimeField(blank=True, null=True)
    wednesday_end = models.TimeField(blank=True, null=True)
    thursday_start = models.TimeField(blank=True, null=True)
    thursday_end = models.TimeField(blank=True, null=True)
    friday_start = models.TimeField(blank=True, null=True)
    friday_end = models.TimeField(blank=True, null=True)
    saturday_start = models.TimeField(blank=True, null=True)
    saturday_end = models.TimeField(blank=True, null=True)
    sunday_start = models.TimeField(blank=True, null=True)
    sunday_end = models.TimeField(blank=True, null=True)
    
    # Settings
    appointment_duration = models.PositiveIntegerField(default=30, help_text="Default appointment duration in minutes")
    advance_booking_days = models.PositiveIntegerField(default=30, help_text="How many days in advance can appointments be booked")
    cancellation_hours = models.PositiveIntegerField(default=24, help_text="Minimum hours before appointment for cancellation")
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Clinic"
        verbose_name_plural = "Clinics"
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Doctor profiles in the clinic"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], blank=True)
    
    # Professional Information
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    registration_number = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    
    # Profile
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    
    # Availability
    is_available = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Patient(models.Model):
    """Patient information and medical records"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Basic Information
    patient_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Contact Information
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    
    # Medical Information
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    height = models.PositiveIntegerField(blank=True, null=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    allergies = models.TextField(blank=True, help_text="Known allergies")
    medical_history = models.TextField(blank=True, help_text="Previous medical conditions")
    current_medications = models.TextField(blank=True, help_text="Current medications")
    
    # Insurance Information
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    insurance_validity = models.DateField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate unique patient ID
            import uuid
            self.patient_id = f"PAT{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class Appointment(models.Model):
    """Appointment scheduling and management"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow Up'),
        ('emergency', 'Emergency'),
        ('checkup', 'Regular Checkup'),
        ('procedure', 'Procedure'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    appointment_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='appointments')
    
    # Appointment Details
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    
    # Status and Notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(help_text="Reason for appointment")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    # Fees
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['-scheduled_date', '-scheduled_time']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name} ({self.scheduled_date})"
    
    def save(self, *args, **kwargs):
        if not self.appointment_id:
            import uuid
            self.appointment_id = f"APT{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Treatment(models.Model):
    """Treatment records and medical procedures"""
    TREATMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure'),
        ('surgery', 'Surgery'),
        ('therapy', 'Therapy'),
        ('medication', 'Medication'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    treatment_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='treatments')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='treatments', blank=True, null=True)
    
    # Treatment Details
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    diagnosis = models.TextField(help_text="Medical diagnosis")
    symptoms = models.TextField(blank=True, help_text="Patient symptoms")
    
    # Treatment Plan
    treatment_plan = models.TextField(help_text="Treatment plan and procedures")
    medications_prescribed = models.TextField(blank=True, help_text="Prescribed medications")
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    follow_up_notes = models.TextField(blank=True)
    
    # Fees
    treatment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='ongoing')
    
    # Timestamps
    treatment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Treatment"
        verbose_name_plural = "Treatments"
        ordering = ['-treatment_date']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.treatment_id:
            import uuid
            self.treatment_id = f"TRT{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Prescription(models.Model):
    """Prescription management"""
    prescription_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='prescriptions', blank=True, null=True)
    
    # Prescription Details
    prescription_date = models.DateTimeField(default=timezone.now)
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField()
    instructions = models.TextField(help_text="Instructions for patient")
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
        ordering = ['-prescription_date']
    
    def __str__(self):
        return f"Prescription for {self.patient.full_name} - {self.prescription_date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        if not self.prescription_id:
            import uuid
            self.prescription_id = f"PRS{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class PrescriptionMedicine(models.Model):
    """Individual medicines in prescriptions"""
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 1 tablet")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice daily, After meals")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days, 2 weeks")
    quantity = models.PositiveIntegerField(default=1)
    instructions = models.TextField(blank=True, help_text="Special instructions")
    
    class Meta:
        verbose_name = "Prescription Medicine"
        verbose_name_plural = "Prescription Medicines"
    
    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"


class Payment(models.Model):
    """Payment records"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Basic Information
    payment_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='payments', blank=True, null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='payments', blank=True, null=True)
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.payment_id} - ₹{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            import uuid
            self.payment_id = f"PAY{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class MedicalRecord(models.Model):
    """Comprehensive medical records"""
    record_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    
    # Record Details
    record_type = models.CharField(max_length=50, choices=[
        ('vital_signs', 'Vital Signs'),
        ('lab_report', 'Lab Report'),
        ('scan_report', 'Scan Report'),
        ('xray_report', 'X-Ray Report'),
        ('prescription', 'Prescription'),
        ('treatment_notes', 'Treatment Notes'),
        ('other', 'Other'),
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # File Attachments
    file_attachment = models.FileField(upload_to='medical_records/', blank=True, null=True)
    
    # Status
    is_important = models.BooleanField(default=False)
    is_confidential = models.BooleanField(default=False)
    
    # Timestamps
    record_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.record_id:
            import uuid
            self.record_id = f"REC{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)