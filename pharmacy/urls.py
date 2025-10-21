from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Medicine Management
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('api/medicine/<int:medicine_id>/', views.get_medicine_details, name='get_medicine_details'),
    
    # Customer Management
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('api/customers/search/', views.search_customers, name='search_customers'),
    
    # Billing System
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.create_bill, name='create_bill'),
    path('bills/<int:pk>/', views.bill_detail, name='bill_detail'),
    path('bills/<int:bill_id>/payment/', views.add_payment, name='add_payment'),
    
    # Prescription Management
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    
    # Stock Management
    path('stock-movements/', views.stock_movement_list, name='stock_movement_list'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]
