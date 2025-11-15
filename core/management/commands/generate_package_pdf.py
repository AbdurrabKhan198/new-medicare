"""
Django management command to generate Clinic Growth OS package PDF
Beautiful, professional design with brand colors
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os


class NumberedCanvas(canvas.Canvas):
    """Add page numbers and header/footer"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(HexColor('#6b7280'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 0.75*inch, 0.5*inch, page_text)
        self.restoreState()


class Command(BaseCommand):
    help = 'Generate Clinic Growth OS Package PDF'

    def create_header_table(self, logo_path, medical_blue, medical_aqua):
        """Create beautiful header with logo and title"""
        logo = None
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
        
        title_data = [
            [Paragraph("<b><font size=24 color='#1e40af'>🩺 MEDIWELLCARE</font></b><br/>"
                      "<font size=18 color='#06b6d4'><b>CLINIC GROWTH OS</b></font><br/>"
                      "<font size=12 color='#6b7280'>AI-Powered Digital System for Clinics & Doctors</font>", 
                      ParagraphStyle('HeaderTitle', alignment=TA_CENTER, leading=20))],
        ]
        
        if logo:
            header_data = [[logo, title_data[0][0]]]
        else:
            header_data = title_data
            
        header_table = Table(header_data, colWidths=[2*inch, 4.5*inch] if logo else [7*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 0, colors.transparent),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        return header_table

    def create_tagline_box(self, medical_blue):
        """Create attractive tagline box"""
        tagline_text = (
            "<i><font size=12 color='#1e40af'><b>\"We don't sell websites. We build full automation systems "
            "that increase appointments, reduce workload, and grow online presence.\"</b></font></i>"
        )
        tagline_table = Table([[Paragraph(tagline_text, ParagraphStyle('Tagline', alignment=TA_CENTER, leading=16))]], 
                              colWidths=[7*inch])
        tagline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#eff6ff')),
            ('BOX', (0, 0), (-1, -1), 2, medical_blue),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#eff6ff')]),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        return tagline_table

    def create_package_box(self, title, subtitle, items, outcomes, ideal_for, package_num, medical_blue, medical_aqua):
        """Create beautiful package box with gradient effect"""
        # Package header with gradient background
        header_bg = medical_blue if package_num < 3 else medical_aqua
        
        package_header = Table([[
            Paragraph(f"<font size=20 color='white'><b>{title}</b></font>", 
                     ParagraphStyle('PackageHeader', alignment=TA_LEFT, leading=22))
        ]], colWidths=[7*inch])
        package_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), header_bg),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        # Subtitle
        subtitle_para = Paragraph(f"<i><font size=10 color='#6b7280'>{subtitle}</font></i>",
                                  ParagraphStyle('Subtitle', alignment=TA_LEFT, leading=14))
        
        # Includes section
        includes_title = Paragraph("<b><font size=13 color='#1e40af'>📋 Includes:</font></b>",
                                  ParagraphStyle('SectionTitle', alignment=TA_LEFT, leading=16, spaceAfter=8))
        
        items_list = []
        for item in items:
            if item.strip() == "":
                items_list.append(["", ""])
            elif item.startswith("<b>"):
                # Section header
                items_list.append([
                    "",
                    Paragraph(f"<font size=11 color='#1e40af'>{item}</font>",
                             ParagraphStyle('SectionHeader', alignment=TA_LEFT, leading=16, spaceBefore=8, spaceAfter=4))
                ])
            elif item.startswith("•"):
                # Sub-item
                items_list.append([
                    Paragraph(f"<font size=9 color='#06b6d4'>•</font>",
                             ParagraphStyle('SubCheck', alignment=TA_LEFT)),
                    Paragraph(f"<font size=10 color='#374151'>{item[1:].strip()}</font>",
                             ParagraphStyle('SubItem', alignment=TA_LEFT, leading=14, leftIndent=5))
                ])
            else:
                # Regular item
                items_list.append([
                    Paragraph(f"<font size=10 color='#22c55e'>✓</font>", 
                             ParagraphStyle('Check', alignment=TA_LEFT)),
                    Paragraph(f"<font size=10 color='#374151'>{item}</font>",
                             ParagraphStyle('Item', alignment=TA_LEFT, leading=14))
                ])
        
        items_table = Table(items_list, colWidths=[0.3*inch, 6.7*inch])
        items_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        # Outcomes section
        outcomes_title = Paragraph("<b><font size=13 color='#1e40af'>🎯 Outcome for doctor:</font></b>",
                                  ParagraphStyle('SectionTitle', alignment=TA_LEFT, leading=16, spaceAfter=8, spaceBefore=15))
        
        outcomes_list = []
        for outcome in outcomes:
            outcomes_list.append([
                Paragraph(f"<font size=10 color='#06b6d4'>✔</font>",
                         ParagraphStyle('Check', alignment=TA_LEFT)),
                Paragraph(f"<font size=10 color='#374151'>{outcome}</font>",
                         ParagraphStyle('Item', alignment=TA_LEFT, leading=14))
            ])
        
        outcomes_table = Table(outcomes_list, colWidths=[0.3*inch, 6.7*inch])
        outcomes_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        # Ideal for
        ideal_para = Paragraph(
            f"<b><font size=10 color='#1e40af'>💡 Ideal for:</font> <font size=10 color='#374151'>{ideal_for}</font></b>",
            ParagraphStyle('Ideal', alignment=TA_LEFT, leading=14, spaceBefore=15)
        )
        
        # Combine all in a bordered box
        content_table = Table([[
            Paragraph("", ParagraphStyle('Spacer', spaceAfter=10))
        ]], colWidths=[7*inch])
        content_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#ffffff')),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return [package_header, Spacer(1, 0.1*inch), subtitle_para, Spacer(1, 0.15*inch),
                includes_title, items_table, Spacer(1, 0.1*inch),
                outcomes_title, outcomes_table, Spacer(1, 0.1*inch), ideal_para]

    def handle(self, *args, **options):
        # Define colors
        medical_blue = HexColor('#1e40af')
        medical_aqua = HexColor('#06b6d4')
        dark_gray = HexColor('#374151')
        light_gray = HexColor('#f3f4f6')
        success_green = HexColor('#22c55e')
        
        # Create PDF
        output_path = os.path.join(settings.BASE_DIR, 'static', 'pdfs', 'MediWellCare_Clinic_Growth_OS_Packages.pdf')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Container for elements
        elements = []
        
        # Logo and Header
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        header_table = self.create_header_table(logo_path, medical_blue, medical_aqua)
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tagline Box
        tagline_box = self.create_tagline_box(medical_blue)
        elements.append(tagline_box)
        elements.append(Spacer(1, 0.4*inch))
        
        # Package 1
        p1_items = [
            "Professional clinic website (1–3 pages)",
            "Google My Business setup & optimization",
            "Clinic branding setup (colors, logo adjustments)",
            "Appointment booking button integration",
            "Basic WhatsApp CTA",
            "5–7 SEO-optimized service pages",
            "Mobile-first design",
            "Speed optimized"
        ]
        p1_outcomes = [
            "Professional online presence",
            "Patients can find clinic easily",
            "Google ranking starts improving"
        ]
        p1_content = self.create_package_box(
            "🔥 PACKAGE 1 — BASIC CLINIC PRESENCE",
            "(For doctors who need a clean online identity)",
            p1_items,
            p1_outcomes,
            "Small clinics, new clinics, or doctors with no online presence.",
            1,
            medical_blue,
            medical_aqua
        )
        elements.extend(p1_content)
        elements.append(PageBreak())
        
        # Package 2
        p2_items = [
            "Everything in BASIC, plus:",
            "",
            "<b>SEO + GMB Growth:</b>",
            "• 20+ SEO pages",
            "• Keyword optimization for local area",
            "• GMB ranking improvement",
            "• Monthly report",
            "",
            "<b>Website Enhancements:</b>",
            "• Condition-based pages",
            "• Before/After gallery",
            "• FAQ + blogs",
            "• Online appointment form",
            "• Photo/video integration",
            "",
            "<b>CRM Setup:</b>",
            "• Lead tracking (new & returning)",
            "• Appointment dashboard",
            "• Basic follow-up reminders"
        ]
        p2_outcomes = [
            "More appointments",
            "Higher Google visibility",
            "Strong reputation",
            "Online growth without ads"
        ]
        p2_content = self.create_package_box(
            "🔥 PACKAGE 2 — CLINIC GROWTH SYSTEM",
            "(For clinics that want more visibility & patient flow)",
            p2_items,
            p2_outcomes,
            "Growing clinics, specialists (dentist, ENT, gynae, ortho, neuro, etc.)",
            2,
            medical_blue,
            medical_aqua
        )
        elements.extend(p2_content)
        elements.append(PageBreak())
        
        # Package 3
        p3_items = [
            "Everything in BASIC + GROWTH, plus:",
            "",
            "<b>AI Automation Suite:</b>",
            "• 1️⃣ AI WhatsApp Auto-Responder - Instant replies 24/7 → no missed patients",
            "• 2️⃣ AI Appointment Reminder System - Reduces no-shows by 40%",
            "• 3️⃣ AI Follow-Up System - Automatic next-day & next-week follow-ups",
            "• 4️⃣ AI Review Booster - Automatically requests reviews → GMB skyrockets",
            "• 5️⃣ AI Chatbot for Website - Handles FAQs, captures patient details",
            "",
            "<b>Clinic CRM PRO:</b>",
            "• Lead pipeline",
            "• Patient database",
            "• Automated reminders",
            "• Staff access",
            "• Visit summary notes",
            "• \"Ready to treat\" dashboard",
            "",
            "<b>Marketing Automation:</b>",
            "• Monthly content plan",
            "• 8 branded posts",
            "• Clinic highlights / services",
            "• Weekly growth tips"
        ]
        p3_outcomes = [
            "20–50 new appointments/month",
            "40% fewer no-shows",
            "Strong GMB dominance",
            "More reviews than competitors",
            "Faster patient replies",
            "Doctor saves 1–2 hours daily",
            "Clinic becomes a digital machine"
        ]
        p3_content = self.create_package_box(
            "🔥🔥 PACKAGE 3 — AI PREMIUM: CLINIC GROWTH OS",
            "(For serious clinics who want automation + highest growth) — <b>This is your flagship.</b>",
            p3_items,
            p3_outcomes,
            "High-demand doctors, multi-chair clinics, specialists, premium practices.",
            3,
            medical_blue,
            medical_aqua
        )
        elements.extend(p3_content)
        elements.append(PageBreak())
        
        # Pricing Section with beautiful design
        pricing_header = Table([[
            Paragraph("<font size=22 color='#1e40af'><b>💰 PRICING</b></font><br/>"
                     "<font size=10 color='#6b7280'><i>(How YOU should present it)</i></font>",
                     ParagraphStyle('PricingHeader', alignment=TA_CENTER, leading=20))
        ]], colWidths=[7*inch])
        pricing_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#eff6ff')),
            ('BOX', (0, 0), (-1, -1), 2, medical_blue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        elements.append(pricing_header)
        elements.append(Spacer(1, 0.3*inch))
        
        pricing_text = Paragraph(
            "<font size=11 color='#374151'>Use a calm, premium, SaaS tone:</font><br/><br/>"
            "<font size=14 color='#1e40af'><b>Basic:</b></font> <font size=12 color='#374151'>₹X/month</font><br/>"
            "<font size=14 color='#1e40af'><b>Growth:</b></font> <font size=12 color='#374151'>₹XX/month</font><br/>"
            "<font size=14 color='#06b6d4'><b>AI Premium:</b></font> <font size=12 color='#374151'>₹XXX/month</font><br/><br/>"
            "<i><font size=10 color='#6b7280'>(Don't give exact numbers until you're on the call. Premium positioning = flexible pricing.)</font></i>",
            ParagraphStyle('Pricing', alignment=TA_CENTER, leading=18, spaceAfter=30)
        )
        elements.append(pricing_text)
        
        # Bonuses Section
        bonus_header = Table([[
            Paragraph("<font size=22 color='#1e40af'><b>🎯 BONUSES</b></font><br/>"
                     "<font size=11 color='#1e40af'><b>(to destroy competitors)</b></font>",
                     ParagraphStyle('BonusHeader', alignment=TA_CENTER, leading=20))
        ]], colWidths=[7*inch])
        bonus_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f0fdf4')),
            ('BOX', (0, 0), (-1, -1), 2, success_green),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        elements.append(bonus_header)
        elements.append(Spacer(1, 0.2*inch))
        
        bonus_intro = Paragraph(
            "<font size=11 color='#374151'>Add these as \"FREE bonuses\" to increase conversion:</font>",
            ParagraphStyle('BonusIntro', alignment=TA_CENTER, leading=16, spaceAfter=15)
        )
        elements.append(bonus_intro)
        
        bonus_items = [
            "Free GMB review guide",
            "Free clinic branding kit",
            "Free 30-second intro video",
            "Free month of AI posts",
            "Free website hosting for 1 year"
        ]
        
        bonus_list = []
        for item in bonus_items:
            bonus_list.append([
                Paragraph(f"<font size=11 color='#22c55e'>✔</font>",
                         ParagraphStyle('BonusCheck', alignment=TA_CENTER)),
                Paragraph(f"<font size=11 color='#374151'>{item}</font>",
                         ParagraphStyle('BonusItem', alignment=TA_LEFT, leading=16))
            ])
        
        bonus_table = Table(bonus_list, colWidths=[0.4*inch, 6.6*inch])
        bonus_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(bonus_table)
        elements.append(Spacer(1, 0.2*inch))
        
        bonus_closing = Paragraph(
            "<font size=13 color='#1e40af'><b>Doctors LOVE bonuses.</b></font>",
            ParagraphStyle('BonusClosing', alignment=TA_CENTER, leading=18)
        )
        elements.append(bonus_closing)
        
        # Footer
        elements.append(Spacer(1, 0.4*inch))
        footer_table = Table([[
            Paragraph(
                "<font size=10 color='#6b7280'><b>MediWellCare — Clinic Growth OS</b><br/>"
                "mediwellcare64@gmail.com | +91-9250757366</font>",
                ParagraphStyle('Footer', alignment=TA_CENTER, leading=14)
            )
        ]], colWidths=[7*inch])
        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f9fafb')),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(footer_table)
        
        # Build PDF with custom canvas for page numbers
        def on_first_page(canvas, doc):
            canvas.saveState()
            canvas.restoreState()
            
        def on_later_pages(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(HexColor('#6b7280'))
            page_text = f"Page {canvas.getPageNumber()}"
            canvas.drawRightString(A4[0] - 0.5*inch, 0.5*inch, page_text)
            canvas.restoreState()
        
        doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully created beautiful PDF at: {output_path}')
        )
