from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctor/<int:doctor_id>/book/', views.PublicAppointmentView.as_view(), name='book_appointment'),
    path('doctor/<int:doctor_id>/slots/', views.get_available_slots, name='available_slots'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),
]
