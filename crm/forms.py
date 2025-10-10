from django import forms
from django.contrib.auth.models import User
from .models import Patient, Appointment, Treatment, Prescription, PrescriptionMedicine, Payment, MedicalRecord


class PatientForm(forms.ModelForm):
    """Form for adding/editing patients"""
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender',
            'phone', 'email', 'address', 'city', 'state', 'pincode',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'blood_group', 'height', 'weight', 'allergies', 'medical_history', 'current_medications',
            'insurance_provider', 'insurance_number', 'insurance_validity'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'insurance_validity': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'medical_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'current_medications': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class AppointmentForm(forms.ModelForm):
    """Form for scheduling appointments"""
    class Meta:
        model = Appointment
        fields = [
            'patient', 'appointment_type', 'scheduled_date', 'scheduled_time', 
            'duration', 'reason', 'notes', 'consultation_fee'
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if doctor:
            # Filter patients who have appointments with this doctor
            self.fields['patient'].queryset = Patient.objects.filter(
                appointments__doctor=doctor
            ).distinct()
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class TreatmentForm(forms.ModelForm):
    """Form for adding treatments"""
    class Meta:
        model = Treatment
        fields = [
            'patient', 'treatment_type', 'name', 'description', 'diagnosis', 
            'symptoms', 'treatment_plan', 'medications_prescribed', 
            'follow_up_required', 'follow_up_date', 'follow_up_notes', 'treatment_fee'
        ]
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'diagnosis': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'symptoms': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'medications_prescribed': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if doctor:
            self.fields['patient'].queryset = Patient.objects.filter(
                appointments__doctor=doctor
            ).distinct()
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class PrescriptionForm(forms.ModelForm):
    """Form for creating prescriptions"""
    class Meta:
        model = Prescription
        fields = ['patient', 'symptoms', 'diagnosis', 'instructions']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'instructions': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if doctor:
            self.fields['patient'].queryset = Patient.objects.filter(
                appointments__doctor=doctor
            ).distinct()
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class PrescriptionMedicineForm(forms.ModelForm):
    """Form for adding medicines to prescriptions"""
    class Meta:
        model = PrescriptionMedicine
        fields = ['medicine_name', 'dosage', 'frequency', 'duration', 'quantity', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class PaymentForm(forms.ModelForm):
    """Form for recording payments"""
    class Meta:
        model = Payment
        fields = ['patient', 'appointment', 'amount', 'payment_method', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if doctor:
            self.fields['patient'].queryset = Patient.objects.filter(
                appointments__doctor=doctor
            ).distinct()
            self.fields['appointment'].queryset = Appointment.objects.filter(
                doctor=doctor
            )
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            })


class MedicalRecordForm(forms.ModelForm):
    """Form for adding medical records"""
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'record_type', 'title', 'description', 'file_attachment', 'is_important', 'is_confidential']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if doctor:
            self.fields['patient'].queryset = Patient.objects.filter(
                appointments__doctor=doctor
            ).distinct()
        
        for field in self.fields:
            if field != 'is_important' and field != 'is_confidential':
                self.fields[field].widget.attrs.update({
                    'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
                })


# Inline formset for prescription medicines
PrescriptionMedicineFormSet = forms.inlineformset_factory(
    Prescription, 
    PrescriptionMedicine, 
    form=PrescriptionMedicineForm,
    extra=1,
    can_delete=True
)
