#!/usr/bin/env python3
"""
PARVAT-SETU Project Proposal PDF Generator
AI-GIS Integrated Social Enterprise Platform for Smallholder Livelihoods
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Preformatted)
from reportlab.platypus.tableofcontents import TableOfContents
import os

OUTPUT_PDF = '/projects/sandbox/mobile-printer-app/PARVAT_SETU_Project_Proposal.pdf'

# ===================== STYLES =====================
styles = getSampleStyleSheet()
TitleStyle = ParagraphStyle('CustomTitle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=20, alignment=TA_CENTER,
    textColor=colors.HexColor('#1a4d2e'), spaceAfter=18, leading=24)
SubtitleStyle = ParagraphStyle('CustomSubtitle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=14, alignment=TA_CENTER,
    textColor=colors.HexColor('#2d5f3f'), spaceAfter=14, leading=18)
H1 = ParagraphStyle('H1', parent=styles['Heading1'],
    fontName='Helvetica-Bold', fontSize=15, textColor=colors.HexColor('#1a4d2e'),
    spaceAfter=10, spaceBefore=14, leading=18, borderPadding=4,
    borderColor=colors.HexColor('#1a4d2e'), borderWidth=0)
H2 = ParagraphStyle('H2', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#2d5f3f'),
    spaceAfter=8, spaceBefore=10, leading=15)
H3 = ParagraphStyle('H3', parent=styles['Heading3'],
    fontName='Helvetica-BoldOblique', fontSize=11, textColor=colors.HexColor('#3d6f4f'),
    spaceAfter=6, spaceBefore=8, leading=14)
Body = ParagraphStyle('Body', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=11, alignment=TA_JUSTIFY,
    spaceAfter=8, leading=15, firstLineIndent=18)
BodyNoIndent = ParagraphStyle('BodyNI', parent=Body, firstLineIndent=0)
Bullet = ParagraphStyle('Bullet', parent=Body, leftIndent=24, firstLineIndent=-12,
    spaceAfter=4, leading=14)
Caption = ParagraphStyle('Caption', parent=styles['Normal'],
    fontName='Helvetica-BoldOblique', fontSize=10, alignment=TA_CENTER,
    textColor=colors.HexColor('#1a4d2e'), spaceAfter=6, spaceBefore=10)
Mono = ParagraphStyle('Mono', parent=styles['Normal'],
    fontName='Courier', fontSize=8, leading=10, alignment=TA_LEFT, leftIndent=0)
CenterBold = ParagraphStyle('CenterBold', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, leading=15, spaceAfter=6)
Center = ParagraphStyle('Center', parent=styles['Normal'],
    fontName='Helvetica', fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=4)

story = []

def H(text, level=1):
    if level==1: story.append(Paragraph(text, H1))
    elif level==2: story.append(Paragraph(text, H2))
    elif level==3: story.append(Paragraph(text, H3))
def P(text): story.append(Paragraph(text, Body))
def PNI(text): story.append(Paragraph(text, BodyNoIndent))
def B(text): story.append(Paragraph(f"• {text}", Bullet))
def CAP(text): story.append(Paragraph(text, Caption))
def MONO(text):
    for line in text.split('\n'):
        line = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        story.append(Preformatted(line, Mono))
def SP(h=8): story.append(Spacer(1, h))
def BR(): story.append(PageBreak())

def TBL(headers, rows, col_widths=None, header_color='#1a4d2e'):
    data = [headers] + rows
    if col_widths is None:
        page_w = A4[0] - 2*inch
        col_widths = [page_w/len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(header_color)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1a4d2e')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f5f0')]),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    SP(8)

# ===================== TITLE PAGE =====================
SP(40)
story.append(Paragraph('GRANT PROJECT FUNDING PROPOSAL', TitleStyle))
SP(6)
story.append(Paragraph('(Pilot Initiative — Social Enterprise Model)', 
    ParagraphStyle('TitleSub', parent=styles['Normal'], fontName='Helvetica-Oblique',
    fontSize=11, alignment=TA_CENTER, textColor=colors.HexColor('#666666'))))
SP(40)

story.append(Paragraph('<b>PARVAT-SETU</b><br/><font size="14">(पर्वत-सेतु — "Mountain Bridge")</font>', 
    ParagraphStyle('PT', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22,
    alignment=TA_CENTER, textColor=colors.HexColor('#1a4d2e'), leading=28, spaceAfter=12)))

SP(12)
story.append(Paragraph(
    'An Artificial Intelligence and Geospatial-Integrated<br/>'
    'Social Enterprise Platform for Digital Aggregation,<br/>'
    'Financial Inclusion, and Sustainable Livelihoods<br/>'
    'of Smallholder Producers in the Indian Himalayan Region',
    ParagraphStyle('PSub', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=14,
    alignment=TA_CENTER, textColor=colors.HexColor('#2d5f3f'), leading=20)))

SP(40)
story.append(Paragraph(
    '<b>A Pilot Project Proposal Integrating:</b><br/>'
    'Sustainable Development &nbsp;|&nbsp; Artificial Intelligence (AI/ML)<br/>'
    'Geographic Information Systems (GIS) &nbsp;|&nbsp; Social Enterprise',
    ParagraphStyle('Theme', parent=styles['Normal'], fontName='Helvetica-Bold',
    fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), leading=18)))

SP(40)
story.append(Paragraph(
    '<b>Submitted to:</b><br/>'
    'Indian Council of Social Science Research (ICSSR) /<br/>'
    'National Bank for Agriculture and Rural Development (NABARD) /<br/>'
    'Ministry of Skill Development &amp; Entrepreneurship /<br/>'
    'NITI Aayog Atal Innovation Mission /<br/>'
    'Bharat Rural Livelihoods Foundation (BRLF) /<br/>'
    'Tata Trusts / Bill &amp; Melinda Gates Foundation /<br/>'
    'Rockefeller Foundation Asia Programme',
    ParagraphStyle('Submit', parent=styles['Normal'], fontName='Helvetica',
    fontSize=11, alignment=TA_CENTER, leading=15)))
SP(20)

story.append(Paragraph(
    '<b>Submitted by:</b><br/>'
    '<b>Department of Environmental Science</b><br/>'
    '<b>DBS Global University, Dehradun</b><br/>'
    'Uttarakhand, India',
    ParagraphStyle('SubmitBy', parent=styles['Normal'], fontName='Helvetica',
    fontSize=12, alignment=TA_CENTER, leading=16)))
SP(12)

story.append(Paragraph(
    '<b>Project Investigator (PI):</b> Dr. Nidhi Rawat, Assistant Professor<br/>'
    '<b>Co-PI / Research Scholar:</b> Raj Amritam, PhD Scholar',
    ParagraphStyle('PIs', parent=styles['Normal'], fontName='Helvetica',
    fontSize=11, alignment=TA_CENTER, leading=15)))

SP(20)
story.append(Paragraph('<b>2025</b>', 
    ParagraphStyle('Yr', parent=styles['Normal'], fontName='Helvetica-Bold',
    fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor('#1a4d2e'))))

BR()

# Save partial file
doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4,
    rightMargin=0.85*inch, leftMargin=0.85*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
    title='PARVAT-SETU Pilot Project Proposal',
    author='Dr. Nidhi Rawat, Raj Amritam')
doc.build(story)
print(f"Title page generated: {os.path.getsize(OUTPUT_PDF):,} bytes")
