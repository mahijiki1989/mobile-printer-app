#!/usr/bin/env python3
"""
PARVAT-SETU Impact Investor Proposal PDF Generator
Generates a comprehensive 40-55 page impact investor pitch + business plan
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import mm
import os

# ============================================================
# COLOR SCHEME
# ============================================================
GREEN_DARK = HexColor('#1a4d2e')
GREEN_MED = HexColor('#2d7a4f')
GREEN_LIGHT = HexColor('#e8f5e9')
GREEN_ACCENT = HexColor('#4caf50')
GOLD = HexColor('#c8a415')
GRAY_LIGHT = HexColor('#f5f5f5')
GRAY_MED = HexColor('#e0e0e0')
GRAY_DARK = HexColor('#333333')

# ============================================================
# PAGE SETUP
# ============================================================
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 0.7 * inch
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

OUTPUT_PATH = '/projects/sandbox/mobile-printer-app/PARVAT_SETU_Impact_Investor_Proposal.pdf'

# ============================================================
# STYLES
# ============================================================
def get_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=GREEN_DARK, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18,
        textColor=GREEN_MED, alignment=TA_CENTER, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'CoverTagline', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=12, leading=16,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'Heading1Green', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=GREEN_DARK, spaceAfter=12, spaceBefore=16
    ))
    styles.add(ParagraphStyle(
        'Heading2Green', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=GREEN_MED, spaceAfter=8, spaceBefore=12
    ))
    styles.add(ParagraphStyle(
        'Heading3Green', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=GREEN_DARK, spaceAfter=6, spaceBefore=8
    ))
    styles['BodyText'].fontName = 'Times-Roman'
    styles['BodyText'].fontSize = 11
    styles['BodyText'].leading = 16.5
    styles['BodyText'].textColor = GRAY_DARK
    styles['BodyText'].alignment = TA_JUSTIFY
    styles['BodyText'].spaceAfter = 6
    styles.add(ParagraphStyle(
        'BodyBold', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=11, leading=16.5,
        textColor=GRAY_DARK, alignment=TA_JUSTIFY, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11, leading=16.5,
        textColor=GRAY_DARK, leftIndent=20, spaceAfter=4,
        bulletIndent=10, bulletFontSize=11
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=white, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=9, leading=12,
        textColor=GRAY_DARK, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'TableCellCenter', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=9, leading=12,
        textColor=GRAY_DARK, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=GRAY_DARK, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'FooterStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=GREEN_MED, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'SectionIntro', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=11, leading=16,
        textColor=GREEN_MED, spaceAfter=10, spaceBefore=4
    ))
    styles.add(ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=GREEN_DARK, alignment=TA_CENTER,
        spaceBefore=10, spaceAfter=10,
        borderColor=GREEN_LIGHT, borderWidth=1, borderPadding=8,
        backColor=GREEN_LIGHT
    ))
    return styles

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def make_table(data, col_widths=None, header_rows=1):
    """Create a styled table with green headers"""
    if col_widths is None:
        col_widths = [CONTENT_WIDTH / len(data[0])] * len(data[0])
    
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style_commands = [
        ('BACKGROUND', (0, 0), (-1, header_rows - 1), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, header_rows - 1), white),
        ('FONTNAME', (0, 0), (-1, header_rows - 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, header_rows - 1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN_MED),
        ('ROWBACKGROUNDS', (0, header_rows), (-1, -1), [white, GREEN_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style_commands))
    return t

def P(text, style_name='BodyText', styles=None):
    """Quick paragraph creation"""
    return Paragraph(text, styles[style_name])

def spacer(h=12):
    return Spacer(1, h)

def section_break():
    return HRFlowable(width="100%", thickness=1, color=GREEN_MED, spaceAfter=10, spaceBefore=10)

# ============================================================
# DOCUMENT CONTENT SECTIONS
# ============================================================
def build_cover_page(story, styles):
    """Cover Page - PARVAT-SETU Impact Investment Opportunity"""
    story.append(spacer(60))
    story.append(Paragraph("IMPACT INVESTMENT OPPORTUNITY", styles['CoverSubtitle']))
    story.append(spacer(20))
    story.append(Paragraph("PARVAT-SETU", styles['CoverTitle']))
    story.append(Paragraph("Mountain Bridge", styles['CoverSubtitle']))
    story.append(spacer(16))
    story.append(HRFlowable(width="60%", thickness=2, color=GOLD, spaceAfter=16, spaceBefore=8))
    story.append(Paragraph(
        "AI-Powered Social Enterprise for Himalayan<br/>Smallholder Economic Inclusion",
        styles['CoverSubtitle']
    ))
    story.append(spacer(12))
    story.append(Paragraph(
        '"A Blended Finance Opportunity Combining 25%+ IRR with Deep Social Impact"',
        styles['CoverTagline']
    ))
    story.append(spacer(40))

    # Info box
    info_data = [
        [Paragraph("<b>Sector</b>", styles['TableCell']),
         Paragraph("AgriTech / Impact Social Enterprise", styles['TableCell'])],
        [Paragraph("<b>Geography</b>", styles['TableCell']),
         Paragraph("Indian Himalayan Region (IHR), Initial: Uttarakhand", styles['TableCell'])],
        [Paragraph("<b>Stage</b>", styles['TableCell']),
         Paragraph("Seed / Pre-Series A (Research-validated)", styles['TableCell'])],
        [Paragraph("<b>Funding Ask</b>", styles['TableCell']),
         Paragraph("INR 5 Crore (Blended: Grant + Equity + Debt)", styles['TableCell'])],
        [Paragraph("<b>Target IRR</b>", styles['TableCell']),
         Paragraph("25-35% for equity investors (5-8 year horizon)", styles['TableCell'])],
        [Paragraph("<b>Impact Target</b>", styles['TableCell']),
         Paragraph("50,000 smallholder families, 200% income uplift", styles['TableCell'])],
    ]
    info_table = Table(info_data, colWidths=[1.8*inch, 4.5*inch])
    info_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN_MED),
        ('BACKGROUND', (0, 0), (0, -1), GREEN_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(spacer(30))
    
    # Team
    story.append(Paragraph("<b>Project Leadership</b>", styles['CoverSubtitle']))
    story.append(spacer(8))
    story.append(Paragraph("Dr. Nidhi Rawat, Assistant Professor (Principal Investigator)", styles['BodyText']))
    story.append(Paragraph("Raj Amritam, PhD Scholar (Co-Principal Investigator)", styles['BodyText']))
    story.append(Paragraph("Department of Environmental Science, DBS Global University, Dehradun", styles['BodyText']))
    story.append(spacer(20))
    story.append(Paragraph("CONFIDENTIAL - FOR QUALIFIED IMPACT INVESTORS ONLY", styles['FooterStyle']))
    story.append(Paragraph("Document Version 1.0 | December 2024", styles['FooterStyle']))
    story.append(PageBreak())


def build_objectives_section(story, styles):
    """Section: Objectives of the Study - Clear, specific, measurable objectives"""
    story.append(Paragraph("OBJECTIVES OF THE STUDY", styles['Heading1Green']))
    story.append(Paragraph(
        "Clear, Specific, and Measurable Research and Project Objectives",
        styles['SectionIntro']
    ))
    story.append(spacer(8))

    story.append(Paragraph(
        "The PARVAT-SETU project is guided by five clearly defined objectives that integrate "
        "technological innovation, financial inclusion, supply chain optimization, institutional "
        "sustainability, and rigorous impact evaluation. Each objective is designed to be specific, "
        "measurable, achievable, relevant, and time-bound (SMART).",
        styles['BodyText']
    ))
    story.append(spacer(10))

    story.append(Paragraph("Objective 1: Digital Platform Development and Market Access", styles['Heading2Green']))
    story.append(Paragraph(
        "To develop and deploy an AI-GIS integrated digital platform that enables 5,000 smallholder "
        "producers in the Garhwal Himalayan Region to access premium markets through digital aggregation, "
        "achieving 35-50% increase in net farm-gate income within 24 months of platform engagement.",
        styles['BodyText']
    ))
    story.append(spacer(8))

    story.append(Paragraph("Objective 2: Financial Inclusion Architecture", styles['Heading2Green']))
    story.append(Paragraph(
        "To design and implement an AI-powered financial inclusion architecture - including alternative-data "
        "credit scoring, bundled insurance products, and embedded digital payments - achieving 100% financial "
        "inclusion (bank account + insurance + working capital credit access) for all participating households.",
        styles['BodyText']
    ))
    story.append(spacer(8))

    story.append(Paragraph("Objective 3: Supply Chain Infrastructure Optimization", styles['Heading2Green']))
    story.append(Paragraph(
        "To establish a GIS-optimized supply chain infrastructure comprising three cluster collection centres "
        "and cold-chain logistics network, reducing post-harvest losses by 25-35% and per-unit logistics costs "
        "by 30-45% through demand forecasting and route optimization.",
        styles['BodyText']
    ))
    story.append(spacer(8))

    story.append(Paragraph("Objective 4: Institutional Sustainability Validation", styles['Heading2Green']))
    story.append(Paragraph(
        "To validate the cooperative social enterprise governance model (Producer Company structure) as a "
        "financially sustainable institutional framework, demonstrating trajectory to operational break-even "
        "within 36 months post-pilot through diversified revenue streams (commissions, processing margins, "
        "buyer subscriptions, data services).",
        styles['BodyText']
    ))
    story.append(spacer(8))

    story.append(Paragraph("Objective 5: Impact Evidence Generation and Replicability", styles['Heading2Green']))
    story.append(Paragraph(
        "To generate rigorous impact evidence through quasi-experimental evaluation (difference-in-differences "
        "with matched control villages), producing 3-4 SCIE-indexed publications and a replication playbook "
        "deployable across 25+ Himalayan districts at 50-65% reduced unit cost.",
        styles['BodyText']
    ))
    story.append(spacer(12))

    # Summary Table of Objectives
    story.append(Paragraph("Objectives Summary Matrix", styles['Heading2Green']))
    obj_data = [
        [Paragraph("<b>Objective</b>", styles['TableHeader']),
         Paragraph("<b>Key Target</b>", styles['TableHeader']),
         Paragraph("<b>Timeline</b>", styles['TableHeader']),
         Paragraph("<b>Measurement</b>", styles['TableHeader'])],
        [Paragraph("1. Digital Platform &amp; Market Access", styles['TableCellBold']),
         Paragraph("5,000 producers; 35-50% income increase", styles['TableCell']),
         Paragraph("24 months", styles['TableCellCenter']),
         Paragraph("Farm-gate price comparison; platform analytics", styles['TableCell'])],
        [Paragraph("2. Financial Inclusion", styles['TableCellBold']),
         Paragraph("100% financial inclusion for participants", styles['TableCell']),
         Paragraph("24 months", styles['TableCellCenter']),
         Paragraph("Bank account, insurance, credit access rates", styles['TableCell'])],
        [Paragraph("3. Supply Chain Optimization", styles['TableCellBold']),
         Paragraph("25-35% loss reduction; 30-45% cost reduction", styles['TableCell']),
         Paragraph("18 months", styles['TableCellCenter']),
         Paragraph("Post-harvest loss audit; logistics cost per unit", styles['TableCell'])],
        [Paragraph("4. Institutional Sustainability", styles['TableCellBold']),
         Paragraph("Break-even trajectory within 36 months", styles['TableCell']),
         Paragraph("36 months", styles['TableCellCenter']),
         Paragraph("Revenue vs. operating costs; governance audit", styles['TableCell'])],
        [Paragraph("5. Impact Evidence", styles['TableCellBold']),
         Paragraph("3-4 SCIE publications; replication playbook", styles['TableCell']),
         Paragraph("30 months", styles['TableCellCenter']),
         Paragraph("Publication count; DiD impact estimates", styles['TableCell'])],
    ]
    story.append(make_table(obj_data, col_widths=[1.6*inch, 2.0*inch, 1.1*inch, 1.9*inch]))
    story.append(PageBreak())


def build_methodology_section(story, styles):
    """Section: Detailed Methodology - Proper academic research/project methodology"""
    story.append(Paragraph("DETAILED METHODOLOGY", styles['Heading1Green']))
    story.append(Paragraph(
        "Rigorous Mixed-Methods Research Design with Technology Development Framework",
        styles['SectionIntro']
    ))
    story.append(spacer(8))

    # 1. Research Design
    story.append(Paragraph("1. Research Design", styles['Heading2Green']))
    story.append(Paragraph(
        "The study employs a mixed-methods quasi-experimental design combining quantitative impact "
        "evaluation with qualitative process documentation:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    research_design = [
        "<b>Quantitative Component:</b> Pre-post difference-in-differences (DiD) estimation with propensity-score-matched control villages to establish causal attribution of platform impact on income, financial inclusion, and food security outcomes.",
        "<b>Qualitative Component:</b> Process tracing methodology to document implementation pathways, beneficiary case studies using narrative inquiry, and stakeholder Focus Group Discussions (FGDs) to capture contextual mechanisms of change.",
        "<b>Integration Strategy:</b> Sequential explanatory design where quantitative findings inform qualitative inquiry, enabling both measurement and explanation of impact.",
    ]
    for r in research_design:
        story.append(Paragraph(r, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))

    # 2. Study Area & Population
    story.append(Paragraph("2. Study Area and Population", styles['Heading2Green']))
    story.append(Paragraph(
        "The study is located in the Garhwal division of Uttarakhand, specifically targeting three districts "
        "that represent the diversity of mountain agricultural systems in the Indian Himalayan Region:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    area_data = [
        [Paragraph("<b>Parameter</b>", styles['TableHeader']),
         Paragraph("<b>Details</b>", styles['TableHeader'])],
        [Paragraph("Study Districts", styles['TableCellBold']),
         Paragraph("Tehri Garhwal, Pauri Garhwal, Chamoli", styles['TableCell'])],
        [Paragraph("Treatment Group", styles['TableCellBold']),
         Paragraph("5,000 smallholder producers enrolled on PARVAT-SETU platform", styles['TableCell'])],
        [Paragraph("Control Group", styles['TableCellBold']),
         Paragraph("1,000 matched households in non-intervention villages", styles['TableCell'])],
        [Paragraph("Sampling Strategy", styles['TableCellBold']),
         Paragraph("Stratified random sampling within SHG clusters; stratification by altitude zone (800-1200m, 1200-1800m, 1800-2400m), crop system, and access to road", styles['TableCell'])],
        [Paragraph("Altitude Range", styles['TableCellBold']),
         Paragraph("800m to 2,400m above sea level", styles['TableCell'])],
        [Paragraph("Agro-climatic Zones", styles['TableCellBold']),
         Paragraph("Subtropical, warm-temperate, and cool-temperate zones", styles['TableCell'])],
    ]
    story.append(make_table(area_data, col_widths=[1.8*inch, 4.8*inch]))
    story.append(spacer(10))

    # 3. Data Collection Methods
    story.append(Paragraph("3. Data Collection Methods", styles['Heading2Green']))
    story.append(Paragraph(
        "A comprehensive multi-modal data collection strategy ensures triangulation of findings:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    dc_data = [
        [Paragraph("<b>Method</b>", styles['TableHeader']),
         Paragraph("<b>Timing</b>", styles['TableHeader']),
         Paragraph("<b>Sample</b>", styles['TableHeader']),
         Paragraph("<b>Key Variables</b>", styles['TableHeader'])],
        [Paragraph("Baseline Household Survey", styles['TableCellBold']),
         Paragraph("Month 1-4", styles['TableCellCenter']),
         Paragraph("n = 2,000", styles['TableCellCenter']),
         Paragraph("Income, assets, financial inclusion, food security, crop production, market access", styles['TableCell'])],
        [Paragraph("Platform Analytics", styles['TableCellBold']),
         Paragraph("Continuous", styles['TableCellCenter']),
         Paragraph("All users", styles['TableCellCenter']),
         Paragraph("Digital transaction data, app usage, pricing data, credit performance", styles['TableCell'])],
        [Paragraph("Midline Assessment", styles['TableCellBold']),
         Paragraph("Month 15", styles['TableCellCenter']),
         Paragraph("n = 1,000", styles['TableCellCenter']),
         Paragraph("Progress indicators, early outcome signals, course corrections", styles['TableCell'])],
        [Paragraph("Endline Survey", styles['TableCellBold']),
         Paragraph("Month 27-30", styles['TableCellCenter']),
         Paragraph("n = 2,000", styles['TableCellCenter']),
         Paragraph("Same instrument as baseline for DiD estimation", styles['TableCell'])],
        [Paragraph("Beneficiary Case Studies", styles['TableCellBold']),
         Paragraph("Month 12-28", styles['TableCellCenter']),
         Paragraph("n = 20", styles['TableCellCenter']),
         Paragraph("In-depth narrative of change pathways, barriers, and enablers", styles['TableCell'])],
        [Paragraph("Focus Group Discussions", styles['TableCellBold']),
         Paragraph("Month 10, 20, 28", styles['TableCellCenter']),
         Paragraph("8 FGDs", styles['TableCellCenter']),
         Paragraph("Community perceptions, collective action dynamics, gender norms", styles['TableCell'])],
        [Paragraph("Key Informant Interviews", styles['TableCellBold']),
         Paragraph("Month 8-28", styles['TableCellCenter']),
         Paragraph("15 KIIs", styles['TableCellCenter']),
         Paragraph("Institutional perspectives, policy context, market dynamics", styles['TableCell'])],
    ]
    story.append(make_table(dc_data, col_widths=[1.5*inch, 1.0*inch, 0.8*inch, 3.3*inch]))
    story.append(spacer(10))

    # 4. Technology Development Methodology
    story.append(Paragraph("4. Technology Development Methodology", styles['Heading2Green']))
    story.append(Paragraph(
        "The platform development follows an Agile methodology adapted for research context:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    tech_method = [
        "<b>Agile Sprints (2-week cycles):</b> Iterative development of mobile application and backend infrastructure with continuous user feedback from field testing with farmer groups.",
        "<b>AI/ML Model Development Pipeline:</b> Train on historical data &rarr; Validate with cross-validation &rarr; A/B test with live users &rarr; Deploy to production &rarr; Monitor performance drift &rarr; Retrain quarterly.",
        "<b>GIS Layer Development:</b> Data acquisition (satellite + field survey) &rarr; Preprocessing and georectification &rarr; Spatial analysis and modeling &rarr; Visualization and decision-support interface &rarr; Validation with ground truth.",
        "<b>User-Centered Design:</b> Participatory design workshops with farmer groups, iterative prototyping, usability testing in low-literacy contexts, voice-first interface design.",
    ]
    for t in tech_method:
        story.append(Paragraph(t, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))

    # 5. AI/ML Methodology
    story.append(Paragraph("5. AI/ML Methodology", styles['Heading2Green']))
    story.append(Paragraph(
        "Five core AI/ML models are developed, each with specific algorithmic approaches and performance targets:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    ai_method_data = [
        [Paragraph("<b>Model</b>", styles['TableHeader']),
         Paragraph("<b>Algorithm</b>", styles['TableHeader']),
         Paragraph("<b>Training Data</b>", styles['TableHeader']),
         Paragraph("<b>Performance Target</b>", styles['TableHeader'])],
        [Paragraph("Demand Forecasting", styles['TableCellBold']),
         Paragraph("LSTM + Prophet ensemble", styles['TableCell']),
         Paragraph("5-year mandi price data + seasonal patterns + weather", styles['TableCell']),
         Paragraph("MAPE &lt; 15%", styles['TableCell'])],
        [Paragraph("Price Prediction", styles['TableCellBold']),
         Paragraph("XGBoost gradient boosting", styles['TableCell']),
         Paragraph("Historical prices, supply data, transport costs, festival calendar", styles['TableCell']),
         Paragraph("R-squared &gt; 0.75", styles['TableCell'])],
        [Paragraph("Credit Scoring", styles['TableCellBold']),
         Paragraph("Random Forest (200+ features)", styles['TableCell']),
         Paragraph("Transaction history, satellite imagery, social network, mobile usage", styles['TableCell']),
         Paragraph("AUC &gt; 0.78", styles['TableCell'])],
        [Paragraph("Quality Grading", styles['TableCellBold']),
         Paragraph("MobileNetV3 CNN (on-device)", styles['TableCell']),
         Paragraph("10,000+ labeled produce images across quality grades", styles['TableCell']),
         Paragraph("Accuracy &gt; 88%", styles['TableCell'])],
        [Paragraph("Logistics Optimization", styles['TableCellBold']),
         Paragraph("OR-Tools + Genetic Algorithm", styles['TableCell']),
         Paragraph("Road network, terrain DEM, vehicle capacity, time windows", styles['TableCell']),
         Paragraph("30-45% cost reduction", styles['TableCell'])],
    ]
    story.append(make_table(ai_method_data, col_widths=[1.3*inch, 1.6*inch, 2.1*inch, 1.6*inch]))
    story.append(spacer(10))

    # 6. GIS Methodology
    story.append(Paragraph("6. GIS Methodology", styles['Heading2Green']))
    story.append(Paragraph(
        "Geospatial analysis forms the backbone of location-intelligence for the platform:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    gis_method = [
        "<b>Producer Mapping with Land Records Linkage:</b> GPS-tagged producer registration integrated with state land records (Bhulekh/DevBhoomi portal) for verified ownership and plot-level production data.",
        "<b>Agro-ecological Zonation:</b> Multi-criteria classification using ICAR-NBSSLUP soil data + SRTM DEM (30m resolution) + IMD climate grids to generate crop suitability maps at village level.",
        "<b>Climate-Risk Overlay:</b> Composite vulnerability layer combining flood zone mapping (HEC-RAS), landslide susceptibility (logistic regression on slope, lithology, land cover, rainfall), and drought probability.",
        "<b>Logistics Network Optimization:</b> Vehicle Routing Problem with Time Windows (VRPTW) solver using actual road network (OpenStreetMap + state PWD data), terrain gradient, seasonal accessibility, and demand nodes.",
        "<b>Market-Shed Analysis:</b> Thiessen polygon-based catchment delineation for buyer targeting, incorporating travel-time isochrones rather than Euclidean distance for mountain terrain accuracy.",
    ]
    for g in gis_method:
        story.append(Paragraph(g, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))

    # 7. Impact Evaluation Methodology
    story.append(Paragraph("7. Impact Evaluation Methodology", styles['Heading2Green']))
    story.append(Paragraph(
        "The impact evaluation employs a rigorous quasi-experimental design:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    story.append(Paragraph("<b>Primary Estimator: Difference-in-Differences (DiD)</b>", styles['BodyBold']))
    story.append(Paragraph(
        "The causal impact is estimated using the DiD framework:",
        styles['BodyText']
    ))
    story.append(Paragraph(
        "Beta = (Y_treatment_post - Y_treatment_pre) - (Y_control_post - Y_control_pre)",
        styles['Callout']
    ))
    story.append(spacer(4))
    impact_method = [
        "<b>Propensity Score Matching:</b> Control villages matched on baseline characteristics (income, landholding, altitude, road access, market distance, SHG density) using nearest-neighbor matching with caliper = 0.2 SD.",
        "<b>Clustering:</b> Standard errors clustered at village level (unit of treatment assignment) to account for intra-cluster correlation.",
        "<b>Robustness Checks:</b> Placebo tests (pre-treatment trends), leave-one-district-out jackknife, heterogeneous effects analysis (by gender, caste, landholding size, altitude zone).",
        "<b>Qualitative Validation:</b> Most Significant Change (MSC) technique to capture transformative impacts not measurable through surveys, with participatory ranking by community members.",
    ]
    for i in impact_method:
        story.append(Paragraph(i, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))

    # 8. Ethical Considerations
    story.append(Paragraph("8. Ethical Considerations", styles['Heading2Green']))
    story.append(Paragraph(
        "The research adheres to the highest ethical standards for human subjects research:",
        styles['BodyText']
    ))
    story.append(spacer(4))
    ethics = [
        "<b>Institutional Ethics Committee Approval:</b> Full protocol review and approval from DBS Global University Ethics Committee prior to any data collection.",
        "<b>Informed Consent:</b> Bilingual consent forms (Hindi/English) with verbal explanation for low-literacy participants; separate consent for digital data collection and platform analytics.",
        "<b>Data Anonymization:</b> All personally identifiable information removed before analysis; compliance with Digital Personal Data Protection (DPDP) Act 2023.",
        "<b>Gender Sensitivity Protocols:</b> Female enumerators for women respondents; FGD timings aligned with women's schedules; childcare provision during data collection events.",
        "<b>Community Feedback:</b> Findings shared with participating communities before publication; right to withdraw at any stage without penalty.",
    ]
    for e in ethics:
        story.append(Paragraph(e, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))

    # Methodology Timeline
    story.append(Paragraph("Methodology Timeline", styles['Heading2Green']))
    timeline_data = [
        [Paragraph("<b>Phase</b>", styles['TableHeader']),
         Paragraph("<b>Months</b>", styles['TableHeader']),
         Paragraph("<b>Activities</b>", styles['TableHeader']),
         Paragraph("<b>Outputs</b>", styles['TableHeader'])],
        [Paragraph("Preparatory", styles['TableCellBold']),
         Paragraph("M1-4", styles['TableCellCenter']),
         Paragraph("Ethics approval, baseline survey design, sampling frame, enumerator training, GIS data acquisition", styles['TableCell']),
         Paragraph("Approved protocol, sampling frame, baseline instrument", styles['TableCell'])],
        [Paragraph("Baseline Data Collection", styles['TableCellBold']),
         Paragraph("M3-6", styles['TableCellCenter']),
         Paragraph("Household surveys (n=2000), producer mapping, land records linkage, agro-ecological zonation", styles['TableCell']),
         Paragraph("Baseline dataset, GIS layers, producer database", styles['TableCell'])],
        [Paragraph("Technology Development", styles['TableCellBold']),
         Paragraph("M2-12", styles['TableCellCenter']),
         Paragraph("Platform development (Agile sprints), AI model training and validation, GIS platform deployment", styles['TableCell']),
         Paragraph("MVP platform, trained AI models, GIS dashboard", styles['TableCell'])],
        [Paragraph("Intervention Rollout", styles['TableCellBold']),
         Paragraph("M6-24", styles['TableCellCenter']),
         Paragraph("Farmer onboarding, market linkage activation, credit facilitation, continuous monitoring", styles['TableCell']),
         Paragraph("Platform analytics, transaction data, credit portfolio", styles['TableCell'])],
        [Paragraph("Midline Assessment", styles['TableCellBold']),
         Paragraph("M15-16", styles['TableCellCenter']),
         Paragraph("Midline survey (n=1000), FGDs, process documentation, model performance review", styles['TableCell']),
         Paragraph("Midline report, course corrections, model retraining", styles['TableCell'])],
        [Paragraph("Endline and Analysis", styles['TableCellBold']),
         Paragraph("M27-30", styles['TableCellCenter']),
         Paragraph("Endline survey (n=2000), case studies, KIIs, DiD estimation, qualitative analysis", styles['TableCell']),
         Paragraph("Impact estimates, publications, replication playbook", styles['TableCell'])],
    ]
    story.append(make_table(timeline_data, col_widths=[1.2*inch, 0.8*inch, 2.5*inch, 2.1*inch]))
    story.append(PageBreak())


def build_problem_page(story, styles):
    """Section 2: The Problem"""
    story.append(Paragraph("THE PROBLEM", styles['Heading1Green']))
    story.append(Paragraph(
        "A INR 3.2 Lakh Crore Market Failure Destroying Mountain Livelihoods",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "India's agricultural sector, despite contributing 18% to GDP and employing 42% of the workforce, "
        "systematically fails its smallest producers. The Indian Himalayan Region (IHR) represents the most "
        "extreme manifestation of this failure, where geography, fragmentation, and institutional neglect "
        "combine to create a poverty trap affecting 12 million farming households.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("The Scale of the Crisis", styles['Heading2Green']))
    
    bullets = [
        "<b>86% of Indian farmers are smallholders</b> (holdings &lt;2 hectares), earning less than INR 6,000/month - below minimum wage standards",
        "<b>70-85% of value is captured by intermediaries</b> - farmers receive only 15-30% of consumer price for their produce",
        "<b>INR 3.2 Lakh Crore in annual value destruction</b> - the gap between what consumers pay and what farmers receive represents one of the world's largest market inefficiencies",
        "<b>Mountain farmers face 200-400% higher logistics costs</b> than plains counterparts due to terrain, road quality, and remoteness",
        "<b>Post-harvest losses reach 25-40%</b> in mountain regions versus 12-16% national average",
        "<b>Only 4% of mountain farmers</b> have access to formal credit, compared to 25% national average",
    ]
    for b in bullets:
        story.append(Paragraph(b, styles['BulletText'], bulletText='\u2022'))
    
    story.append(spacer(10))
    story.append(Paragraph("Why Mountain Farmers Are Trapped", styles['Heading2Green']))
    story.append(Paragraph(
        "The Himalayan smallholder faces a unique quadruple barrier that existing solutions have failed to address:",
        styles['BodyText']
    ))
    
    barrier_data = [
        [Paragraph("<b>Barrier</b>", styles['TableHeader']),
         Paragraph("<b>Description</b>", styles['TableHeader']),
         Paragraph("<b>Impact</b>", styles['TableHeader']),
         Paragraph("<b>Scale</b>", styles['TableHeader'])],
        [Paragraph("Aggregation Failure", styles['TableCellBold']),
         Paragraph("Average holding 0.68 ha, scattered across 3-5 terraced plots at different altitudes", styles['TableCell']),
         Paragraph("Cannot meet minimum order quantities for institutional buyers", styles['TableCell']),
         Paragraph("12M households affected", styles['TableCell'])],
        [Paragraph("Financial Exclusion", styles['TableCellBold']),
         Paragraph("No collateral (land records unclear), no credit history, no insurance", styles['TableCell']),
         Paragraph("Forced to sell at harvest (distress sale) losing 30-50% value", styles['TableCell']),
         Paragraph("96% without formal credit", styles['TableCell'])],
        [Paragraph("Information Asymmetry", styles['TableCellBold']),
         Paragraph("No real-time price data, no weather advisories, no demand signals", styles['TableCell']),
         Paragraph("Systematic underpricing and inability to plan production", styles['TableCell']),
         Paragraph("Zero digital penetration", styles['TableCell'])],
        [Paragraph("Logistics Failure", styles['TableCellBold']),
         Paragraph("Last-mile road density 40% of national average, seasonal disruption", styles['TableCell']),
         Paragraph("200-400% higher transport costs, spoilage, market inaccessibility", styles['TableCell']),
         Paragraph("6 months/year disruption", styles['TableCell'])],
    ]
    story.append(make_table(barrier_data, col_widths=[1.2*inch, 2.2*inch, 2.0*inch, 1.2*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph(
        "The human cost is devastating: 67% of mountain farming households report food insecurity for at least "
        "3 months per year. Youth out-migration exceeds 40% in hill districts, creating 'ghost villages' and "
        "destroying traditional knowledge systems built over millennia. Women, who perform 70-80% of agricultural "
        "labor in mountain regions, bear the disproportionate burden of this systemic failure.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_solution_page(story, styles):
    """Section 3: The Solution"""
    story.append(Paragraph("THE SOLUTION", styles['Heading1Green']))
    story.append(Paragraph(
        "PARVAT-SETU: An AI+GIS Powered Cooperative Platform for Mountain Economic Inclusion",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "PARVAT-SETU (Participatory AI-enabled Resource Valuation and Access Technology for "
        "Sustainable Economic Transformation in Uplands) is a producer-owned social enterprise "
        "that combines cutting-edge AI/GIS technology with cooperative governance to systematically "
        "dismantle each barrier facing mountain smallholders.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Three Pillars of the Solution", styles['Heading2Green']))
    
    pillars_data = [
        [Paragraph("<b>Pillar</b>", styles['TableHeader']),
         Paragraph("<b>What It Does</b>", styles['TableHeader']),
         Paragraph("<b>How It Works</b>", styles['TableHeader']),
         Paragraph("<b>Impact</b>", styles['TableHeader'])],
        [Paragraph("Digital Aggregation", styles['TableCellBold']),
         Paragraph("Virtually consolidates fragmented production into market-ready volumes", styles['TableCell']),
         Paragraph("AI demand forecasting + GIS-optimized collection routing + quality standardization", styles['TableCell']),
         Paragraph("Unlocks institutional buyer access for 50,000+ farmers", styles['TableCell'])],
        [Paragraph("Embedded Finance", styles['TableCellBold']),
         Paragraph("Provides working capital, insurance, and savings without traditional collateral", styles['TableCell']),
         Paragraph("Cash-flow based lending using transaction history + satellite crop monitoring", styles['TableCell']),
         Paragraph("INR 500 Cr credit unlocked over 5 years", styles['TableCell'])],
        [Paragraph("Premium Market Access", styles['TableCellBold']),
         Paragraph("Connects mountain produce to high-value buyers willing to pay 40-100% premium", styles['TableCell']),
         Paragraph("GI-tagged products + organic certification + traceability + direct-to-consumer", styles['TableCell']),
         Paragraph("200% income uplift for participating farmers", styles['TableCell'])],
    ]
    story.append(make_table(pillars_data, col_widths=[1.3*inch, 1.8*inch, 2.2*inch, 1.4*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Why This is Different", styles['Heading2Green']))
    story.append(Paragraph(
        "Unlike existing AgriTech platforms that extract value through margins, PARVAT-SETU is "
        "<b>producer-owned</b>. This single design choice creates fundamentally aligned incentives:",
        styles['BodyText']
    ))
    
    diff_bullets = [
        "<b>Ownership = Trust:</b> Farmer adoption rates 3-5x higher than commercial platforms because producers control governance",
        "<b>Ownership = Retention:</b> Zero churn once onboarded (vs. 40-60% annual churn on commercial AgriTech platforms)",
        "<b>Ownership = Sustainability:</b> Surplus returns to producers, creating a virtuous cycle of reinvestment",
        "<b>Technology = Force Multiplier:</b> AI/GIS doesn't replace human judgment but amplifies cooperative capacity",
    ]
    for b in diff_bullets:
        story.append(Paragraph(b, styles['BulletText'], bulletText='\u2022'))
    
    story.append(spacer(10))
    story.append(Paragraph("Proven Model, New Technology", styles['Heading2Green']))
    story.append(Paragraph(
        "The cooperative model is proven (Amul delivers 80% of value to producers). The technology layer "
        "(AI/GIS) is proven (precision agriculture has demonstrated 20-40% efficiency gains globally). "
        "PARVAT-SETU's innovation is combining both for mountain-specific conditions - a combination "
        "no existing player has achieved because it requires deep domain expertise in both Himalayan "
        "geography AND cooperative economics.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_business_model_canvas(story, styles):
    """Section 4: Business Model Canvas"""
    story.append(Paragraph("BUSINESS MODEL CANVAS", styles['Heading1Green']))
    story.append(Paragraph(
        "A Producer-Owned Platform with Multiple Revenue Streams",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    # 3x3 Business Model Canvas
    canvas_data = [
        [Paragraph("<b>Key Partners</b>", styles['TableHeader']),
         Paragraph("<b>Key Activities</b>", styles['TableHeader']),
         Paragraph("<b>Value Propositions</b>", styles['TableHeader'])],
        [Paragraph("- NABARD/SIDBI (finance)<br/>- State Horticulture Dept<br/>- FPOs &amp; SHGs<br/>- ICAR/GB Pant Institute<br/>- CSR partners<br/>- Organic certifiers<br/>- Last-mile logistics", styles['TableCell']),
         Paragraph("- AI model development<br/>- Farmer onboarding<br/>- Quality aggregation<br/>- Market linkage<br/>- Credit facilitation<br/>- Training &amp; capacity building<br/>- GIS mapping", styles['TableCell']),
         Paragraph("<b>For Farmers:</b><br/>- 200% income uplift<br/>- Assured procurement<br/>- Working capital access<br/>- Real-time advisories<br/><b>For Buyers:</b><br/>- Traceable sourcing<br/>- Volume reliability<br/>- Quality certification", styles['TableCell'])],
        [Paragraph("<b>Key Resources</b>", styles['TableHeader']),
         Paragraph("<b>Channels</b>", styles['TableHeader']),
         Paragraph("<b>Customer Segments</b>", styles['TableHeader'])],
        [Paragraph("- AI/ML models (6 proprietary)<br/>- GIS spatial platform<br/>- Producer trust network<br/>- Academic research base<br/>- Domain expertise (IHR)<br/>- Cooperative license", styles['TableCell']),
         Paragraph("- SHG network (zero CAC)<br/>- FPO partnerships<br/>- Digital platform (mobile)<br/>- Village-level entrepreneurs<br/>- Government schemes<br/>- Direct B2B sales team", styles['TableCell']),
         Paragraph("<b>Primary:</b><br/>- Mountain smallholders (&lt;2 ha)<br/>- Women farmer groups<br/><b>Secondary:</b><br/>- Organic/premium buyers<br/>- HoReCa sector<br/>- Export houses<br/>- Institutional buyers", styles['TableCell'])],
        [Paragraph("<b>Cost Structure</b>", styles['TableHeader']),
         Paragraph("<b>Revenue Streams</b>", styles['TableHeader']),
         Paragraph("<b>Customer Relationships</b>", styles['TableHeader'])],
        [Paragraph("- Technology (30%): AI/GIS platform<br/>- Market infrastructure (25%)<br/>- Team &amp; operations (25%)<br/>- Field operations (20%)<br/>Variable: logistics, processing", styles['TableCell']),
         Paragraph("- Transaction commission (3-5%)<br/>- Value-added processing (15-25%)<br/>- Buyer subscriptions (INR 25K-1L)<br/>- Financial services (1-2%)<br/>- Data services (insurance, govt)", styles['TableCell']),
         Paragraph("- Producer ownership (governance)<br/>- Weekly advisory touchpoints<br/>- Transparent price discovery<br/>- Annual dividend distribution<br/>- Community trust building<br/>- Dedicated field coordinators", styles['TableCell'])],
    ]
    
    canvas_table = Table(canvas_data, colWidths=[CONTENT_WIDTH/3.0]*3)
    canvas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
        ('BACKGROUND', (0, 2), (-1, 2), GREEN_DARK),
        ('BACKGROUND', (0, 4), (-1, 4), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 2), (-1, 2), white),
        ('TEXTCOLOR', (0, 4), (-1, 4), white),
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN_MED),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(canvas_table)
    story.append(PageBreak())


def build_market_opportunity(story, styles):
    """Section 5: Market Opportunity"""
    story.append(Paragraph("MARKET OPPORTUNITY", styles['Heading1Green']))
    story.append(Paragraph(
        "A INR 12 Lakh Crore Market with 14% CAGR - Massively Underserved",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "The Indian agriculture market is undergoing a fundamental transformation driven by "
        "digitization, consumer premiumization, and policy reform. Within this massive market, "
        "the Indian Himalayan Region represents a uniquely attractive segment due to its natural "
        "advantages in organic, specialty, and medicinal produce.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    market_data = [
        [Paragraph("<b>Market Tier</b>", styles['TableHeader']),
         Paragraph("<b>Size</b>", styles['TableHeader']),
         Paragraph("<b>Description</b>", styles['TableHeader']),
         Paragraph("<b>Growth</b>", styles['TableHeader'])],
        [Paragraph("TAM", styles['TableCellBold']),
         Paragraph("INR 12 Lakh Crore", styles['TableCellCenter']),
         Paragraph("Total Indian agriculture and allied market including processing, inputs, and services", styles['TableCell']),
         Paragraph("11% CAGR", styles['TableCellCenter'])],
        [Paragraph("SAM", styles['TableCellBold']),
         Paragraph("INR 85,000 Crore", styles['TableCellCenter']),
         Paragraph("IHR agriculture economy across 12 states - horticulture, spices, medicinal plants, dairy", styles['TableCell']),
         Paragraph("14% CAGR", styles['TableCellCenter'])],
        [Paragraph("SOM", styles['TableCellBold']),
         Paragraph("INR 2,500 Crore", styles['TableCellCenter']),
         Paragraph("Addressable market in 5 years: Uttarakhand + Himachal + NE states with platform coverage", styles['TableCell']),
         Paragraph("22% CAGR", styles['TableCellCenter'])],
    ]
    story.append(make_table(market_data, col_widths=[1.0*inch, 1.5*inch, 3.0*inch, 1.1*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Key Market Drivers", styles['Heading2Green']))
    drivers = [
        "<b>Consumer Premiumization:</b> Urban consumers willing to pay 40-100% premium for traceable, organic, mountain-origin produce. Market growing at 25% CAGR.",
        "<b>Policy Tailwinds:</b> New FPO policy (10,000 FPOs by 2027), PMFME scheme, organic farming missions, and Digital Agriculture Mission create favorable conditions.",
        "<b>Technology Adoption:</b> 850M smartphone users, UPI penetration reaching rural areas, satellite imagery costs dropping 90% in 5 years.",
        "<b>Climate Premium:</b> Mountain agro-biodiversity increasingly valued as climate adaptation resource. Carbon credit markets emerging.",
        "<b>Export Opportunity:</b> GI-tagged Himalayan products (Uttarakhand Tejpatta, Munsyari Rajma, Kumaon honey) have strong export demand with 50-200% premium over domestic.",
    ]
    for d in drivers:
        story.append(Paragraph(d, styles['BulletText'], bulletText='\u2022'))
    
    story.append(spacer(10))
    story.append(Paragraph(
        "The convergence of these factors creates a time-limited window of opportunity. First-mover advantage "
        "in building producer trust networks will be decisive - these relationships take 2-3 years to build "
        "and cannot be replicated by later entrants regardless of capital deployed.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_traction_page(story, styles):
    """Section 6: Traction & Proof Points"""
    story.append(Paragraph("TRACTION &amp; PROOF POINTS", styles['Heading1Green']))
    story.append(Paragraph(
        "Research-Validated Model with Institutional Backing",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "While PARVAT-SETU is at seed stage for commercial deployment, it is built on a foundation "
        "of rigorous academic research, institutional validation, and comparable proof from similar models globally.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Academic Validation", styles['Heading2Green']))
    academic = [
        "PhD research with 3+ years of field data across 50+ mountain villages in Uttarakhand",
        "4 SCIE/Scopus indexed publications validating core methodology and AI models",
        "Presented at 6 national/international conferences with peer review",
        "Institutional backing from DBS Global University as academic anchor",
        "Multi-disciplinary approach combining environmental science, AI/ML, hydrology, and development economics",
    ]
    for a in academic:
        story.append(Paragraph(a, styles['BulletText'], bulletText='\u2022'))
    
    story.append(spacer(8))
    story.append(Paragraph("Institutional Partnerships", styles['Heading2Green']))
    partners = [
        "<b>NABARD:</b> Engagement on FPO development, potential grant funding pipeline",
        "<b>State Disaster Management Authority (SDMA):</b> GIS/remote sensing collaboration validated",
        "<b>Farmer Producer Organizations:</b> 3 FPOs with 2,500+ member farmers engaged",
        "<b>Self-Help Groups:</b> 45+ SHGs with 500+ women members in pilot geography",
        "<b>ICAR Institutes:</b> Technical advisory for crop-specific AI model development",
    ]
    for p in partners:
        story.append(Paragraph(p, styles['BulletText'], bulletText='\u2022'))
    
    story.append(spacer(8))
    story.append(Paragraph("Comparable Models - Validated at Scale", styles['Heading2Green']))
    
    comp_data = [
        [Paragraph("<b>Comparable</b>", styles['TableHeader']),
         Paragraph("<b>Model</b>", styles['TableHeader']),
         Paragraph("<b>Scale Achieved</b>", styles['TableHeader']),
         Paragraph("<b>Relevance to PARVAT-SETU</b>", styles['TableHeader'])],
        [Paragraph("One Acre Fund", styles['TableCellBold']),
         Paragraph("Bundled services for smallholders (inputs + credit + training)", styles['TableCell']),
         Paragraph("1.5M farmers, 9 countries", styles['TableCell']),
         Paragraph("40-50% income uplift validates our 200% target with tech layer", styles['TableCell'])],
        [Paragraph("Amul (GCMMF)", styles['TableCellBold']),
         Paragraph("Producer-owned cooperative with tech-enabled aggregation", styles['TableCell']),
         Paragraph("3.6M producers, INR 72,000 Cr revenue", styles['TableCell']),
         Paragraph("80% value to producers proves cooperative economics at scale", styles['TableCell'])],
        [Paragraph("FarmFundr / Harvesting", styles['TableCellBold']),
         Paragraph("AI-powered crop advisory + market linkage", styles['TableCell']),
         Paragraph("500K+ farmers in 2 years", styles['TableCell']),
         Paragraph("Technology-led rapid scaling validates AI approach", styles['TableCell'])],
        [Paragraph("Araku Coffee", styles['TableCellBold']),
         Paragraph("Tribal cooperative producing premium coffee", styles['TableCell']),
         Paragraph("200K families, exports to 15 countries", styles['TableCell']),
         Paragraph("Mountain/tribal premium product strategy validated", styles['TableCell'])],
    ]
    story.append(make_table(comp_data, col_widths=[1.2*inch, 1.8*inch, 1.5*inch, 2.1*inch]))
    story.append(PageBreak())


def build_financial_summary(story, styles):
    """Section 7: Financial Summary"""
    story.append(Paragraph("FINANCIAL SUMMARY", styles['Heading1Green']))
    story.append(Paragraph(
        "Clear Path to Profitability with Attractive Risk-Adjusted Returns",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "PARVAT-SETU's financial model is built on conservative assumptions validated by comparable "
        "enterprises. The blended finance structure de-risks early-stage execution while preserving "
        "attractive returns for equity investors.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    fin_data = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 2</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 4</b>", styles['TableHeader']),
         Paragraph("<b>Year 5</b>", styles['TableHeader'])],
        [Paragraph("Revenue (INR Lakhs)", styles['TableCellBold']),
         Paragraph("20", styles['TableCellCenter']),
         Paragraph("185", styles['TableCellCenter']),
         Paragraph("720", styles['TableCellCenter']),
         Paragraph("1,450", styles['TableCellCenter']),
         Paragraph("2,700", styles['TableCellCenter'])],
        [Paragraph("Gross Margin", styles['TableCellBold']),
         Paragraph("35%", styles['TableCellCenter']),
         Paragraph("38%", styles['TableCellCenter']),
         Paragraph("42%", styles['TableCellCenter']),
         Paragraph("48%", styles['TableCellCenter']),
         Paragraph("55%", styles['TableCellCenter'])],
        [Paragraph("EBITDA Margin", styles['TableCellBold']),
         Paragraph("-180%", styles['TableCellCenter']),
         Paragraph("-45%", styles['TableCellCenter']),
         Paragraph("5%", styles['TableCellCenter']),
         Paragraph("18%", styles['TableCellCenter']),
         Paragraph("28%", styles['TableCellCenter'])],
        [Paragraph("Farmers Enrolled", styles['TableCellBold']),
         Paragraph("2,500", styles['TableCellCenter']),
         Paragraph("8,000", styles['TableCellCenter']),
         Paragraph("18,000", styles['TableCellCenter']),
         Paragraph("32,000", styles['TableCellCenter']),
         Paragraph("50,000", styles['TableCellCenter'])],
        [Paragraph("GMV (INR Lakhs)", styles['TableCellBold']),
         Paragraph("80", styles['TableCellCenter']),
         Paragraph("620", styles['TableCellCenter']),
         Paragraph("2,400", styles['TableCellCenter']),
         Paragraph("5,800", styles['TableCellCenter']),
         Paragraph("12,000", styles['TableCellCenter'])],
    ]
    story.append(make_table(fin_data, col_widths=[1.6*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Key Unit Economics", styles['Heading2Green']))
    unit_data = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Value</b>", styles['TableHeader']),
         Paragraph("<b>Benchmark</b>", styles['TableHeader'])],
        [Paragraph("Customer Acquisition Cost (CAC)", styles['TableCellBold']),
         Paragraph("INR 3,700 per farmer", styles['TableCellCenter']),
         Paragraph("Industry avg: INR 5,000-8,000", styles['TableCell'])],
        [Paragraph("Lifetime Value (LTV)", styles['TableCellBold']),
         Paragraph("INR 45,000 per farmer", styles['TableCellCenter']),
         Paragraph("Based on 8-year retention", styles['TableCell'])],
        [Paragraph("LTV/CAC Ratio", styles['TableCellBold']),
         Paragraph("12.2x", styles['TableCellCenter']),
         Paragraph("Excellent (>3x is viable)", styles['TableCell'])],
        [Paragraph("Payback Period", styles['TableCellBold']),
         Paragraph("14 months", styles['TableCellCenter']),
         Paragraph("Industry avg: 18-24 months", styles['TableCell'])],
        [Paragraph("Break-even", styles['TableCellBold']),
         Paragraph("Month 48", styles['TableCellCenter']),
         Paragraph("Comparable: 36-60 months", styles['TableCell'])],
    ]
    story.append(make_table(unit_data, col_widths=[2.2*inch, 1.8*inch, 2.6*inch]))
    story.append(PageBreak())


def build_the_ask(story, styles):
    """Section 8: The Ask"""
    story.append(Paragraph("THE ASK", styles['Heading1Green']))
    story.append(Paragraph(
        "INR 5 Crore Seed Round - Blended Finance Structure",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "We are raising INR 5 Crore in a blended finance seed round designed to optimize the "
        "risk-return-impact balance for different investor types. This structure allows grant capital "
        "to absorb early-stage pilot risk while equity investors benefit from de-risked growth.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    ask_data = [
        [Paragraph("<b>Capital Type</b>", styles['TableHeader']),
         Paragraph("<b>Amount</b>", styles['TableHeader']),
         Paragraph("<b>Share</b>", styles['TableHeader']),
         Paragraph("<b>Source</b>", styles['TableHeader']),
         Paragraph("<b>Terms</b>", styles['TableHeader'])],
        [Paragraph("Grant Capital", styles['TableCellBold']),
         Paragraph("INR 3.0 Crore", styles['TableCellCenter']),
         Paragraph("60%", styles['TableCellCenter']),
         Paragraph("NABARD, foundations, CSR, bilateral donors", styles['TableCell']),
         Paragraph("Non-returnable; milestone-based disbursement", styles['TableCell'])],
        [Paragraph("Impact Equity", styles['TableCellBold']),
         Paragraph("INR 1.25 Crore", styles['TableCellCenter']),
         Paragraph("25%", styles['TableCellCenter']),
         Paragraph("Impact investors (Omidyar, Acumen, Aavishkaar)", styles['TableCell']),
         Paragraph("25%+ IRR target; 15-20% equity stake; board seat", styles['TableCell'])],
        [Paragraph("Concessional Debt", styles['TableCellBold']),
         Paragraph("INR 0.75 Crore", styles['TableCellCenter']),
         Paragraph("15%", styles['TableCellCenter']),
         Paragraph("DFIs, social lenders (SIDBI, Caspian)", styles['TableCell']),
         Paragraph("8-12% interest; 2-year moratorium; 5-year tenure", styles['TableCell'])],
    ]
    story.append(make_table(ask_data, col_widths=[1.2*inch, 1.1*inch, 0.7*inch, 1.8*inch, 1.8*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Use of Funds", styles['Heading2Green']))
    use_data = [
        [Paragraph("<b>Category</b>", styles['TableHeader']),
         Paragraph("<b>Allocation</b>", styles['TableHeader']),
         Paragraph("<b>Amount</b>", styles['TableHeader']),
         Paragraph("<b>Key Items</b>", styles['TableHeader'])],
        [Paragraph("Technology", styles['TableCellBold']),
         Paragraph("30%", styles['TableCellCenter']),
         Paragraph("INR 1.50 Cr", styles['TableCellCenter']),
         Paragraph("AI model development, GIS platform, mobile app, cloud infrastructure", styles['TableCell'])],
        [Paragraph("Market Infrastructure", styles['TableCellBold']),
         Paragraph("25%", styles['TableCellCenter']),
         Paragraph("INR 1.25 Cr", styles['TableCellCenter']),
         Paragraph("Collection centers, grading equipment, cold storage, packaging", styles['TableCell'])],
        [Paragraph("Team", styles['TableCellBold']),
         Paragraph("25%", styles['TableCellCenter']),
         Paragraph("INR 1.25 Cr", styles['TableCellCenter']),
         Paragraph("Core team (12 people), field coordinators (25), training", styles['TableCell'])],
        [Paragraph("Operations", styles['TableCellBold']),
         Paragraph("20%", styles['TableCellCenter']),
         Paragraph("INR 1.00 Cr", styles['TableCellCenter']),
         Paragraph("Working capital, logistics, farmer onboarding, compliance", styles['TableCell'])],
    ]
    story.append(make_table(use_data, col_widths=[1.4*inch, 1.0*inch, 1.1*inch, 3.1*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph(
        "This capital will fund 30 months of operations through to break-even and initial traction "
        "proof points, positioning PARVAT-SETU for a Series A round of INR 20-30 Crore for pan-IHR expansion.",
        styles['BodyText']
    ))
    story.append(PageBreak())


# ============================================================
# PART B: DETAILED BUSINESS PLAN
# ============================================================

def build_detailed_problem(story, styles):
    """Section 9: Detailed Problem Analysis"""
    story.append(Paragraph("PART B: DETAILED BUSINESS PLAN", styles['Heading1Green']))
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN_DARK, spaceAfter=20))
    story.append(spacer(8))
    
    story.append(Paragraph("DETAILED PROBLEM ANALYSIS", styles['Heading1Green']))
    story.append(Paragraph(
        "Understanding the Structural Market Failure in Mountain Agriculture",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("The Four Barriers - Deep Dive", styles['Heading2Green']))
    story.append(spacer(6))
    
    story.append(Paragraph("1. Aggregation Barrier", styles['Heading3Green']))
    story.append(Paragraph(
        "The average landholding in IHR is 0.68 hectares, fragmented across 3-5 terraced plots at different "
        "altitudes (800-2,400m). This extreme fragmentation means a single farmer produces 200-500 kg of any "
        "single crop - far below the 5-10 ton minimum order quantity required by institutional buyers, mandis, "
        "or processors. Physical aggregation is expensive due to scattered settlements (average 15-20 households "
        "per hamlet) connected by footpaths rather than motorable roads. Traditional aggregation through APMCs "
        "requires farmers to travel 20-80 km to the nearest mandi, losing 1-2 days of labor plus transport cost "
        "of INR 500-2,000 per trip.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("2. Financial Exclusion Barrier", styles['Heading3Green']))
    story.append(Paragraph(
        "Mountain farmers face near-complete exclusion from formal financial services. Only 4% have access to "
        "institutional credit (vs. 25% national average). Land records are disputed or unmutated in 60%+ cases, "
        "eliminating traditional collateral-based lending. Crop insurance penetration is below 2% due to lack of "
        "weather station data for mountain microclimates. This forces reliance on informal moneylenders charging "
        "36-60% annual interest, or distress sale of harvest at 30-50% below market price to meet immediate cash "
        "needs. The working capital gap for a typical mountain farmer is INR 25,000-50,000 per season - small "
        "enough to solve with appropriate financial products, but unserved by existing institutions.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("3. Information Asymmetry Barrier", styles['Heading3Green']))
    story.append(Paragraph(
        "Mountain farmers operate in an information vacuum. Real-time market prices are unavailable (the nearest "
        "mandi may be 50+ km away with no digital connectivity). Weather advisories are calibrated for plains "
        "agriculture and irrelevant for mountain microclimates where conditions vary dramatically within 500m "
        "altitude bands. Pest/disease early warning systems don't exist for mountain crops. Demand signals from "
        "urban markets don't reach producers, leading to glut-and-shortage cycles. This asymmetry is exploited "
        "by intermediaries who buy at suppressed prices and sell at 200-400% markup in urban markets.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("4. Logistics Barrier", styles['Heading3Green']))
    story.append(Paragraph(
        "The IHR road network has density 40% below national average. Only 35% of roads are all-weather. "
        "Landslides, monsoon damage, and snowfall disrupt connectivity for 3-6 months annually. Cold chain "
        "infrastructure is virtually absent - the entire state of Uttarakhand has fewer cold storage facilities "
        "than a single district in Punjab. Last-mile logistics cost per kg is INR 8-15 in mountains vs. INR 2-4 "
        "in plains. This makes conventional supply chain models unviable and results in 25-40% post-harvest "
        "losses for perishable mountain produce (fruits, vegetables, dairy, medicinal plants).",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Why Existing Solutions Fail", styles['Heading2Green']))
    
    fail_data = [
        [Paragraph("<b>Platform</b>", styles['TableHeader']),
         Paragraph("<b>Approach</b>", styles['TableHeader']),
         Paragraph("<b>Why It Fails in Mountains</b>", styles['TableHeader']),
         Paragraph("<b>Limitation</b>", styles['TableHeader'])],
        [Paragraph("eNAM", styles['TableCellBold']),
         Paragraph("Digital mandi platform for online trading", styles['TableCell']),
         Paragraph("Requires physical delivery to mandi; doesn't solve aggregation or logistics", styles['TableCell']),
         Paragraph("Only 20% of mountain mandis connected", styles['TableCell'])],
        [Paragraph("DeHaat", styles['TableCellBold']),
         Paragraph("Input supply + advisory + output linkage", styles['TableCell']),
         Paragraph("Designed for plains agriculture; unit economics don't work in low-density mountain areas", styles['TableCell']),
         Paragraph("No presence in IHR", styles['TableCell'])],
        [Paragraph("Ninjacart", styles['TableCellBold']),
         Paragraph("B2B fresh produce supply chain", styles['TableCell']),
         Paragraph("Requires 500+ kg minimum per pickup; cold chain dependent; urban-centric", styles['TableCell']),
         Paragraph("Cannot operate in road-disrupted areas", styles['TableCell'])],
        [Paragraph("Traditional FPOs", styles['TableCellBold']),
         Paragraph("Cooperative aggregation", styles['TableCell']),
         Paragraph("Lack technology, market access, and working capital; governance issues", styles['TableCell']),
         Paragraph("70% of FPOs financially unviable", styles['TableCell'])],
    ]
    story.append(make_table(fail_data, col_widths=[1.1*inch, 1.5*inch, 2.2*inch, 1.8*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph(
        "The fundamental insight is that mountain agriculture requires a fundamentally different approach - "
        "one that is designed ground-up for low-density, high-diversity, terrain-constrained environments "
        "rather than adapted from plains-optimized models. This is PARVAT-SETU's core innovation.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_solution_architecture(story, styles):
    """Section 10: Solution Architecture"""
    story.append(Paragraph("SOLUTION ARCHITECTURE", styles['Heading1Green']))
    story.append(Paragraph(
        "Technology Stack Designed for Mountain-Specific Challenges",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Platform Overview", styles['Heading2Green']))
    story.append(Paragraph(
        "PARVAT-SETU's technology platform is a multi-layered system designed to operate in low-connectivity, "
        "terrain-constrained environments while delivering enterprise-grade analytics and market intelligence. "
        "The architecture prioritizes offline-first design, edge computing capability, and progressive "
        "connectivity to ensure functionality even in remote mountain areas with intermittent network access.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    # Platform Architecture Diagram using Paragraph
    arch_diagram = Paragraph(
        '<b>PARVAT-SETU PLATFORM ARCHITECTURE</b><br/><br/>'
        '&nbsp;&nbsp;[FARMER LAYER]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PLATFORM LAYER]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MARKET LAYER]<br/>'
        '&nbsp;&nbsp;+----------------+&nbsp;&nbsp;&nbsp;+-------------------+&nbsp;&nbsp;&nbsp;+----------------+<br/>'
        '&nbsp;&nbsp;| Mobile App&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;| AI Engine&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;| Buyer Portal&nbsp;&nbsp; |<br/>'
        '&nbsp;&nbsp;| USSD Gateway&nbsp;&nbsp; |&lt;--&gt;| GIS Platform&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&lt;--&gt;| B2B Marketplace|<br/>'
        '&nbsp;&nbsp;| Voice Bot&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;| Data Lake&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;| Export Connect&nbsp;|<br/>'
        '&nbsp;&nbsp;| Field Devices&nbsp; |&nbsp;&nbsp;&nbsp;| Blockchain Trace&nbsp; |&nbsp;&nbsp;&nbsp;| Finance APIs&nbsp;&nbsp; |<br/>'
        '&nbsp;&nbsp;+----------------+&nbsp;&nbsp;&nbsp;+-------------------+&nbsp;&nbsp;&nbsp;+----------------+<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>'
        '&nbsp;&nbsp;+---------------------------------------------------------------+<br/>'
        '&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;COOPERATIVE GOVERNANCE LAYER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>'
        '&nbsp;&nbsp;|&nbsp;&nbsp;SHG Network&nbsp;&nbsp;|&nbsp;&nbsp;FPO Federation&nbsp;&nbsp;|&nbsp;&nbsp;Producer Company&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>'
        '&nbsp;&nbsp;+---------------------------------------------------------------+<br/>',
        styles['BodyText']
    )
    story.append(arch_diagram)
    story.append(spacer(12))
    
    story.append(Paragraph("AI Capabilities - 6 Proprietary Models", styles['Heading2Green']))
    
    ai_data = [
        [Paragraph("<b>Model</b>", styles['TableHeader']),
         Paragraph("<b>Function</b>", styles['TableHeader']),
         Paragraph("<b>Technology</b>", styles['TableHeader']),
         Paragraph("<b>Accuracy/Performance</b>", styles['TableHeader'])],
        [Paragraph("CropSense AI", styles['TableCellBold']),
         Paragraph("Crop health monitoring from satellite + drone imagery", styles['TableCell']),
         Paragraph("CNN (ResNet-50) + multispectral analysis", styles['TableCell']),
         Paragraph("92% accuracy in disease detection", styles['TableCell'])],
        [Paragraph("PriceCast AI", styles['TableCellBold']),
         Paragraph("Market price prediction (7-30 day forecast)", styles['TableCell']),
         Paragraph("LSTM + transformer architecture + market data", styles['TableCell']),
         Paragraph("87% accuracy within 10% band", styles['TableCell'])],
        [Paragraph("RouteMaster AI", styles['TableCellBold']),
         Paragraph("Optimal collection and delivery routing", styles['TableCell']),
         Paragraph("Genetic algorithm + GIS terrain modeling", styles['TableCell']),
         Paragraph("35% logistics cost reduction", styles['TableCell'])],
        [Paragraph("YieldPredict AI", styles['TableCellBold']),
         Paragraph("Harvest volume forecasting by region and crop", styles['TableCell']),
         Paragraph("Random Forest + weather data + historical yields", styles['TableCell']),
         Paragraph("85% accuracy at block level", styles['TableCell'])],
        [Paragraph("CreditScore AI", styles['TableCellBold']),
         Paragraph("Alternative credit scoring for unbanked farmers", styles['TableCell']),
         Paragraph("Gradient boosting + transaction history + satellite data", styles['TableCell']),
         Paragraph("78% default prediction accuracy", styles['TableCell'])],
        [Paragraph("ClimateAdapt AI", styles['TableCellBold']),
         Paragraph("Microclimate advisory for mountain farming", styles['TableCell']),
         Paragraph("Ensemble methods + IoT sensor data + topography", styles['TableCell']),
         Paragraph("5-day hyperlocal forecasts at 1km resolution", styles['TableCell'])],
    ]
    story.append(make_table(ai_data, col_widths=[1.2*inch, 1.7*inch, 2.0*inch, 1.7*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("GIS Capabilities - 5 Spatial Applications", styles['Heading2Green']))
    
    gis_data = [
        [Paragraph("<b>Application</b>", styles['TableHeader']),
         Paragraph("<b>Function</b>", styles['TableHeader']),
         Paragraph("<b>Data Sources</b>", styles['TableHeader']),
         Paragraph("<b>Output</b>", styles['TableHeader'])],
        [Paragraph("Terrain Mapping", styles['TableCellBold']),
         Paragraph("High-resolution DEM for farming zone classification", styles['TableCell']),
         Paragraph("SRTM + Cartosat + field surveys", styles['TableCell']),
         Paragraph("5m resolution terrain maps", styles['TableCell'])],
        [Paragraph("Land Use Classification", styles['TableCellBold']),
         Paragraph("Automated crop type and area mapping", styles['TableCell']),
         Paragraph("Sentinel-2 + Landsat + ground truth", styles['TableCell']),
         Paragraph("90% classification accuracy", styles['TableCell'])],
        [Paragraph("Watershed Analysis", styles['TableCellBold']),
         Paragraph("Water resource mapping for irrigation planning", styles['TableCell']),
         Paragraph("DEM + rainfall + soil + springs mapping", styles['TableCell']),
         Paragraph("Irrigation potential assessment", styles['TableCell'])],
        [Paragraph("Vulnerability Mapping", styles['TableCellBold']),
         Paragraph("Climate and disaster risk assessment per village", styles['TableCell']),
         Paragraph("Multi-hazard models + exposure data", styles['TableCell']),
         Paragraph("Village-level risk scores", styles['TableCell'])],
        [Paragraph("Infrastructure Planning", styles['TableCellBold']),
         Paragraph("Optimal location for collection centers, cold storage", styles['TableCell']),
         Paragraph("Accessibility analysis + demand modeling", styles['TableCell']),
         Paragraph("Location recommendations with ROI", styles['TableCell'])],
    ]
    story.append(make_table(gis_data, col_widths=[1.3*inch, 1.8*inch, 1.8*inch, 1.7*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph("Technology Stack", styles['Heading2Green']))
    tech_stack = [
        "<b>Frontend:</b> React Native (mobile), Progressive Web App (feature phones via USSD bridge)",
        "<b>Backend:</b> Python (FastAPI) + Node.js microservices on Kubernetes",
        "<b>AI/ML:</b> TensorFlow, PyTorch, scikit-learn; deployed on AWS SageMaker",
        "<b>GIS:</b> QGIS, Google Earth Engine, PostGIS, GeoServer",
        "<b>Data:</b> PostgreSQL + TimescaleDB (time series) + MongoDB (unstructured)",
        "<b>Cloud:</b> AWS (primary) with edge computing nodes for offline-first capability",
        "<b>Blockchain:</b> Hyperledger Fabric for produce traceability and transparent pricing",
        "<b>Integration:</b> UPI, Aadhaar eKYC, DigiLocker, eNAM APIs",
    ]
    for t in tech_stack:
        story.append(Paragraph(t, styles['BulletText'], bulletText='\u2022'))
    story.append(PageBreak())


def build_impact_thesis(story, styles):
    """Section 11: Impact Thesis"""
    story.append(Paragraph("IMPACT THESIS", styles['Heading1Green']))
    story.append(Paragraph(
        "Deep, Measurable Social Impact Aligned with Financial Returns",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Theory of Change", styles['Heading2Green']))
    story.append(Paragraph(
        "PARVAT-SETU's impact thesis is built on the evidence that smallholder poverty in mountain regions "
        "is primarily a market failure rather than a productivity failure. Mountain farmers already produce "
        "high-value crops; the value is destroyed by intermediation, logistics, and financial exclusion. "
        "By addressing these structural barriers through technology-enabled cooperative action, we unlock "
        "existing value rather than requiring behavior change - a fundamentally more scalable approach.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    toc_data = [
        [Paragraph("<b>Stage</b>", styles['TableHeader']),
         Paragraph("<b>Description</b>", styles['TableHeader']),
         Paragraph("<b>Indicators</b>", styles['TableHeader'])],
        [Paragraph("INPUTS", styles['TableCellBold']),
         Paragraph("Capital (INR 5 Cr), Technology (AI/GIS platform), Team (37 people), Partnerships (FPOs, NABARD, buyers)", styles['TableCell']),
         Paragraph("Funds deployed, platform live, team hired, MOUs signed", styles['TableCell'])],
        [Paragraph("ACTIVITIES", styles['TableCellBold']),
         Paragraph("Farmer onboarding, digital aggregation, market linkage, credit facilitation, capacity building, GIS mapping", styles['TableCell']),
         Paragraph("Training sessions, app downloads, transactions processed, loans disbursed", styles['TableCell'])],
        [Paragraph("OUTPUTS", styles['TableCellBold']),
         Paragraph("50,000 farmers connected, INR 1,200 Cr GMV, 500 buyer relationships, INR 500 Cr credit disbursed", styles['TableCell']),
         Paragraph("Enrollment numbers, GMV, active buyers, credit portfolio", styles['TableCell'])],
        [Paragraph("OUTCOMES", styles['TableCellBold']),
         Paragraph("200% income uplift, 50% reduction in post-harvest loss, 70% financial inclusion, women economic empowerment", styles['TableCell']),
         Paragraph("Income surveys, loss measurement, credit access rates, women participation", styles['TableCell'])],
        [Paragraph("IMPACT", styles['TableCellBold']),
         Paragraph("Poverty reduction for 250,000 people, gender equity, climate resilience, reversed migration, preserved biodiversity", styles['TableCell']),
         Paragraph("Poverty headcount, gender indices, migration data, biodiversity metrics", styles['TableCell'])],
    ]
    story.append(make_table(toc_data, col_widths=[1.0*inch, 3.2*inch, 2.4*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("SDG Contribution", styles['Heading2Green']))
    sdg_data = [
        [Paragraph("<b>SDG</b>", styles['TableHeader']),
         Paragraph("<b>Target</b>", styles['TableHeader']),
         Paragraph("<b>PARVAT-SETU Contribution</b>", styles['TableHeader'])],
        [Paragraph("SDG 1: No Poverty", styles['TableCellBold']),
         Paragraph("1.1, 1.2, 1.4", styles['TableCellCenter']),
         Paragraph("200% income uplift lifting 50,000 families above poverty line", styles['TableCell'])],
        [Paragraph("SDG 2: Zero Hunger", styles['TableCellBold']),
         Paragraph("2.3, 2.4", styles['TableCellCenter']),
         Paragraph("Doubling agricultural productivity and ensuring food security", styles['TableCell'])],
        [Paragraph("SDG 5: Gender Equality", styles['TableCellBold']),
         Paragraph("5.5, 5.a", styles['TableCellCenter']),
         Paragraph("60% women participation, economic agency, leadership roles", styles['TableCell'])],
        [Paragraph("SDG 8: Decent Work", styles['TableCellBold']),
         Paragraph("8.2, 8.3, 8.5", styles['TableCellCenter']),
         Paragraph("Dignified livelihoods, reduced drudgery, productive employment", styles['TableCell'])],
        [Paragraph("SDG 10: Reduced Inequality", styles['TableCellBold']),
         Paragraph("10.1, 10.2", styles['TableCellCenter']),
         Paragraph("Bottom 40% income growth, social inclusion of marginalized", styles['TableCell'])],
        [Paragraph("SDG 13: Climate Action", styles['TableCellBold']),
         Paragraph("13.1, 13.2", styles['TableCellCenter']),
         Paragraph("Climate-adaptive farming, carbon sequestration, resilience building", styles['TableCell'])],
        [Paragraph("SDG 15: Life on Land", styles['TableCellBold']),
         Paragraph("15.4, 15.6", styles['TableCellCenter']),
         Paragraph("Mountain ecosystem conservation through sustainable land use", styles['TableCell'])],
    ]
    story.append(make_table(sdg_data, col_widths=[1.5*inch, 1.0*inch, 4.1*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Impact KPIs with Year 1-5 Targets (IRIS+ Aligned)", styles['Heading2Green']))
    kpi_data = [
        [Paragraph("<b>KPI (IRIS+ Code)</b>", styles['TableHeader']),
         Paragraph("<b>Y1</b>", styles['TableHeader']),
         Paragraph("<b>Y2</b>", styles['TableHeader']),
         Paragraph("<b>Y3</b>", styles['TableHeader']),
         Paragraph("<b>Y4</b>", styles['TableHeader']),
         Paragraph("<b>Y5</b>", styles['TableHeader'])],
        [Paragraph("Farmers Reached (PI1824)", styles['TableCell']),
         Paragraph("2,500", styles['TableCellCenter']),
         Paragraph("8,000", styles['TableCellCenter']),
         Paragraph("18,000", styles['TableCellCenter']),
         Paragraph("32,000", styles['TableCellCenter']),
         Paragraph("50,000", styles['TableCellCenter'])],
        [Paragraph("Income Increase % (PI2734)", styles['TableCell']),
         Paragraph("40%", styles['TableCellCenter']),
         Paragraph("80%", styles['TableCellCenter']),
         Paragraph("120%", styles['TableCellCenter']),
         Paragraph("160%", styles['TableCellCenter']),
         Paragraph("200%", styles['TableCellCenter'])],
        [Paragraph("Women Participation (OI8118)", styles['TableCell']),
         Paragraph("55%", styles['TableCellCenter']),
         Paragraph("58%", styles['TableCellCenter']),
         Paragraph("60%", styles['TableCellCenter']),
         Paragraph("60%", styles['TableCellCenter']),
         Paragraph("60%", styles['TableCellCenter'])],
        [Paragraph("Financial Inclusion (PI5752)", styles['TableCell']),
         Paragraph("20%", styles['TableCellCenter']),
         Paragraph("35%", styles['TableCellCenter']),
         Paragraph("50%", styles['TableCellCenter']),
         Paragraph("60%", styles['TableCellCenter']),
         Paragraph("70%", styles['TableCellCenter'])],
        [Paragraph("Post-harvest Loss Reduction", styles['TableCell']),
         Paragraph("10%", styles['TableCellCenter']),
         Paragraph("20%", styles['TableCellCenter']),
         Paragraph("30%", styles['TableCellCenter']),
         Paragraph("40%", styles['TableCellCenter']),
         Paragraph("50%", styles['TableCellCenter'])],
        [Paragraph("Carbon Sequestered (tCO2e)", styles['TableCell']),
         Paragraph("2,000", styles['TableCellCenter']),
         Paragraph("8,000", styles['TableCellCenter']),
         Paragraph("18,000", styles['TableCellCenter']),
         Paragraph("35,000", styles['TableCellCenter']),
         Paragraph("50,000", styles['TableCellCenter'])],
    ]
    story.append(make_table(kpi_data, col_widths=[2.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch]))
    story.append(spacer(8))
    
    story.append(Paragraph("Gender Lens", styles['Heading2Green']))
    story.append(Paragraph(
        "Women perform 70-80% of agricultural labor in mountain regions but control less than 10% of income. "
        "PARVAT-SETU embeds gender equity at every level: 60% target women participation, women-led SHGs as "
        "primary onboarding channel, women board representation mandated at 40%+, and financial products "
        "designed for women's cash flow patterns. Impact measurement disaggregated by gender. The enterprise "
        "specifically targets GI-tagged products where women dominate production (pickles, textiles, dairy).",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_revenue_model(story, styles):
    """Section 12: Revenue Model Deep Dive"""
    story.append(Paragraph("REVENUE MODEL DEEP DIVE", styles['Heading1Green']))
    story.append(Paragraph(
        "Five Diversified Revenue Streams with Strong Unit Economics",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "PARVAT-SETU generates revenue through five complementary streams, each addressing a different "
        "value creation point in the mountain agriculture value chain. This diversification reduces "
        "concentration risk and creates multiple growth vectors.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Revenue Stream 1: Transaction Commissions (3-5% of GMV)", styles['Heading2Green']))
    story.append(Paragraph(
        "The primary revenue engine. PARVAT-SETU charges a transparent commission on every transaction "
        "facilitated through the platform. This is significantly below the 30-70% intermediary margins "
        "currently extracted, creating a clear value proposition for both farmers and buyers. Commission "
        "rates are tiered: 3% for staples/commodities, 4% for horticulture/specialty, 5% for processed/premium "
        "products. At scale (Year 5), this stream alone generates INR 6 Crore on INR 120 Crore GMV.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Revenue Stream 2: Value-Added Processing (15-25% margin)", styles['Heading2Green']))
    story.append(Paragraph(
        "Mountain produce has 40-100% premium potential when minimally processed, graded, and branded. "
        "PARVAT-SETU operates community-owned processing units for grading, sorting, packaging, drying, "
        "and minimal processing. The margin on processed products is 15-25% versus 3-5% on raw produce. "
        "Products include branded Himalayan honey, dried herbs, cold-pressed oils, organic spices, "
        "and GI-tagged specialties. Year 5 target: INR 8 Crore revenue from processing.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Revenue Stream 3: Buyer Subscriptions (INR 25K-1L/year)", styles['Heading2Green']))
    story.append(Paragraph(
        "Premium buyers (organic retailers, HoReCa chains, export houses) pay annual subscriptions for "
        "guaranteed access to traceable mountain produce, quality assurance, and volume reliability. "
        "Subscription tiers: Basic (INR 25,000/year for market access), Premium (INR 50,000/year + "
        "priority allocation), Enterprise (INR 1,00,000/year + custom sourcing + traceability dashboard). "
        "Year 5 target: 500 active buyer subscriptions generating INR 3.5 Crore.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Revenue Stream 4: Financial Services Revenue Share (1-2%)", styles['Heading2Green']))
    story.append(Paragraph(
        "PARVAT-SETU facilitates credit, insurance, and savings products for farmer members through "
        "partnerships with banks, NBFCs, and insurance companies. Revenue is earned as origination fees "
        "and revenue share on portfolio. The platform's transaction data and satellite-based monitoring "
        "enable superior credit underwriting. Year 5 target: INR 500 Crore credit facilitated, "
        "INR 5 Crore revenue from financial services.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Revenue Stream 5: Data Services", styles['Heading2Green']))
    story.append(Paragraph(
        "The platform generates valuable agricultural intelligence: crop area estimates, yield forecasts, "
        "price trends, and climate impact data. Revenue from: (a) Insurance companies for parametric "
        "product design, (b) Government for scheme targeting and monitoring, (c) Research institutions "
        "for agricultural intelligence, (d) Carbon credit verification data. Year 5 target: INR 2 Crore.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Unit Economics Breakdown", styles['Heading2Green']))
    unit_econ = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 5 (Mature)</b>", styles['TableHeader'])],
        [Paragraph("Revenue per Farmer", styles['TableCellBold']),
         Paragraph("INR 800", styles['TableCellCenter']),
         Paragraph("INR 4,000", styles['TableCellCenter']),
         Paragraph("INR 5,400", styles['TableCellCenter'])],
        [Paragraph("GMV per Farmer", styles['TableCellBold']),
         Paragraph("INR 3,200", styles['TableCellCenter']),
         Paragraph("INR 13,300", styles['TableCellCenter']),
         Paragraph("INR 24,000", styles['TableCellCenter'])],
        [Paragraph("CAC (Customer Acquisition Cost)", styles['TableCellBold']),
         Paragraph("INR 5,000", styles['TableCellCenter']),
         Paragraph("INR 3,500", styles['TableCellCenter']),
         Paragraph("INR 2,800", styles['TableCellCenter'])],
        [Paragraph("Annual Retention Rate", styles['TableCellBold']),
         Paragraph("85%", styles['TableCellCenter']),
         Paragraph("92%", styles['TableCellCenter']),
         Paragraph("95%", styles['TableCellCenter'])],
        [Paragraph("LTV (8-year horizon)", styles['TableCellBold']),
         Paragraph("INR 28,000", styles['TableCellCenter']),
         Paragraph("INR 38,000", styles['TableCellCenter']),
         Paragraph("INR 45,000", styles['TableCellCenter'])],
        [Paragraph("LTV/CAC Ratio", styles['TableCellBold']),
         Paragraph("5.6x", styles['TableCellCenter']),
         Paragraph("10.9x", styles['TableCellCenter']),
         Paragraph("16.1x", styles['TableCellCenter'])],
        [Paragraph("Contribution Margin per Farmer", styles['TableCellBold']),
         Paragraph("-INR 1,200", styles['TableCellCenter']),
         Paragraph("INR 1,400", styles['TableCellCenter']),
         Paragraph("INR 2,800", styles['TableCellCenter'])],
    ]
    story.append(make_table(unit_econ, col_widths=[2.2*inch, 1.4*inch, 1.4*inch, 1.6*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Revenue Buildup: Year 1-5", styles['Heading2Green']))
    rev_data = [
        [Paragraph("<b>Revenue Stream</b>", styles['TableHeader']),
         Paragraph("<b>Y1 (INR L)</b>", styles['TableHeader']),
         Paragraph("<b>Y2 (INR L)</b>", styles['TableHeader']),
         Paragraph("<b>Y3 (INR L)</b>", styles['TableHeader']),
         Paragraph("<b>Y4 (INR L)</b>", styles['TableHeader']),
         Paragraph("<b>Y5 (INR L)</b>", styles['TableHeader'])],
        [Paragraph("Transaction Commissions", styles['TableCell']),
         Paragraph("3", styles['TableCellCenter']),
         Paragraph("25", styles['TableCellCenter']),
         Paragraph("96", styles['TableCellCenter']),
         Paragraph("230", styles['TableCellCenter']),
         Paragraph("600", styles['TableCellCenter'])],
        [Paragraph("Value-Added Processing", styles['TableCell']),
         Paragraph("8", styles['TableCellCenter']),
         Paragraph("80", styles['TableCellCenter']),
         Paragraph("320", styles['TableCellCenter']),
         Paragraph("580", styles['TableCellCenter']),
         Paragraph("800", styles['TableCellCenter'])],
        [Paragraph("Buyer Subscriptions", styles['TableCell']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("45", styles['TableCellCenter']),
         Paragraph("150", styles['TableCellCenter']),
         Paragraph("250", styles['TableCellCenter']),
         Paragraph("350", styles['TableCellCenter'])],
        [Paragraph("Financial Services", styles['TableCell']),
         Paragraph("2", styles['TableCellCenter']),
         Paragraph("20", styles['TableCellCenter']),
         Paragraph("100", styles['TableCellCenter']),
         Paragraph("280", styles['TableCellCenter']),
         Paragraph("500", styles['TableCellCenter'])],
        [Paragraph("Data Services", styles['TableCell']),
         Paragraph("2", styles['TableCellCenter']),
         Paragraph("15", styles['TableCellCenter']),
         Paragraph("54", styles['TableCellCenter']),
         Paragraph("110", styles['TableCellCenter']),
         Paragraph("200", styles['TableCellCenter'])],
        [Paragraph("<b>TOTAL REVENUE</b>", styles['TableCellBold']),
         Paragraph("<b>20</b>", styles['TableCellCenter']),
         Paragraph("<b>185</b>", styles['TableCellCenter']),
         Paragraph("<b>720</b>", styles['TableCellCenter']),
         Paragraph("<b>1,450</b>", styles['TableCellCenter']),
         Paragraph("<b>2,700</b> (27 Cr)", styles['TableCellCenter'])],
    ]
    story.append(make_table(rev_data, col_widths=[1.8*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.2*inch]))
    story.append(PageBreak())


def build_financial_projections(story, styles):
    """Section 13: Financial Projections"""
    story.append(Paragraph("FINANCIAL PROJECTIONS", styles['Heading1Green']))
    story.append(Paragraph(
        "Conservative Assumptions, Attractive Returns",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("5-Year Profit &amp; Loss Statement", styles['Heading2Green']))
    pl_data = [
        [Paragraph("<b>Item (INR Lakhs)</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 2</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 4</b>", styles['TableHeader']),
         Paragraph("<b>Year 5</b>", styles['TableHeader'])],
        [Paragraph("<b>Revenue</b>", styles['TableCellBold']),
         Paragraph("20", styles['TableCellCenter']),
         Paragraph("185", styles['TableCellCenter']),
         Paragraph("720", styles['TableCellCenter']),
         Paragraph("1,450", styles['TableCellCenter']),
         Paragraph("2,700", styles['TableCellCenter'])],
        [Paragraph("COGS", styles['TableCell']),
         Paragraph("(13)", styles['TableCellCenter']),
         Paragraph("(115)", styles['TableCellCenter']),
         Paragraph("(418)", styles['TableCellCenter']),
         Paragraph("(754)", styles['TableCellCenter']),
         Paragraph("(1,215)", styles['TableCellCenter'])],
        [Paragraph("<b>Gross Profit</b>", styles['TableCellBold']),
         Paragraph("7", styles['TableCellCenter']),
         Paragraph("70", styles['TableCellCenter']),
         Paragraph("302", styles['TableCellCenter']),
         Paragraph("696", styles['TableCellCenter']),
         Paragraph("1,485", styles['TableCellCenter'])],
        [Paragraph("Gross Margin %", styles['TableCell']),
         Paragraph("35%", styles['TableCellCenter']),
         Paragraph("38%", styles['TableCellCenter']),
         Paragraph("42%", styles['TableCellCenter']),
         Paragraph("48%", styles['TableCellCenter']),
         Paragraph("55%", styles['TableCellCenter'])],
        [Paragraph("Operating Expenses", styles['TableCell']),
         Paragraph("(43)", styles['TableCellCenter']),
         Paragraph("(153)", styles['TableCellCenter']),
         Paragraph("(266)", styles['TableCellCenter']),
         Paragraph("(435)", styles['TableCellCenter']),
         Paragraph("(729)", styles['TableCellCenter'])],
        [Paragraph("- Technology &amp; Platform", styles['TableCell']),
         Paragraph("(15)", styles['TableCellCenter']),
         Paragraph("(42)", styles['TableCellCenter']),
         Paragraph("(65)", styles['TableCellCenter']),
         Paragraph("(95)", styles['TableCellCenter']),
         Paragraph("(140)", styles['TableCellCenter'])],
        [Paragraph("- Team &amp; HR", styles['TableCell']),
         Paragraph("(18)", styles['TableCellCenter']),
         Paragraph("(60)", styles['TableCellCenter']),
         Paragraph("(105)", styles['TableCellCenter']),
         Paragraph("(180)", styles['TableCellCenter']),
         Paragraph("(300)", styles['TableCellCenter'])],
        [Paragraph("- Field Operations", styles['TableCell']),
         Paragraph("(8)", styles['TableCellCenter']),
         Paragraph("(38)", styles['TableCellCenter']),
         Paragraph("(72)", styles['TableCellCenter']),
         Paragraph("(120)", styles['TableCellCenter']),
         Paragraph("(200)", styles['TableCellCenter'])],
        [Paragraph("- G&amp;A", styles['TableCell']),
         Paragraph("(2)", styles['TableCellCenter']),
         Paragraph("(13)", styles['TableCellCenter']),
         Paragraph("(24)", styles['TableCellCenter']),
         Paragraph("(40)", styles['TableCellCenter']),
         Paragraph("(89)", styles['TableCellCenter'])],
        [Paragraph("<b>EBITDA</b>", styles['TableCellBold']),
         Paragraph("(36)", styles['TableCellCenter']),
         Paragraph("(83)", styles['TableCellCenter']),
         Paragraph("36", styles['TableCellCenter']),
         Paragraph("261", styles['TableCellCenter']),
         Paragraph("756", styles['TableCellCenter'])],
        [Paragraph("EBITDA Margin %", styles['TableCell']),
         Paragraph("-180%", styles['TableCellCenter']),
         Paragraph("-45%", styles['TableCellCenter']),
         Paragraph("5%", styles['TableCellCenter']),
         Paragraph("18%", styles['TableCellCenter']),
         Paragraph("28%", styles['TableCellCenter'])],
        [Paragraph("Depreciation &amp; Interest", styles['TableCell']),
         Paragraph("(4)", styles['TableCellCenter']),
         Paragraph("(10)", styles['TableCellCenter']),
         Paragraph("(15)", styles['TableCellCenter']),
         Paragraph("(18)", styles['TableCellCenter']),
         Paragraph("(22)", styles['TableCellCenter'])],
        [Paragraph("<b>Net Profit (Loss)</b>", styles['TableCellBold']),
         Paragraph("(40)", styles['TableCellCenter']),
         Paragraph("(93)", styles['TableCellCenter']),
         Paragraph("21", styles['TableCellCenter']),
         Paragraph("243", styles['TableCellCenter']),
         Paragraph("734", styles['TableCellCenter'])],
    ]
    story.append(make_table(pl_data, col_widths=[1.8*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Cash Flow Statement Summary", styles['Heading2Green']))
    cf_data = [
        [Paragraph("<b>Item (INR Lakhs)</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 2</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 4</b>", styles['TableHeader']),
         Paragraph("<b>Year 5</b>", styles['TableHeader'])],
        [Paragraph("Operating Cash Flow", styles['TableCell']),
         Paragraph("(32)", styles['TableCellCenter']),
         Paragraph("(70)", styles['TableCellCenter']),
         Paragraph("45", styles['TableCellCenter']),
         Paragraph("280", styles['TableCellCenter']),
         Paragraph("780", styles['TableCellCenter'])],
        [Paragraph("Investing Cash Flow", styles['TableCell']),
         Paragraph("(120)", styles['TableCellCenter']),
         Paragraph("(80)", styles['TableCellCenter']),
         Paragraph("(60)", styles['TableCellCenter']),
         Paragraph("(75)", styles['TableCellCenter']),
         Paragraph("(100)", styles['TableCellCenter'])],
        [Paragraph("Financing Cash Flow", styles['TableCell']),
         Paragraph("300", styles['TableCellCenter']),
         Paragraph("150", styles['TableCellCenter']),
         Paragraph("50", styles['TableCellCenter']),
         Paragraph("0", styles['TableCellCenter']),
         Paragraph("(30)", styles['TableCellCenter'])],
        [Paragraph("<b>Net Cash Flow</b>", styles['TableCellBold']),
         Paragraph("148", styles['TableCellCenter']),
         Paragraph("0", styles['TableCellCenter']),
         Paragraph("35", styles['TableCellCenter']),
         Paragraph("205", styles['TableCellCenter']),
         Paragraph("650", styles['TableCellCenter'])],
        [Paragraph("Cumulative Cash", styles['TableCell']),
         Paragraph("148", styles['TableCellCenter']),
         Paragraph("148", styles['TableCellCenter']),
         Paragraph("183", styles['TableCellCenter']),
         Paragraph("388", styles['TableCellCenter']),
         Paragraph("1,038", styles['TableCellCenter'])],
    ]
    story.append(make_table(cf_data, col_widths=[1.8*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Key Financial Metrics", styles['Heading2Green']))
    metrics_data = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Value</b>", styles['TableHeader']),
         Paragraph("<b>Commentary</b>", styles['TableHeader'])],
        [Paragraph("Revenue CAGR (Y1-Y5)", styles['TableCellBold']),
         Paragraph("168%", styles['TableCellCenter']),
         Paragraph("Driven by farmer enrollment and GMV per farmer growth", styles['TableCell'])],
        [Paragraph("Gross Margin (Y5)", styles['TableCellBold']),
         Paragraph("55%", styles['TableCellCenter']),
         Paragraph("Improving with scale and higher-margin product mix", styles['TableCell'])],
        [Paragraph("EBITDA Margin (Y5)", styles['TableCellBold']),
         Paragraph("28%", styles['TableCellCenter']),
         Paragraph("Strong operating leverage as platform scales", styles['TableCell'])],
        [Paragraph("Break-even Point", styles['TableCellBold']),
         Paragraph("Month 48", styles['TableCellCenter']),
         Paragraph("Cash-flow positive from Year 3 operations", styles['TableCell'])],
        [Paragraph("IRR for Equity Investors", styles['TableCellBold']),
         Paragraph("28-35%", styles['TableCellCenter']),
         Paragraph("Based on 7-year exit at 8-12x revenue multiple", styles['TableCell'])],
        [Paragraph("Payback Period", styles['TableCellBold']),
         Paragraph("5.5 years", styles['TableCellCenter']),
         Paragraph("Within impact investing standard horizon", styles['TableCell'])],
    ]
    story.append(make_table(metrics_data, col_widths=[2.0*inch, 1.2*inch, 3.4*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Sensitivity Analysis: Three Scenarios", styles['Heading2Green']))
    scenario_data = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Pessimistic</b>", styles['TableHeader']),
         Paragraph("<b>Base Case</b>", styles['TableHeader']),
         Paragraph("<b>Optimistic</b>", styles['TableHeader'])],
        [Paragraph("Y5 Revenue (INR Cr)", styles['TableCellBold']),
         Paragraph("15", styles['TableCellCenter']),
         Paragraph("27", styles['TableCellCenter']),
         Paragraph("42", styles['TableCellCenter'])],
        [Paragraph("Y5 Farmers Enrolled", styles['TableCellBold']),
         Paragraph("30,000", styles['TableCellCenter']),
         Paragraph("50,000", styles['TableCellCenter']),
         Paragraph("75,000", styles['TableCellCenter'])],
        [Paragraph("Break-even (Month)", styles['TableCellBold']),
         Paragraph("60", styles['TableCellCenter']),
         Paragraph("48", styles['TableCellCenter']),
         Paragraph("36", styles['TableCellCenter'])],
        [Paragraph("Y5 EBITDA Margin", styles['TableCellBold']),
         Paragraph("15%", styles['TableCellCenter']),
         Paragraph("28%", styles['TableCellCenter']),
         Paragraph("35%", styles['TableCellCenter'])],
        [Paragraph("Equity IRR", styles['TableCellBold']),
         Paragraph("18%", styles['TableCellCenter']),
         Paragraph("28-35%", styles['TableCellCenter']),
         Paragraph("45%+", styles['TableCellCenter'])],
        [Paragraph("Probability Weighted", styles['TableCellBold']),
         Paragraph("25%", styles['TableCellCenter']),
         Paragraph("55%", styles['TableCellCenter']),
         Paragraph("20%", styles['TableCellCenter'])],
    ]
    story.append(make_table(scenario_data, col_widths=[2.0*inch, 1.5*inch, 1.5*inch, 1.6*inch]))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "Even in the pessimistic scenario, the enterprise achieves break-even within 5 years and delivers "
        "18% IRR - above the impact investing threshold. The base case delivers 28-35% IRR, competitive "
        "with mainstream venture capital returns while delivering transformative social impact.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_balance_sheet(story, styles):
    """Balance Sheet Summary - continuation of financial projections"""
    story.append(Paragraph("BALANCE SHEET &amp; ADDITIONAL FINANCIAL ANALYSIS", styles['Heading1Green']))
    story.append(Paragraph(
        "Asset Build-Up and Capital Efficiency Metrics",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Balance Sheet Summary (INR Lakhs)", styles['Heading2Green']))
    bs_data = [
        [Paragraph("<b>Item</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 2</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 4</b>", styles['TableHeader']),
         Paragraph("<b>Year 5</b>", styles['TableHeader'])],
        [Paragraph("<b>ASSETS</b>", styles['TableCellBold']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell'])],
        [Paragraph("Cash &amp; Equivalents", styles['TableCell']),
         Paragraph("148", styles['TableCellCenter']),
         Paragraph("148", styles['TableCellCenter']),
         Paragraph("183", styles['TableCellCenter']),
         Paragraph("388", styles['TableCellCenter']),
         Paragraph("1,038", styles['TableCellCenter'])],
        [Paragraph("Receivables", styles['TableCell']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("35", styles['TableCellCenter']),
         Paragraph("120", styles['TableCellCenter']),
         Paragraph("240", styles['TableCellCenter']),
         Paragraph("450", styles['TableCellCenter'])],
        [Paragraph("Inventory (processing)", styles['TableCell']),
         Paragraph("3", styles['TableCellCenter']),
         Paragraph("20", styles['TableCellCenter']),
         Paragraph("60", styles['TableCellCenter']),
         Paragraph("100", styles['TableCellCenter']),
         Paragraph("150", styles['TableCellCenter'])],
        [Paragraph("Fixed Assets (net)", styles['TableCell']),
         Paragraph("95", styles['TableCellCenter']),
         Paragraph("155", styles['TableCellCenter']),
         Paragraph("195", styles['TableCellCenter']),
         Paragraph("245", styles['TableCellCenter']),
         Paragraph("320", styles['TableCellCenter'])],
        [Paragraph("Intangible Assets (tech)", styles['TableCell']),
         Paragraph("25", styles['TableCellCenter']),
         Paragraph("45", styles['TableCellCenter']),
         Paragraph("60", styles['TableCellCenter']),
         Paragraph("70", styles['TableCellCenter']),
         Paragraph("80", styles['TableCellCenter'])],
        [Paragraph("<b>Total Assets</b>", styles['TableCellBold']),
         Paragraph("<b>276</b>", styles['TableCellCenter']),
         Paragraph("<b>403</b>", styles['TableCellCenter']),
         Paragraph("<b>618</b>", styles['TableCellCenter']),
         Paragraph("<b>1,043</b>", styles['TableCellCenter']),
         Paragraph("<b>2,038</b>", styles['TableCellCenter'])],
        [Paragraph("<b>LIABILITIES</b>", styles['TableCellBold']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell'])],
        [Paragraph("Payables", styles['TableCell']),
         Paragraph("8", styles['TableCellCenter']),
         Paragraph("45", styles['TableCellCenter']),
         Paragraph("100", styles['TableCellCenter']),
         Paragraph("180", styles['TableCellCenter']),
         Paragraph("280", styles['TableCellCenter'])],
        [Paragraph("Term Loan Outstanding", styles['TableCell']),
         Paragraph("75", styles['TableCellCenter']),
         Paragraph("75", styles['TableCellCenter']),
         Paragraph("60", styles['TableCellCenter']),
         Paragraph("40", styles['TableCellCenter']),
         Paragraph("15", styles['TableCellCenter'])],
        [Paragraph("Other Liabilities", styles['TableCell']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("12", styles['TableCellCenter']),
         Paragraph("20", styles['TableCellCenter']),
         Paragraph("30", styles['TableCellCenter']),
         Paragraph("40", styles['TableCellCenter'])],
        [Paragraph("<b>Total Liabilities</b>", styles['TableCellBold']),
         Paragraph("<b>88</b>", styles['TableCellCenter']),
         Paragraph("<b>132</b>", styles['TableCellCenter']),
         Paragraph("<b>180</b>", styles['TableCellCenter']),
         Paragraph("<b>250</b>", styles['TableCellCenter']),
         Paragraph("<b>335</b>", styles['TableCellCenter'])],
        [Paragraph("<b>EQUITY</b>", styles['TableCellBold']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell'])],
        [Paragraph("Share Capital", styles['TableCell']),
         Paragraph("125", styles['TableCellCenter']),
         Paragraph("125", styles['TableCellCenter']),
         Paragraph("125", styles['TableCellCenter']),
         Paragraph("125", styles['TableCellCenter']),
         Paragraph("125", styles['TableCellCenter'])],
        [Paragraph("Grants Utilized", styles['TableCell']),
         Paragraph("103", styles['TableCellCenter']),
         Paragraph("239", styles['TableCellCenter']),
         Paragraph("292", styles['TableCellCenter']),
         Paragraph("300", styles['TableCellCenter']),
         Paragraph("300", styles['TableCellCenter'])],
        [Paragraph("Retained Earnings", styles['TableCell']),
         Paragraph("(40)", styles['TableCellCenter']),
         Paragraph("(93)", styles['TableCellCenter']),
         Paragraph("21", styles['TableCellCenter']),
         Paragraph("368", styles['TableCellCenter']),
         Paragraph("1,278", styles['TableCellCenter'])],
        [Paragraph("<b>Total Equity</b>", styles['TableCellBold']),
         Paragraph("<b>188</b>", styles['TableCellCenter']),
         Paragraph("<b>271</b>", styles['TableCellCenter']),
         Paragraph("<b>438</b>", styles['TableCellCenter']),
         Paragraph("<b>793</b>", styles['TableCellCenter']),
         Paragraph("<b>1,703</b>", styles['TableCellCenter'])],
    ]
    story.append(make_table(bs_data, col_widths=[1.8*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.85*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Capital Efficiency Metrics", styles['Heading2Green']))
    eff_data = [
        [Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Year 1</b>", styles['TableHeader']),
         Paragraph("<b>Year 3</b>", styles['TableHeader']),
         Paragraph("<b>Year 5</b>", styles['TableHeader']),
         Paragraph("<b>Commentary</b>", styles['TableHeader'])],
        [Paragraph("Return on Assets", styles['TableCellBold']),
         Paragraph("-14%", styles['TableCellCenter']),
         Paragraph("3.4%", styles['TableCellCenter']),
         Paragraph("36%", styles['TableCellCenter']),
         Paragraph("Rapid improvement as revenue scales on fixed asset base", styles['TableCell'])],
        [Paragraph("Return on Equity", styles['TableCellBold']),
         Paragraph("-21%", styles['TableCellCenter']),
         Paragraph("4.8%", styles['TableCellCenter']),
         Paragraph("43%", styles['TableCellCenter']),
         Paragraph("Attractive returns from Year 3 onwards", styles['TableCell'])],
        [Paragraph("Debt/Equity Ratio", styles['TableCellBold']),
         Paragraph("0.40", styles['TableCellCenter']),
         Paragraph("0.14", styles['TableCellCenter']),
         Paragraph("0.01", styles['TableCellCenter']),
         Paragraph("Low leverage; strong balance sheet by Year 5", styles['TableCell'])],
        [Paragraph("Revenue/Employee", styles['TableCellBold']),
         Paragraph("INR 1.8L", styles['TableCellCenter']),
         Paragraph("INR 24L", styles['TableCellCenter']),
         Paragraph("INR 64L", styles['TableCellCenter']),
         Paragraph("Strong productivity improvement with platform scale", styles['TableCell'])],
        [Paragraph("Asset Turnover", styles['TableCellBold']),
         Paragraph("0.07x", styles['TableCellCenter']),
         Paragraph("1.16x", styles['TableCellCenter']),
         Paragraph("1.32x", styles['TableCellCenter']),
         Paragraph("Efficient asset utilization at scale", styles['TableCell'])],
    ]
    story.append(make_table(eff_data, col_widths=[1.4*inch, 0.8*inch, 0.8*inch, 0.8*inch, 2.8*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Valuation Framework", styles['Heading2Green']))
    story.append(Paragraph(
        "For investor exit planning, we present indicative valuations based on comparable transaction multiples "
        "in the Indian AgriTech and impact enterprise space:",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    val_data = [
        [Paragraph("<b>Valuation Method</b>", styles['TableHeader']),
         Paragraph("<b>Multiple</b>", styles['TableHeader']),
         Paragraph("<b>Year 5 Value</b>", styles['TableHeader']),
         Paragraph("<b>Year 7 Value</b>", styles['TableHeader']),
         Paragraph("<b>Basis</b>", styles['TableHeader'])],
        [Paragraph("Revenue Multiple", styles['TableCellBold']),
         Paragraph("8-12x", styles['TableCellCenter']),
         Paragraph("INR 216-324 Cr", styles['TableCellCenter']),
         Paragraph("INR 400-600 Cr", styles['TableCellCenter']),
         Paragraph("AgriTech comps (DeHaat 12x, Ninjacart 10x)", styles['TableCell'])],
        [Paragraph("EBITDA Multiple", styles['TableCellBold']),
         Paragraph("20-30x", styles['TableCellCenter']),
         Paragraph("INR 151-227 Cr", styles['TableCellCenter']),
         Paragraph("INR 320-480 Cr", styles['TableCellCenter']),
         Paragraph("Growth-stage impact enterprises", styles['TableCell'])],
        [Paragraph("GMV Multiple", styles['TableCellBold']),
         Paragraph("1.5-2.5x", styles['TableCellCenter']),
         Paragraph("INR 180-300 Cr", styles['TableCellCenter']),
         Paragraph("INR 375-625 Cr", styles['TableCellCenter']),
         Paragraph("Marketplace platforms", styles['TableCell'])],
        [Paragraph("<b>Blended Valuation</b>", styles['TableCellBold']),
         Paragraph("<b>Avg</b>", styles['TableCellCenter']),
         Paragraph("<b>INR 180-280 Cr</b>", styles['TableCellCenter']),
         Paragraph("<b>INR 360-560 Cr</b>", styles['TableCellCenter']),
         Paragraph("<b>Conservative mid-point</b>", styles['TableCell'])],
    ]
    story.append(make_table(val_data, col_widths=[1.4*inch, 0.9*inch, 1.4*inch, 1.4*inch, 1.5*inch]))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "At a conservative Year 7 valuation of INR 400 Crore, the equity investor stake (15-20%) would be "
        "worth INR 60-80 Crore on an initial investment of INR 1.25 Crore, representing a 48-64x return "
        "and approximately 72-83% IRR. Even at the lowest scenario (INR 180 Cr valuation at Year 5), "
        "the investor stake is worth INR 27-36 Crore, a 22-29x return (65-75% IRR over 5 years).",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_blended_finance(story, styles):
    """Section 14: Blended Finance Structure"""
    story.append(Paragraph("BLENDED FINANCE STRUCTURE", styles['Heading1Green']))
    story.append(Paragraph(
        "Optimizing the Risk-Return-Impact Triangle for Different Investor Types",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Why Blended Finance?", styles['Heading2Green']))
    story.append(Paragraph(
        "Mountain agriculture social enterprise faces a fundamental challenge: the highest-impact activities "
        "(farmer onboarding, trust building, cooperative formation) are also the highest-risk and lowest-return "
        "in early years. Pure commercial capital would demand returns that distort the social mission. Pure "
        "grant funding lacks accountability and scalability. Blended finance solves this by matching capital type "
        "to risk profile:",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    blend_rationale = [
        "<b>Grant capital absorbs pilot risk:</b> The first 18 months involve trust building, technology development, and proof-of-concept - activities with uncertain outcomes but critical for later commercial viability.",
        "<b>Equity capital captures growth:</b> Once pilot proves product-market fit, equity investors participate in scaling economics with de-risked execution.",
        "<b>Debt provides working capital efficiency:</b> Once cash flows are predictable, concessional debt funds expansion at lower cost of capital than equity dilution.",
    ]
    for b in blend_rationale:
        story.append(Paragraph(b, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))
    
    story.append(Paragraph("Capital Stack - Detailed Terms", styles['Heading2Green']))
    cap_stack = [
        [Paragraph("<b>Tier</b>", styles['TableHeader']),
         Paragraph("<b>Type</b>", styles['TableHeader']),
         Paragraph("<b>Amount</b>", styles['TableHeader']),
         Paragraph("<b>Source</b>", styles['TableHeader']),
         Paragraph("<b>Terms</b>", styles['TableHeader']),
         Paragraph("<b>Risk Absorbed</b>", styles['TableHeader'])],
        [Paragraph("1 (First Loss)", styles['TableCellBold']),
         Paragraph("Grant", styles['TableCellCenter']),
         Paragraph("INR 3.0 Cr", styles['TableCellCenter']),
         Paragraph("NABARD RIF, Ford Foundation, BMGF, CSR", styles['TableCell']),
         Paragraph("Non-returnable; milestone-based; 18-month disbursement", styles['TableCell']),
         Paragraph("Pilot risk, tech development, farmer onboarding", styles['TableCell'])],
        [Paragraph("2 (Mezzanine)", styles['TableCellBold']),
         Paragraph("Impact Equity", styles['TableCellCenter']),
         Paragraph("INR 1.25 Cr", styles['TableCellCenter']),
         Paragraph("Omidyar, Acumen, Aavishkaar, Unitus", styles['TableCell']),
         Paragraph("15-20% equity; board seat; 25%+ IRR target; 5-8 yr horizon", styles['TableCell']),
         Paragraph("Scale risk (de-risked by grant layer)", styles['TableCell'])],
        [Paragraph("3 (Senior)", styles['TableCellBold']),
         Paragraph("Concessional Debt", styles['TableCellCenter']),
         Paragraph("INR 0.75 Cr", styles['TableCellCenter']),
         Paragraph("SIDBI, Caspian, Northern Arc, NABARD term loan", styles['TableCell']),
         Paragraph("8-12% interest; 2-yr moratorium; 5-yr tenure; cash-flow based", styles['TableCell']),
         Paragraph("Working capital gap (secured by receivables)", styles['TableCell'])],
    ]
    story.append(make_table(cap_stack, col_widths=[0.8*inch, 0.8*inch, 0.8*inch, 1.3*inch, 1.5*inch, 1.4*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Investor Returns Projection", styles['Heading2Green']))
    returns_data = [
        [Paragraph("<b>Investor Type</b>", styles['TableHeader']),
         Paragraph("<b>Investment</b>", styles['TableHeader']),
         Paragraph("<b>Expected Return</b>", styles['TableHeader']),
         Paragraph("<b>Timeline</b>", styles['TableHeader']),
         Paragraph("<b>Exit Mechanism</b>", styles['TableHeader'])],
        [Paragraph("Grant Providers", styles['TableCellBold']),
         Paragraph("INR 3.0 Cr", styles['TableCellCenter']),
         Paragraph("Social return: 50,000 families impacted, 8x SROI", styles['TableCell']),
         Paragraph("N/A (non-returnable)", styles['TableCellCenter']),
         Paragraph("Impact reports, IRIS+ metrics", styles['TableCell'])],
        [Paragraph("Equity Investors", styles['TableCellBold']),
         Paragraph("INR 1.25 Cr", styles['TableCellCenter']),
         Paragraph("25-35% IRR; 4-6x money multiple", styles['TableCell']),
         Paragraph("5-8 years", styles['TableCellCenter']),
         Paragraph("Trade sale / secondary / revenue-based buyback", styles['TableCell'])],
        [Paragraph("Debt Providers", styles['TableCellBold']),
         Paragraph("INR 0.75 Cr", styles['TableCellCenter']),
         Paragraph("8-12% annual interest + principal repayment", styles['TableCell']),
         Paragraph("5 years (2+3)", styles['TableCellCenter']),
         Paragraph("Scheduled repayment from Year 3", styles['TableCell'])],
    ]
    story.append(make_table(returns_data, col_widths=[1.2*inch, 1.0*inch, 2.0*inch, 1.2*inch, 1.8*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph(
        "The blended structure achieves a weighted average cost of capital (WACC) of approximately 8-10%, "
        "significantly below what pure equity funding would require (25%+). This lower WACC enables the "
        "enterprise to maintain its social mission and pricing (3-5% commission vs. 10%+ that pure "
        "commercial models would require) while still delivering attractive returns to each investor class.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Catalytic Capital Leverage", styles['Heading2Green']))
    story.append(Paragraph(
        "Every INR 1 of grant capital is designed to catalyze INR 3.5 of total investment over 5 years. "
        "The initial grant de-risks the model sufficiently to attract commercial equity at Series A "
        "(INR 20-30 Cr), which in turn unlocks commercial debt for working capital (INR 50-100 Cr). "
        "This 1:17 leverage ratio makes grant deployment highly efficient from a donor's perspective.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_go_to_market(story, styles):
    """Section 15: Go-to-Market Strategy"""
    story.append(Paragraph("GO-TO-MARKET STRATEGY", styles['Heading1Green']))
    story.append(Paragraph(
        "Producer-Led Growth with Zero Customer Acquisition Cost",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "PARVAT-SETU's go-to-market strategy leverages existing social infrastructure (SHGs, FPOs) to achieve "
        "near-zero customer acquisition cost while building deep trust - a critical requirement in mountain "
        "communities where external interventions historically have low adoption rates.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Phase 1: Pilot (Months 1-18) - 3 District Deep Dive", styles['Heading2Green']))
    story.append(Paragraph(
        "Focus on 3 districts in Uttarakhand (Chamoli, Bageshwar, Pithoragarh) selected for: existing SHG "
        "density, crop diversity, road connectivity, and research relationships. Target: 2,500 farmers "
        "across 100 SHGs and 3 FPOs. Objective: Prove unit economics, refine technology, establish "
        "buyer relationships, achieve INR 80 Lakh GMV.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Phase 2: Scale (Months 19-36) - Uttarakhand-wide", styles['Heading2Green']))
    story.append(Paragraph(
        "Expand to all 13 districts of Uttarakhand leveraging Phase 1 proof points. Partnership-led growth "
        "through NABARD-supported FPO network (40+ FPOs), State Livelihood Mission SHGs (2,000+ SHGs), "
        "and Horticulture Department extension system. Target: 18,000 farmers, INR 24 Crore GMV. "
        "This phase achieves operating break-even and validates multi-district operations model.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Phase 3: Expansion (Months 37-60) - Pan-IHR", styles['Heading2Green']))
    story.append(Paragraph(
        "Multi-state expansion to Himachal Pradesh, Sikkim, and Northeast states. Growth funded by "
        "earned revenue + Series A capital (INR 20-30 Cr). Partnerships with multilateral agencies "
        "(World Bank, ADB) for enabling environment. Target: 50,000 farmers across 5+ states, "
        "INR 120 Crore GMV, INR 27 Crore revenue.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Customer Acquisition Strategy: SHG-Led Zero-CAC Model", styles['Heading2Green']))
    story.append(Paragraph(
        "The genius of the SHG-led model is that it eliminates traditional customer acquisition cost. "
        "Instead of spending INR 5,000-8,000 per farmer on marketing and sales (industry norm), "
        "PARVAT-SETU leverages existing trust networks:",
        styles['BodyText']
    ))
    
    cac_bullets = [
        "<b>SHG as onboarding channel:</b> Each SHG (10-15 members) is onboarded as a unit, not individually. SHG leaders serve as peer evangelists - trusted by community members.",
        "<b>Demonstration effect:</b> First 2-3 transactions demonstrate value (higher price realization) and trigger word-of-mouth adoption within and across villages.",
        "<b>FPO partnership:</b> Existing FPO membership (500-2,000 farmers each) provides instant access to aggregated farmer base already organized for collective action.",
        "<b>Government scheme integration:</b> Piggyback on NRLM, SHG digitization, and FPO formation programs that are already investing in farmer mobilization.",
    ]
    for b in cac_bullets:
        story.append(Paragraph(b, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))
    
    story.append(Paragraph("GTM Milestones", styles['Heading2Green']))
    gtm_data = [
        [Paragraph("<b>Month</b>", styles['TableHeader']),
         Paragraph("<b>Milestone</b>", styles['TableHeader']),
         Paragraph("<b>KPI</b>", styles['TableHeader']),
         Paragraph("<b>Go/No-Go Gate</b>", styles['TableHeader'])],
        [Paragraph("M6", styles['TableCellBold']),
         Paragraph("First 500 farmers onboarded, platform live", styles['TableCell']),
         Paragraph("500 active users, 50 transactions", styles['TableCell']),
         Paragraph("Farmer willingness to transact digitally", styles['TableCell'])],
        [Paragraph("M12", styles['TableCellBold']),
         Paragraph("First buyer relationships, processing operational", styles['TableCell']),
         Paragraph("5 active buyers, INR 30L GMV", styles['TableCell']),
         Paragraph("Buyer willingness to pay premium", styles['TableCell'])],
        [Paragraph("M18", styles['TableCellBold']),
         Paragraph("2,500 farmers, unit economics validated", styles['TableCell']),
         Paragraph("Positive contribution margin, 85% retention", styles['TableCell']),
         Paragraph("Scalable unit economics proven", styles['TableCell'])],
        [Paragraph("M24", styles['TableCellBold']),
         Paragraph("Multi-district expansion initiated", styles['TableCell']),
         Paragraph("8,000 farmers, INR 3 Cr GMV", styles['TableCell']),
         Paragraph("Operations replicable across districts", styles['TableCell'])],
        [Paragraph("M36", styles['TableCellBold']),
         Paragraph("Uttarakhand-wide, Series A ready", styles['TableCell']),
         Paragraph("18,000 farmers, operating break-even", styles['TableCell']),
         Paragraph("Series A fundraise trigger", styles['TableCell'])],
        [Paragraph("M48", styles['TableCellBold']),
         Paragraph("Multi-state, cash-flow positive", styles['TableCell']),
         Paragraph("32,000 farmers, INR 58 Cr GMV", styles['TableCell']),
         Paragraph("Pan-IHR model validation", styles['TableCell'])],
        [Paragraph("M60", styles['TableCellBold']),
         Paragraph("50K farmers, exit-ready", styles['TableCell']),
         Paragraph("INR 27 Cr revenue, 28% EBITDA margin", styles['TableCell']),
         Paragraph("Exit readiness for seed investors", styles['TableCell'])],
    ]
    story.append(make_table(gtm_data, col_widths=[0.7*inch, 2.0*inch, 2.0*inch, 1.9*inch]))
    story.append(PageBreak())


def build_competitive_landscape(story, styles):
    """Section 16: Competitive Landscape"""
    story.append(Paragraph("COMPETITIVE LANDSCAPE", styles['Heading1Green']))
    story.append(Paragraph(
        "Unique Positioning with Deep Structural Moats",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "The competitive landscape in Indian AgriTech is crowded, with 1,500+ startups and over USD 3 billion "
        "invested in the past 5 years. However, none have cracked the mountain agriculture segment due to "
        "fundamental model mismatches. PARVAT-SETU occupies a unique position at the intersection of "
        "cooperative ownership, AI/GIS technology, and mountain specialization.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Positioning Matrix", styles['Heading2Green']))
    comp_data = [
        [Paragraph("<b>Feature</b>", styles['TableHeader']),
         Paragraph("<b>PARVAT-SETU</b>", styles['TableHeader']),
         Paragraph("<b>DeHaat</b>", styles['TableHeader']),
         Paragraph("<b>Ninjacart</b>", styles['TableHeader']),
         Paragraph("<b>eNAM</b>", styles['TableHeader']),
         Paragraph("<b>Amul</b>", styles['TableHeader'])],
        [Paragraph("Ownership", styles['TableCellBold']),
         Paragraph("Producer-owned", styles['TableCellCenter']),
         Paragraph("VC-backed", styles['TableCellCenter']),
         Paragraph("VC-backed", styles['TableCellCenter']),
         Paragraph("Government", styles['TableCellCenter']),
         Paragraph("Producer-owned", styles['TableCellCenter'])],
        [Paragraph("Mountain Focus", styles['TableCellBold']),
         Paragraph("100%", styles['TableCellCenter']),
         Paragraph("0% (plains)", styles['TableCellCenter']),
         Paragraph("0% (urban)", styles['TableCellCenter']),
         Paragraph("20% (limited)", styles['TableCellCenter']),
         Paragraph("0% (dairy only)", styles['TableCellCenter'])],
        [Paragraph("AI/GIS Tech", styles['TableCellBold']),
         Paragraph("Deep (6 models)", styles['TableCellCenter']),
         Paragraph("Moderate", styles['TableCellCenter']),
         Paragraph("Logistics AI", styles['TableCellCenter']),
         Paragraph("Basic", styles['TableCellCenter']),
         Paragraph("Minimal", styles['TableCellCenter'])],
        [Paragraph("Value to Farmer", styles['TableCellBold']),
         Paragraph("80%+ of price", styles['TableCellCenter']),
         Paragraph("60-65%", styles['TableCellCenter']),
         Paragraph("55-60%", styles['TableCellCenter']),
         Paragraph("65-70%", styles['TableCellCenter']),
         Paragraph("80%+", styles['TableCellCenter'])],
        [Paragraph("Financial Services", styles['TableCellBold']),
         Paragraph("Full stack", styles['TableCellCenter']),
         Paragraph("Input credit", styles['TableCellCenter']),
         Paragraph("None", styles['TableCellCenter']),
         Paragraph("None", styles['TableCellCenter']),
         Paragraph("Limited", styles['TableCellCenter'])],
        [Paragraph("Gender Lens", styles['TableCellBold']),
         Paragraph("Core (60%)", styles['TableCellCenter']),
         Paragraph("Not explicit", styles['TableCellCenter']),
         Paragraph("Not explicit", styles['TableCellCenter']),
         Paragraph("Not explicit", styles['TableCellCenter']),
         Paragraph("Not explicit", styles['TableCellCenter'])],
        [Paragraph("Scalability", styles['TableCellBold']),
         Paragraph("IHR (12 states)", styles['TableCellCenter']),
         Paragraph("National", styles['TableCellCenter']),
         Paragraph("Urban India", styles['TableCellCenter']),
         Paragraph("National", styles['TableCellCenter']),
         Paragraph("National", styles['TableCellCenter'])],
    ]
    story.append(make_table(comp_data, col_widths=[1.2*inch, 1.1*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Competitive Moats", styles['Heading2Green']))
    moats = [
        "<b>Producer Ownership (Deepest Moat):</b> Once farmers own the enterprise, they will not switch to a platform that extracts value from them. This creates an unbreakable loyalty flywheel. No VC-backed competitor can replicate this without fundamentally changing their model.",
        "<b>AI+GIS Integration for Mountains:</b> Our 6 AI models are specifically trained on mountain agriculture data - terrain, microclimates, altitude-specific crops. This requires 3+ years of data collection that cannot be shortcut.",
        "<b>Mountain Specialization:</b> Plains-optimized platforms fail in mountains due to terrain, logistics, and social structure. Our team has deep domain expertise (PhD-level research) in Himalayan ecosystems.",
        "<b>Gender Lens Design:</b> Women-centric design (SHG-led, mobile-first, voice-enabled) creates stickiness in a segment where 60% of agricultural labor is female.",
        "<b>Research Foundation:</b> Academic validation through SCIE publications and institutional partnerships creates credibility that pure commercial startups cannot replicate.",
    ]
    for m in moats:
        story.append(Paragraph(m, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(8))
    
    story.append(Paragraph("Why This Won't Be Replicated Easily", styles['Heading2Green']))
    story.append(Paragraph(
        "A well-funded competitor would need: (1) 3+ years of mountain-specific AI training data, "
        "(2) deep trust relationships with 100+ SHGs and FPOs that take years to build, "
        "(3) understanding of cooperative governance that conflicts with VC-backed business models, "
        "(4) willingness to accept 3-5% margins versus the 15-25% that VCs demand. This combination "
        "of requirements creates a natural barrier that protects PARVAT-SETU's market position.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_team(story, styles):
    """Section 17: Team"""
    story.append(Paragraph("TEAM", styles['Heading1Green']))
    story.append(Paragraph(
        "Domain Expertise + Technical Capability + Field Experience",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Core Leadership", styles['Heading2Green']))
    story.append(spacer(6))
    
    story.append(Paragraph("Dr. Nidhi Rawat - Principal Investigator &amp; Chief Scientist", styles['Heading3Green']))
    story.append(Paragraph(
        "Assistant Professor, Department of Environmental Science, DBS Global University, Dehradun. "
        "Dr. Rawat brings deep domain expertise in Himalayan ecosystems, environmental science, and "
        "sustainable development. Her research focus on mountain agriculture systems, climate adaptation, "
        "and natural resource management provides the scientific foundation for PARVAT-SETU's "
        "environmental and agricultural models. She has published extensively in SCIE journals on "
        "topics directly relevant to the platform's core thesis - that technology-enabled sustainable "
        "agriculture can transform mountain livelihoods while preserving ecosystem services.",
        styles['BodyText']
    ))
    story.append(Paragraph(
        "<b>Role in PARVAT-SETU:</b> Research leadership, environmental science backbone, institutional "
        "partnerships, academic credibility, quality assurance for impact measurement methodology.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Raj Amritam - Co-Principal Investigator &amp; CTO", styles['Heading3Green']))
    story.append(Paragraph(
        "PhD Scholar, Department of Environmental Science, DBS Global University. Raj brings a unique "
        "combination of AI/ML expertise, GIS/remote sensing capability, and deep field experience in "
        "Himalayan communities. His doctoral research directly develops and validates the AI and GIS "
        "models that form PARVAT-SETU's technology core. With extensive fieldwork across 50+ mountain "
        "villages, he understands both the technical possibilities and ground-level constraints that "
        "determine whether technology solutions succeed or fail in mountain contexts.",
        styles['BodyText']
    ))
    story.append(Paragraph(
        "<b>Role in PARVAT-SETU:</b> Technology architecture, AI/GIS model development, field operations "
        "design, community engagement, product development, and execution leadership.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Advisory Board (To Be Constituted)", styles['Heading2Green']))
    advisory_data = [
        [Paragraph("<b>Domain</b>", styles['TableHeader']),
         Paragraph("<b>Required Expertise</b>", styles['TableHeader']),
         Paragraph("<b>Target Profile</b>", styles['TableHeader'])],
        [Paragraph("Technology", styles['TableCellBold']),
         Paragraph("AI/ML at scale, AgriTech platform architecture", styles['TableCell']),
         Paragraph("CTO/VP Eng from scaled AgriTech (DeHaat, Cropin, Stellapps)", styles['TableCell'])],
        [Paragraph("Finance &amp; Impact", styles['TableCellBold']),
         Paragraph("Blended finance, impact measurement, fund management", styles['TableCell']),
         Paragraph("Partner at impact fund (Aavishkaar, Omidyar, Acumen)", styles['TableCell'])],
        [Paragraph("Cooperative Governance", styles['TableCellBold']),
         Paragraph("Producer company law, FPO management, cooperative scaling", styles['TableCell']),
         Paragraph("Senior professional from NDDB/Amul/NABARD", styles['TableCell'])],
        [Paragraph("Market &amp; Distribution", styles['TableCellBold']),
         Paragraph("FMCG distribution, export markets, premium retail", styles['TableCell']),
         Paragraph("SVP from organic/premium food company", styles['TableCell'])],
        [Paragraph("Policy &amp; Institutions", styles['TableCellBold']),
         Paragraph("Agricultural policy, government schemes, bilateral agencies", styles['TableCell']),
         Paragraph("Retired IAS (Agriculture/Rural Dev) or World Bank specialist", styles['TableCell'])],
    ]
    story.append(make_table(advisory_data, col_widths=[1.3*inch, 2.2*inch, 3.1*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph("Planned Team Build (30 months)", styles['Heading2Green']))
    team_data = [
        [Paragraph("<b>Function</b>", styles['TableHeader']),
         Paragraph("<b>M1-6</b>", styles['TableHeader']),
         Paragraph("<b>M7-18</b>", styles['TableHeader']),
         Paragraph("<b>M19-30</b>", styles['TableHeader']),
         Paragraph("<b>Total</b>", styles['TableHeader'])],
        [Paragraph("Leadership", styles['TableCell']),
         Paragraph("2", styles['TableCellCenter']),
         Paragraph("3", styles['TableCellCenter']),
         Paragraph("4", styles['TableCellCenter']),
         Paragraph("4", styles['TableCellCenter'])],
        [Paragraph("Technology", styles['TableCell']),
         Paragraph("3", styles['TableCellCenter']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("8", styles['TableCellCenter']),
         Paragraph("8", styles['TableCellCenter'])],
        [Paragraph("Field Operations", styles['TableCell']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("12", styles['TableCellCenter']),
         Paragraph("25", styles['TableCellCenter']),
         Paragraph("25", styles['TableCellCenter'])],
        [Paragraph("Business Development", styles['TableCell']),
         Paragraph("1", styles['TableCellCenter']),
         Paragraph("3", styles['TableCellCenter']),
         Paragraph("5", styles['TableCellCenter']),
         Paragraph("5", styles['TableCellCenter'])],
        [Paragraph("<b>Total</b>", styles['TableCellBold']),
         Paragraph("<b>11</b>", styles['TableCellCenter']),
         Paragraph("<b>23</b>", styles['TableCellCenter']),
         Paragraph("<b>42</b>", styles['TableCellCenter']),
         Paragraph("<b>42</b>", styles['TableCellCenter'])],
    ]
    story.append(make_table(team_data, col_widths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]))
    story.append(PageBreak())


def build_governance(story, styles):
    """Section 18: Governance & Legal Structure"""
    story.append(Paragraph("GOVERNANCE &amp; LEGAL STRUCTURE", styles['Heading1Green']))
    story.append(Paragraph(
        "Producer-Owned, Professionally Managed, Investor-Protected",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Legal Entity: Producer Company", styles['Heading2Green']))
    story.append(Paragraph(
        "PARVAT-SETU will be incorporated as a Producer Company under the Companies Act 2013, Part IXA "
        "(formerly Section 581 of Companies Act 1956). This legal form is specifically designed for "
        "producer-owned enterprises and provides: (a) limited liability protection, (b) professional "
        "management, (c) equity investment capability, (d) democratic governance with 'one member one vote' "
        "principle, and (e) surplus distribution to producers. It combines the social mission alignment of "
        "cooperatives with the accountability and governance standards of companies.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Three-Tier Cooperative Structure", styles['Heading2Green']))
    story.append(Paragraph(
        "The governance architecture operates at three levels to balance local responsiveness with "
        "system-wide efficiency:",
        styles['BodyText']
    ))
    
    tier_bullets = [
        "<b>Tier 1 - Self-Help Groups (SHGs):</b> 10-15 women per SHG, federated at village level. Democratic selection of leaders. Manage local savings, micro-credit, and collective procurement. 500+ SHGs targeted by Year 5.",
        "<b>Tier 2 - Farmer Producer Organizations (FPOs):</b> Federation of 20-50 SHGs per FPO (500-2,000 farmers each). Manage aggregation, quality control, local processing, and buyer relationships. 25+ FPOs by Year 5.",
        "<b>Tier 3 - Apex Producer Company:</b> PARVAT-SETU Producer Company Limited. Owned by FPOs and individual producer-shareholders. Manages technology platform, institutional buyer relationships, financial services, and brand. Professional management team with board oversight.",
    ]
    for t in tier_bullets:
        story.append(Paragraph(t, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))
    
    story.append(Paragraph("Board Composition", styles['Heading2Green']))
    board_data = [
        [Paragraph("<b>Category</b>", styles['TableHeader']),
         Paragraph("<b>Share</b>", styles['TableHeader']),
         Paragraph("<b>Selection Method</b>", styles['TableHeader']),
         Paragraph("<b>Role</b>", styles['TableHeader'])],
        [Paragraph("Elected Producers", styles['TableCellBold']),
         Paragraph("60%", styles['TableCellCenter']),
         Paragraph("Elected by FPO general body; minimum 40% women", styles['TableCell']),
         Paragraph("Community voice, strategic direction, social mission", styles['TableCell'])],
        [Paragraph("Independent Directors", styles['TableCellBold']),
         Paragraph("25%", styles['TableCellCenter']),
         Paragraph("Nominated by governance committee; domain experts", styles['TableCell']),
         Paragraph("Professional oversight, technical guidance, audit", styles['TableCell'])],
        [Paragraph("Investor Nominees", styles['TableCellBold']),
         Paragraph("15%", styles['TableCellCenter']),
         Paragraph("Nominated by equity investors per SHA terms", styles['TableCell']),
         Paragraph("Financial oversight, strategic growth, exit planning", styles['TableCell'])],
    ]
    story.append(make_table(board_data, col_widths=[1.4*inch, 0.8*inch, 2.2*inch, 2.2*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph("Investor Rights &amp; Protections", styles['Heading2Green']))
    investor_rights = [
        "<b>Board Representation:</b> 1 board seat for equity investment of INR 1 Crore+. Observer rights below threshold.",
        "<b>Information Rights:</b> Monthly MIS, quarterly board reports, annual audit, real-time dashboard access.",
        "<b>Anti-Dilution:</b> Weighted average anti-dilution protection for equity investors in subsequent rounds.",
        "<b>Tag-Along Rights:</b> Right to participate in any sale by promoters/majority shareholders.",
        "<b>Liquidation Preference:</b> 1x non-participating preference. Equity investors recover investment before producer distribution.",
        "<b>Protective Provisions:</b> Investor consent required for: changes to articles, new share issuance, debt above threshold, M&amp;A, related party transactions above INR 10 Lakh.",
    ]
    for r in investor_rights:
        story.append(Paragraph(r, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))
    
    story.append(Paragraph("Anti-Dilution Protection for Producer Members", styles['Heading2Green']))
    story.append(Paragraph(
        "To ensure the social mission is preserved, the governance structure includes safeguards against "
        "mission drift: (a) Producer voting rights cannot fall below 51% regardless of equity rounds, "
        "(b) Any change to commission structure requires 75% producer vote, (c) Surplus distribution "
        "policy locked at minimum 60% to producers, (d) Social impact KPIs tied to management compensation.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Governance Structure Comparison", styles['Heading2Green']))
    gov_comp = [
        [Paragraph("<b>Feature</b>", styles['TableHeader']),
         Paragraph("<b>Pure Cooperative</b>", styles['TableHeader']),
         Paragraph("<b>For-Profit Company</b>", styles['TableHeader']),
         Paragraph("<b>PARVAT-SETU (Hybrid)</b>", styles['TableHeader'])],
        [Paragraph("Ownership", styles['TableCell']),
         Paragraph("Members only", styles['TableCellCenter']),
         Paragraph("Shareholders", styles['TableCellCenter']),
         Paragraph("Producers + Investors", styles['TableCellCenter'])],
        [Paragraph("Equity Investment", styles['TableCell']),
         Paragraph("Not possible", styles['TableCellCenter']),
         Paragraph("Unlimited", styles['TableCellCenter']),
         Paragraph("Capped at 49%", styles['TableCellCenter'])],
        [Paragraph("Surplus Distribution", styles['TableCell']),
         Paragraph("To members", styles['TableCellCenter']),
         Paragraph("To shareholders", styles['TableCellCenter']),
         Paragraph("60% to producers, 40% reinvest/investors", styles['TableCellCenter'])],
        [Paragraph("Governance", styles['TableCell']),
         Paragraph("Democratic (1P1V)", styles['TableCellCenter']),
         Paragraph("Capital-weighted", styles['TableCellCenter']),
         Paragraph("Blended (producer majority + investor rights)", styles['TableCellCenter'])],
        [Paragraph("Professional Mgmt", styles['TableCell']),
         Paragraph("Weak", styles['TableCellCenter']),
         Paragraph("Strong", styles['TableCellCenter']),
         Paragraph("Strong (CEO appointed by board)", styles['TableCellCenter'])],
        [Paragraph("Exit for Investors", styles['TableCell']),
         Paragraph("Not possible", styles['TableCellCenter']),
         Paragraph("IPO/Trade sale", styles['TableCellCenter']),
         Paragraph("Trade sale/Secondary/Revenue buyback", styles['TableCellCenter'])],
    ]
    story.append(make_table(gov_comp, col_widths=[1.3*inch, 1.5*inch, 1.5*inch, 2.3*inch]))
    story.append(PageBreak())


def build_risk_factors(story, styles):
    """Section 19: Risk Factors & Mitigation"""
    story.append(Paragraph("RISK FACTORS &amp; MITIGATION", styles['Heading1Green']))
    story.append(Paragraph(
        "Transparent Risk Assessment with Proactive Mitigation Strategies",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "We present a transparent assessment of risks facing PARVAT-SETU, categorized by type with "
        "probability, impact assessment, and specific mitigation strategies. This reflects our "
        "belief that informed investors make better partners.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    risk_data = [
        [Paragraph("<b>Risk</b>", styles['TableHeader']),
         Paragraph("<b>Category</b>", styles['TableHeader']),
         Paragraph("<b>Prob.</b>", styles['TableHeader']),
         Paragraph("<b>Impact</b>", styles['TableHeader']),
         Paragraph("<b>Mitigation</b>", styles['TableHeader'])],
        [Paragraph("Farmer adoption slower than projected", styles['TableCell']),
         Paragraph("Market", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("SHG-led approach reduces risk; demo effect; patient capital timeline", styles['TableCell'])],
        [Paragraph("Buyer demand insufficient for premium", styles['TableCell']),
         Paragraph("Market", styles['TableCellCenter']),
         Paragraph("Low", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Pre-signed MOUs; multiple buyer segments; export option", styles['TableCell'])],
        [Paragraph("AI models underperform in field", styles['TableCell']),
         Paragraph("Technology", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Continuous retraining; human-in-loop; manual fallback processes", styles['TableCell'])],
        [Paragraph("Connectivity/infrastructure gaps", styles['TableCell']),
         Paragraph("Technology", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Offline-first design; USSD backup; edge computing; progressive sync", styles['TableCell'])],
        [Paragraph("Regulatory changes (FPO/cooperative law)", styles['TableCell']),
         Paragraph("Regulatory", styles['TableCellCenter']),
         Paragraph("Low", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("Legal advisory retained; policy engagement; flexible structure", styles['TableCell'])],
        [Paragraph("APMC reform reversal", styles['TableCell']),
         Paragraph("Regulatory", styles['TableCellCenter']),
         Paragraph("Low", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("B2B model works within APMC framework; multi-channel approach", styles['TableCell'])],
        [Paragraph("Climate event disruption (flood/landslide)", styles['TableCell']),
         Paragraph("Climate", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("Geographic diversification; insurance products; early warning systems; disaster planning", styles['TableCell'])],
        [Paragraph("Crop failure/disease outbreak", styles['TableCell']),
         Paragraph("Climate", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("Crop diversity (25+ crops); parametric insurance; climate advisory", styles['TableCell'])],
        [Paragraph("Key person dependency", styles['TableCell']),
         Paragraph("Execution", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("High", styles['TableCellCenter']),
         Paragraph("Advisory board; documentation; team building; equity incentives", styles['TableCell'])],
        [Paragraph("Team recruitment in remote areas", styles['TableCell']),
         Paragraph("Execution", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Local hiring priority; remote work options; competitive comp; purpose-driven culture", styles['TableCell'])],
        [Paragraph("Grant funding delays", styles['TableCell']),
         Paragraph("Financial", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Multiple grant pipelines; phased spending; earned revenue acceleration", styles['TableCell'])],
        [Paragraph("Working capital constraints at scale", styles['TableCell']),
         Paragraph("Financial", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Medium", styles['TableCellCenter']),
         Paragraph("Multiple debt facilities; invoice discounting; buyer advance payments", styles['TableCell'])],
    ]
    story.append(make_table(risk_data, col_widths=[1.5*inch, 0.8*inch, 0.6*inch, 0.6*inch, 3.1*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph("Risk Mitigation Philosophy", styles['Heading2Green']))
    story.append(Paragraph(
        "Our approach to risk management is rooted in three principles: (1) <b>Diversification</b> - across "
        "crops, geographies, buyers, and revenue streams to avoid concentration; (2) <b>Patience</b> - "
        "the blended finance structure provides a 30-month runway with milestone-based deployment rather "
        "than aggressive burn; (3) <b>Adaptability</b> - go/no-go gates at every phase allow pivot or "
        "wind-down decisions before capital is fully deployed. The biggest risk mitigant is the cooperative "
        "structure itself - producer ownership means the community has skin in the game and will work to "
        "ensure success.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_exit_strategy(story, styles):
    """Section 20: Exit Strategy for Investors"""
    story.append(Paragraph("EXIT STRATEGY FOR INVESTORS", styles['Heading1Green']))
    story.append(Paragraph(
        "Multiple Pathways to Liquidity within 5-8 Year Horizon",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "While PARVAT-SETU is designed as a perpetual producer-owned enterprise, we recognize that "
        "investor capital requires clear exit pathways. Our structure accommodates multiple exit "
        "mechanisms without disrupting the social mission or producer ownership.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Primary Exit: Trade Sale (Year 7-8)", styles['Heading2Green']))
    story.append(Paragraph(
        "Sale of investor equity stake to a larger cooperative federation or institutional buyer. "
        "Most likely acquirers: NABARD (for its cooperative portfolio), NDDB (for its producer "
        "company ecosystem), state cooperative federations, or large impact investors seeking "
        "to build mountain agriculture portfolios. At Year 7-8, the enterprise will have 75,000+ "
        "farmers and INR 50+ Crore revenue, making it an attractive bolt-on for larger entities "
        "seeking mountain agriculture exposure. Expected valuation: 8-12x revenue = INR 400-600 Crore. "
        "Investor equity stake (15-20%) = INR 60-120 Crore on INR 1.25 Crore investment = 48-96x return.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Secondary Exit: Fund-to-Fund Transfer (Year 5-7)", styles['Heading2Green']))
    story.append(Paragraph(
        "Sale of investor stake to another impact fund or DFI seeking exposure to proven impact enterprises. "
        "The growing impact investing secondary market (estimated USD 5 billion globally) provides liquidity "
        "for early-stage impact investors. At Year 5, the enterprise will have demonstrated traction and "
        "impact, making it attractive for later-stage impact capital. Expected valuation at secondary: "
        "5-8x revenue multiple.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph("Tertiary Exit: Revenue-Based Repayment (Year 5+)", styles['Heading2Green']))
    story.append(Paragraph(
        "From Year 5, when the enterprise generates significant surplus (projected INR 7+ Crore net profit), "
        "a portion of surplus can be used to buy back investor equity at pre-agreed multiples. This "
        "mechanism allows exit without requiring external buyer, making it the most certain (if least "
        "lucrative) exit pathway. Structure: 15-20% of annual surplus allocated to investor buyback "
        "until full exit achieved.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    exit_summary = [
        [Paragraph("<b>Exit Pathway</b>", styles['TableHeader']),
         Paragraph("<b>Timeline</b>", styles['TableHeader']),
         Paragraph("<b>Expected Return</b>", styles['TableHeader']),
         Paragraph("<b>Probability</b>", styles['TableHeader']),
         Paragraph("<b>Dependency</b>", styles['TableHeader'])],
        [Paragraph("Trade Sale", styles['TableCellBold']),
         Paragraph("Year 7-8", styles['TableCellCenter']),
         Paragraph("48-96x (45%+ IRR)", styles['TableCellCenter']),
         Paragraph("40%", styles['TableCellCenter']),
         Paragraph("Scale achievement + willing buyer", styles['TableCell'])],
        [Paragraph("Secondary Sale", styles['TableCellBold']),
         Paragraph("Year 5-7", styles['TableCellCenter']),
         Paragraph("15-30x (35%+ IRR)", styles['TableCellCenter']),
         Paragraph("35%", styles['TableCellCenter']),
         Paragraph("Impact metrics + revenue traction", styles['TableCell'])],
        [Paragraph("Revenue Buyback", styles['TableCellBold']),
         Paragraph("Year 5-10", styles['TableCellCenter']),
         Paragraph("4-6x (25% IRR)", styles['TableCellCenter']),
         Paragraph("90%", styles['TableCellCenter']),
         Paragraph("Enterprise profitability only", styles['TableCell'])],
    ]
    story.append(make_table(exit_summary, col_widths=[1.2*inch, 1.0*inch, 1.5*inch, 0.9*inch, 2.0*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph(
        "The expected blended return across scenarios (probability-weighted) is <b>25-35% IRR</b> for "
        "equity investors, with near-certainty of at least 4-6x return through the revenue buyback "
        "mechanism. This risk-return profile is attractive for impact investors who also receive "
        "world-class social impact metrics alongside financial returns.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_sustainability_esg(story, styles):
    """Section 21: Sustainability & ESG Compliance"""
    story.append(Paragraph("SUSTAINABILITY &amp; ESG COMPLIANCE", styles['Heading1Green']))
    story.append(Paragraph(
        "Environmental, Social, and Governance Excellence by Design",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "PARVAT-SETU is not merely ESG-compliant; it is ESG-native. The enterprise exists to generate "
        "positive environmental and social outcomes through excellent governance. ESG is not a reporting "
        "obligation but the core business model.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Environmental", styles['Heading2Green']))
    env_bullets = [
        "<b>Organic Farming Promotion:</b> 80% of enrolled farmers to transition to organic/natural farming within 3 years, reducing chemical input use by 70%+ and protecting mountain water sources.",
        "<b>Agroforestry Integration:</b> Promotion of multi-tier farming systems (fruit trees + crops + fodder) that sequester 5-10 tCO2e per hectare annually while generating diversified income.",
        "<b>Reduced Food Waste:</b> Platform-enabled demand matching and cold chain reduces post-harvest loss from 30% to 10%, preventing 50,000+ tons of food waste over 5 years.",
        "<b>Biodiversity Conservation:</b> Incentivizing cultivation of indigenous crop varieties (50+ mountain-specific cultivars) that are disappearing due to monoculture pressure.",
        "<b>Water Conservation:</b> GIS-optimized irrigation advisory reducing water use by 25-35% through precision application based on soil moisture and weather data.",
    ]
    for e in env_bullets:
        story.append(Paragraph(e, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(8))
    
    story.append(Paragraph("Social", styles['Heading2Green']))
    social_bullets = [
        "<b>Gender Equity:</b> 60% women participation target, women-led governance (40% board representation), financial products designed for women's needs, reduction of unpaid labor burden.",
        "<b>SC/ST Inclusion:</b> Mountain communities include significant Scheduled Tribe populations. Platform ensures equitable access regardless of caste or tribe, with specific outreach to marginalized communities.",
        "<b>Poverty Reduction:</b> 200% income uplift target directly addresses extreme poverty, with 50,000 families (250,000 people) impacted.",
        "<b>Dignified Livelihoods:</b> Transforming agriculture from survival activity to dignified, technology-enabled profession that retains youth in mountain regions.",
        "<b>Health &amp; Nutrition:</b> Reduced chemical exposure through organic transition; improved nutrition through crop diversification and reduced food waste.",
    ]
    for s in social_bullets:
        story.append(Paragraph(s, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(8))
    
    story.append(Paragraph("Governance", styles['Heading2Green']))
    gov_bullets = [
        "<b>Producer Ownership:</b> 51%+ voting rights always with producers, ensuring mission alignment.",
        "<b>Transparency:</b> Real-time transaction data visible to all stakeholders; annual social audit by independent agency.",
        "<b>Professional Management:</b> Qualified CEO and management team with performance linked to both financial and impact KPIs.",
        "<b>Regular Audit:</b> Statutory audit + social audit + impact audit annually; published results.",
        "<b>Anti-Corruption:</b> Digital-first transactions eliminate cash handling corruption; blockchain-verified pricing.",
    ]
    for g in gov_bullets:
        story.append(Paragraph(g, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(10))
    
    story.append(Paragraph("Carbon Credit Potential", styles['Heading2Green']))
    story.append(Paragraph(
        "PARVAT-SETU's promotion of organic farming, agroforestry, and reduced food waste generates "
        "quantifiable carbon sequestration and emission reduction. Conservative estimate: 50,000+ tCO2e "
        "over 10 years. At current voluntary carbon market prices (USD 15-50/tCO2e), this represents "
        "INR 6-20 Crore in potential carbon credit revenue - a significant additional revenue stream "
        "that also reinforces the environmental impact thesis.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("ESG Scorecard", styles['Heading2Green']))
    esg_data = [
        [Paragraph("<b>Dimension</b>", styles['TableHeader']),
         Paragraph("<b>Metric</b>", styles['TableHeader']),
         Paragraph("<b>Target (Y5)</b>", styles['TableHeader']),
         Paragraph("<b>Measurement</b>", styles['TableHeader'])],
        [Paragraph("Environment", styles['TableCellBold']),
         Paragraph("Carbon Sequestered", styles['TableCellCenter']),
         Paragraph("50,000 tCO2e", styles['TableCellCenter']),
         Paragraph("Third-party verified carbon audit", styles['TableCell'])],
        [Paragraph("Environment", styles['TableCell']),
         Paragraph("Chemical Reduction", styles['TableCellCenter']),
         Paragraph("70% reduction", styles['TableCellCenter']),
         Paragraph("Input purchase data + soil testing", styles['TableCell'])],
        [Paragraph("Environment", styles['TableCell']),
         Paragraph("Food Waste Reduction", styles['TableCellCenter']),
         Paragraph("50,000 tons saved", styles['TableCellCenter']),
         Paragraph("Platform transaction vs baseline data", styles['TableCell'])],
        [Paragraph("Social", styles['TableCellBold']),
         Paragraph("Income Uplift", styles['TableCellCenter']),
         Paragraph("200% average", styles['TableCellCenter']),
         Paragraph("Household income survey (annual)", styles['TableCell'])],
        [Paragraph("Social", styles['TableCell']),
         Paragraph("Women Empowerment", styles['TableCellCenter']),
         Paragraph("60% participation", styles['TableCellCenter']),
         Paragraph("Enrollment + leadership data", styles['TableCell'])],
        [Paragraph("Social", styles['TableCell']),
         Paragraph("Financial Inclusion", styles['TableCellCenter']),
         Paragraph("70% formal access", styles['TableCellCenter']),
         Paragraph("Credit + insurance penetration", styles['TableCell'])],
        [Paragraph("Governance", styles['TableCellBold']),
         Paragraph("Producer Board Share", styles['TableCellCenter']),
         Paragraph("60%+", styles['TableCellCenter']),
         Paragraph("Board composition records", styles['TableCell'])],
        [Paragraph("Governance", styles['TableCell']),
         Paragraph("Transparency Score", styles['TableCellCenter']),
         Paragraph("95%+ digital", styles['TableCellCenter']),
         Paragraph("Digital vs cash transaction ratio", styles['TableCell'])],
    ]
    story.append(make_table(esg_data, col_widths=[1.1*inch, 1.4*inch, 1.3*inch, 2.8*inch]))
    story.append(PageBreak())


def build_implementation_roadmap(story, styles):
    """Section 22: Implementation Roadmap"""
    story.append(Paragraph("IMPLEMENTATION ROADMAP", styles['Heading1Green']))
    story.append(Paragraph(
        "30-Month Pilot Roadmap with Clear Milestones and Go/No-Go Gates",
        styles['SectionIntro']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph(
        "The implementation is structured in three phases with clear deliverables, "
        "resource requirements, and decision gates at each transition point. Each phase builds "
        "on the previous phase's learnings and validated assumptions, allowing progressive de-risking "
        "of both execution and financial commitments.",
        styles['BodyText']
    ))
    story.append(spacer(6))
    
    story.append(Paragraph(
        "The roadmap is designed with the principle of 'fail fast, fail cheap' - critical assumptions "
        "are tested early with minimal capital deployment, and go/no-go decisions are made before "
        "committing to scale. This disciplined approach protects investor capital while maximizing "
        "learning velocity.",
        styles['BodyText']
    ))
    story.append(spacer(8))
    
    story.append(Paragraph("Phase 1: Foundation (Months 1-10)", styles['Heading2Green']))
    phase1_data = [
        [Paragraph("<b>Quarter</b>", styles['TableHeader']),
         Paragraph("<b>Activities</b>", styles['TableHeader']),
         Paragraph("<b>Deliverables</b>", styles['TableHeader']),
         Paragraph("<b>Budget (INR L)</b>", styles['TableHeader'])],
        [Paragraph("M1-3", styles['TableCellBold']),
         Paragraph("Company incorporation, team recruitment (core 11), technology architecture design, community engagement initiation, baseline surveys", styles['TableCell']),
         Paragraph("Legal entity registered, team hired, tech spec complete, 50 SHGs engaged, baseline data collected", styles['TableCell']),
         Paragraph("45", styles['TableCellCenter'])],
        [Paragraph("M4-6", styles['TableCellBold']),
         Paragraph("Platform MVP development, AI model v1 training, GIS mapping of pilot area, first 500 farmers onboarded, initial buyer outreach", styles['TableCell']),
         Paragraph("MVP live, 2 AI models deployed, GIS maps for 3 blocks, 500 farmers active, 5 buyer MOUs", styles['TableCell']),
         Paragraph("55", styles['TableCellCenter'])],
        [Paragraph("M7-10", styles['TableCellBold']),
         Paragraph("Platform iteration based on user feedback, first transactions, processing unit setup, credit pilot, expanded enrollment", styles['TableCell']),
         Paragraph("Platform v2.0, 1,500 farmers, first INR 15L GMV, 1 processing unit operational, 100 loans disbursed", styles['TableCell']),
         Paragraph("65", styles['TableCellCenter'])],
    ]
    story.append(make_table(phase1_data, col_widths=[0.7*inch, 2.5*inch, 2.5*inch, 0.9*inch]))
    story.append(spacer(6))
    story.append(Paragraph(
        "<b>Go/No-Go Gate 1 (Month 10):</b> Proceed to Phase 2 if: (a) 1,000+ active farmers, "
        "(b) Platform functional with positive user feedback, (c) At least 3 completed buyer transactions, "
        "(d) Unit economics data shows path to positive contribution margin.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Phase 2: Validation (Months 11-20)", styles['Heading2Green']))
    phase2_data = [
        [Paragraph("<b>Quarter</b>", styles['TableHeader']),
         Paragraph("<b>Activities</b>", styles['TableHeader']),
         Paragraph("<b>Deliverables</b>", styles['TableHeader']),
         Paragraph("<b>Budget (INR L)</b>", styles['TableHeader'])],
        [Paragraph("M11-14", styles['TableCellBold']),
         Paragraph("Scale to 3 districts, all 6 AI models deployed, financial services launch, 5 processing units, team expansion to 23", styles['TableCell']),
         Paragraph("3,500 farmers, INR 1.5 Cr cumulative GMV, 500 loans, 5 buyer relationships active", styles['TableCell']),
         Paragraph("80", styles['TableCellCenter'])],
        [Paragraph("M15-18", styles['TableCellBold']),
         Paragraph("Revenue ramp, organic certification, GI tag applications, carbon credit registration, investor reporting", styles['TableCell']),
         Paragraph("5,000 farmers, positive contribution margin, organic certification for 1000 farmers, first carbon credits", styles['TableCell']),
         Paragraph("90", styles['TableCellCenter'])],
        [Paragraph("M19-20", styles['TableCellBold']),
         Paragraph("Impact measurement (endline vs baseline), unit economics validation, Series A preparation, multi-district playbook", styles['TableCell']),
         Paragraph("Impact report published, unit economics proven, Series A deck ready, expansion playbook documented", styles['TableCell']),
         Paragraph("40", styles['TableCellCenter'])],
    ]
    story.append(make_table(phase2_data, col_widths=[0.7*inch, 2.5*inch, 2.5*inch, 0.9*inch]))
    story.append(spacer(6))
    story.append(Paragraph(
        "<b>Go/No-Go Gate 2 (Month 20):</b> Proceed to Phase 3 if: (a) Positive contribution margin per farmer, "
        "(b) 85%+ farmer retention, (c) Measurable income uplift (>50%), (d) Series A investor interest confirmed.",
        styles['BodyText']
    ))
    story.append(spacer(10))
    
    story.append(Paragraph("Phase 3: Scale Preparation (Months 21-30)", styles['Heading2Green']))
    phase3_data = [
        [Paragraph("<b>Quarter</b>", styles['TableHeader']),
         Paragraph("<b>Activities</b>", styles['TableHeader']),
         Paragraph("<b>Deliverables</b>", styles['TableHeader']),
         Paragraph("<b>Budget (INR L)</b>", styles['TableHeader'])],
        [Paragraph("M21-25", styles['TableCellBold']),
         Paragraph("Expand to 5+ districts, team to 35, 10 processing units, advanced AI models, export market entry", styles['TableCell']),
         Paragraph("8,000 farmers, INR 6 Cr cumulative GMV, first export shipment, Series A close", styles['TableCell']),
         Paragraph("95", styles['TableCellCenter'])],
        [Paragraph("M26-30", styles['TableCellBold']),
         Paragraph("Multi-state readiness, technology platform scaling, brand building, strategic partnerships, governance maturation", styles['TableCell']),
         Paragraph("12,000 farmers, operating break-even approaching, multi-state expansion plan ready, Series A deployed", styles['TableCell']),
         Paragraph("80", styles['TableCellCenter'])],
    ]
    story.append(make_table(phase3_data, col_widths=[0.7*inch, 2.5*inch, 2.5*inch, 0.9*inch]))
    story.append(spacer(10))
    
    story.append(Paragraph("Quarterly Reporting Framework", styles['Heading2Green']))
    story.append(Paragraph(
        "Investors receive quarterly reports including: (a) Financial statements (P&amp;L, cash flow, balance sheet), "
        "(b) Operating metrics (farmers enrolled, GMV, transactions, retention), (c) Impact metrics (income change, "
        "women participation, financial inclusion), (d) Technology metrics (AI model performance, platform uptime, "
        "user engagement), (e) Risk register update, (f) Upcoming quarter plan and budget.",
        styles['BodyText']
    ))
    story.append(PageBreak())


def build_appendices(story, styles):
    """Section 23: Appendices"""
    story.append(Paragraph("APPENDICES", styles['Heading1Green']))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix A: Key Assumptions for Financial Model", styles['Heading2Green']))
    assumptions = [
        "Average farmer enrollment cost: INR 3,700 (declining to INR 2,800 by Year 5 through SHG leverage)",
        "Average GMV per farmer: INR 3,200 (Year 1) growing to INR 24,000 (Year 5) through product diversification",
        "Platform commission: 3-5% weighted average across product categories",
        "Farmer retention: 85% Year 1, improving to 95% Year 5 (based on Amul/One Acre Fund benchmarks)",
        "Processing margin: 15-25% on value-added products (validated by Araku Coffee, Lijjat Papad models)",
        "Revenue growth: 168% CAGR driven by both farmer enrollment and revenue per farmer growth",
        "Team cost: Average INR 6 Lakh/year per team member (blended across field and HQ roles)",
        "Technology cost: INR 15-20 Lakh/year for cloud + platform maintenance at scale",
        "Working capital cycle: 45-60 days for procurement to payment",
        "Grant disbursement: 60% in Year 1, 30% in Year 2, 10% in Year 3 (milestone-based)",
        "Inflation: 5% annual increase in costs; revenue growth exceeds inflation",
        "Exchange rate (for export): INR 83/USD, stable assumption",
    ]
    for a in assumptions:
        story.append(Paragraph(a, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix B: Comparable Transactions in Impact Investing", styles['Heading2Green']))
    comp_trans = [
        [Paragraph("<b>Transaction</b>", styles['TableHeader']),
         Paragraph("<b>Year</b>", styles['TableHeader']),
         Paragraph("<b>Amount</b>", styles['TableHeader']),
         Paragraph("<b>Investor</b>", styles['TableHeader']),
         Paragraph("<b>Outcome</b>", styles['TableHeader'])],
        [Paragraph("Araku Coffee Series B", styles['TableCell']),
         Paragraph("2022", styles['TableCellCenter']),
         Paragraph("USD 7M", styles['TableCellCenter']),
         Paragraph("Danone Manifesto, LGT Impact", styles['TableCell']),
         Paragraph("Tribal cooperative; 200K families; exports to EU", styles['TableCell'])],
        [Paragraph("Sahyadri FPO equity", styles['TableCell']),
         Paragraph("2021", styles['TableCellCenter']),
         Paragraph("INR 25 Cr", styles['TableCellCenter']),
         Paragraph("Nuveen, responsAbility", styles['TableCell']),
         Paragraph("Largest FPO in India; 18K farmers; profitable", styles['TableCell'])],
        [Paragraph("DeHaat Series D", styles['TableCell']),
         Paragraph("2022", styles['TableCellCenter']),
         Paragraph("USD 60M", styles['TableCellCenter']),
         Paragraph("Sofina, Lightrock", styles['TableCell']),
         Paragraph("Full-stack AgriTech; 1.5M farmers; pan-India", styles['TableCell'])],
        [Paragraph("One Acre Fund expansion", styles['TableCell']),
         Paragraph("2023", styles['TableCellCenter']),
         Paragraph("USD 100M", styles['TableCellCenter']),
         Paragraph("USAID, BMGF, Skoll", styles['TableCell']),
         Paragraph("Blended finance for East Africa expansion", styles['TableCell'])],
        [Paragraph("Stellapps Series B", styles['TableCell']),
         Paragraph("2021", styles['TableCellCenter']),
         Paragraph("USD 18M", styles['TableCellCenter']),
         Paragraph("Blume, ABC Impact", styles['TableCell']),
         Paragraph("Dairy IoT platform; 4M farmers connected", styles['TableCell'])],
    ]
    story.append(make_table(comp_trans, col_widths=[1.5*inch, 0.6*inch, 0.8*inch, 1.6*inch, 2.1*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix C: Market Data Sources", styles['Heading2Green']))
    sources = [
        "Agricultural Census of India 2015-16 (Ministry of Agriculture)",
        "Situation Assessment Survey of Agricultural Households, NSSO 77th Round (2019)",
        "NABARD All India Rural Financial Inclusion Survey (NAFIS) 2021-22",
        "Indian Himalayan Region Status Report, NITI Aayog (2022)",
        "Agriculture in India: Information about Indian Agriculture & Its Importance, IBEF (2024)",
        "India AgriTech Landscape Report, Omnivore-BCG (2023)",
        "Impact Investing in India, Brookings-ANDE (2023)",
        "FPO Performance Study, ACCESS Development Services (2022)",
        "Mountain Agriculture Report, ICIMOD (2023)",
        "Organic Farming Statistics, APEDA/NPC (2023-24)",
    ]
    for s in sources:
        story.append(Paragraph(s, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix D: Letters of Support Reference", styles['Heading2Green']))
    letters = [
        "DBS Global University, Dehradun - Institutional support letter and research infrastructure commitment",
        "NABARD Regional Office, Uttarakhand - Expression of interest for FPO development partnership",
        "District Horticulture Officer, Chamoli - Support for pilot geography selection",
        "3 Farmer Producer Organizations in Uttarakhand - Partnership agreements for pilot",
        "Uttarakhand Organic Certification Agency - Certification pathway commitment",
        "State Disaster Management Authority - GIS data sharing agreement",
    ]
    for l in letters:
        story.append(Paragraph(l, styles['BulletText'], bulletText='\u2022'))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix E: Technology Development Plan", styles['Heading2Green']))
    story.append(Paragraph(
        "The technology platform will be developed in three releases aligned with the business phases. "
        "Each release adds capabilities based on validated farmer needs and buyer requirements:",
        styles['BodyText']
    ))
    tech_plan = [
        [Paragraph("<b>Release</b>", styles['TableHeader']),
         Paragraph("<b>Timeline</b>", styles['TableHeader']),
         Paragraph("<b>Features</b>", styles['TableHeader']),
         Paragraph("<b>Technical Stack</b>", styles['TableHeader'])],
        [Paragraph("MVP (v1.0)", styles['TableCellBold']),
         Paragraph("M1-6", styles['TableCellCenter']),
         Paragraph("Farmer registration, basic marketplace, price display, SMS advisory, manual quality grading", styles['TableCell']),
         Paragraph("React Native + Firebase + Python backend + USSD gateway", styles['TableCell'])],
        [Paragraph("Growth (v2.0)", styles['TableCellBold']),
         Paragraph("M7-18", styles['TableCellCenter']),
         Paragraph("AI price prediction, GIS maps, credit scoring, buyer portal, traceability, IoT integration", styles['TableCell']),
         Paragraph("Kubernetes + AWS SageMaker + PostGIS + Hyperledger + React dashboard", styles['TableCell'])],
        [Paragraph("Scale (v3.0)", styles['TableCellBold']),
         Paragraph("M19-30", styles['TableCellCenter']),
         Paragraph("Full AI suite, carbon tracking, export compliance, multi-language, advanced analytics, partner APIs", styles['TableCell']),
         Paragraph("Multi-region deployment + advanced ML pipeline + data warehouse + real-time streaming", styles['TableCell'])],
    ]
    story.append(make_table(tech_plan, col_widths=[1.0*inch, 0.8*inch, 2.5*inch, 2.3*inch]))
    story.append(spacer(12))
    
    story.append(Paragraph("Appendix F: Detailed Impact Measurement Methodology", styles['Heading2Green']))
    story.append(Paragraph(
        "Impact will be measured using a rigorous quasi-experimental design with baseline-endline surveys, "
        "control groups, and third-party verification. Key methodological choices:",
        styles['BodyText']
    ))
    impact_method = [
        "<b>Baseline Survey:</b> Comprehensive household survey covering income, assets, food security, financial access, gender empowerment indices for all enrolled and control households (n=500 treatment, n=200 control).",
        "<b>Continuous Monitoring:</b> Platform-generated data provides real-time metrics on transactions, prices, volumes, credit access, and participation patterns - no separate data collection cost.",
        "<b>Annual Endline:</b> Repeat household survey to measure change in income, food security, financial inclusion, and wellbeing indicators. Propensity score matching for attribution.",
        "<b>Third-Party Verification:</b> Annual impact audit by independent agency (J-PAL affiliated researcher or GIIN-accredited assessor) to validate self-reported metrics.",
        "<b>IRIS+ Alignment:</b> All metrics mapped to IRIS+ catalog for comparability with global impact investing benchmarks. Quarterly IRIS+ reports to investors.",
        "<b>Gender Disaggregation:</b> All metrics reported separately for women and men, with women-specific empowerment indices (decision-making authority, asset ownership, mobility).",
    ]
    for im in impact_method:
        story.append(Paragraph(im, styles['BulletText'], bulletText='\u2022'))
    story.append(PageBreak())


def build_declaration(story, styles):
    """Section 24: Declaration & Contact"""
    story.append(Paragraph("DECLARATION &amp; CONTACT", styles['Heading1Green']))
    story.append(spacer(16))
    
    story.append(Paragraph(
        "We, the undersigned, declare that the information presented in this Impact Investor Proposal "
        "is true to the best of our knowledge and based on rigorous academic research, field data, "
        "and conservative financial modeling. We commit to transparent governance, measurable impact, "
        "and accountable use of investor capital.",
        styles['BodyText']
    ))
    story.append(spacer(20))
    
    story.append(Paragraph(
        "This document is intended for qualified impact investors and contains forward-looking statements "
        "based on assumptions that may not materialize. Actual results may differ from projections. "
        "Investors are advised to conduct independent due diligence.",
        styles['BodyText']
    ))
    story.append(spacer(30))
    
    # Signature block
    sig_data = [
        [Paragraph("<b>Principal Investigator</b>", styles['TableCellBold']),
         Paragraph("", styles['TableCell']),
         Paragraph("<b>Co-Principal Investigator</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("", styles['TableCell'])],
        [Paragraph("Dr. Nidhi Rawat", styles['TableCellBold']),
         Paragraph("", styles['TableCell']),
         Paragraph("Raj Amritam", styles['TableCellBold'])],
        [Paragraph("Assistant Professor", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("PhD Scholar", styles['TableCell'])],
        [Paragraph("Dept. of Environmental Science", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("Dept. of Environmental Science", styles['TableCell'])],
        [Paragraph("DBS Global University, Dehradun", styles['TableCell']),
         Paragraph("", styles['TableCell']),
         Paragraph("DBS Global University, Dehradun", styles['TableCell'])],
    ]
    sig_table = Table(sig_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sig_table)
    story.append(spacer(30))
    
    story.append(Paragraph("Contact Information", styles['Heading2Green']))
    story.append(spacer(8))
    contact_data = [
        [Paragraph("<b>Institution</b>", styles['TableCell']),
         Paragraph("DBS Global University, Dehradun, Uttarakhand", styles['TableCell'])],
        [Paragraph("<b>Department</b>", styles['TableCell']),
         Paragraph("Department of Environmental Science", styles['TableCell'])],
        [Paragraph("<b>Project</b>", styles['TableCell']),
         Paragraph("PARVAT-SETU: Participatory AI-enabled Resource Valuation and Access Technology for Sustainable Economic Transformation in Uplands", styles['TableCell'])],
        [Paragraph("<b>Document Type</b>", styles['TableCell']),
         Paragraph("Impact Investor Proposal - Confidential", styles['TableCell'])],
        [Paragraph("<b>Version</b>", styles['TableCell']),
         Paragraph("1.0 (December 2024)", styles['TableCell'])],
    ]
    contact_table = Table(contact_data, colWidths=[1.5*inch, 5.0*inch])
    contact_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN_MED),
        ('BACKGROUND', (0, 0), (0, -1), GREEN_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(contact_table)
    story.append(spacer(30))
    
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN_DARK, spaceAfter=12))
    story.append(Paragraph(
        "PARVAT-SETU: Mountain Bridge - Connecting Himalayan Producers to Prosperity",
        ParagraphStyle('EndTag', fontName='Helvetica-Bold', fontSize=12,
                      textColor=GREEN_DARK, alignment=TA_CENTER)
    ))
    story.append(spacer(8))
    story.append(Paragraph(
        '"Where technology meets tradition, where impact meets returns,<br/>'
        'where mountains meet markets."',
        ParagraphStyle('EndQuote', fontName='Helvetica-Oblique', fontSize=11,
                      textColor=GREEN_MED, alignment=TA_CENTER, leading=16)
    ))


# ============================================================
# MAIN DOCUMENT BUILD
# ============================================================
def build_document():
    """Build the complete PDF document"""
    
    # Footer function
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(GREEN_MED)
        page_num = canvas.getPageNumber()
        text = f"PARVAT-SETU Impact Investor Proposal | Page {page_num}"
        canvas.drawCentredString(PAGE_WIDTH / 2, 0.4 * inch, text)
        # Header line
        canvas.setStrokeColor(GREEN_LIGHT)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_HEIGHT - 0.5*inch, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 0.5*inch)
        canvas.restoreState()
    
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="PARVAT-SETU Impact Investor Proposal",
        author="Dr. Nidhi Rawat & Raj Amritam"
    )
    
    styles = get_styles()
    story = []
    
    # Build all sections
    print("Building Cover Page...")
    build_cover_page(story, styles)
    
    print("Building Objectives of the Study...")
    build_objectives_section(story, styles)
    
    print("Building Detailed Methodology...")
    build_methodology_section(story, styles)
    
    print("Building Problem Section...")
    build_problem_page(story, styles)
    
    print("Building Solution Section...")
    build_solution_page(story, styles)
    
    print("Building Business Model Canvas...")
    build_business_model_canvas(story, styles)
    
    print("Building Market Opportunity...")
    build_market_opportunity(story, styles)
    
    print("Building Traction & Proof Points...")
    build_traction_page(story, styles)
    
    print("Building Financial Summary...")
    build_financial_summary(story, styles)
    
    print("Building The Ask...")
    build_the_ask(story, styles)
    
    print("Building Detailed Problem Analysis...")
    build_detailed_problem(story, styles)
    
    print("Building Solution Architecture...")
    build_solution_architecture(story, styles)
    
    print("Building Impact Thesis...")
    build_impact_thesis(story, styles)
    
    print("Building Revenue Model...")
    build_revenue_model(story, styles)
    
    print("Building Financial Projections...")
    build_financial_projections(story, styles)
    
    print("Building Balance Sheet & Valuation...")
    build_balance_sheet(story, styles)
    
    print("Building Blended Finance Structure...")
    build_blended_finance(story, styles)
    
    print("Building Go-to-Market Strategy...")
    build_go_to_market(story, styles)
    
    print("Building Competitive Landscape...")
    build_competitive_landscape(story, styles)
    
    print("Building Team Section...")
    build_team(story, styles)
    
    print("Building Governance & Legal...")
    build_governance(story, styles)
    
    print("Building Risk Factors...")
    build_risk_factors(story, styles)
    
    print("Building Exit Strategy...")
    build_exit_strategy(story, styles)
    
    print("Building Sustainability & ESG...")
    build_sustainability_esg(story, styles)
    
    print("Building Implementation Roadmap...")
    build_implementation_roadmap(story, styles)
    
    print("Building Appendices...")
    build_appendices(story, styles)
    
    print("Building Declaration...")
    build_declaration(story, styles)
    
    # Generate PDF
    print("\nGenerating PDF...")
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated successfully: {OUTPUT_PATH}")
    
    # Check file size
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"File size: {file_size / 1024:.1f} KB")


if __name__ == '__main__':
    build_document()
