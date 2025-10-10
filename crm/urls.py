from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Dashboard
    path('', views.CRMDashboardView.as_view(), name='dashboard'),
    
    # Patients
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/add/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    
    # Appointments
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/add/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('patients/<int:patient_id>/appointment/', views.quick_appointment, name='quick_appointment'),
    
    # Treatments
    path('treatments/', views.TreatmentListView.as_view(), name='treatment_list'),
    path('treatments/<int:pk>/', views.TreatmentDetailView.as_view(), name='treatment_detail'),
    path('treatments/add/', views.TreatmentCreateView.as_view(), name='treatment_create'),
    
    # Prescriptions
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/add/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('patients/<int:patient_id>/prescription/', views.quick_prescription, name='quick_prescription'),
    
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.PaymentCreateView.as_view(), name='payment_create'),
    
    # Medical Records
    path('medical-records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('medical-records/add/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    
    # AJAX endpoints
    path('api/patient/<int:patient_id>/appointments/', views.get_patient_appointments, name='patient_appointments'),
    path('api/patient/<int:patient_id>/treatments/', views.get_patient_treatments, name='patient_treatments'),
    path('api/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
]
