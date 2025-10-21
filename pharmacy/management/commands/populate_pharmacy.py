from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pharmacy.models import (
    MedicineCategory, Medicine, Customer, Supplier, Prescription, PrescriptionItem,
    Bill, BillItem, Payment, StockMovement, PurchaseOrder, PurchaseOrderItem
)
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate the pharmacy with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate pharmacy with sample data...')
        
        # Create medicine categories
        self.create_medicine_categories()
        
        # Create medicines
        self.create_medicines()
        
        # Create customers
        self.create_customers()
        
        # Create suppliers
        self.create_suppliers()
        
        # Create stock movements
        self.create_stock_movements()
        
        # Create prescriptions
        self.create_prescriptions()
        
        # Create bills
        self.create_bills()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated pharmacy with sample data!'))

    def create_medicine_categories(self):
        if not MedicineCategory.objects.exists():
            categories = [
                {'name': 'Antibiotics', 'slug': 'antibiotics', 'description': 'Antibacterial medications'},
                {'name': 'Pain Relief', 'slug': 'pain-relief', 'description': 'Pain management medications'},
                {'name': 'Cardiovascular', 'slug': 'cardiovascular', 'description': 'Heart and blood vessel medications'},
                {'name': 'Diabetes', 'slug': 'diabetes', 'description': 'Diabetes management medications'},
                {'name': 'Respiratory', 'slug': 'respiratory', 'description': 'Lung and breathing medications'},
                {'name': 'Gastrointestinal', 'slug': 'gastrointestinal', 'description': 'Digestive system medications'},
                {'name': 'Vitamins', 'slug': 'vitamins', 'description': 'Vitamin and mineral supplements'},
                {'name': 'Dermatology', 'slug': 'dermatology', 'description': 'Skin care medications'},
            ]
            
            for cat in categories:
                MedicineCategory.objects.create(**cat)
            self.stdout.write('Created medicine categories')

    def create_medicines(self):
        if not Medicine.objects.exists():
            categories = MedicineCategory.objects.all()
            
            medicines = [
                {
                    'name': 'Paracetamol 500mg',
                    'generic_name': 'Acetaminophen',
                    'manufacturer': 'Sun Pharma',
                    'category': categories[1],  # Pain Relief
                    'unit': 'tablet',
                    'strength': '500mg',
                    'description': 'Pain relief and fever reducer',
                    'stock_quantity': 1000,
                    'minimum_stock': 100,
                    'maximum_stock': 2000,
                    'cost_price': 0.50,
                    'selling_price': 1.00,
                    'requires_prescription': False,
                },
                {
                    'name': 'Amoxicillin 250mg',
                    'generic_name': 'Amoxicillin',
                    'manufacturer': 'Cipla',
                    'category': categories[0],  # Antibiotics
                    'unit': 'capsule',
                    'strength': '250mg',
                    'description': 'Antibiotic for bacterial infections',
                    'stock_quantity': 500,
                    'minimum_stock': 50,
                    'maximum_stock': 1000,
                    'cost_price': 2.00,
                    'selling_price': 4.00,
                    'requires_prescription': True,
                },
                {
                    'name': 'Metformin 500mg',
                    'generic_name': 'Metformin',
                    'manufacturer': 'Dr. Reddy\'s',
                    'category': categories[3],  # Diabetes
                    'unit': 'tablet',
                    'strength': '500mg',
                    'description': 'Diabetes medication',
                    'stock_quantity': 300,
                    'minimum_stock': 50,
                    'maximum_stock': 500,
                    'cost_price': 1.50,
                    'selling_price': 3.00,
                    'requires_prescription': True,
                },
                {
                    'name': 'Amlodipine 5mg',
                    'generic_name': 'Amlodipine',
                    'manufacturer': 'Lupin',
                    'category': categories[2],  # Cardiovascular
                    'unit': 'tablet',
                    'strength': '5mg',
                    'description': 'Blood pressure medication',
                    'stock_quantity': 400,
                    'minimum_stock': 50,
                    'maximum_stock': 800,
                    'cost_price': 2.50,
                    'selling_price': 5.00,
                    'requires_prescription': True,
                },
                {
                    'name': 'Vitamin D3 1000 IU',
                    'generic_name': 'Cholecalciferol',
                    'manufacturer': 'Himalaya',
                    'category': categories[6],  # Vitamins
                    'unit': 'tablet',
                    'strength': '1000 IU',
                    'description': 'Vitamin D supplement',
                    'stock_quantity': 200,
                    'minimum_stock': 25,
                    'maximum_stock': 500,
                    'cost_price': 1.00,
                    'selling_price': 2.50,
                    'requires_prescription': False,
                },
                {
                    'name': 'Salbutamol Inhaler',
                    'generic_name': 'Salbutamol',
                    'manufacturer': 'GSK',
                    'category': categories[4],  # Respiratory
                    'unit': 'inhaler',
                    'strength': '100mcg',
                    'description': 'Bronchodilator for asthma',
                    'stock_quantity': 50,
                    'minimum_stock': 10,
                    'maximum_stock': 100,
                    'cost_price': 50.00,
                    'selling_price': 100.00,
                    'requires_prescription': True,
                },
                {
                    'name': 'Omeprazole 20mg',
                    'generic_name': 'Omeprazole',
                    'manufacturer': 'Torrent',
                    'category': categories[5],  # Gastrointestinal
                    'unit': 'capsule',
                    'strength': '20mg',
                    'description': 'Acid reflux medication',
                    'stock_quantity': 250,
                    'minimum_stock': 25,
                    'maximum_stock': 500,
                    'cost_price': 1.80,
                    'selling_price': 3.60,
                    'requires_prescription': True,
                },
                {
                    'name': 'Cetirizine 10mg',
                    'generic_name': 'Cetirizine',
                    'manufacturer': 'Zydus',
                    'category': categories[7],  # Dermatology
                    'unit': 'tablet',
                    'strength': '10mg',
                    'description': 'Antihistamine for allergies',
                    'stock_quantity': 150,
                    'minimum_stock': 20,
                    'maximum_stock': 300,
                    'cost_price': 0.80,
                    'selling_price': 1.60,
                    'requires_prescription': False,
                },
            ]
            
            for medicine in medicines:
                Medicine.objects.create(**medicine)
            self.stdout.write('Created medicines')

    def create_customers(self):
        if not Customer.objects.exists():
            customers = [
                {
                    'first_name': 'Rajesh',
                    'last_name': 'Kumar',
                    'phone': '9876543210',
                    'email': 'rajesh.kumar@email.com',
                    'address': '123 Main Street, Sector 15',
                    'city': 'Delhi',
                    'state': 'Delhi',
                    'pincode': '110015',
                    'date_of_birth': date(1985, 5, 15),
                    'gender': 'male',
                },
                {
                    'first_name': 'Priya',
                    'last_name': 'Sharma',
                    'phone': '9876543211',
                    'email': 'priya.sharma@email.com',
                    'address': '456 Park Avenue, Model Town',
                    'city': 'Mumbai',
                    'state': 'Maharashtra',
                    'pincode': '400001',
                    'date_of_birth': date(1990, 8, 22),
                    'gender': 'female',
                },
                {
                    'first_name': 'Amit',
                    'last_name': 'Patel',
                    'phone': '9876543212',
                    'email': 'amit.patel@email.com',
                    'address': '789 Garden Road, Civil Lines',
                    'city': 'Bangalore',
                    'state': 'Karnataka',
                    'pincode': '560001',
                    'date_of_birth': date(1988, 3, 10),
                    'gender': 'male',
                },
                {
                    'first_name': 'Sunita',
                    'last_name': 'Singh',
                    'phone': '9876543213',
                    'email': 'sunita.singh@email.com',
                    'address': '321 Lake View, Salt Lake',
                    'city': 'Kolkata',
                    'state': 'West Bengal',
                    'pincode': '700001',
                    'date_of_birth': date(1992, 11, 5),
                    'gender': 'female',
                },
                {
                    'first_name': 'Vikram',
                    'last_name': 'Reddy',
                    'phone': '9876543214',
                    'email': 'vikram.reddy@email.com',
                    'address': '654 Tech Park, HITEC City',
                    'city': 'Hyderabad',
                    'state': 'Telangana',
                    'pincode': '500001',
                    'date_of_birth': date(1987, 7, 18),
                    'gender': 'male',
                },
            ]
            
            for customer in customers:
                Customer.objects.create(**customer)
            self.stdout.write('Created customers')

    def create_suppliers(self):
        if not Supplier.objects.exists():
            suppliers = [
                {
                    'name': 'Sun Pharma Distributors',
                    'contact_person': 'Mr. Rajesh Gupta',
                    'phone': '022-12345678',
                    'email': 'orders@sunpharma.com',
                    'address': '123 Industrial Area, Phase 1',
                    'city': 'Mumbai',
                    'state': 'Maharashtra',
                    'pincode': '400001',
                    'gst_number': '27AABCS1234C1Z5',
                    'credit_limit': 100000,
                },
                {
                    'name': 'Cipla Medical Supplies',
                    'contact_person': 'Ms. Priya Sharma',
                    'phone': '011-87654321',
                    'email': 'supplies@cipla.com',
                    'address': '456 Business Park, Sector 18',
                    'city': 'Delhi',
                    'state': 'Delhi',
                    'pincode': '110015',
                    'gst_number': '07AABCS5678C1Z5',
                    'credit_limit': 150000,
                },
                {
                    'name': 'Dr. Reddy\'s Pharmaceuticals',
                    'contact_person': 'Mr. Amit Kumar',
                    'phone': '040-98765432',
                    'email': 'distribution@drreddys.com',
                    'address': '789 Pharma Hub, Gachibowli',
                    'city': 'Hyderabad',
                    'state': 'Telangana',
                    'pincode': '500032',
                    'gst_number': '36AABCS9012C1Z5',
                    'credit_limit': 200000,
                },
            ]
            
            for supplier in suppliers:
                Supplier.objects.create(**supplier)
            self.stdout.write('Created suppliers')

    def create_stock_movements(self):
        if not StockMovement.objects.exists():
            medicines = Medicine.objects.all()
            user = User.objects.first()
            
            for medicine in medicines:
                # Initial stock in
                StockMovement.objects.create(
                    medicine=medicine,
                    movement_type='in',
                    quantity=medicine.stock_quantity,
                    previous_stock=0,
                    new_stock=medicine.stock_quantity,
                    reference_number='INITIAL_STOCK',
                    notes='Initial stock entry',
                    created_by=user
                )
            self.stdout.write('Created stock movements')

    def create_prescriptions(self):
        if not Prescription.objects.exists():
            customers = Customer.objects.all()
            medicines = Medicine.objects.all()
            
            for i, customer in enumerate(customers):
                prescription = Prescription.objects.create(
                    customer=customer,
                    doctor_name=f'Dr. {["Sharma", "Patel", "Kumar", "Singh", "Reddy"][i]}',
                    doctor_license=f'DL{i+1:03d}',
                    clinic_name=f'{["City", "Central", "General", "Specialty", "Metro"][i]} Hospital',
                    prescription_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                    diagnosis=f'Patient complaint: {["Fever", "Cough", "Headache", "Stomach pain", "Allergy"][i]}',
                    symptoms=f'Symptoms: {["High temperature", "Persistent cough", "Severe headache", "Abdominal pain", "Skin rash"][i]}',
                    instructions='Take as directed by physician',
                    status='pending' if i < 3 else 'dispensed',
                )
                
                # Add prescription items
                selected_medicines = random.sample(list(medicines), random.randint(1, 3))
                for medicine in selected_medicines:
                    PrescriptionItem.objects.create(
                        prescription=prescription,
                        medicine=medicine,
                        dosage=medicine.strength,
                        frequency='Twice daily',
                        duration='7 days',
                        quantity=random.randint(10, 30),
                        unit_price=medicine.selling_price,
                    )
            self.stdout.write('Created prescriptions')

    def create_bills(self):
        if not Bill.objects.exists():
            customers = Customer.objects.all()
            medicines = Medicine.objects.all()
            prescriptions = Prescription.objects.all()
            user = User.objects.first()
            
            for i in range(10):
                customer = random.choice(customers)
                prescription = random.choice(prescriptions) if random.choice([True, False]) else None
                
                # Create bill first
                bill = Bill.objects.create(
                    customer=customer,
                    prescription=prescription,
                    discount_percentage=random.choice([0, 5, 10]),
                    tax_percentage=random.choice([0, 5, 12, 18]),
                    payment_method=random.choice(['cash', 'card', 'upi']),
                    payment_status=random.choice(['paid', 'pending', 'partial']),
                    notes=f'Bill notes for customer {customer.full_name}',
                    created_by=user,
                )
                
                # Add bill items
                selected_medicines = random.sample(list(medicines), random.randint(1, 4))
                subtotal = 0
                for medicine in selected_medicines:
                    quantity = random.randint(1, 10)
                    item_total = medicine.selling_price * quantity
                    subtotal += item_total
                    
                    BillItem.objects.create(
                        bill=bill,
                        medicine=medicine,
                        quantity=quantity,
                        unit_price=medicine.selling_price,
                        batch_number=f'BATCH{random.randint(1000, 9999)}',
                        expiry_date=date.today() + timedelta(days=random.randint(30, 365)),
                    )
                    
                    # Update stock
                    medicine.stock_quantity -= quantity
                    medicine.save()
                    
                    # Create stock movement
                    StockMovement.objects.create(
                        medicine=medicine,
                        movement_type='out',
                        quantity=-quantity,
                        previous_stock=medicine.stock_quantity + quantity,
                        new_stock=medicine.stock_quantity,
                        reference_number=bill.bill_id,
                        created_by=user,
                    )
                
                # Calculate and update bill totals
                bill.subtotal = subtotal
                if bill.discount_percentage > 0:
                    bill.discount_amount = (subtotal * bill.discount_percentage) / 100
                
                taxable_amount = subtotal - bill.discount_amount
                if bill.tax_percentage > 0:
                    bill.tax_amount = (taxable_amount * bill.tax_percentage) / 100
                
                bill.total_amount = taxable_amount + bill.tax_amount
                bill.save()
                
                # Add payment if bill is paid
                if bill.payment_status == 'paid':
                    Payment.objects.create(
                        bill=bill,
                        customer=customer,
                        amount=bill.total_amount,
                        payment_method=bill.payment_method,
                        payment_status='completed',
                        created_by=user,
                    )
                    bill.paid_amount = bill.total_amount
                    bill.save()
                elif bill.payment_status == 'partial':
                    partial_amount = bill.total_amount * Decimal('0.5')
                    Payment.objects.create(
                        bill=bill,
                        customer=customer,
                        amount=partial_amount,
                        payment_method=bill.payment_method,
                        payment_status='completed',
                        created_by=user,
                    )
                    bill.paid_amount = partial_amount
                    bill.save()
            
            self.stdout.write('Created bills')
