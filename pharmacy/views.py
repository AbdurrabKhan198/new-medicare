from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count, F
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import transaction, models
from decimal import Decimal
import json
from datetime import datetime, timedelta

from .models import (
    Medicine, MedicineCategory, Customer, Prescription, PrescriptionItem,
    Bill, BillItem, Payment, StockMovement, Supplier, PurchaseOrder, PurchaseOrderItem
)
from .forms import (
    CustomerForm, PrescriptionForm, BillForm, PaymentForm,
    MedicineForm, StockMovementForm
)


@login_required
def dashboard(request):
    """Pharmacy dashboard with key metrics"""
    # Get current date
    today = timezone.now().date()
    
    # Dashboard metrics
    total_customers = Customer.objects.filter(is_active=True).count()
    total_medicines = Medicine.objects.filter(is_active=True).count()
    low_stock_medicines = Medicine.objects.filter(is_active=True, stock_quantity__lte=F('minimum_stock')).count()
    
    # Today's sales
    today_sales = Bill.objects.filter(
        bill_date__date=today,
        payment_status__in=['paid', 'partial']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Today's bills
    today_bills = Bill.objects.filter(bill_date__date=today).count()
    
    # Recent bills
    recent_bills = Bill.objects.select_related('customer').order_by('-bill_date')[:10]
    
    # Low stock medicines
    low_stock_items = Medicine.objects.filter(
        is_active=True,
        stock_quantity__lte=models.F('minimum_stock')
    ).order_by('stock_quantity')[:10]
    
    # Recent prescriptions
    recent_prescriptions = Prescription.objects.select_related('customer').order_by('-prescription_date')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_medicines': total_medicines,
        'low_stock_medicines': low_stock_medicines,
        'today_sales': today_sales,
        'today_bills': today_bills,
        'recent_bills': recent_bills,
        'low_stock_items': low_stock_items,
        'recent_prescriptions': recent_prescriptions,
    }
    
    return render(request, 'pharmacy/dashboard.html', context)


