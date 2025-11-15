from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SiteSettings, TeamMember, Testimonial, Counter, HeroSection, FeatureCard, HomePageSection
from services.models import ServiceCategory, Service, ServicePackage, ServiceFAQ
from portfolio.models import CaseStudy, CaseStudyImage, DoctorWebsite, Technology
from blog.models import BlogCategory, BlogPost, BlogTag, BlogPostTag
from contact.models import ContactInfo
from django.utils import timezone
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with dummy data for Mediwell Care'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database with dummy data...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@mediwellcare.com', 'admin123')
            self.stdout.write('Created superuser: admin/admin123')
        
        # Create site settings
        self.create_site_settings()
        
        # Create hero section
        self.create_hero_section()
        
        # Create feature cards
        self.create_feature_cards()
        
        # Create counters
        self.create_counters()
        
        # Create team members
        self.create_team_members()
        
        # Create testimonials
        self.create_testimonials()
        
        # Create service categories and services
        self.create_services()
        
        # Create case studies
        self.create_case_studies()
        
        # Create doctor websites
        self.create_doctor_websites()
        
        # Create technologies
        self.create_technologies()
        
        # Create blog categories and posts
        self.create_blog_content()
        
        # Create contact info
        self.create_contact_info()
        
        
        # Create homepage sections
        self.create_homepage_sections()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))

    def create_site_settings(self):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name="Mediwell Care",
                tagline="Empowering Doctors Digitally",
                description="Your digital partner for websites, CRM, SEO & patient growth. We specialize in comprehensive digital solutions for doctors and healthcare professionals.",
                phone="+91 9616651137",
                email="abdurrabkhan709@gmail.com",
                address="Lucknow, Uttar Pradesh, India",
                facebook_url="https://facebook.com/mediwellcare",
                twitter_url="https://twitter.com/mediwellcare",
                linkedin_url="https://linkedin.com/company/mediwellcare",
                instagram_url="https://instagram.com/mediwellcare",
                whatsapp_number="919616651137",
                meta_title="Mediwell Care - Digital Solutions for Doctors",
                meta_description="Transform your medical practice with our comprehensive digital solutions. Custom websites, CRM systems, SEO optimization, and social media management for healthcare professionals.",
                meta_keywords="doctor website, healthcare digital marketing, medical SEO, doctor CRM, healthcare social media, medical practice management"
            )
            self.stdout.write('Created site settings')

    def create_hero_section(self):
        if not HeroSection.objects.exists():
            HeroSection.objects.create(
                title="Empowering Doctors Digitally with Mediwell Care",
                subtitle="Your digital partner for websites, CRM, SEO & patient growth",
                description="We specialize in creating powerful digital solutions exclusively for doctors and healthcare professionals. From custom websites to comprehensive CRM systems, we help you grow your practice and serve more patients.",
                primary_cta_text="Get Free Consultation",
                primary_cta_url="#contact",
                secondary_cta_text="View Our Work",
                secondary_cta_url="#portfolio",
                is_active=True
            )
            self.stdout.write('Created hero section')

    def create_feature_cards(self):
        if not FeatureCard.objects.exists():
            features = [
                {
                    'title': 'Websites for Clinics',
                    'description': 'Professional, responsive websites designed specifically for medical practices with patient portals and appointment booking.',
                    'icon': 'fas fa-laptop-medical',
                    'cta_text': 'Learn More',
                    'cta_url': '/services/website-development/',
                    'order': 1
                },
                {
                    'title': 'Social Media Growth',
                    'description': 'Strategic social media management to build your online presence and attract more patients to your practice.',
                    'icon': 'fas fa-share-alt',
                    'cta_text': 'Get Started',
                    'cta_url': '/services/social-media-management/',
                    'order': 2
                },
                {
                    'title': 'Smart CRM for Doctors',
                    'description': 'Comprehensive patient management systems that streamline your practice operations and improve patient care.',
                    'icon': 'fas fa-users-cog',
                    'cta_text': 'Explore CRM',
                    'cta_url': '/services/crm-systems/',
                    'order': 3
                }
            ]
            
            for feature in features:
                FeatureCard.objects.create(**feature)
            self.stdout.write('Created feature cards')

    def create_counters(self):
        if not Counter.objects.exists():
            counters = [
                {'title': 'Doctors Served', 'number': 500, 'suffix': '+', 'icon': 'fas fa-user-md', 'order': 1},
                {'title': 'Websites Built', 'number': 150, 'suffix': '+', 'icon': 'fas fa-laptop', 'order': 2},
                {'title': 'Cities Covered', 'number': 25, 'suffix': '+', 'icon': 'fas fa-map-marker-alt', 'order': 3},
                {'title': 'Happy Clients', 'number': 98, 'suffix': '%', 'icon': 'fas fa-heart', 'order': 4}
            ]
            
            for counter in counters:
                Counter.objects.create(**counter)
            self.stdout.write('Created counters')

    def create_team_members(self):
        if not TeamMember.objects.exists():
            team_members = [
                {
                    'name': 'Dr. Sarah Johnson',
                    'position': 'Medical Director',
                    'specialization': 'Healthcare Technology',
                    'bio': 'Leading expert in healthcare digital transformation with 15+ years of experience.',
                    'email': 'sarah@mediwellcare.com',
                    'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
                    'order': 1
                },
                {
                    'name': 'Rajesh Kumar',
                    'position': 'Lead Developer',
                    'specialization': 'Full-Stack Development',
                    'bio': 'Experienced developer specializing in healthcare applications and secure systems.',
                    'email': 'rajesh@mediwellcare.com',
                    'linkedin_url': 'https://linkedin.com/in/rajeshkumar',
                    'order': 2
                },
                {
                    'name': 'Priya Sharma',
                    'position': 'Digital Marketing Specialist',
                    'specialization': 'Healthcare SEO',
                    'bio': 'Expert in healthcare digital marketing with proven track record of growing medical practices.',
                    'email': 'priya@mediwellcare.com',
                    'linkedin_url': 'https://linkedin.com/in/priyasharma',
                    'order': 3
                }
            ]
            
            for member in team_members:
                TeamMember.objects.create(**member)
            self.stdout.write('Created team members')

    def create_testimonials(self):
        if not Testimonial.objects.exists():
            testimonials = [
                {
                    'name': 'Dr. Amit Patel',
                    'title': 'Cardiologist',
                    'clinic_name': 'Heart Care Clinic',
                    'content': 'Mediwell Care transformed our practice completely. Our patient inquiries increased by 300% within 6 months. The website they built is professional and user-friendly.',
                    'rating': 5,
                    'is_featured': True,
                    'order': 1
                },
                {
                    'name': 'Dr. Priya Singh',
                    'title': 'Dermatologist',
                    'clinic_name': 'Skin Care Center',
                    'content': 'Excellent service! They understood our needs perfectly and delivered beyond expectations. Our online presence has never been stronger.',
                    'rating': 5,
                    'is_featured': True,
                    'order': 2
                },
                {
                    'name': 'Dr. Rajesh Gupta',
                    'title': 'Orthopedic Surgeon',
                    'clinic_name': 'Bone & Joint Clinic',
                    'content': 'The CRM system they implemented has streamlined our patient management. Highly recommend their services to fellow doctors.',
                    'rating': 5,
                    'is_featured': True,
                    'order': 3
                }
            ]
            
            for testimonial in testimonials:
                Testimonial.objects.create(**testimonial)
            self.stdout.write('Created testimonials')

    def create_services(self):
        if not ServiceCategory.objects.exists():
            categories = [
                {'name': 'Website Development', 'slug': 'website-development', 'description': 'Professional websites for medical practices', 'icon': 'fas fa-laptop-medical', 'order': 1},
                {'name': 'Digital Marketing', 'slug': 'digital-marketing', 'description': 'SEO, social media, and online marketing', 'icon': 'fas fa-bullhorn', 'order': 2},
                {'name': 'Practice Management', 'slug': 'practice-management', 'description': 'CRM and practice management solutions', 'icon': 'fas fa-cogs', 'order': 3}
            ]
            
            for cat in categories:
                ServiceCategory.objects.create(**cat)
        
        if not Service.objects.exists():
            services = [
                {
                    'category': ServiceCategory.objects.get(slug='website-development'),
                    'name': 'Doctor Website Development',
                    'slug': 'doctor-website-development',
                    'short_description': 'Professional, responsive websites designed specifically for doctors and medical practices.',
                    'description': 'Our custom doctor websites are built with healthcare professionals in mind. Features include patient portals, appointment booking, online consultations, and HIPAA-compliant design.',
                    'features': 'Responsive Design\nPatient Portal\nAppointment Booking\nOnline Consultations\nHIPAA Compliant\nSEO Optimized\nMobile Friendly\nFast Loading',
                    'icon': 'fas fa-laptop-medical',
                    'starting_price': 25000,
                    'price_unit': 'Starting from',
                    'is_featured': True,
                    'order': 1
                },
                {
                    'category': ServiceCategory.objects.get(slug='digital-marketing'),
                    'name': 'Healthcare SEO Services',
                    'slug': 'healthcare-seo-services',
                    'short_description': 'Specialized SEO services to help doctors rank higher in local search results.',
                    'description': 'Our healthcare SEO experts understand the unique challenges of medical practice marketing. We focus on local SEO, medical keywords, and patient acquisition strategies.',
                    'features': 'Local SEO Optimization\nMedical Keyword Research\nGoogle My Business Setup\nPatient Review Management\nContent Marketing\nLink Building\nAnalytics & Reporting\nCompetitor Analysis',
                    'icon': 'fas fa-search',
                    'starting_price': 15000,
                    'price_unit': 'Starting from',
                    'is_featured': True,
                    'order': 2
                },
                {
                    'category': ServiceCategory.objects.get(slug='practice-management'),
                    'name': 'Doctor CRM System',
                    'slug': 'doctor-crm-system',
                    'short_description': 'Comprehensive patient management system designed for medical practices.',
                    'description': 'Our CRM system helps doctors manage patient relationships, appointments, medical records, and practice operations efficiently.',
                    'features': 'Patient Management\nAppointment Scheduling\nMedical Records\nBilling Integration\nPrescription Management\nFollow-up Reminders\nAnalytics Dashboard\nMobile Access',
                    'icon': 'fas fa-users-cog',
                    'starting_price': 30000,
                    'price_unit': 'Starting from',
                    'is_featured': True,
                    'order': 3
                }
            ]
            
            for service in services:
                Service.objects.create(**service)
            
            # Create service packages
            service = Service.objects.get(slug='doctor-website-development')
            packages = [
                {
                    'service': service,
                    'name': 'Basic Website',
                    'description': 'Perfect for individual practitioners',
                    'price': 25000,
                    'duration': '2-3 weeks',
                    'features': '5-7 pages\nContact forms\nAppointment booking\nMobile responsive\nBasic SEO\n1 year support',
                    'is_popular': False,
                    'order': 1
                },
                {
                    'service': service,
                    'name': 'Professional Website',
                    'description': 'Ideal for clinics and hospitals',
                    'price': 50000,
                    'duration': '4-6 weeks',
                    'features': '10-15 pages\nPatient portal\nOnline consultations\nAdvanced SEO\nSocial media integration\n2 years support',
                    'is_popular': True,
                    'order': 2
                },
                {
                    'service': service,
                    'name': 'Enterprise Website',
                    'description': 'Complete digital solution for large practices',
                    'price': 100000,
                    'duration': '8-12 weeks',
                    'features': 'Unlimited pages\nCustom features\nCRM integration\nAdvanced analytics\nPriority support\n3 years support',
                    'is_popular': False,
                    'order': 3
                }
            ]
            
            for package in packages:
                ServicePackage.objects.create(**package)
            
            # Create service FAQs
            faqs = [
                {
                    'service': service,
                    'question': 'How long does it take to build a doctor website?',
                    'answer': 'Typically 2-4 weeks depending on the complexity and features required. We work closely with you throughout the process.',
                    'order': 1
                },
                {
                    'service': service,
                    'question': 'Do you provide ongoing support after launch?',
                    'answer': 'Yes, we offer comprehensive maintenance and support packages to keep your website updated and secure.',
                    'order': 2
                },
                {
                    'service': service,
                    'question': 'Is the website mobile-friendly?',
                    'answer': 'Absolutely! All our websites are fully responsive and optimized for mobile devices.',
                    'order': 3
                }
            ]
            
            for faq in faqs:
                ServiceFAQ.objects.create(**faq)
            
            self.stdout.write('Created services and packages')

    def create_case_studies(self):
        if not CaseStudy.objects.exists():
            case_studies = [
                {
                    'title': 'Digital Transformation Success Story',
                    'slug': 'digital-transformation-success-story',
                    'doctor_name': 'Dr. Amit Patel',
                    'doctor_specialization': 'Cardiologist',
                    'clinic_name': 'Heart Care Clinic',
                    'location': 'Mumbai, Maharashtra',
                    'project_type': 'Complete Digital Makeover',
                    'duration': '3 Months',
                    'budget_range': '₹75,000 - ₹1,50,000',
                    'challenge': 'Dr. Patel\'s clinic was struggling with low online visibility and patient acquisition. The existing website was outdated and not mobile-friendly.',
                    'solution': 'We developed a modern, responsive website with patient portal, implemented comprehensive SEO strategy, and set up Google My Business optimization.',
                    'results': 'Within 6 months, the clinic saw a 300% increase in patient inquiries, 250% growth in website traffic, and 40% increase in appointment bookings.',
                    'testimonial': 'Mediwell Care transformed our practice completely. The results speak for themselves!',
                    'website_traffic_increase': '300%',
                    'patient_inquiries_increase': '250%',
                    'social_media_growth': '400%',
                    'is_featured': True,
                    'order': 1
                },
                {
                    'title': 'SEO Success for Dermatology Practice',
                    'slug': 'seo-success-dermatology-practice',
                    'doctor_name': 'Dr. Priya Singh',
                    'doctor_specialization': 'Dermatologist',
                    'clinic_name': 'Skin Care Center',
                    'location': 'Delhi, NCR',
                    'project_type': 'SEO & Digital Marketing',
                    'duration': '6 Months',
                    'budget_range': '₹50,000 - ₹1,00,000',
                    'challenge': 'The dermatology practice needed better online visibility to compete with larger hospitals in the area.',
                    'solution': 'Implemented comprehensive local SEO strategy, created valuable content, and optimized Google My Business profile.',
                    'results': 'Achieved #1 ranking for key dermatology keywords, increased organic traffic by 400%, and generated 60% more patient inquiries.',
                    'testimonial': 'Our online presence has never been stronger. Highly recommend their SEO services!',
                    'website_traffic_increase': '400%',
                    'patient_inquiries_increase': '60%',
                    'social_media_growth': '200%',
                    'is_featured': True,
                    'order': 2
                }
            ]
            
            for case_study in case_studies:
                CaseStudy.objects.create(**case_study)
            self.stdout.write('Created case studies')

    def create_doctor_websites(self):
        if not DoctorWebsite.objects.exists():
            websites = [
                {
                    'doctor_name': 'Dr. Rajesh Gupta',
                    'specialization': 'Orthopedic Surgeon',
                    'clinic_name': 'Bone & Joint Clinic',
                    'location': 'Bangalore, Karnataka',
                    'website_url': 'https://bonejointclinic.com',
                    'website_type': 'Clinic Website',
                    'technologies_used': 'WordPress, Elementor, WooCommerce',
                    'launch_date': date.today() - timedelta(days=90),
                    'monthly_visitors': 2500,
                    'patient_inquiries': 45,
                    'is_featured': True,
                    'order': 1
                },
                {
                    'doctor_name': 'Dr. Sunita Reddy',
                    'specialization': 'Gynecologist',
                    'clinic_name': 'Women\'s Health Center',
                    'location': 'Hyderabad, Telangana',
                    'website_url': 'https://womenshealthcenter.com',
                    'website_type': 'Specialty Clinic',
                    'technologies_used': 'React, Node.js, MongoDB',
                    'launch_date': date.today() - timedelta(days=120),
                    'monthly_visitors': 3200,
                    'patient_inquiries': 60,
                    'is_featured': True,
                    'order': 2
                }
            ]
            
            for website in websites:
                DoctorWebsite.objects.create(**website)
            self.stdout.write('Created doctor websites')

    def create_technologies(self):
        if not Technology.objects.exists():
            technologies = [
                {'name': 'WordPress', 'category': 'CMS', 'icon': 'fab fa-wordpress', 'order': 1},
                {'name': 'React', 'category': 'Frontend', 'icon': 'fab fa-react', 'order': 2},
                {'name': 'Django', 'category': 'Backend', 'icon': 'fab fa-python', 'order': 3},
                {'name': 'Node.js', 'category': 'Backend', 'icon': 'fab fa-node-js', 'order': 4},
                {'name': 'MongoDB', 'category': 'Database', 'icon': 'fas fa-database', 'order': 5},
                {'name': 'PostgreSQL', 'category': 'Database', 'icon': 'fas fa-database', 'order': 6}
            ]
            
            for tech in technologies:
                Technology.objects.create(**tech)
            self.stdout.write('Created technologies')

    def create_blog_content(self):
        if not BlogCategory.objects.exists():
            categories = [
                {'name': 'Digital Marketing', 'slug': 'digital-marketing', 'description': 'Healthcare digital marketing tips and strategies', 'color': '#3B82F6', 'order': 1},
                {'name': 'Website Development', 'slug': 'website-development', 'description': 'Doctor website development insights', 'color': '#10B981', 'order': 2},
                {'name': 'SEO', 'slug': 'seo', 'description': 'Healthcare SEO best practices', 'color': '#F59E0B', 'order': 3}
            ]
            
            for cat in categories:
                BlogCategory.objects.create(**cat)
        
        if not BlogPost.objects.exists():
            author = User.objects.first()
            category = BlogCategory.objects.first()
            
            posts = [
                {
                    'title': 'Why Every Doctor Needs a Professional Website',
                    'slug': 'why-every-doctor-needs-professional-website',
                    'author': author,
                    'category': category,
                    'excerpt': 'In today\'s digital age, having a professional website is crucial for doctors to attract and retain patients.',
                    'content': 'A professional website is no longer optional for doctors. It\'s a necessity that can significantly impact your practice\'s growth and patient satisfaction...',
                    'status': 'published',
                    'is_featured': True,
                    'published_at': timezone.now() - timedelta(days=5)
                },
                {
                    'title': 'Healthcare SEO: A Complete Guide for Doctors',
                    'slug': 'healthcare-seo-complete-guide-doctors',
                    'author': author,
                    'category': category,
                    'excerpt': 'Learn how to optimize your medical practice for search engines and attract more patients online.',
                    'content': 'Healthcare SEO is different from regular SEO. It requires understanding of medical terminology, local search, and patient behavior...',
                    'status': 'published',
                    'is_featured': True,
                    'published_at': timezone.now() - timedelta(days=10)
                }
            ]
            
            for post in posts:
                BlogPost.objects.create(**post)
            self.stdout.write('Created blog content')

    def create_contact_info(self):
        if not ContactInfo.objects.exists():
            ContactInfo.objects.create(
                title="Get in Touch",
                description="Ready to transform your practice? Contact us for a free consultation.",
                phone="+91 9616651137",
                email="abdurrabkhan709@gmail.com",
                address="Lucknow, Uttar Pradesh, India",
                whatsapp_number="919616651137",
                office_hours="Monday - Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM",
                facebook_url="https://facebook.com/mediwellcare",
                twitter_url="https://twitter.com/mediwellcare",
                linkedin_url="https://linkedin.com/company/mediwellcare",
                instagram_url="https://instagram.com/mediwellcare",
                is_active=True
            )
            self.stdout.write('Created contact information')

    def create_homepage_sections(self):
        if not HomePageSection.objects.exists():
            sections = [
                {
                    'section_name': 'hero',
                    'title': 'Empowering Doctors Digitally',
                    'subtitle': 'Your digital partner for websites, CRM, SEO & patient growth',
                    'description': 'We specialize in creating powerful digital solutions exclusively for doctors and healthcare professionals.',
                    'order': 1
                },
                {
                    'section_name': 'features',
                    'title': 'Why Choose Mediwell Care?',
                    'subtitle': 'We understand the unique challenges doctors face in today\'s digital world',
                    'description': 'Our solutions are designed specifically for healthcare professionals.',
                    'order': 2
                },
                {
                    'section_name': 'services',
                    'title': 'Our Digital Solutions',
                    'subtitle': 'Comprehensive digital services tailored for doctors and healthcare professionals',
                    'description': 'From websites to CRM systems, we provide complete digital transformation.',
                    'order': 3
                },
                {
                    'section_name': 'case_studies',
                    'title': 'Success Stories',
                    'subtitle': 'See how we\'ve helped doctors transform their practices with our digital solutions',
                    'description': 'Real results from real doctors who trusted us with their digital transformation.',
                    'order': 6
                },
                {
                    'section_name': 'testimonials',
                    'title': 'What Doctors Say About Us',
                    'subtitle': 'Don\'t just take our word for it. Here\'s what our clients have to say about our services.',
                    'description': 'Hear from doctors who have experienced the Mediwell Care difference.',
                    'order': 7
                },
                {
                    'section_name': 'websites',
                    'title': 'Doctor Websites We\'ve Built',
                    'subtitle': 'Professional, modern websites designed specifically for healthcare professionals',
                    'description': 'See examples of our work and the results we\'ve achieved for our clients.',
                    'order': 8
                },
                {
                    'section_name': 'blog',
                    'title': 'Latest Insights',
                    'subtitle': 'Stay updated with the latest trends in healthcare digital marketing',
                    'description': 'Expert insights and tips to help you grow your medical practice.',
                    'order': 9
                },
                {
                    'section_name': 'counters',
                    'title': 'Our Impact in Numbers',
                    'subtitle': 'Trusted by doctors across India for their digital transformation',
                    'description': 'The numbers speak for themselves - see the impact we\'ve made.',
                    'order': 10
                }
            ]
            
            for section in sections:
                HomePageSection.objects.create(**section)
            self.stdout.write('Created homepage sections')
