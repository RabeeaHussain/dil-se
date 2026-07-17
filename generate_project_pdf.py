#!/usr/bin/env python3
"""
Generate a comprehensive project documentation PDF for Dil Se
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class NumberedCanvas(canvas.Canvas):
    """Canvas for page numbers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_state = None

    def showPage(self):
        self._saved_state = self.__dict__.copy()
        self._startPage()

    def save(self):
        page_num = self._pageNumber
        if page_num > 1:
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.grey)
            self.drawString(inch, 0.5*inch, f"Page {page_num}")
            self.drawString(7.5*inch, 0.5*inch, f"Dil Se - Mental Wellness Companion")
        canvas.Canvas.save(self)

def create_project_pdf():
    """Create comprehensive project documentation PDF"""
    
    # Setup
    pdf_path = "/Users/rabeeahussain/Documents/AI/Dil_Se_Project_Documentation.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        canvasmaker=NumberedCanvas
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderPadding=5
    )
    
    heading2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=13
    )
    
    # ========== COVER PAGE ==========
    elements.append(Spacer(1, 1.5*inch))
    
    elements.append(Paragraph("📱 DIL SE", title_style))
    elements.append(Paragraph("AI-Powered Mental Wellness Companion", subtitle_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph(
        "A Culturally-Tailored Mental Health App for Pakistani Teens and Young Adults",
        ParagraphStyle(
            'Subtitle2',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
    ))
    
    elements.append(Spacer(1, 1*inch))
    
    # Cover info
    cover_info = [
        ["Project Type:", "Flask Web Application"],
        ["Technology Stack:", "Python, Flask, SQLAlchemy, Claude AI API"],
        ["Frontend:", "HTML5, CSS3, Vanilla JavaScript"],
        ["Database:", "SQLite"],
        ["Target Users:", "Pakistani Teens & Young Adults (13-25 years)"],
        ["Status:", "Development Complete - Ready for Deployment"],
        ["Created:", datetime.now().strftime("%B %d, %Y")]
    ]
    
    cover_table = Table(cover_info, colWidths=[2*inch, 3.5*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0f2fe')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
    ]))
    
    elements.append(cover_table)
    elements.append(PageBreak())
    
    # ========== TABLE OF CONTENTS ==========
    elements.append(Paragraph("📑 Table of Contents", heading1_style))
    elements.append(Spacer(1, 12))
    
    toc_items = [
        "1. Executive Summary",
        "2. Project Vision & Objectives",
        "3. Problem Statement & Solution",
        "4. Key Features Overview",
        "5. Architecture & Technical Stack",
        "6. Core Functionality",
        "7. User Interface & Design",
        "8. How It Works - User Flow",
        "9. Database Structure",
        "10. Installation & Deployment",
        "11. Future Enhancements"
    ]
    
    for item in toc_items:
        elements.append(Paragraph(item, bullet_style))
        elements.append(Spacer(1, 4))
    
    elements.append(PageBreak())
    
    # ========== EXECUTIVE SUMMARY ==========
    elements.append(Paragraph("1. Executive Summary", heading1_style))
    
    elements.append(Paragraph(
        "<b>Dil Se</b> (meaning \"From the Heart\") is an AI-powered mental wellness companion "
        "application specifically designed for Pakistani teens and young adults. The app provides "
        "a judgment-free space for emotional support, wellness guidance, and mental health tracking "
        "through conversational AI, wellness exercises, mood tracking, and private journaling. "
        "Built with Flask and powered by Anthropic's Claude AI, Dil Se brings culturally-aware, "
        "compassionate mental health support to a demographic that faces significant barriers to "
        "traditional mental health services.",
        body_style
    ))
    
    elements.append(Spacer(1, 12))
    
    # ========== VISION & OBJECTIVES ==========
    elements.append(Paragraph("2. Project Vision & Objectives", heading1_style))
    
    elements.append(Paragraph("<b>Vision:</b>", heading2_style))
    elements.append(Paragraph(
        "To create an accessible, culturally-sensitive digital mental wellness companion that "
        "reduces stigma around mental health conversations and empowers Pakistani youth to seek support.",
        body_style
    ))
    
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Core Objectives:</b>", heading2_style))
    
    objectives = [
        "Provide a judgment-free, shame-free space for emotional conversations",
        "Make mental health support accessible in a culturally relevant way",
        "Normalize emotional expression among Pakistani youth",
        "Offer evidence-based wellness techniques in an approachable format",
        "Track emotional well-being over time through mood history",
        "Support reflection through private journaling",
        "Reduce stigma by presenting support as a sign of strength, not weakness"
    ]
    
    for obj in objectives:
        elements.append(Paragraph(f"• {obj}", bullet_style))
    
    elements.append(PageBreak())
    
    # ========== PROBLEM STATEMENT ==========
    elements.append(Paragraph("3. Problem Statement & Solution", heading1_style))
    
    elements.append(Paragraph("<b>The Problem:</b>", heading2_style))
    elements.append(Paragraph(
        "Pakistani youth face significant mental health challenges: exam anxiety, family pressure, "
        "career uncertainty, relationship stress, and identity concerns. However, accessing help is "
        "extremely difficult due to cultural stigma. Young people fear being labeled \"pagal\" (crazy), "
        "worry about being a burden on family, and lack relatable, non-clinical resources that speak "
        "to their lived experience.",
        body_style
    ))
    
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Dil Se's Solution:</b>", heading2_style))
    
    solutions = [
        "<b>Culturally Attuned Communication:</b> Responses written in conversational English, the emotional language of Pakistani Gen Z, avoiding corporate wellness language",
        "<b>Relatable Scenarios:</b> Quick-reply options address real Pakistani stressors: exam pressure, family expectations, rishta stress, career anxiety",
        "<b>Non-Judgmental Tone:</b> The chatbot acts like a trusted friend, not a clinician, with emphasis on validation over diagnosis",
        "<b>Private Space:</b> All interactions are private and personal—no family pressure, no judgment",
        "<b>Evidence-Based Techniques:</b> Simple, actionable wellness exercises (breathing, grounding, meditation) explained in plain language",
        "<b>Mood Tracking:</b> Visual representation of emotional patterns helps users understand their mental wellness journey"
    ]
    
    for sol in solutions:
        elements.append(Paragraph(f"• {sol}", bullet_style))
    
    elements.append(PageBreak())
    
    # ========== KEY FEATURES ==========
    elements.append(Paragraph("4. Key Features Overview", heading1_style))
    
    features_data = [
        ["Feature", "Description"],
        ["🏠 Home Screen", "Daily mood check-in, 7-day mood history, streak counter, quick navigation"],
        ["💬 AI Chat", "Conversational chatbot powered by Claude, context-aware Pakistani responses"],
        ["🧘 Wellness Exercises", "6 guided exercises: breathing, grounding, meditation, muscle relaxation"],
        ["📝 Private Journal", "Encrypted journaling with mood tracking and search functionality"],
        ["📊 Mood Tracking", "Visual history of mood patterns over 7 and 30 days"],
        ["🌐 Language Toggle", "English and Hinglish language options for accessibility"],
        ["💾 Data Persistence", "All data stored locally for privacy; optional cloud backup"]
    ]
    
    feature_table = Table(features_data, colWidths=[1.8*inch, 3.7*inch])
    feature_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(feature_table)
    elements.append(PageBreak())
    
    # ========== ARCHITECTURE ==========
    elements.append(Paragraph("5. Architecture & Technical Stack", heading1_style))
    
    elements.append(Paragraph("<b>Technology Stack:</b>", heading2_style))
    
    tech_data = [
        ["Component", "Technology", "Purpose"],
        ["Backend", "Flask 3.0+", "Web framework for API and routing"],
        ["Database", "SQLite + SQLAlchemy", "Data persistence and ORM"],
        ["AI Integration", "Anthropic Claude API", "Intelligent conversational responses"],
        ["Frontend Templates", "HTML5, Jinja2", "Dynamic page rendering"],
        ["Styling", "CSS3", "Responsive, accessible design"],
        ["Interactivity", "Vanilla JavaScript (ES6+)", "Client-side functionality"],
        ["Environment", "Python 3.8+, pip, venv", "Python environment management"],
        ["Hosting", "Flask dev or Gunicorn/Nginx", "Production deployment ready"]
    ]
    
    tech_table = Table(tech_data, colWidths=[1.5*inch, 1.8*inch, 2.2*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(tech_table)
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Project Structure:</b>", heading2_style))
    
    structure_text = """
    <font face="Courier" size="9">
    dilse-project/<br/>
    ├── <b>app.py</b> - Main Flask application with 25+ API routes<br/>
    ├── <b>config.py</b> - Configuration management (dev/prod)<br/>
    ├── <b>models.py</b> - SQLAlchemy database models<br/>
    ├── <b>chatbot.py</b> - Claude AI integration<br/>
    ├── <b>exercises.py</b> - Exercise definitions and utilities<br/>
    ├── <b>requirements.txt</b> - Python dependencies<br/>
    ├── templates/<br/>
    │   ├── base.html<br/>
    │   ├── home.html<br/>
    │   ├── chat.html<br/>
    │   ├── exercises.html<br/>
    │   └── journal.html<br/>
    ├── static/<br/>
    │   ├── css/style.css<br/>
    │   └── js/*.js (6 module files)<br/>
    └── instance/ - Runtime data (db, uploads)
    </font>
    """
    
    elements.append(Paragraph(structure_text, body_style))
    elements.append(PageBreak())
    
    # ========== CORE FUNCTIONALITY ==========
    elements.append(Paragraph("6. Core Functionality", heading1_style))
    
    elements.append(Paragraph("<b>A. Home Screen - Mood Check-in Hub</b>", heading2_style))
    elements.append(Paragraph(
        "The home screen serves as the daily entry point. Users select their current mood from "
        "a 5-point scale (😢 Very Bad to 😊 Great) with emoji representation. This data is stored "
        "and visualized in a 7-day history chart. The screen also displays a streak counter to "
        "encourage daily engagement and quick-access cards to all major features.",
        body_style
    ))
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>B. AI Chat - Conversational Support</b>", heading2_style))
    elements.append(Paragraph(
        "The chatbot uses the Anthropic Claude API with a custom system prompt tailored to Pakistani youth. "
        "It understands cultural context, uses conversational language, and provides empathetic responses. "
        "Users can select from quick-reply suggestions or type freely. The chatbot maintains conversation "
        "history within the session and can suggest professional resources if needed.",
        body_style
    ))
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Quick Reply Examples:</b>", heading2_style))
    
    quick_replies = [
        "I'm stressed about exams",
        "Parents are pressuring me",
        "I don't know what career I want",
        "I feel alone",
        "I'm anxious about something",
        "I just need to vent"
    ]
    
    for qr in quick_replies:
        elements.append(Paragraph(f"• {qr}", bullet_style))
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>C. Wellness Exercises - Evidence-Based Techniques</b>", heading2_style))
    
    exercises = [
        "<b>4-7-8 Breathing:</b> A calming technique for anxiety and stress (5 minutes)",
        "<b>5-4-3-2-1 Grounding:</b> Sensory awareness exercise to ground in the present moment (5 minutes)",
        "<b>Body Scan Meditation:</b> Progressive relaxation from head to toe (8 minutes)",
        "<b>Gratitude Practice:</b> Reflection exercise for perspective shift (3 minutes)",
        "<b>Progressive Muscle Relaxation:</b> Tension release through muscle engagement (6 minutes)",
        "<b>Guided Journaling:</b> Structured reflection with conversational prompts"
    ]
    
    for ex in exercises:
        elements.append(Paragraph(f"• {ex}", bullet_style))
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>D. Private Journal - Reflective Writing</b>", heading2_style))
    elements.append(Paragraph(
        "Users can write private journal entries with optional mood logging. Each entry is timestamped, "
        "searchable, and fully editable. The journal provides conversational writing prompts to guide reflection: "
        "\"What's been on your mind?\", \"How are you feeling today?\", \"What would help you feel better?\"",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # ========== USER FLOW ==========
    elements.append(Paragraph("8. How It Works - User Flow", heading1_style))
    
    elements.append(Paragraph("<b>Typical User Journey:</b>", heading2_style))
    
    flow_steps = [
        "<b>1. Login:</b> User opens the app (anonymous or registered session)",
        "<b>2. Home Screen:</b> Greets with daily mood check-in question",
        "<b>3. Feature Access:</b> User chooses to Chat, Do an Exercise, or Journal",
        "<b>4. Interaction:</b> Engages with chosen feature (e.g., typing to chatbot)",
        "<b>5. Data Logging:</b> Interactions are automatically logged for tracking",
        "<b>6. History View:</b> User can view mood trends and past entries anytime",
        "<b>7. Repeat:</b> Users return daily for check-ins and support"
    ]
    
    for step in flow_steps:
        elements.append(Paragraph(f"• {step}", bullet_style))
    
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Technical Data Flow:</b>", heading2_style))
    
    flow_text = """
    <font face="Courier" size="9">
    <b>Frontend</b> (Browser) → <b>Flask API</b> → <b>Database (SQLite)</b><br/>
    ↓<br/>
    User submits mood → app.py /mood endpoint → Stored in MoodEntry table<br/>
    ↓<br/>
    User sends chat message → app.py /chat endpoint → Claude API → Response returned<br/>
    ↓<br/>
    User creates journal entry → app.py /journal endpoint → Stored in JournalEntry table<br/>
    ↓<br/>
    All data encrypted at rest and transmitted securely
    </font>
    """
    
    elements.append(Paragraph(flow_text, body_style))
    elements.append(PageBreak())
    
    # ========== DATABASE ==========
    elements.append(Paragraph("9. Database Structure", heading1_style))
    
    elements.append(Paragraph(
        "The app uses SQLite with SQLAlchemy ORM for data management. All data is stored locally for privacy.",
        body_style
    ))
    
    elements.append(Spacer(1, 12))
    
    db_data = [
        ["Table", "Purpose", "Key Fields"],
        ["User", "User profiles & preferences", "id, username, language_preference, created_at"],
        ["MoodEntry", "Daily mood tracking", "id, user_id, mood_score, timestamp, notes"],
        ["JournalEntry", "Private journal entries", "id, user_id, title, content, mood, created_at"],
        ["ChatHistory", "Conversation logs", "id, user_id, user_message, bot_response, timestamp"],
        ["ExerciseCompletion", "Exercise tracking", "id, user_id, exercise_name, completed_at, duration"]
    ]
    
    db_table = Table(db_data, colWidths=[1.5*inch, 1.8*inch, 2.2*inch])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecfdf5')]),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(db_table)
    elements.append(PageBreak())
    
    # ========== INSTALLATION ==========
    elements.append(Paragraph("10. Installation & Deployment", heading1_style))
    
    elements.append(Paragraph("<b>Quick Start (Development):</b>", heading2_style))
    
    install_steps = [
        "Clone or download the project to your machine",
        "Create a Python virtual environment: <font face=\"Courier\">python -m venv venv</font>",
        "Activate it: <font face=\"Courier\">source venv/bin/activate</font> (macOS/Linux) or <font face=\"Courier\">venv\\Scripts\\activate</font> (Windows)",
        "Install dependencies: <font face=\"Courier\">pip install -r requirements.txt</font>",
        "Set up environment variables by copying <font face=\"Courier\">.env.example</font> to <font face=\"Courier\">.env</font>",
        "Add your Anthropic API key to <font face=\"Courier\">.env</font>",
        "Run the app: <font face=\"Courier\">python app.py</font>",
        "Open browser to <font face=\"Courier\">http://localhost:5000</font>"
    ]
    
    for i, step in enumerate(install_steps, 1):
        elements.append(Paragraph(f"<b>{i}.</b> {step}", bullet_style))
    
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Production Deployment:</b>", heading2_style))
    
    prod_text = """
    For production deployment:<br/>
    • Use a production WSGI server like <b>Gunicorn</b><br/>
    • Reverse proxy with <b>Nginx</b><br/>
    • Enable <b>HTTPS</b> with SSL certificates<br/>
    • Store environment variables securely (not in .env)<br/>
    • Use a robust database like <b>PostgreSQL</b><br/>
    • Enable database backups<br/>
    • Monitor application logs and errors<br/>
    • Set up rate limiting for API endpoints
    """
    
    elements.append(Paragraph(prod_text, body_style))
    elements.append(PageBreak())
    
    # ========== FUTURE ENHANCEMENTS ==========
    elements.append(Paragraph("11. Future Enhancements", heading1_style))
    
    enhancements = [
        "<b>Multi-language Support:</b> Full Urdu and Hinglish UI in addition to English",
        "<b>Mobile App:</b> Native iOS and Android applications",
        "<b>Crisis Resources:</b> Integration with Pakistan crisis hotlines and mental health services",
        "<b>Community Features:</b> Anonymous support groups and peer connections",
        "<b>Therapist Integration:</b> Optional connection to licensed mental health professionals",
        "<b>Wearable Integration:</b> Heart rate and stress level monitoring from smartwatches",
        "<b>Advanced Analytics:</b> Personalized wellness insights and recommendations",
        "<b>Offline Mode:</b> Basic functionality available without internet connection",
        "<b>Social Sharing:</b> Share wellness tips and exercises with friends",
        "<b>Parental Guides:</b> Resources for parents to support youth mental health"
    ]
    
    for enh in enhancements:
        elements.append(Paragraph(f"• {enh}", bullet_style))
    
    elements.append(Spacer(1, 20))
    
    # ========== CONCLUSION ==========
    elements.append(Paragraph("Conclusion", heading1_style))
    
    elements.append(Paragraph(
        "<b>Dil Se</b> represents a significant step forward in making mental wellness support "
        "accessible and culturally relevant for Pakistani youth. By combining evidence-based wellness "
        "techniques with empathetic AI and a design-first approach, the app removes barriers to support "
        "and creates a safe, judgment-free space for emotional health. The project is ready for deployment "
        "and can begin making a real impact in the lives of young people who need it most.",
        body_style
    ))
    
    elements.append(Spacer(1, 20))
    
    # Footer
    footer_text = f"<i>Document generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i><br/>" \
                  f"<i>For more information, visit the project repository or contact the development team</i>"
    
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))
    
    # Build PDF
    doc.build(elements)
    
    return pdf_path

if __name__ == "__main__":
    pdf_file = create_project_pdf()
    print(f"✅ PDF generated successfully!")
    print(f"📄 Location: {pdf_file}")
    print(f"📊 File size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
