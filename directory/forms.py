from django import forms
from crm.models import Patient, Appointment


class PublicAppointmentForm(forms.Form):
    # Patient details
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)

    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)

    # Appointment details
    appointment_type = forms.ChoiceField(choices=Appointment.APPOINTMENT_TYPE_CHOICES)
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    scheduled_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    reason = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            base = 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent'
            if isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs.setdefault('class', base)
            else:
                field.widget.attrs.setdefault('class', base)
