# Mediwell Care - Digital Solutions for Doctors

A comprehensive Django-based website for Mediwell Care, a digital service company exclusively for doctors and healthcare professionals.

## 🎯 Purpose

Mediwell Care is a one-stop digital solution provider for doctors, offering:
- Custom website development
- CRM systems for patient management
- SEO optimization
- Google My Business setup
- Social media management
- Reputation management

## 🎨 Design Features

- **Medical-grade professional UI** with white + royal blue + aqua green color palette
- **Modern typography** using Poppins and Inter fonts
- **Fully responsive** design (desktop, tablet, mobile)
- **Subtle animations** on scroll and hover
- **Premium look** with realistic content and testimonials

## ⚙️ Technical Stack

- **Backend**: Django 5, PostgreSQL
- **Frontend**: Tailwind CSS + Alpine.js
- **Authentication**: Django Allauth
- **Admin**: Customized Django Admin with Mediwell branding
- **Email**: Django Email backend for contact forms

## 🏗️ Website Structure

### 1. Home Page
- Hero section with compelling CTA
- Feature cards highlighting key services
- Client showcase slider
- Testimonials carousel
- Animated counters
- Recent blog posts

### 2. About Page
- Company mission and values
- Team section with professional profiles
- Statistics and impact metrics
- Client testimonials

### 3. Services Page
- Category-based service listings
- Detailed service pages with packages
- FAQ sections
- Pricing information

### 4. Portfolio Page
- Case studies with before/after results
- Doctor website showcases
- Technology stack
- Process overview

### 5. Contact Page
- Inquiry and quote request forms
- Contact information
- Google Maps integration
- WhatsApp chat integration
- FAQ section

### 6. Blog Page
- Healthcare digital marketing insights
- Category filtering
- Featured articles
- Newsletter subscription

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mediwell-care
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=mediwell_care
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Populate with Dummy Data
```bash
python manage.py populate_data
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the website.

## 📊 Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials.

### Key Admin Features:
- **Site Settings**: Configure site-wide settings, contact info, social media
- **Content Management**: Manage services, blog posts, testimonials, case studies
- **Contact Inquiries**: Track and respond to contact form submissions
- **Analytics**: View lead generation and traffic statistics

## 🎨 Customization

### Colors
The website uses a medical-grade color palette:
- Primary Blue: `#1E40AF`
- Light Blue: `#3B82F6`
- Aqua: `#06B6D4`
- Light Aqua: `#67E8F9`

### Fonts
- Primary: Poppins (headings)
- Secondary: Inter (body text)

### Components
- Responsive navigation with mobile menu
- Animated counters
- Hover effects and transitions
- AOS (Animate On Scroll) integration
- Alpine.js for interactive elements

## 📱 Features

### For Doctors
- **Free Consultation**: Easy contact forms
- **Quote Requests**: Detailed service inquiries
- **Case Studies**: Real success stories
- **Blog Content**: Healthcare digital marketing insights

### For Administrators
- **Content Management**: Easy content updates
- **Lead Tracking**: Contact form submissions
- **Analytics**: Performance metrics
- **SEO Tools**: Meta tags and optimization

## 🔧 Development

### Adding New Services
1. Go to Admin Panel → Services → Service Categories
2. Create new category if needed
3. Add service with details, pricing, and features
4. Create service packages and FAQs

### Adding Blog Posts
1. Go to Admin Panel → Blog → Blog Posts
2. Create new post with title, content, and featured image
3. Assign category and tags
4. Set status to "Published"

### Managing Contact Forms
1. Go to Admin Panel → Contact → Contact Inquiries
2. View and respond to inquiries
3. Update status and add admin notes

## 📈 SEO Features

- **Meta Tags**: Optimized for each page
- **Schema Markup**: Healthcare business schema
- **Sitemap**: Automatic sitemap generation
- **Open Graph**: Social media sharing optimization
- **Local SEO**: Google My Business integration

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in environment
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Set up SSL certificate

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud hosting

## 📞 Support

For technical support or customization requests:
- Email: info@mediwellcare.com
- Phone: +91 98765 43210
- WhatsApp: +91 98765 43210

## 📄 License

This project is proprietary software developed for Mediwell Care. All rights reserved.

---

**Mediwell Care** - Empowering Doctors Digitally
