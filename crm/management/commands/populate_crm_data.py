from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from crm.models import (
    Clinic, Doctor, Patient, Appointment, Treatment, 
    Prescription, PrescriptionMedicine, Payment, MedicalRecord
)


class Command(BaseCommand):
    help = 'Populate CRM with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate CRM with sample data...')
        
        # Create clinic
        clinic, created = Clinic.objects.get_or_create(
            name="Mediwell Care Clinic",
            defaults={
                'slug': 'mediwell-care-clinic',
                'description': 'A comprehensive healthcare facility providing quality medical services',
                'phone': '+91 98765 43210',
                'email': 'info@mediwellcare.com',
                'address': '123 Medical Street, Healthcare District',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001',
                'registration_number': 'REG123456',
                'license_number': 'LIC789012',
                'established_date': datetime(2020, 1, 1).date(),
                'monday_start': datetime.strptime('09:00', '%H:%M').time(),
                'monday_end': datetime.strptime('18:00', '%H:%M').time(),
                'tuesday_start': datetime.strptime('09:00', '%H:%M').time(),
                'tuesday_end': datetime.strptime('18:00', '%H:%M').time(),
                'wednesday_start': datetime.strptime('09:00', '%H:%M').time(),
                'wednesday_end': datetime.strptime('18:00', '%H:%M').time(),
                'thursday_start': datetime.strptime('09:00', '%H:%M').time(),
                'thursday_end': datetime.strptime('18:00', '%H:%M').time(),
                'friday_start': datetime.strptime('09:00', '%H:%M').time(),
                'friday_end': datetime.strptime('18:00', '%H:%M').time(),
                'saturday_start': datetime.strptime('09:00', '%H:%M').time(),
                'saturday_end': datetime.strptime('14:00', '%H:%M').time(),
                'appointment_duration': 30,
                'advance_booking_days': 30,
                'cancellation_hours': 24,
            }
        )
        
        if created:
            self.stdout.write(f'Created clinic: {clinic.name}')
        else:
            self.stdout.write(f'Using existing clinic: {clinic.name}')
        
        # Create doctors
        doctors_data = [
            {
                'username': 'dr_smith',
                'email': 'dr.smith@mediwellcare.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'specialization': 'Cardiology',
                'qualification': 'MD, DM Cardiology',
                'experience_years': 15,
                'consultation_fee': 1500.00,
            },
            {
                'username': 'dr_johnson',
                'email': 'dr.johnson@mediwellcare.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'specialization': 'Pediatrics',
                'qualification': 'MD Pediatrics',
                'experience_years': 12,
                'consultation_fee': 1200.00,
            },
            {
                'username': 'dr_williams',
                'email': 'dr.williams@mediwellcare.com',
                'first_name': 'Michael',
                'last_name': 'Williams',
                'specialization': 'Orthopedics',
                'qualification': 'MS Orthopedics',
                'experience_years': 18,
                'consultation_fee': 2000.00,
            },
        ]
        
        doctors = []
        for doctor_data in doctors_data:
            user, created = User.objects.get_or_create(
                username=doctor_data['username'],
                defaults={
                    'email': doctor_data['email'],
                    'first_name': doctor_data['first_name'],
                    'last_name': doctor_data['last_name'],
                }
            )
            
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'clinic': clinic,
                    'first_name': doctor_data['first_name'],
                    'last_name': doctor_data['last_name'],
                    'specialization': doctor_data['specialization'],
                    'qualification': doctor_data['qualification'],
                    'experience_years': doctor_data['experience_years'],
                    'consultation_fee': doctor_data['consultation_fee'],
                    'phone': '+91 98765 4321' + str(random.randint(0, 9)),
                    'email': doctor_data['email'],
                    'bio': f"Experienced {doctor_data['specialization']} specialist with {doctor_data['experience_years']} years of practice.",
                }
            )
            
            doctors.append(doctor)
            if created:
                self.stdout.write(f'Created doctor: {doctor.full_name}')
            else:
                self.stdout.write(f'Using existing doctor: {doctor.full_name}')
        
        # Create patients
        patients_data = [
            {
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'phone': '+91 98765 12345',
                'email': 'rajesh.kumar@email.com',
                'date_of_birth': datetime(1985, 5, 15).date(),
                'gender': 'male',
                'blood_group': 'B+',
                'height': 175,
                'weight': 70.5,
                'allergies': 'Penicillin',
                'medical_history': 'Hypertension, Diabetes Type 2',
            },
            {
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'phone': '+91 98765 23456',
                'email': 'priya.sharma@email.com',
                'date_of_birth': datetime(1990, 8, 22).date(),
                'gender': 'female',
                'blood_group': 'A+',
                'height': 160,
                'weight': 55.2,
                'allergies': 'None',
                'medical_history': 'None',
            },
            {
                'first_name': 'Amit',
                'last_name': 'Patel',
                'phone': '+91 98765 34567',
                'email': 'amit.patel@email.com',
                'date_of_birth': datetime(1978, 12, 10).date(),
                'gender': 'male',
                'blood_group': 'O+',
                'height': 170,
                'weight': 75.8,
                'allergies': 'Dust, Pollen',
                'medical_history': 'Asthma',
            },
            {
                'first_name': 'Sunita',
                'last_name': 'Singh',
                'phone': '+91 98765 45678',
                'email': 'sunita.singh@email.com',
                'date_of_birth': datetime(1995, 3, 8).date(),
                'gender': 'female',
                'blood_group': 'AB+',
                'height': 165,
                'weight': 58.3,
                'allergies': 'Shellfish',
                'medical_history': 'Migraine',
            },
            {
                'first_name': 'Vikram',
                'last_name': 'Gupta',
                'phone': '+91 98765 56789',
                'email': 'vikram.gupta@email.com',
                'date_of_birth': datetime(1982, 7, 25).date(),
                'gender': 'male',
                'blood_group': 'B-',
                'height': 180,
                'weight': 82.1,
                'allergies': 'None',
                'medical_history': 'High Cholesterol',
            },
        ]
        
        patients = []
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                phone=patient_data['phone'],
                defaults={
                    'first_name': patient_data['first_name'],
                    'last_name': patient_data['last_name'],
                    'email': patient_data['email'],
                    'date_of_birth': patient_data['date_of_birth'],
                    'gender': patient_data['gender'],
                    'blood_group': patient_data['blood_group'],
                    'height': patient_data['height'],
                    'weight': patient_data['weight'],
                    'allergies': patient_data['allergies'],
                    'medical_history': patient_data['medical_history'],
                    'address': f"{random.randint(1, 100)} Street, Area {random.randint(1, 10)}",
                    'city': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']),
                    'state': random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal']),
                    'pincode': f"{random.randint(100000, 999999)}",
                    'emergency_contact_name': f"Emergency Contact {patient_data['first_name']}",
                    'emergency_contact_phone': f"+91 98765 {random.randint(10000, 99999)}",
                    'emergency_contact_relation': random.choice(['Spouse', 'Parent', 'Sibling', 'Friend']),
                }
            )
            
            patients.append(patient)
            if created:
                self.stdout.write(f'Created patient: {patient.full_name}')
            else:
                self.stdout.write(f'Using existing patient: {patient.full_name}')
        
        # Create appointments
        appointment_reasons = [
            'Regular checkup',
            'Chest pain',
            'Fever and cough',
            'Back pain',
            'Headache',
            'Stomach ache',
            'Follow-up visit',
            'Vaccination',
            'Blood pressure check',
            'Diabetes monitoring',
        ]
        
        for i in range(20):
            appointment_date = timezone.now().date() + timedelta(days=random.randint(-30, 30))
            appointment_time = datetime.strptime(f"{random.randint(9, 17)}:{random.choice(['00', '30'])}", '%H:%M').time()
            
            appointment = Appointment.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                clinic=clinic,
                appointment_type=random.choice(['consultation', 'follow_up', 'checkup', 'emergency']),
                scheduled_date=appointment_date,
                scheduled_time=appointment_time,
                duration=30,
                status=random.choice(['scheduled', 'confirmed', 'completed', 'cancelled']),
                reason=random.choice(appointment_reasons),
                consultation_fee=random.choice(doctors).consultation_fee,
                paid_amount=random.choice([0, random.choice(doctors).consultation_fee]),
                payment_status=random.choice(['pending', 'paid', 'partial']),
            )
            
            self.stdout.write(f'Created appointment: {appointment.patient.full_name} - {appointment.scheduled_date}')
        
        # Create treatments
        treatment_names = [
            'Blood pressure monitoring',
            'Diabetes management',
            'Pain management',
            'Respiratory therapy',
            'Cardiac rehabilitation',
            'Physical therapy',
            'Medication adjustment',
            'Lifestyle counseling',
            'Diet consultation',
            'Exercise prescription',
        ]
        
        for i in range(15):
            treatment = Treatment.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                appointment=random.choice(Appointment.objects.all()) if Appointment.objects.exists() else None,
                treatment_type=random.choice(['consultation', 'procedure', 'therapy', 'medication']),
                name=random.choice(treatment_names),
                description=f"Treatment for {random.choice(['hypertension', 'diabetes', 'pain', 'respiratory issues'])}",
                diagnosis=random.choice([
                    'Hypertension',
                    'Type 2 Diabetes',
                    'Chronic pain syndrome',
                    'Asthma',
                    'High cholesterol',
                    'Migraine',
                    'Anxiety disorder',
                    'Depression',
                ]),
                symptoms=random.choice([
                    'Chest pain, shortness of breath',
                    'Frequent urination, excessive thirst',
                    'Persistent pain in lower back',
                    'Wheezing, difficulty breathing',
                    'Fatigue, weakness',
                    'Severe headaches, nausea',
                    'Restlessness, worry',
                    'Sadness, loss of interest',
                ]),
                treatment_plan=random.choice([
                    'Medication therapy with lifestyle modifications',
                    'Physical therapy and exercise program',
                    'Dietary changes and regular monitoring',
                    'Breathing exercises and medication',
                    'Pain management with physical therapy',
                    'Regular follow-ups and medication adjustment',
                ]),
                medications_prescribed=random.choice([
                    'Metformin 500mg twice daily',
                    'Lisinopril 10mg once daily',
                    'Ibuprofen 400mg as needed',
                    'Albuterol inhaler as needed',
                    'Atorvastatin 20mg once daily',
                    'Sumatriptan 50mg as needed',
                ]),
                follow_up_required=random.choice([True, False]),
                follow_up_date=timezone.now().date() + timedelta(days=random.randint(7, 30)) if random.choice([True, False]) else None,
                treatment_fee=random.randint(500, 3000),
                paid_amount=random.randint(0, 3000),
                status=random.choice(['ongoing', 'completed', 'cancelled']),
            )
            
            self.stdout.write(f'Created treatment: {treatment.name} for {treatment.patient.full_name}')
        
        # Create prescriptions
        for i in range(10):
            prescription = Prescription.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                treatment=random.choice(Treatment.objects.all()) if Treatment.objects.exists() else None,
                symptoms=random.choice([
                    'Chest pain and shortness of breath',
                    'Frequent urination and excessive thirst',
                    'Persistent back pain',
                    'Wheezing and difficulty breathing',
                    'Severe headaches',
                ]),
                diagnosis=random.choice([
                    'Hypertension',
                    'Type 2 Diabetes',
                    'Chronic back pain',
                    'Asthma',
                    'Migraine',
                ]),
                instructions=random.choice([
                    'Take medication with food',
                    'Take on empty stomach',
                    'Avoid alcohol while taking medication',
                    'Take at bedtime',
                    'Take with plenty of water',
                ]),
            )
            
            # Add medicines to prescription
            medicines = [
                {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': '30 days'},
                {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily', 'duration': '30 days'},
                {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'As needed', 'duration': '7 days'},
                {'name': 'Albuterol', 'dosage': '90mcg', 'frequency': 'As needed', 'duration': '30 days'},
                {'name': 'Atorvastatin', 'dosage': '20mg', 'frequency': 'Once daily', 'duration': '30 days'},
            ]
            
            for medicine in random.sample(medicines, random.randint(1, 3)):
                PrescriptionMedicine.objects.create(
                    prescription=prescription,
                    medicine_name=medicine['name'],
                    dosage=medicine['dosage'],
                    frequency=medicine['frequency'],
                    duration=medicine['duration'],
                    quantity=random.randint(1, 3),
                    instructions=random.choice([
                        'Take with food',
                        'Take on empty stomach',
                        'Avoid alcohol',
                        'Take at bedtime',
                    ]),
                )
            
            self.stdout.write(f'Created prescription: {prescription.prescription_id} for {prescription.patient.full_name}')
        
        # Create payments
        for i in range(25):
            payment = Payment.objects.create(
                patient=random.choice(patients),
                appointment=random.choice(Appointment.objects.all()) if Appointment.objects.exists() else None,
                treatment=random.choice(Treatment.objects.all()) if Treatment.objects.exists() else None,
                amount=random.randint(500, 5000),
                payment_method=random.choice(['cash', 'card', 'upi', 'netbanking']),
                payment_status=random.choice(['completed', 'pending', 'failed']),
                transaction_id=f"TXN{random.randint(100000, 999999)}" if random.choice([True, False]) else "",
                notes=random.choice([
                    'Payment received',
                    'Partial payment',
                    'Full payment',
                    'Refund processed',
                ]),
            )
            
            self.stdout.write(f'Created payment: ₹{payment.amount} for {payment.patient.full_name}')
        
        # Create medical records
        record_types = [
            'vital_signs',
            'lab_report',
            'scan_report',
            'xray_report',
            'prescription',
            'treatment_notes',
        ]
        
        for i in range(15):
            medical_record = MedicalRecord.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                record_type=random.choice(record_types),
                title=random.choice([
                    'Blood Pressure Reading',
                    'Blood Sugar Report',
                    'X-Ray Chest',
                    'ECG Report',
                    'Blood Test Results',
                    'Treatment Notes',
                    'Vital Signs',
                    'Lab Report',
                ]),
                description=random.choice([
                    'Patient shows improvement in blood pressure',
                    'Blood sugar levels are within normal range',
                    'X-ray shows clear lungs',
                    'ECG shows normal rhythm',
                    'Blood test results are normal',
                    'Patient responding well to treatment',
                ]),
                is_important=random.choice([True, False]),
                is_confidential=random.choice([True, False]),
            )
            
            self.stdout.write(f'Created medical record: {medical_record.title} for {medical_record.patient.full_name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated CRM with sample data!')
        )
        self.stdout.write(f'Created:')
        self.stdout.write(f'- 1 Clinic')
        self.stdout.write(f'- {len(doctors)} Doctors')
        self.stdout.write(f'- {len(patients)} Patients')
        self.stdout.write(f'- {Appointment.objects.count()} Appointments')
        self.stdout.write(f'- {Treatment.objects.count()} Treatments')
        self.stdout.write(f'- {Prescription.objects.count()} Prescriptions')
        self.stdout.write(f'- {Payment.objects.count()} Payments')
        self.stdout.write(f'- {MedicalRecord.objects.count()} Medical Records')