@login_required
def medicine_list(request):
    """List all medicines with search and filter"""
    medicines = Medicine.objects.filter(is_active=True).select_related('category')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(generic_name__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(medicine_code__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        medicines = medicines.filter(category_id=category_id)
    
    # Filter by stock status
    stock_filter = request.GET.get('stock')
    if stock_filter == 'low':
        medicines = medicines.filter(stock_quantity__lte=F('minimum_stock'))
    elif stock_filter == 'out':
        medicines = medicines.filter(stock_quantity=0)
    
    # Pagination
    paginator = Paginator(medicines, 20)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = MedicineCategory.objects.filter(is_active=True)
    
    context = {
        'medicines': medicines,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_stock': stock_filter,
    }
    
    return render(request, 'pharmacy/medicine_list.html', context)


@login_required
def medicine_detail(request, pk):
    """Medicine detail view"""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    # Get recent stock movements
    stock_movements = StockMovement.objects.filter(medicine=medicine).order_by('-movement_date')[:10]
    
    # Get recent bills containing this medicine
    recent_bills = BillItem.objects.filter(medicine=medicine).select_related('bill__customer').order_by('-bill__bill_date')[:5]
    
    context = {
        'medicine': medicine,
        'stock_movements': stock_movements,
        'recent_bills': recent_bills,
    }
    
    return render(request, 'pharmacy/medicine_detail.html', context)


@login_required
def customer_list(request):
    """List all customers with search"""
    customers = Customer.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(customer_id__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    
    context = {
        'customers': customers,
        'search_query': search_query,
    }
    
    return render(request, 'pharmacy/customer_list.html', context)


@login_required
def customer_detail(request, pk):
    """Customer detail view"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # Get customer's recent bills
    recent_bills = Bill.objects.filter(customer=customer).order_by('-bill_date')[:10]
    
    # Get customer's prescriptions
    prescriptions = Prescription.objects.filter(customer=customer).order_by('-prescription_date')[:10]
    
    # Get total spent
    total_spent = Bill.objects.filter(
        customer=customer,
        payment_status__in=['paid', 'partial']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'customer': customer,
        'recent_bills': recent_bills,
        'prescriptions': prescriptions,
        'total_spent': total_spent,
    }
    
    return render(request, 'pharmacy/customer_detail.html', context)


@login_required
def create_bill(request):
    """Create a new bill"""
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.created_by = request.user
            bill.save()
            
            # Add bill items from JSON data
            items_data = request.POST.get('items', '[]')
            items = json.loads(items_data)
            
            for item in items:
                medicine = Medicine.objects.get(pk=item['medicine_id'])
                BillItem.objects.create(
                    bill=bill,
                    medicine=medicine,
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    batch_number=item.get('batch_number', ''),
                    expiry_date=item.get('expiry_date') or None
                )
                
                # Update stock
                medicine.stock_quantity -= item['quantity']
                medicine.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    medicine=medicine,
                    movement_type='out',
                    quantity=-item['quantity'],
                    previous_stock=medicine.stock_quantity + item['quantity'],
                    new_stock=medicine.stock_quantity,
                    reference_number=bill.bill_id,
                    created_by=request.user
                )
            
            messages.success(request, f'Bill {bill.bill_id} created successfully!')
            return redirect('pharmacy:bill_detail', pk=bill.pk)
    else:
        form = BillForm()
    
    # Get medicines for autocomplete
    medicines = Medicine.objects.filter(is_active=True, stock_quantity__gt=0)
    
    context = {
        'form': form,
        'medicines': medicines,
    }
    
    return render(request, 'pharmacy/create_bill.html', context)


@login_required
def bill_list(request):
    """List all bills with search and filter"""
    bills = Bill.objects.select_related('customer', 'created_by').order_by('-bill_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        bills = bills.filter(
            Q(bill_id__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(customer__phone__icontains=search_query)
        )
    
    # Filter by payment status
    status_filter = request.GET.get('status')
    if status_filter:
        bills = bills.filter(payment_status=status_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        bills = bills.filter(bill_date__date__gte=date_from)
    if date_to:
        bills = bills.filter(bill_date__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(bills, 20)
    page_number = request.GET.get('page')
    bills = paginator.get_page(page_number)
    
    context = {
        'bills': bills,
        'search_query': search_query,
        'selected_status': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'pharmacy/bill_list.html', context)


@login_required
def bill_detail(request, pk):
    """Bill detail view"""
    bill = get_object_or_404(Bill, pk=pk)
    bill_items = BillItem.objects.filter(bill=bill).select_related('medicine')
    payments = Payment.objects.filter(bill=bill).order_by('-payment_date')
    
    context = {
        'bill': bill,
        'bill_items': bill_items,
        'payments': payments,
    }
    
    return render(request, 'pharmacy/bill_detail.html', context)


@login_required
def add_payment(request, bill_id):
    """Add payment to a bill"""
    bill = get_object_or_404(Bill, pk=bill_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.customer = bill.customer
            payment.created_by = request.user
            payment.save()
            
            # Update bill payment status
            bill.paid_amount += payment.amount
            if bill.paid_amount >= bill.total_amount:
                bill.payment_status = 'paid'
                bill.paid_at = timezone.now()
            elif bill.paid_amount > 0:
                bill.payment_status = 'partial'
            bill.save()
            
            messages.success(request, f'Payment of ₹{payment.amount} added successfully!')
            return redirect('pharmacy:bill_detail', pk=bill.pk)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'bill': bill,
    }
    
    return render(request, 'pharmacy/add_payment.html', context)


@login_required
def prescription_list(request):
    """List all prescriptions"""
    prescriptions = Prescription.objects.select_related('customer').order_by('-prescription_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        prescriptions = prescriptions.filter(
            Q(prescription_id__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(doctor_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(prescriptions, 20)
    page_number = request.GET.get('page')
    prescriptions = paginator.get_page(page_number)
    
    context = {
        'prescriptions': prescriptions,
        'search_query': search_query,
        'selected_status': status_filter,
    }
    
    return render(request, 'pharmacy/prescription_list.html', context)


@login_required
def prescription_detail(request, pk):
    """Prescription detail view"""
    prescription = get_object_or_404(Prescription, pk=pk)
    prescription_items = PrescriptionItem.objects.filter(prescription=prescription).select_related('medicine')
    
    context = {
        'prescription': prescription,
        'prescription_items': prescription_items,
    }
    
    return render(request, 'pharmacy/prescription_detail.html', context)


@login_required
def stock_movement_list(request):
    """List all stock movements"""
    movements = StockMovement.objects.select_related('medicine', 'created_by').order_by('-movement_date')
    
    # Filter by medicine
    medicine_id = request.GET.get('medicine')
    if medicine_id:
        movements = movements.filter(medicine_id=medicine_id)
    
    # Filter by movement type
    movement_type = request.GET.get('type')
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        movements = movements.filter(movement_date__date__gte=date_from)
    if date_to:
        movements = movements.filter(movement_date__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(movements, 50)
    page_number = request.GET.get('page')
    movements = paginator.get_page(page_number)
    
    # Get medicines for filter
    medicines = Medicine.objects.filter(is_active=True).order_by('name')
    
    context = {
        'movements': movements,
        'medicines': medicines,
        'selected_medicine': medicine_id,
        'selected_type': movement_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'pharmacy/stock_movement_list.html', context)


@login_required
def reports(request):
    """Pharmacy reports"""
    # Date range for reports
    date_from = request.GET.get('date_from', (timezone.now().date() - timedelta(days=30)).strftime('%Y-%m-%d'))
    date_to = request.GET.get('date_to', timezone.now().date().strftime('%Y-%m-%d'))
    
    # Sales report
    sales_data = Bill.objects.filter(
        bill_date__date__range=[date_from, date_to],
        payment_status__in=['paid', 'partial']
    ).aggregate(
        total_sales=Sum('total_amount'),
        total_bills=Count('id')
    )
    
    # Top selling medicines
    top_medicines = BillItem.objects.filter(
        bill__bill_date__date__range=[date_from, date_to]
    ).values('medicine__name').annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum('total_price')
    ).order_by('-total_quantity')[:10]
    
    # Customer statistics
    customer_stats = Customer.objects.filter(
        bills__bill_date__date__range=[date_from, date_to]
    ).aggregate(
        total_customers=Count('id', distinct=True)
    )
    
    context = {
        'date_from': date_from,
        'date_to': date_to,
        'sales_data': sales_data,
        'top_medicines': top_medicines,
        'customer_stats': customer_stats,
    }
    
    return render(request, 'pharmacy/reports.html', context)


# API Views for AJAX requests
@login_required
def get_medicine_details(request, medicine_id):
    """Get medicine details for AJAX requests"""
    try:
        medicine = Medicine.objects.get(pk=medicine_id)
        data = {
            'name': medicine.name,
            'selling_price': float(medicine.selling_price),
            'stock_quantity': medicine.stock_quantity,
            'unit': medicine.unit,
            'strength': medicine.strength,
        }
        return JsonResponse(data)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)


@login_required
def search_customers(request):
    """Search customers for AJAX requests"""
    query = request.GET.get('q', '')
    customers = Customer.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(phone__icontains=query) |
        Q(customer_id__icontains=query)
    ).filter(is_active=True)[:10]
    
    data = []
    for customer in customers:
        data.append({
            'id': customer.id,
            'customer_id': customer.customer_id,
            'name': customer.full_name,
            'phone': customer.phone,
        })
    
    return JsonResponse(data, safe=False)