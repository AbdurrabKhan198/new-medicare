from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Clinic, Doctor, Patient, Appointment, Treatment, 
    Prescription, PrescriptionMedicine, Payment, MedicalRecord
)


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'state', 'created_at']
    search_fields = ['name', 'phone', 'email', 'city']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'city', 'state', 'pincode')
        }),
        ('Clinic Details', {
            'fields': ('registration_number', 'license_number', 'established_date')
        }),
        ('Business Hours', {
            'fields': (
                ('monday_start', 'monday_end'),
                ('tuesday_start', 'tuesday_end'),
                ('wednesday_start', 'wednesday_end'),
                ('thursday_start', 'thursday_end'),
                ('friday_start', 'friday_end'),
                ('saturday_start', 'saturday_end'),
                ('sunday_start', 'sunday_end'),
            ),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('appointment_duration', 'advance_booking_days', 'cancellation_hours', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'clinic', 'phone', 'is_available', 'is_active']
    list_filter = ['is_active', 'is_available', 'specialization', 'clinic', 'gender']
    search_fields = ['first_name', 'last_name', 'specialization', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'clinic')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'qualification', 'experience_years', 'registration_number', 'license_number')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'emergency_contact')
        }),
        ('Profile', {
            'fields': ('bio', 'profile_picture')
        }),
        ('Availability & Fees', {
            'fields': ('is_available', 'consultation_fee')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'phone', 'age', 'gender', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'gender', 'blood_group', 'city', 'state', 'created_at']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'email', 'city']
    readonly_fields = ['patient_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_id', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'city', 'state', 'pincode')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Medical Information', {
            'fields': ('blood_group', 'height', 'weight', 'allergies', 'medical_history', 'current_medications')
        }),
        ('Insurance Information', {
            'fields': ('insurance_provider', 'insurance_number', 'insurance_validity')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'patient', 'doctor', 'prescription_date', 'created_at']
    list_filter = ['prescription_date', 'created_at']
    search_fields = ['prescription_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    readonly_fields = ['prescription_id', 'created_at', 'updated_at']
    inlines = [PrescriptionMedicineInline]
    fieldsets = (
        ('Prescription Information', {
            'fields': ('prescription_id', 'patient', 'doctor', 'treatment', 'prescription_date')
        }),
        ('Medical Details', {
            'fields': ('symptoms', 'diagnosis', 'instructions')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient', 'doctor', 'scheduled_date', 'scheduled_time', 'status', 'payment_status']
    list_filter = ['status', 'appointment_type', 'payment_status', 'scheduled_date', 'created_at']
    search_fields = ['appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    readonly_fields = ['appointment_id', 'created_at', 'updated_at', 'confirmed_at', 'completed_at', 'cancelled_at']
    fieldsets = (
        ('Appointment Information', {
            'fields': ('appointment_id', 'patient', 'doctor', 'clinic', 'appointment_type')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'scheduled_time', 'duration')
        }),
        ('Details', {
            'fields': ('status', 'reason', 'notes')
        }),
        ('Fees', {
            'fields': ('consultation_fee', 'paid_amount', 'payment_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['treatment_id', 'patient', 'doctor', 'name', 'treatment_type', 'status', 'treatment_date']
    list_filter = ['treatment_type', 'status', 'treatment_date', 'created_at']
    search_fields = ['treatment_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'name']
    readonly_fields = ['treatment_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Treatment Information', {
            'fields': ('treatment_id', 'patient', 'doctor', 'appointment', 'treatment_type', 'name')
        }),
        ('Medical Details', {
            'fields': ('description', 'diagnosis', 'symptoms', 'treatment_plan')
        }),
        ('Prescription & Follow-up', {
            'fields': ('medications_prescribed', 'follow_up_required', 'follow_up_date', 'follow_up_notes')
        }),
        ('Fees', {
            'fields': ('treatment_fee', 'paid_amount')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('treatment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'patient', 'amount', 'payment_method', 'payment_status', 'payment_date']
    list_filter = ['payment_method', 'payment_status', 'payment_date', 'created_at']
    search_fields = ['payment_id', 'patient__first_name', 'patient__last_name', 'transaction_id']
    readonly_fields = ['payment_id', 'created_at']
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'patient', 'appointment', 'treatment')
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_method', 'payment_status', 'transaction_id')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'patient', 'doctor', 'title', 'record_type', 'is_important', 'record_date']
    list_filter = ['record_type', 'is_important', 'is_confidential', 'record_date', 'created_at']
    search_fields = ['record_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'title']
    readonly_fields = ['record_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Record Information', {
            'fields': ('record_id', 'patient', 'doctor', 'record_type', 'title')
        }),
        ('Content', {
            'fields': ('description', 'file_attachment')
        }),
        ('Settings', {
            'fields': ('is_important', 'is_confidential')
        }),
        ('Timestamps', {
            'fields': ('record_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site
admin.site.site_header = "Mediwell Care CRM"
admin.site.site_title = "Mediwell CRM"
admin.site.index_title = "Clinic Relationship Management"