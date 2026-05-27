#!/usr/bin/env python3
"""PARVAT-SETU Project Proposal PDF Generator (FULL)"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted)
import os

OUTPUT_PDF = '/projects/sandbox/mobile-printer-app/PARVAT_SETU_Project_Proposal.pdf'

styles = getSampleStyleSheet()
TitleStyle = ParagraphStyle('CT', parent=styles['Title'], fontName='Helvetica-Bold',
    fontSize=20, alignment=TA_CENTER, textColor=colors.HexColor('#1a4d2e'),
    spaceAfter=18, leading=24)
H1S = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=15, textColor=colors.HexColor('#1a4d2e'), spaceAfter=12, spaceBefore=18, leading=20, keepWithNext=1)
H2S = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold',
    fontSize=12, textColor=colors.HexColor('#2d5f3f'), spaceAfter=8, spaceBefore=14, leading=16, keepWithNext=1)
H3S = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-BoldOblique',
    fontSize=11, textColor=colors.HexColor('#3d6f4f'), spaceAfter=6, spaceBefore=12, leading=15, keepWithNext=1)
Body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Times-Roman',
    fontSize=11, alignment=TA_JUSTIFY, spaceAfter=10, leading=16, firstLineIndent=18)
BNI = ParagraphStyle('BNI', parent=Body, firstLineIndent=0)
Bullet = ParagraphStyle('Bullet', parent=Body, leftIndent=24, firstLineIndent=-12,
    spaceAfter=4, leading=14)
Caption = ParagraphStyle('Cap', parent=styles['Normal'], fontName='Helvetica-BoldOblique',
    fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#1a4d2e'),
    spaceAfter=6, spaceBefore=14, keepWithNext=1)
Mono = ParagraphStyle('Mono', parent=styles['Normal'], fontName='Courier',
    fontSize=7, leading=8.5, alignment=TA_LEFT, leftIndent=0, spaceAfter=0, spaceBefore=0)

story = []

def H(t, lvl=1):
    s = {1:H1S, 2:H2S, 3:H3S}[lvl]
    story.append(Paragraph(t, s))
def P(t): story.append(Paragraph(t, Body))
def PNI(t): story.append(Paragraph(t, BNI))
def B(t): story.append(Paragraph(f"&bull; {t}", Bullet))
def CAP(t): story.append(Paragraph(t, Caption))
def MONO(t):
    lines = t.split('\n')
    safe_lines = []
    for line in lines:
        line = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        line = line.replace(' ', '&nbsp;')
        safe_lines.append(line)
    html_content = '<br/>'.join(safe_lines)
    diag_style = ParagraphStyle('diagram', parent=styles['Normal'],
        fontName='Courier', fontSize=6.5, leading=8, alignment=TA_LEFT,
        spaceAfter=10, spaceBefore=4, leftIndent=0)
    story.append(Paragraph(html_content, diag_style))
    story.append(Spacer(1, 6))
def SP(h=8): story.append(Spacer(1, h))
def BR(): story.append(PageBreak())
def TBL(headers, rows, col_widths=None, hcolor='#1a4d2e'):
    cell_style = ParagraphStyle('cell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11, alignment=TA_LEFT,
        leftIndent=0, rightIndent=0, spaceAfter=0, spaceBefore=0)
    header_style = ParagraphStyle('hdr', parent=cell_style,
        fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_CENTER, fontSize=8.5)
    wrapped_headers = [Paragraph(str(h), header_style) for h in headers]
    wrapped_rows = []
    for row in rows:
        wrapped_rows.append([Paragraph(str(c), cell_style) for c in row])
    data = [wrapped_headers] + wrapped_rows
    if col_widths is None:
        pw = A4[0] - 1.4*inch
        col_widths = [pw/len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(hcolor)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
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
story.append(Paragraph('(Pilot Initiative &mdash; Social Enterprise Model)',
    ParagraphStyle('TS', parent=styles['Normal'], fontName='Helvetica-Oblique',
    fontSize=11, alignment=TA_CENTER, textColor=colors.HexColor('#666666'))))
SP(35)
story.append(Paragraph('<b>PARVAT-SETU</b>',
    ParagraphStyle('PT', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=26,
    alignment=TA_CENTER, textColor=colors.HexColor('#1a4d2e'), leading=30, spaceAfter=4)))
story.append(Paragraph('(पर्वत-सेतु &mdash; "Mountain Bridge")',
    ParagraphStyle('PT2', parent=styles['Title'], fontName='Helvetica-Oblique', fontSize=14,
    alignment=TA_CENTER, textColor=colors.HexColor('#2d5f3f'), leading=18, spaceAfter=18)))
SP(12)
story.append(Paragraph(
    'An Artificial Intelligence and Geospatial-Integrated<br/>'
    'Social Enterprise Platform for Digital Aggregation,<br/>'
    'Financial Inclusion, and Sustainable Livelihoods<br/>'
    'of Smallholder Producers in the Indian Himalayan Region',
    ParagraphStyle('PS', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=14,
    alignment=TA_CENTER, textColor=colors.HexColor('#2d5f3f'), leading=20)))
SP(35)
story.append(Paragraph(
    '<b>A Pilot Project Proposal Integrating:</b><br/>'
    'Sustainable Development &nbsp;|&nbsp; Artificial Intelligence (AI/ML)<br/>'
    'Geographic Information Systems (GIS) &nbsp;|&nbsp; Social Enterprise',
    ParagraphStyle('TM', parent=styles['Normal'], fontName='Helvetica-Bold',
    fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), leading=18)))
SP(30)
story.append(Paragraph(
    '<b>Submitted to:</b><br/>'
    'NABARD / ICSSR / NITI Aayog Atal Innovation Mission /<br/>'
    'Bharat Rural Livelihoods Foundation (BRLF) /<br/>'
    'Tata Trusts / Bill &amp; Melinda Gates Foundation',
    ParagraphStyle('SUB', parent=styles['Normal'], fontName='Helvetica',
    fontSize=11, alignment=TA_CENTER, leading=15)))
SP(20)
story.append(Paragraph(
    '<b>Submitted by:</b><br/>'
    '<b>Department of Environmental Science</b><br/>'
    '<b>DBS Global University, Dehradun, Uttarakhand</b>',
    ParagraphStyle('SBY', parent=styles['Normal'], fontName='Helvetica',
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
print("Title page added")

# ===================== ABSTRACT =====================
H('ABSTRACT', 1)
P('India hosts approximately 86% of farmers as smallholders cultivating less than two hectares of land, contributing roughly 51% of the nation\'s agricultural output yet capturing only 11-15% of consumer rupee due to fragmented value chains, multiple intermediaries, and severe information asymmetry. In the Indian Himalayan Region — comprising 13 states with over 50 million smallholders — this exclusion is compounded by extreme geographical isolation, climate vulnerability, lack of cold-chain infrastructure, and digital divide. Average mountain farmer net income hovers at INR 6,000-12,000 per month, well below the all-India rural mean and acutely below dignified livelihood thresholds.')

P('PARVAT-SETU (पर्वत-सेतु, "Mountain Bridge") proposes an integrated Artificial Intelligence (AI) and Geographic Information Systems (GIS) powered Social Enterprise Pilot Platform that systematically dismantles the four core barriers to smallholder economic inclusion: (i) the aggregation deficit, through digital producer-buyer matching; (ii) the finance access deficit, via embedded fintech and credit scoring; (iii) the information asymmetry, through AI-driven price prediction and demand forecasting; and (iv) the logistics inefficiency, via GIS-optimized routing and cold-chain coordination. The platform is structured as a producer-owned cooperative social enterprise with explicit pathways to operational and financial sustainability within five years through commission-based revenue, value-added processing, and institutional buyer subscriptions.')

P('The 30-month pilot will operate across three Himalayan districts (Tehri Garhwal, Pauri Garhwal, and Chamoli in Uttarakhand) covering 5,000 directly enrolled smallholder producers organized through 150 Self-Help Groups (SHGs) and 12 Farmer Producer Organizations (FPOs), with explicit gender mainstreaming targeting minimum 60% women participation. Quantified outcome targets include 35-50% increase in net producer income, 25-35% reduction in post-harvest losses through demand forecasting, full financial inclusion (Jan Dhan + insurance + working capital credit) for participating households, and demonstrated platform unit economics with break-even projected within 36 months post-pilot.')

P('The integrated technology stack combines: (i) a vernacular-language Android-lite mobile application for producer onboarding, listing, and order management; (ii) machine learning models for demand forecasting (LSTM/Prophet), price prediction (gradient boosting), credit scoring (random forest), and quality grading (computer vision); (iii) GIS-based resource mapping, agro-ecological zonation, climate-risk overlay, and last-mile logistics optimization; and (iv) blockchain-anchored traceability for premium-market access. Total investment of INR 1,85,00,000 (One Crore Eighty-Five Lakh) over 30 months delivers a replicable, evidence-based template scalable to all 13 Himalayan states protecting and uplifting an estimated 5,00,000+ smallholder households in subsequent phases.')

H('Keywords', 2)
P('Social Enterprise; Smallholder Producers; Digital Aggregation; Artificial Intelligence; Machine Learning; Geographic Information Systems; Financial Inclusion; Sustainable Livelihoods; Indian Himalayan Region; Farmer Producer Organizations; Self-Help Groups; Climate-Resilient Agriculture; Economic Uplift; Inclusive Growth; SDG 1, 2, 5, 8, 10, 12, 13.')

BR()
print("Abstract added")

# ===================== SECTION 1: METADATA =====================
H('SECTION 1: PROJECT IDENTIFICATION AND METADATA', 1)
TBL(['Field', 'Information'], [
    ['Project Title', 'PARVAT-SETU: An AI-GIS Integrated Social Enterprise Platform for Digital Aggregation, Financial Inclusion, and Sustainable Livelihoods of Smallholder Producers in the Indian Himalayan Region'],
    ['Project Acronym', 'PARVAT-SETU (पर्वत-सेतु)'],
    ['Proposed Tenure', '30 Months (2.5-Year Fast-Track Pilot)'],
    ['Total Financial Request', 'INR 1,85,00,000 (One Crore Eighty-Five Lakh Only)'],
    ['Targeted Pilot Region', 'Tehri Garhwal, Pauri Garhwal, Chamoli districts (Uttarakhand)'],
    ['Direct Beneficiaries', '5,000 smallholder producers (150 SHGs + 12 FPOs)'],
    ['Indirect Beneficiaries', '25,000 household members + 5,00,000 in scaling phase'],
    ['Women Participation Target', 'Minimum 60% (gender-mainstreamed design)'],
    ['SC/ST Inclusion Target', 'Minimum 35% participation'],
    ['Affiliation', 'Department of Environmental Science, DBS Global University, Dehradun'],
    ['Project Investigator (PI)', 'Dr. Nidhi Rawat, Assistant Professor'],
    ['Co-PI / Research Scholar', 'Raj Amritam, PhD Research Scholar'],
    ['Strategic Alignment', 'SDG 1, 2, 5, 8, 10, 12, 13; National Mission on Sustainable Agriculture; Atmanirbhar Bharat; PM Vishwakarma; PMFBY'],
    ['Technology Pillars', 'AI/ML + GIS + Mobile + Cloud + Blockchain Traceability'],
    ['Sustainability Model', 'Producer-owned Cooperative Social Enterprise with Self-Sustaining Revenue Model (Year 4+)'],
    ['Expected Income Uplift', '35-50% net income increase per participating household'],
], col_widths=[1.8*inch, 5.0*inch])

BR()
print("Section 1 added")

# ===================== SECTION 2: EXECUTIVE SUMMARY =====================
H('SECTION 2: EXECUTIVE SUMMARY AND STRATEGIC RATIONALE', 1)

H('2.1 The Smallholder Economic Inclusion Crisis', 2)
P('India is the only major economy where 86% of its farmers remain smallholders cultivating less than two hectares each, contributing 51% of national agricultural output yet remaining persistently locked into low-income, high-risk livelihood configurations. The 2018-19 Situation Assessment Survey (NSSO) documents that average monthly net agricultural income of smallholder households stands at INR 6,170 — a figure that, when adjusted for the high input costs of mountain agriculture and the seasonality of Himalayan production cycles, places the median Indian Himalayan smallholder household well below the World Bank moderate poverty line of USD 3.65 per person per day. The gap between farm-gate and consumer prices for typical mountain produce (apples, kiwis, walnuts, traditional millets, medicinal plants, off-season vegetables) routinely exceeds 300-500%, with smallholders capturing 15-25% of consumer rupee while the remaining 75-85% accrues to a chain of intermediaries — village commission agents, district mandi traders, transporters, wholesalers, and retailers — none of whom add proportionate value to justify their margin extraction.')

P('This systemic exclusion is not a market accident but a structural outcome of four mutually reinforcing barriers. First, the AGGREGATION DEFICIT: smallholders cannot individually achieve the volume thresholds required by institutional buyers (modern retail, food processors, exporters, e-commerce platforms), forcing them into spot-market sales at unfavourable terms. Second, the FINANCE ACCESS DEFICIT: 67% of Indian Himalayan smallholders remain outside formal credit systems, relying on private moneylenders charging 36-60% annual interest, while crop insurance penetration in mountain districts hovers at 12-18% versus 38% in irrigated plains. Third, the INFORMATION ASYMMETRY: producers lack real-time price information, demand forecasts, weather advisories, and quality-standard awareness, leading to mis-timed sales and post-harvest losses estimated at 28-40% by value. Fourth, the LOGISTICS INEFFICIENCY: fragmented production locations, absent cold-chain infrastructure, and unoptimized routing waste 18-25% of perishable output before it reaches markets, while inflating per-unit transportation costs by 200-400% versus plains-region benchmarks.')

H('2.2 The PARVAT-SETU Value Proposition', 2)
P('PARVAT-SETU directly addresses each of these four barriers through a single integrated platform combining cutting-edge Artificial Intelligence, Geographic Information Systems, mobile technology, and a producer-owned social enterprise governance structure. The platform aggregates fragmented smallholder supply through digital onboarding via vernacular Android-lite applications, matches it with institutional and consumer demand through AI-driven recommendation engines, optimizes logistics through GIS-based routing and cold-chain coordination, and embeds financial services (credit scoring, insurance, payments) directly into transactional workflows — simultaneously achieving income uplift, risk reduction, asset building, and dignified market participation for marginalized mountain smallholders.')

P('Unlike conventional agriculture-tech ventures that operate as for-profit intermediaries (DeHaat, Ninjacart, Crofarm) capturing platform value for venture investors, or government schemes (e-NAM, FPO formation) that deliver infrastructure without operational sustainability, PARVAT-SETU is structured deliberately as a producer-owned cooperative social enterprise. This means: (i) governance authority rests with elected smallholder representatives at SHG, cluster, and federation levels; (ii) commercial surplus is reinvested into producer welfare, technology improvement, and geographic expansion rather than distributed as external dividends; (iii) revenue model relies on transaction commissions (3-5%), value-added processing margins, and institutional buyer subscriptions designed to achieve operational break-even within 36 months post-pilot without external grant dependency. This hybrid architecture — combining the scale efficiency of digital platforms, the analytical power of AI/GIS, and the equity ethics of cooperative governance — represents an unprecedented integration in the Indian smallholder ecosystem.')

H('2.3 Why Now? The Convergent Enabling Environment', 2)
P('Five contemporaneous factors create an unprecedented enabling environment for PARVAT-SETU at this specific historical moment. First, smartphone penetration in Indian rural households has crossed 67% (2024 ICRIER survey), with 4G coverage reaching 82% of inhabited Himalayan villages — making mobile-first platforms operationally viable for the first time. Second, the Unified Payments Interface (UPI), Aadhaar-enabled payment systems, and Account Aggregator framework have collectively reduced the marginal cost of digital financial transactions to near-zero, enabling embedded fintech at smallholder scale. Third, Indian government priorities under PM Vishwakarma, the Agriculture Infrastructure Fund, the FPO scheme (10,000 FPOs by 2027), and the Digital Public Infrastructure (DPI) for agriculture (Agri Stack) provide both regulatory facilitation and complementary funding pathways. Fourth, advances in open-source AI/ML libraries (Hugging Face, TensorFlow Lite, ONNX) have reduced model development costs by 80-90% versus 2018 levels, while edge computing capabilities enable on-device inference even with intermittent connectivity. Fifth, climate change-induced market volatility and consumer demand for traceable, sustainable, mountain-origin produce (premium apple varieties, traditional millets, organic herbs, single-origin honey) creates a value-premium opportunity that smallholder producers can capture only through digital aggregation platforms enabling producer-to-buyer trust at scale.')

H('2.4 International and Indian Precedents Validating Feasibility', 2)
P('PARVAT-SETU\'s design synthesizes lessons from rigorously evaluated precedents. The Self Employed Women\'s Association (SEWA) in India has demonstrated since 1972 that cooperative ownership combined with embedded finance can deliver 200-400% income uplift for marginalized women workers. Amul has demonstrated that producer-owned aggregation at scale can sustainably capture 70-80% of consumer rupee for dairy farmers. Internationally, M-Pesa in Kenya transformed financial inclusion for 96% of Kenyan adults through mobile money. One Acre Fund (East Africa) has documented 40-50% income increase across 1.5 million smallholders through bundled inputs-credit-training-markets. Microsoft AI Sowing App has demonstrated 30% yield increase through AI-driven advisory in Andhra Pradesh. These precedents collectively validate that each component of the PARVAT-SETU design — cooperative governance, embedded finance, AI advisory, digital aggregation, GIS optimization — has individually proven feasibility at scale; what is unprecedented is their integration within a single platform tailored to the Indian Himalayan smallholder context.')

H('2.5 Investment Logic and Expected Returns', 2)
P('The total investment of INR 1,85,00,000 over 30 months translates to approximately INR 3,700 per directly enrolled producer over the pilot period. With expected median income uplift of 40% (INR 30,000-50,000 additional annual income per household), the project achieves an aggregate annual income increase of INR 15-25 Crore for 5,000 households at the end of the pilot — representing an Internal Rate of Return (IRR) of 800-1300% on the grant investment, computed on the income-uplift basis alone, before considering platform unit economics, asset accumulation effects, intergenerational poverty reduction, and externalities such as climate adaptation and gender empowerment. The pilot is explicitly designed for scalability: the technology stack, training curricula, governance templates, and institutional partnerships developed during the pilot can be deployed across additional Himalayan districts at marginal cost reductions of 50-65% per unit, enabling the protection and uplift of 5,00,000+ smallholder households across the broader Indian Himalayan Region within seven years of pilot completion.')
BR()
print("Section 2 (Executive Summary) added")

# ===================== SECTION 3: PROBLEM STATEMENT =====================
H('SECTION 3: DETAILED PROBLEM STATEMENT AND CONTEXT', 1)

H('3.1 The Indian Himalayan Region: Geographic and Demographic Profile', 2)
P('The Indian Himalayan Region (IHR) spans approximately 5,33,604 square kilometres across 13 states and union territories — Jammu &amp; Kashmir, Ladakh, Himachal Pradesh, Uttarakhand, Sikkim, Arunachal Pradesh, Nagaland, Manipur, Mizoram, Tripura, Meghalaya, Assam (hilly portions), and West Bengal (Darjeeling) — hosting approximately 5 crore (50 million) inhabitants of whom over 70% are directly dependent on agriculture, horticulture, animal husbandry, and forest-based livelihoods. The pilot region selected for PARVAT-SETU encompasses three Garhwal Himalayan districts of Uttarakhand: Tehri Garhwal (4,080 sq km, population 6.18 lakh), Pauri Garhwal (5,329 sq km, population 6.87 lakh), and Chamoli (8,030 sq km, population 3.91 lakh) — collectively covering 17,439 sq km with approximately 16.96 lakh inhabitants, of whom approximately 11 lakh reside in agricultural households cultivating an average landholding of 0.68 hectares.')

H('3.2 The Four Compounding Barriers to Smallholder Economic Inclusion', 2)

CAP('TABLE 3.1: Quantified Barrier Matrix &mdash; Indian Himalayan Smallholders')
TBL(['Barrier', 'Specific Manifestation', 'Quantified Impact', 'PARVAT-SETU Response'], [
    ['Aggregation Deficit', 'Fragmented production, distance to markets, no collective bargaining', '70-85% margin loss to intermediaries; 28-40% post-harvest loss', 'Digital aggregation platform; AI demand-supply matching; GIS clustering'],
    ['Finance Exclusion', 'No formal credit, low insurance penetration, no working capital', '67% outside formal credit; moneylenders charge 36-60%; 12-18% insurance', 'Embedded fintech; AI credit scoring; bundled insurance; account aggregator'],
    ['Information Asymmetry', 'No real-time prices, demand forecasts, weather, quality standards', 'Mis-timed sales costing 25-35% revenue loss', 'AI price prediction; demand forecasting; vernacular advisory; quality CV'],
    ['Logistics Inefficiency', 'No cold chain, fragmented routing, perishable losses', '18-25% perishable spoilage; 200-400% higher per-unit transport cost', 'GIS-optimized routing; shared cold-chain; consolidated load planning'],
])

H('3.3 The Climate-Economic Compound Vulnerability', 2)
P('A defining and underappreciated feature of the Indian Himalayan smallholder context is the compound vulnerability arising from the simultaneous escalation of climate risks and economic exclusion. Climate change is intensifying flash floods, debris flows, glacial lake outburst floods, prolonged dry spells, and unseasonal precipitation events — all of which disproportionately impact smallholders who lack risk-transfer mechanisms (insurance), liquidity buffers (savings), and adaptive capacity (information and inputs to shift cropping patterns). The 2013 Kedarnath disaster wiped out an estimated INR 5,000 Crore of smallholder assets in a single event; the 2021 Chamoli flood destroyed produce inventory worth INR 200+ Crore for downstream smallholders; the recurring monsoon-season landslides annually disrupt market access for 30-40% of Garhwal smallholders for 15-30 cumulative days per year, forcing distress sales of perishables. Without integrated platforms providing insurance, weather advisories, alternative-route logistics, and emergency credit, every climate event compounds into an economic catastrophe for affected households.')

H('3.4 Specific Production-System Profile in Pilot Region', 2)
CAP('TABLE 3.2: Pilot Region Production System Diversity')
TBL(['Crop / Product', 'Approximate Producers', 'Avg Area / HH', 'Current Farm-Gate Price', 'Premium Market Potential'], [
    ['Apple (premium varieties)', '15,000', '0.4 ha', 'INR 25-45/kg', 'INR 80-200/kg traceable'],
    ['Walnut', '12,000', '0.2 ha', 'INR 200-300/kg in-shell', 'INR 600-900/kg organic'],
    ['Kiwi', '3,500', '0.15 ha', 'INR 80-120/kg', 'INR 200-400/kg organic'],
    ['Off-season vegetables', '25,000', '0.3 ha', 'INR 8-25/kg', 'INR 30-80/kg fresh-direct'],
    ['Traditional millets (Mandua, Jhangora)', '40,000', '0.4 ha', 'INR 25-40/kg', 'INR 80-150/kg branded'],
    ['Medicinal/Aromatic Plants', '5,000', '0.2 ha', 'INR 50-300/kg dry', 'INR 200-2,000/kg processed'],
    ['Honey (mountain origin)', '4,000', 'N/A', 'INR 200-400/kg', 'INR 600-1,200/kg single-origin'],
    ['Handicrafts (women SHGs)', '8,000', 'N/A', 'INR 200-1,500/piece', 'INR 800-5,000/piece designer'],
    ['Dairy (mountain breeds)', '20,000', '2-4 cattle', 'INR 25-40/L', 'INR 60-100/L A2 / organic'],
])

P('This profile reveals a critical pattern: every product category in the pilot region exhibits a 200-500% premium-market potential over current farm-gate prices — but capturing this premium requires the precise capabilities that PARVAT-SETU provides: traceability (blockchain), quality grading (AI computer vision), volume aggregation (digital platform), institutional buyer access (B2B portal), and consumer trust signals (origin certification, organic verification, fair-trade compliance). Without these capabilities, smallholders remain locked into commodity-grade pricing despite producing artisanal-quality output. With them, even partial premium capture (50-80% of the gap between commodity and premium prices) translates to 50-200% income uplift per household.')
BR()
print("Section 3 added")

# ===================== SECTION 4: LITERATURE REVIEW =====================
H('SECTION 4: LITERATURE REVIEW &mdash; PRIOR WORK AND BEST PRACTICES', 1)
P('PARVAT-SETU explicitly synthesizes lessons from rigorously documented Indian and international precedents across four thematic streams: (i) cooperative social enterprise models, (ii) digital agriculture aggregation platforms, (iii) AI applications in smallholder agriculture, and (iv) GIS applications for rural livelihoods. This section comprehensively reviews each stream, identifying both validated success patterns and documented failure modes that inform PARVAT-SETU\'s design.')

H('4.1 Indian Cooperative Social Enterprise Precedents', 2)
P('The Self Employed Women\'s Association (SEWA), founded in 1972 by Ela Bhatt in Ahmedabad, organizes 1.7 million informal-sector women workers across 18 Indian states into producer cooperatives, savings groups, and service collectives. SEWA Bank, established 1974, demonstrates that women smallholders provided with savings, credit, and insurance services achieve 200-400% income growth over five-year periods compared to non-member peers. Critical lessons informing PARVAT-SETU: (i) member ownership creates governance accountability that no NGO or for-profit can replicate; (ii) bundled services (organize + finance + train + market) outperform single-service interventions by 3-5x; (iii) explicit gender focus is operationally sustainable when paired with economic outcomes.')

P('Amul (Anand Milk Union Limited), launched in 1946 and matured into the Gujarat Cooperative Milk Marketing Federation, demonstrates that producer-owned aggregation at national scale can sustainably capture 70-80% of consumer rupee for 3.6 million dairy farmers. The Amul model — village dairy cooperative society aggregated into district unions, in turn federated at state level — provides the institutional template for PARVAT-SETU\'s three-tier governance: SHG-level micro-cooperatives, cluster-level Federations, and the apex Producer Company. The Amul success demonstrates that cooperative architecture, when combined with daily-cash-flow products (milk) and minimal-loss commodities (powder, butter, cheese), can become both economically self-sustaining and socially transformative.')

P('The Indian government\'s FPO (Farmer Producer Organization) scheme, launched 2014 and accelerated to a target of 10,000 FPOs by 2027 with INR 6,865 Crore committed budget, provides direct institutional and funding alignment for PARVAT-SETU. SFAC (Small Farmers\' Agribusiness Consortium), NCDC (National Cooperative Development Corporation), and NABARD jointly support FPO formation, capacity building, and infrastructure. PARVAT-SETU will integrate with 12 existing or newly-formed FPOs in the pilot region, providing them with the technology stack and market linkages they currently lack — addressing the documented FPO challenge that 60-70% of formed FPOs remain operationally weak due to absence of digital infrastructure and market connectivity.')

H('4.2 Digital Agriculture Aggregation Platforms &mdash; What Worked, What Failed', 2)
CAP('TABLE 4.1: Comparative Analysis of Digital Aggregation Platforms')
TBL(['Platform', 'Type', 'Geography', 'Producers Reached', 'Key Outcome', 'Critical Lesson'], [
    ['DeHaat', 'For-profit B2B', 'Bihar, UP, Odisha, Jharkhand, WB', '15 lakh+', '20-30% income uplift', 'Scale via local micro-entrepreneurs'],
    ['Ninjacart', 'For-profit B2B', 'Bangalore, Hyderabad, Chennai', 'Not disclosed', 'Cold-chain efficiency', 'Capital-intensive; sustainability unclear'],
    ['eNAM (Govt)', 'Mandi e-trading', 'All India', '1.7 crore registered', 'Limited active usage', 'Govt platform requires offline reform'],
    ['Crofarm', 'For-profit B2B', 'Delhi NCR, Mumbai', 'Closed 2023', 'Failed sustainability', 'Pure tech without producer ownership fails'],
    ['SEWA-RUDI', 'Cooperative', 'Gujarat', '50,000+', 'Sustainable for 15 years', 'Cooperative + tech integration works'],
    ['Amul', 'Cooperative', 'National', '36 lakh', '70-80% margin to producer', 'Daily-cash products + scale = sustainability'],
    ['ITC e-Choupal', 'Corporate B2B', 'Multi-state', '40 lakh', 'Procurement efficiency', 'Information access dramatically improves outcomes'],
    ['One Acre Fund', 'NGO Hybrid (East Africa)', 'Kenya, Rwanda, Tanzania', '15 lakh', '40-50% income uplift', 'Bundled inputs+finance+training+markets'],
    ['M-Pesa', 'Telecom Fintech (Kenya)', 'Kenya, Tanzania, Mozambique', '5 crore+', '2% GDP poverty reduction', 'Mobile money transforms financial inclusion'],
])

P('The comparative analysis yields five critical design lessons informing PARVAT-SETU. First, PURE FOR-PROFIT TECH PLATFORMS WITHOUT PRODUCER OWNERSHIP STRUGGLE WITH SUSTAINABILITY (Crofarm closed; Ninjacart faces ongoing scrutiny; Crofarm-style failures number in the hundreds globally). Second, COOPERATIVE OWNERSHIP COMBINED WITH MODERN TECHNOLOGY ACHIEVES BOTH SCALE AND SUSTAINABILITY (Amul, SEWA, Mondragon-Spain). Third, BUNDLING SERVICES (aggregate + finance + advise + market) DRAMATICALLY OUTPERFORMS UNBUNDLED INTERVENTIONS (One Acre Fund\'s 40-50% income gain versus single-service interventions averaging 8-15%). Fourth, MOBILE-FIRST + VERNACULAR + EMBEDDED FINANCE IS THE OPERATIONAL UNLOCK in low-literacy rural settings (M-Pesa\'s transformation of Kenya). Fifth, GOVERNMENT PLATFORMS REQUIRE COMPLEMENTARY DIGITAL CIVIL-SOCIETY ENABLERS to translate registered enrollment into active usage (eNAM, despite enrolling 1.7 crore farmers, sees less than 8% active monthly usage).')

H('4.3 AI Applications in Smallholder Agriculture &mdash; State of the Art', 2)
P('Recent advances in machine learning, computer vision, and natural language processing have moved AI applications in smallholder agriculture from research demonstrations into operational deployment. Microsoft\'s AI Sowing App, deployed in Andhra Pradesh\'s Devanakonda mandal in partnership with ICRISAT (2017-present), uses weather-based AI predictions to advise optimal sowing dates — documented to deliver 30% yield increase versus historical practice. IBM Watson Decision Platform for Agriculture provides field-level analytics combining satellite imagery, weather data, and soil sensors. CropIn (Bangalore-based) uses computer vision and ML for crop monitoring across 9.4 million acres globally. Plantix (Berlin-Hyderabad) deploys deep learning image classification for plant disease diagnosis with 95%+ accuracy across 30+ crops in 18 languages. Wadhwani AI\'s Cotton Pest Management platform achieves 23% pesticide reduction through AI-driven targeted intervention.')

P('PARVAT-SETU will integrate four production-grade AI capabilities: (i) DEMAND FORECASTING through LSTM (Long Short-Term Memory) and Prophet time-series models trained on multi-year market price data, weather patterns, festival calendars, and consumer search trends; (ii) PRICE PREDICTION through gradient boosting (XGBoost) ensembles producing 7-day, 30-day, and seasonal price forecasts at district granularity; (iii) CREDIT SCORING through random forest classifiers using 30+ alternative data signals including transaction history, weather exposure, asset ownership, and SHG repayment patterns to enable credit access for the credit-history-less; and (iv) QUALITY GRADING through computer vision models (CNN architectures, mobile-optimized via TensorFlow Lite) running on producer smartphones to automate produce quality assessment at point of harvest.')

H('4.4 GIS Applications for Rural Livelihoods', 2)
P('Geographic Information Systems have moved from research-only tools into operational platforms enabling rural livelihood interventions at scale. The MGNREGA Information System (NREGASoft) integrates GIS-based asset tracking across 1.6 lakh Gram Panchayats. ICRISAT\'s Digital Atlas of Indian Agriculture provides high-resolution agro-ecological zonation. The Bhuvan portal (ISRO) provides free geospatial data layers for the entire country. The Land Resources Information System (LRIS) maps soil quality, water resources, and land-use across 500+ districts. PARVAT-SETU\'s GIS layer integrates these existing public datasets with project-specific overlays: (i) producer location mapping with linkage to land records; (ii) agro-ecological zonation for crop-suitability advisory; (iii) climate-risk overlays (flood zones, landslide susceptibility) for site-specific insurance pricing; (iv) logistics-network mapping with optimization for collection-route planning; and (v) market-shed analysis for buyer-side facility location.')
BR()
print("Section 4 added")

# ===================== SECTION 5: VISION, OBJECTIVES & HYPOTHESES =====================
H('SECTION 5: VISION, OBJECTIVES, AND TESTABLE HYPOTHESES', 1)

H('5.1 Long-Term Vision (10-Year Horizon)', 2)
P('To transform the economic position of 5,00,000+ smallholder producers across the Indian Himalayan Region by 2035 through a producer-owned, AI-GIS-powered social enterprise platform that delivers 40-60% sustained net income increase, full financial inclusion, climate resilience, and dignified market participation — establishing a globally replicable template for technology-enabled cooperative enterprise in mountain economies.')

H('5.2 Pilot-Specific Objectives (30 Months)', 2)
B('<b>Objective 1 (Aggregation):</b> Onboard 5,000 smallholder producers across 150 SHGs and 12 FPOs in Tehri Garhwal, Pauri Garhwal, and Chamoli districts onto the PARVAT-SETU platform, with verified production listings, banking integration, and active transaction history.')
B('<b>Objective 2 (Income Uplift):</b> Demonstrate 35-50% increase in net farm-gate income for participating producers over 24 months of platform engagement, validated through pre-post difference-in-differences quasi-experimental design with matched control villages.')
B('<b>Objective 3 (Financial Inclusion):</b> Achieve 100% financial inclusion (Jan Dhan account + insurance + working capital credit access) for participating households, with at least 60% of credit issued via AI-scored alternative-data lending.')
B('<b>Objective 4 (Loss Reduction):</b> Achieve 25-35% reduction in post-harvest losses through AI demand forecasting, GIS-optimized logistics, and shared cold-chain infrastructure deployment at three strategic cluster locations.')
B('<b>Objective 5 (Gender &amp; Equity):</b> Ensure minimum 60% women participation, minimum 35% Scheduled Caste / Scheduled Tribe participation, and demonstrate gender-disaggregated income outcomes with no statistically significant adverse differential.')
B('<b>Objective 6 (Sustainability Pathway):</b> Demonstrate platform unit economics with revenue from commissions (3-5%), value-added processing margins, and institutional buyer subscriptions; establish trajectory to operational break-even within 36 months post-pilot completion.')
B('<b>Objective 7 (Replicability):</b> Document the technology stack, training curricula, governance templates, and partnership protocols sufficient for direct replication across 10+ Himalayan districts at 50-65% reduced unit cost.')

H('5.3 Testable Hypotheses', 2)
P('<b>Hypothesis H1 (Income):</b> Smallholder producers actively engaged with PARVAT-SETU for 18+ months will demonstrate net farm-gate income increase of 35-50% compared to matched control producers in adjacent non-platform villages, after controlling for crop type, landholding size, household demographics, and macro price trends. (Verified via difference-in-differences with two-period panel data and matched-comparison household survey.)')
P('<b>Hypothesis H2 (Information Premium):</b> AI-driven price prediction and demand forecasting will enable participating producers to time sales and select crops yielding 15-25% revenue premium over uninformed-decision baselines, measured as the difference between actual realized prices and counterfactual prices that would have been received without platform information.')
P('<b>Hypothesis H3 (Financial Inclusion Access):</b> AI-based alternative-data credit scoring will enable working-capital credit access for at least 70% of credit-history-less smallholder applicants, with default rates remaining below 4% over 24-month observation, validating the methodology for scaling.')
P('<b>Hypothesis H4 (Logistics Efficiency):</b> GIS-optimized routing combined with shared cold-chain infrastructure will reduce per-unit logistics costs by 30-45% and post-harvest losses by 25-35% compared to baseline producer experience.')
P('<b>Hypothesis H5 (Gender Equity):</b> Gender-mainstreamed platform design will deliver income outcomes for women producers that are statistically equivalent to (and trending higher than) those for male producers, controlling for crop type and landholding — demonstrating that digital platforms can systematically narrow rather than widen rural gender economic gaps.')
P('<b>Hypothesis H6 (Sustainability):</b> Platform commission revenue plus value-added processing margins plus institutional buyer subscriptions will achieve trajectory to cover operational costs by month 36 (6 months post-pilot), demonstrating that producer-owned social enterprise architectures can achieve financial self-sustainability without permanent grant dependency.')

# ===================== SECTION 6: CONCEPTUAL FRAMEWORK =====================
H('SECTION 6: CONCEPTUAL FRAMEWORK', 1)
P('PARVAT-SETU\'s conceptual architecture is grounded in three interlocking analytical lenses: (i) the SUSTAINABLE LIVELIHOODS FRAMEWORK (DFID 1999) which conceptualizes household well-being as a function of five capital stocks (human, social, natural, physical, financial) and the institutional context that mediates access to these capitals; (ii) the THEORY OF CHANGE for digital platforms in development contexts which articulates the causal pathway from technology inputs through behavioural change to economic outcomes; and (iii) the COOPERATIVE SOCIAL ENTERPRISE THEORY which frames producer-owned platforms as alternative institutional architectures that internalize externalities (e.g., information, trust, governance) which conventional markets fail to provide.')

CAP('DIAGRAM 1: PARVAT-SETU Conceptual Framework &mdash; AI + GIS + Social Enterprise Integration')
MONO('''
================================================================================
         PARVAT-SETU INTEGRATED CONCEPTUAL FRAMEWORK
================================================================================

  +--------------------------------------------------------------+
  |                    SMALLHOLDER PRODUCERS                      |
  |  (5,000 across 150 SHGs + 12 FPOs in Garhwal Himalaya)        |
  |  60% women | 35%+ SC/ST | <2 ha landholding median            |
  +-------------------------+------------------------------------+
                            |
                            v Onboarding via vernacular mobile app
  +--------------------------------------------------------------+
  |              PARVAT-SETU PLATFORM CORE                        |
  |                                                                |
  |  +------------+   +------------+   +------------+              |
  |  |   AI/ML    |   |    GIS     |   |  FINTECH   |              |
  |  | LAYER      |   |   LAYER    |   |   LAYER    |              |
  |  |            |   |            |   |            |              |
  |  | * Demand   |   | * Producer |   | * Embedded |              |
  |  |   forecast |   |   mapping  |   |   payments |              |
  |  | * Price    |   | * Agro-eco |   | * AI credit|              |
  |  |   predict  |   |   zonation |   |   scoring  |              |
  |  | * Credit   |   | * Climate  |   | * Insurance|              |
  |  |   scoring  |   |   risk map |   |   bundling |              |
  |  | * Quality  |   | * Logistics|   | * UPI/JAM  |              |
  |  |   grading  |   |   routing  |   |   linkage  |              |
  |  | * Vernac.  |   | * Market   |   | * Account  |              |
  |  |   advisory |   |   sheds    |   |   aggregator              |
  |  +------------+   +------------+   +------------+              |
  +-------------------------+------------------------------------+
                            |
                            v Producer-owned governance
  +--------------------------------------------------------------+
  |         COOPERATIVE SOCIAL ENTERPRISE GOVERNANCE              |
  |                                                                |
  |  Three-tier producer ownership:                                |
  |  Tier 1: SHG-level (15-20 producers)                           |
  |  Tier 2: Cluster Federation (10-12 SHGs)                       |
  |  Tier 3: Apex Producer Company (12 FPOs federated)             |
  +-------------------------+------------------------------------+
                            |
                            v Market linkage
  +--------------------------------------------------------------+
  |              INSTITUTIONAL & CONSUMER MARKETS                 |
  |                                                                |
  |  * Modern retail (Reliance Smart, BigBasket, DMart)           |
  |  * Food processors / FMCG companies                            |
  |  * Direct-to-consumer (D2C) e-commerce                         |
  |  * Export markets (premium organic, single-origin)             |
  |  * Hotel/hospitality / institutional canteens                  |
  +--------------------------------------------------------------+
                            |
                            v Income flows back to producers
  +--------------------------------------------------------------+
  |          ECONOMIC UPLIFT + SUSTAINABILITY OUTCOMES            |
  |                                                                |
  |  * 35-50% net income increase                                  |
  |  * 25-35% post-harvest loss reduction                          |
  |  * 100% financial inclusion                                    |
  |  * Climate resilience via insurance + advisory                 |
  |  * Gender equity (60%+ women)                                  |
  |  * Asset accumulation (savings, credit history, land)          |
  +--------------------------------------------------------------+
''')
BR()
print("Sections 5-6 added")

# ===================== SECTION 7: METHODOLOGY =====================
H('SECTION 7: DETAILED METHODOLOGY &mdash; SIX-PHASE EXECUTION ARCHITECTURE', 1)
P('The PARVAT-SETU methodology is structured as six sequential yet interconnected execution phases, each designed for measurable progress while feeding learnings forward. The methodology balances rigour (validated technology, comparison-group design for impact measurement) with pragmatism (mobile-first, vernacular-language, embedded-finance) to ensure both academic credibility and operational deployment success.')

CAP('DIAGRAM 2: Six-Phase Execution Pipeline')
MONO('''
================================================================================
              PARVAT-SETU SIX-PHASE EXECUTION PIPELINE
================================================================================

  PHASE 1 (M1-4): BASELINE GIS MAPPING & STAKEHOLDER MOBILIZATION
  +-------------------------------------------------------------+
  | * GIS overlay: producer locations + agro-eco + climate risk |
  | * SHG/FPO identification and partnership MoUs                |
  | * Baseline household survey (2,000 sample)                   |
  | * Control village identification (matched-pair design)       |
  +-------------------------------------------------------------+
                            |
                            v
  PHASE 2 (M3-8): TECHNOLOGY DEVELOPMENT & PRODUCER ONBOARDING
  +-------------------------------------------------------------+
  | * Mobile app development (Android-lite, vernacular)          |
  | * Backend infrastructure (cloud, API, blockchain)            |
  | * Producer enrollment: 5,000 across 3 districts              |
  | * Vernacular training content development                    |
  +-------------------------------------------------------------+
                            |
                            v
  PHASE 3 (M6-14): AI MODEL TRAINING & DEPLOYMENT
  +-------------------------------------------------------------+
  | * Demand forecasting models (LSTM/Prophet)                   |
  | * Price prediction models (XGBoost ensembles)                |
  | * Credit scoring models (random forest, alt-data)            |
  | * Quality grading CV models (mobile-deployed)                |
  | * Vernacular voice/text advisory deployment                  |
  +-------------------------------------------------------------+
                            |
                            v
  PHASE 4 (M8-22): FINANCIAL INCLUSION INTEGRATION
  +-------------------------------------------------------------+
  | * Bank partnership MoUs (NABARD, RRBs, scheduled banks)      |
  | * Insurance partnerships (PMFBY, AIC, private insurers)      |
  | * Embedded payments (UPI, AePS, Account Aggregator)          |
  | * Credit disbursement: target INR 5 Cr to 2,000 producers    |
  | * Insurance enrollment: 100% participating households        |
  +-------------------------------------------------------------+
                            |
                            v
  PHASE 5 (M10-26): MARKET LINKAGE & TRANSACTION SCALING
  +-------------------------------------------------------------+
  | * Buyer onboarding: 50+ institutional, 5+ retail chains      |
  | * D2C e-commerce platform launch                              |
  | * Export market certification (organic, fair-trade)          |
  | * Cold-chain infrastructure: 3 cluster collection centres    |
  | * Transaction volume target: INR 50+ Cr GMV by M30           |
  +-------------------------------------------------------------+
                            |
                            v
  PHASE 6 (M22-30): IMPACT EVALUATION & SCALING DOCUMENTATION
  +-------------------------------------------------------------+
  | * Endline household survey + DiD analysis                    |
  | * Platform unit economics validation                          |
  | * Replication playbook documentation                          |
  | * Scaling-phase fundraising (Phase 2: 10 districts)          |
  | * Academic publications (3-4 SCIE papers)                    |
  +-------------------------------------------------------------+
''')

H('7.1 Phase 1: Baseline GIS Mapping &amp; Stakeholder Mobilization (Months 1-4)', 2)
P('The foundational phase establishes the geospatial baseline and institutional partnerships necessary for subsequent intervention. Detailed activities: (i) GIS-based producer mapping integrating Census 2011 village-level data with land records (Bhulekh portal), agro-ecological zonation (ICAR-NBSSLUP), climate-risk overlays (IMD historical data + IPCC AR6 downscaled projections), and existing infrastructure (mandis, cold storage, road network); (ii) SHG and FPO identification through partnership with Uttarakhand Livelihoods Mission (REAP), NABARD-supported FPOs, NRLM Ajeevika network; (iii) Memorandum of Understanding with 12 partner FPOs and 150 SHGs covering 5,000 producers; (iv) Baseline household survey of 2,000 households (1,000 platform-eligible + 1,000 control) measuring income, expenditure, asset base, financial inclusion, and well-being indicators; (v) Identification of matched control villages using propensity-score-matching algorithms ensuring statistical comparability for impact evaluation.')

H('7.2 Phase 2: Technology Development &amp; Producer Onboarding (Months 3-8)', 2)
P('Parallel technology development and human onboarding tracks operate simultaneously. Technology development: (i) Android-lite mobile application (target 15 MB installed size, offline-first sync, supporting Hindi, Garhwali, Kumaoni); (ii) Backend infrastructure on Indian cloud (NIC Cloud or AWS Mumbai region for data sovereignty); (iii) RESTful API layer enabling third-party integrations; (iv) Blockchain anchor layer (Hyperledger Fabric) for traceability records; (v) Web-based admin dashboards for FPO managers and PARVAT-SETU operations team. Producer onboarding: (i) Cluster-based enrollment camps in 50+ villages; (ii) Smartphone provisioning support for producers without devices (subsidy + buyback model); (iii) Aadhaar-linked KYC with eKYC API integration; (iv) Bank account verification via Account Aggregator framework; (v) Production listing capture (current crops, area, expected yields, harvest calendar); (vi) Training module deployment with vernacular video content.')

H('7.3 Phase 3: AI Model Training &amp; Deployment (Months 6-14)', 2)
P('The AI capability stack is built incrementally as data accumulates from producer onboarding and early transactions. Each model follows a rigorous development protocol: data collection &rarr; feature engineering &rarr; model training (multiple architectures benchmarked) &rarr; cross-validation &rarr; deployment to staging &rarr; A/B testing &rarr; production deployment &rarr; continuous monitoring with drift detection.')

CAP('TABLE 7.1: AI/ML Model Specifications')
TBL(['Model', 'Algorithm', 'Training Data', 'Performance Target', 'Deployment'], [
    ['Demand Forecasting', 'LSTM + Prophet ensemble', 'Multi-year mandi prices, weather, festival calendar, e-com search trends', 'MAPE &lt; 15%', 'Cloud, 7-day rolling'],
    ['Price Prediction', 'XGBoost gradient boosting', '5-year district mandi data, futures prices, supply signals', 'R&sup2; &gt; 0.75', 'Cloud, real-time API'],
    ['Credit Scoring', 'Random Forest + Logistic Regression', 'SHG repayment, transaction history, asset proxies, weather exposure', 'AUC &gt; 0.78, default &lt; 4%', 'Cloud + edge'],
    ['Quality Grading', 'CNN (MobileNetV3, EfficientNet-Lite)', 'Crowd-sourced labelled produce images', 'Top-1 accuracy &gt; 88%', 'Mobile (TensorFlow Lite)'],
    ['Vernacular Advisory', 'Indic-BERT + IndicTrans2', 'AGMARKNET advisories, KVK content, Bhuvan agro data', 'BLEU &gt; 30 for translation', 'Mobile + cloud hybrid'],
    ['Logistics Optimization', 'OR-Tools + Genetic Algorithm', 'GIS network, vehicle capacity, perishability, demand', '20-35% cost reduction', 'Cloud, daily route plans'],
])

H('7.4 Phase 4: Financial Inclusion Integration (Months 8-22)', 2)
P('Financial inclusion is operationalized through partnerships with regulated financial institutions, leveraging India\'s Digital Public Infrastructure (DPI) — Aadhaar, UPI, Account Aggregator, and JAM (Jan Dhan-Aadhaar-Mobile) trinity. Specific deployment streams: (i) JAN DHAN-LINKAGE for the 8-12% of producers without bank accounts, leveraging Bank Mitra Network in pilot districts; (ii) UPI-INTEGRATED PAYMENTS enabling direct producer-to-buyer settlement bypassing intermediaries; (iii) AI-SCORED WORKING-CAPITAL CREDIT through partnership with Uttarakhand Gramin Bank and Bank of Baroda, targeting INR 5 Crore disbursement to 2,000 producers in pilot period; (iv) BUNDLED INSURANCE combining PMFBY (crop), PMSBY (accident), PMJJBY (life), and weather-index micro-insurance products from Agriculture Insurance Company of India and Bharti AXA; (v) ACCOUNT AGGREGATOR INTEGRATION enabling consent-based financial data flow for credit assessment without document collection burden.')

H('7.5 Phase 5: Market Linkage &amp; Transaction Scaling (Months 10-26)', 2)
P('Market linkage operates across four channels with progressively scaling transaction volumes: (i) INSTITUTIONAL B2B channel targeting modern retail (Reliance Smart, More Retail, Spencer\'s), e-commerce grocery (BigBasket, Amazon Fresh, Blinkit), food processors (Nestl&eacute;, ITC, Tata Consumer), and hotel/hospitality (Oberoi, Taj, Marriott group sustainable-sourcing programs); (ii) DIRECT-TO-CONSUMER (D2C) e-commerce channel via PARVAT-SETU\'s own branded storefront on Shopify/Open Network for Digital Commerce (ONDC) reaching urban consumers willing to pay 30-80% premium for traceable mountain-origin products; (iii) EXPORT channel through partnership with APEDA-registered exporters and direct overseas certification (USDA Organic, Fair Trade, EU Ecolabel) for premium walnut, honey, and saffron categories; (iv) PUBLIC PROCUREMENT channel including PDS, mid-day-meal, and ICDS for traditional millets and pulses leveraging the Indian government\'s ongoing nutrition-focused procurement diversification.')
P('Three strategic cluster collection centres will be established (one per district) functioning as multi-purpose facilities: aggregation point, primary grading and packaging, cold-chain pre-cooling for perishables, and cross-docking for outbound logistics. These centres will be owned by the apex Producer Company and operated by trained SHG members, generating both employment (30-45 jobs across three centres) and infrastructure for sustained operations beyond pilot tenure.')

H('7.6 Phase 6: Impact Evaluation &amp; Scaling Documentation (Months 22-30)', 2)
P('The final phase transitions from operations into rigorous evaluation and replication preparation. Impact evaluation uses a quasi-experimental difference-in-differences design with matched control villages, supplemented by qualitative process tracing and beneficiary case studies. Endline household survey (target 2,000 households matching baseline) measures the same indicators as baseline, enabling unbiased estimation of treatment effects with proper standard errors. Platform unit economics analysis documents revenue streams, cost structure, and break-even trajectory. Replication playbook captures all technology code (open-sourced on GitHub), training curricula, governance templates, partnership protocols, and risk-mitigation frameworks in a format directly deployable in other Himalayan districts. Three to four academic publications in Q1 SCIE journals (target: World Development, Food Policy, Economic Development and Cultural Change, AI &amp; Society) document the rigorous evidence base.')
BR()
print("Section 7 added")

# ===================== SECTION 8: TECHNOLOGY ARCHITECTURE =====================
H('SECTION 8: TECHNOLOGY ARCHITECTURE', 1)
P('The PARVAT-SETU technology stack is engineered for three operational realities of the Indian Himalayan smallholder context: intermittent connectivity, low-end smartphone hardware (Android 7-9, 1-2 GB RAM, 16-32 GB storage), and predominantly low-literacy users requiring vernacular voice-and-image interfaces. The architecture combines on-device AI inference (for offline functionality), cloud-based heavy computation (for model training and global optimization), and India-DPI integration (for identity, payments, and data sharing) into a coherent, secure, and scalable platform.')

CAP('DIAGRAM 3: Five-Layer Technology Architecture')
MONO('''
================================================================================
        PARVAT-SETU FIVE-LAYER TECHNOLOGY ARCHITECTURE
================================================================================

  LAYER 5: USER INTERFACE
  +-------------------------------------------------------------+
  | * Producer Mobile App (Android-lite, vernacular)             |
  | * FPO Manager Web Dashboard (React + Next.js)                |
  | * Buyer B2B Portal (search, order, traceability)             |
  | * D2C Consumer Storefront (Shopify + ONDC)                   |
  | * Admin / Analytics Dashboard (Apache Superset)              |
  +-------------------------------------------------------------+
                             |
  LAYER 4: APPLICATION SERVICES (REST API + GraphQL)
  +-------------------------------------------------------------+
  | * Onboarding & KYC service        | * Order management       |
  | * Production listing service      | * Logistics coordination |
  | * Marketplace search & matching   | * Payment processing     |
  | * Notifications (SMS, WhatsApp)   | * Analytics & reporting  |
  +-------------------------------------------------------------+
                             |
  LAYER 3: AI/ML + GIS COMPUTE LAYER
  +-------------------------------------------------------------+
  | AI/ML stack:                    | GIS stack:                  |
  | * TensorFlow / PyTorch          | * PostgreSQL + PostGIS      |
  | * scikit-learn (XGBoost, RF)    | * QGIS (analyst use)        |
  | * Hugging Face (Indic models)   | * Mapbox / OSM (display)    |
  | * MLflow (model registry)       | * Google Earth Engine       |
  | * Apache Airflow (pipelines)    | * Google OR-Tools (logist.) |
  | * Edge: TensorFlow Lite, ONNX   |                             |
  +-------------------------------------------------------------+
                             |
  LAYER 2: DATA LAYER
  +-------------------------------------------------------------+
  | * Primary DB: PostgreSQL (transactional)                     |
  | * Spatial DB: PostgreSQL + PostGIS                           |
  | * Time-series: TimescaleDB (sensor + price data)             |
  | * Object storage: S3-compatible (images, documents)          |
  | * Search: Elasticsearch (product search)                     |
  | * Cache: Redis (session, hot data)                            |
  | * Blockchain: Hyperledger Fabric (traceability anchor)       |
  +-------------------------------------------------------------+
                             |
  LAYER 1: INFRASTRUCTURE & DPI INTEGRATION
  +-------------------------------------------------------------+
  | * Cloud: NIC Cloud / AWS Mumbai (data sovereignty)           |
  | * CDN: Cloudflare for static assets                          |
  | * DPI: Aadhaar eKYC, UPI, Account Aggregator, DigiLocker     |
  | * Telecom: SMS (Exotel/Knowlarity), WhatsApp Business API    |
  | * Maps: Bhuvan (ISRO) + OSM + Mapbox                         |
  | * Compliance: ISO 27001, DPDP Act 2023, NDHM principles      |
  +-------------------------------------------------------------+
''')

H('8.1 Mobile Application: Producer-Facing Interface', 2)
P('The producer-facing mobile application is engineered as the most critical user interface in the system, recognizing that 95%+ of producer interactions will occur through this channel. Design principles: (i) ANDROID-LITE BUILD targeting installed size below 15 MB and operational on Android 7+ devices with 1 GB RAM (enabling deployment on the majority of available rural smartphones); (ii) OFFLINE-FIRST ARCHITECTURE allowing producers to record listings, capture quality grading photos, and queue actions without internet connectivity, with automatic sync when connectivity is restored; (iii) VERNACULAR LANGUAGE SUPPORT in Hindi, Garhwali, and Kumaoni with voice-input/output for low-literacy users using Indic-BERT and IndicTrans2 transformer models; (iv) IMAGE-FIRST INTERFACE minimizing text dependence through photo-based listing capture, quality assessment, and order confirmation; (v) BIOMETRIC AUTHENTICATION via Aadhaar fingerprint integration for high-trust transactions. Core feature modules: dashboard (today\'s prices, weather, advisories), listing management (create, edit, photograph produce listings), order management (incoming orders, delivery scheduling), wallet (balance, transactions, withdrawals), credit (eligibility, applications, repayments), insurance (active policies, claims), and learning (vernacular video tutorials).')

H('8.2 AI/ML Production Stack', 2)
P('All AI/ML models follow a unified MLOps pipeline architected around MLflow (model registry and experiment tracking), Apache Airflow (data pipeline orchestration), and Kubeflow (training-serving infrastructure). Models are trained in cloud Jupyter environments, registered with metadata (training data version, hyperparameters, performance metrics), deployed to staging endpoints for shadow testing, A/B tested against production baselines, and only promoted to full production on demonstrated improvement. Continuous monitoring tracks model drift via population stability index (PSI) and prediction distribution analysis, automatically triggering retraining when drift exceeds thresholds. Edge deployment for quality grading and offline advisory uses ONNX Runtime and TensorFlow Lite, achieving inference latency below 200 ms on target hardware.')

H('8.3 GIS Production Stack', 2)
P('The GIS stack combines PostgreSQL+PostGIS as the spatial database backbone, QGIS for analyst workflows, Google Earth Engine for satellite imagery analysis at scale (NDVI time-series, crop classification, moisture indices), Mapbox for end-user map rendering, and Google OR-Tools for routing optimization. Core spatial datasets ingested: Census 2011 village boundaries, Bhuvan land-use/land-cover (ISRO), SRTM 30m DEM and ALOS PALSAR 12.5m DEM for terrain analysis, ICAR-NBSSLUP soil database, IMD historical and forecast weather grids, mandi locations from AGMARKNET, and project-collected producer location points. Derived analytical layers: agro-ecological zonation (productivity potential by crop), climate-risk overlay (flood/landslide/drought susceptibility), infrastructure connectivity index (distance-weighted access to mandis/cold storage), and logistics optimization meshes for routing.')

H('8.4 Blockchain Traceability Layer', 2)
P('Hyperledger Fabric provides the blockchain anchor for end-to-end traceability — critical for premium-market positioning. Each transaction (harvest event, quality grading, transit step, buyer receipt) generates a cryptographically signed record on a permissioned blockchain. Consumers scanning QR codes on retail packaging access the complete provenance: producer identity (with privacy controls), GPS-verified harvest location, quality certification timestamps, transit chain, and any organic/fair-trade certifications. This traceability layer enables 30-80% price premium capture for verified mountain-origin products, providing the economic incentive that converts blockchain from technology novelty into operational value driver.')

H('8.5 India Digital Public Infrastructure (DPI) Integration', 2)
P('PARVAT-SETU systematically leverages every relevant DPI building block, recognizing that India\'s DPI is the single largest competitive advantage available for digital platforms operating at smallholder scale. Integrations: (i) AADHAAR eKYC for paperless onboarding (cost reduction from INR 80-150 per onboarding to INR 5); (ii) UPI for instant settlement enabling cash-flow improvements that directly reduce smallholder distress sales; (iii) ACCOUNT AGGREGATOR for consent-based financial data flow enabling AI credit scoring without document burden; (iv) DIGILOCKER for verified document storage; (v) ONDC (Open Network for Digital Commerce) for D2C consumer reach without dependence on private platforms; (vi) AGRI STACK for crop registry and government scheme convergence. This DPI-native architecture ensures that PARVAT-SETU benefits from continuous infrastructure improvements at zero marginal cost rather than building parallel systems.')
BR()
print("Section 8 added")

# ===================== SECTION 9: SOCIAL ENTERPRISE MODEL =====================
H('SECTION 9: SOCIAL ENTERPRISE GOVERNANCE AND OWNERSHIP MODEL', 1)
P('PARVAT-SETU\'s governance architecture deliberately implements a producer-owned cooperative social enterprise structure, drawing from validated Indian precedents (Amul, SEWA, Kudumbashree) while adapting them for the digital-platform era. The architecture is engineered to align all incentives — economic, governance, and developmental — toward producer welfare, while maintaining operational efficiency comparable to private platforms.')

CAP('DIAGRAM 4: Three-Tier Cooperative Governance Structure')
MONO('''
================================================================================
            THREE-TIER COOPERATIVE GOVERNANCE STRUCTURE
================================================================================

  +----------------------------------------------------------+
  |  TIER 3: PARVAT-SETU PRODUCER COMPANY (Apex)              |
  |  ----------------------------------------------------    |
  |  * Registered under Producer Companies Act 2013          |
  |  * Board: 12 elected directors (1 per FPO)               |
  |  * 35% women on board (mandatory)                         |
  |  * Authorized share capital: INR 5 Crore                  |
  |  * Functions: tech platform, branding, B2B contracts,    |
  |    export coordination, working-capital revolving fund   |
  +-------------------------+--------------------------------+
                            ^
                            | Aggregation
                            |
  +----------------------------------------------------------+
  |  TIER 2: 12 CLUSTER-LEVEL FEDERATIONS                     |
  |  ----------------------------------------------------    |
  |  * One per FPO (existing or newly formed)                |
  |  * 10-15 SHGs per FPO                                     |
  |  * Local governance committee                             |
  |  * Functions: aggregation, primary grading, training,    |
  |    cluster collection centre operations                  |
  +-------------------------+--------------------------------+
                            ^
                            | Aggregation
                            |
  +----------------------------------------------------------+
  |  TIER 1: 150 SHGS (SELF-HELP GROUPS)                      |
  |  ----------------------------------------------------    |
  |  * 15-25 producers per SHG (avg 33 producers)            |
  |  * Existing SHGs leveraged (NRLM Ajeevika network)       |
  |  * Women-led: 60% target compliance                       |
  |  * Functions: peer support, savings/credit, last-mile    |
  |    onboarding, quality assurance                          |
  +----------------------------------------------------------+
''')

H('9.1 Revenue Model and Pathway to Sustainability', 2)
P('PARVAT-SETU is designed to achieve operational financial sustainability — covering all operating costs from earned revenue without permanent grant dependency — within 36 months of pilot completion (i.e., by Month 66 from project start). The pathway combines multiple complementary revenue streams calibrated to grow with platform transaction volume:')
B('<b>Stream 1 &mdash; Transaction Commissions (3-5%):</b> Charged on platform-mediated B2B and D2C transactions. At target Year 5 transaction volume of INR 250 Crore, this generates INR 7.5-12.5 Crore annual revenue.')
B('<b>Stream 2 &mdash; Value-Added Processing Margins (15-25%):</b> Cleaning, grading, packaging, branded retailing of select premium products (millets, walnuts, honey). At Year 5 processed-product turnover of INR 60 Crore, this generates INR 9-15 Crore annual margin.')
B('<b>Stream 3 &mdash; Institutional Buyer Subscriptions (INR 25K-1L per buyer/year):</b> Tiered subscription for guaranteed-volume contracts, traceability access, and direct producer connection. Target 200 institutional subscribers by Year 5 generating INR 1.5-3 Crore.')
B('<b>Stream 4 &mdash; Financial Services Revenue Sharing (1-2% of credit volume):</b> Negotiated revenue share with banking partners on AI-scored credit disbursements. At Year 5 credit volume INR 50 Crore, this generates INR 50 lakh - 1 Crore.')
B('<b>Stream 5 &mdash; Data Services for Insurance &amp; Government:</b> Aggregated, anonymized agricultural intelligence sold to insurance companies (for crop insurance pricing) and government departments (for policy planning). Target Year 5 revenue INR 50 lakh - 1.5 Crore.')

P('Aggregate target Year 5 revenue: INR 19-32 Crore against estimated Year 5 operating cost of INR 12-15 Crore — yielding 30-55% operating margin. This margin is structurally retained within the producer cooperative, reinvested in: (i) producer welfare programmes (insurance subsidy, education stipends); (ii) technology improvement (AI model expansion, infrastructure scaling); (iii) geographic expansion to additional Himalayan districts; (iv) member dividends declared annually based on transaction patronage. Critically, NO EXTERNAL EQUITY INVESTORS receive returns from this surplus — distinguishing PARVAT-SETU from VC-backed agriculture-tech ventures and ensuring that platform value creation remains within the smallholder community that generates it.')

# ===================== SECTION 10: ECONOMIC FEASIBILITY =====================
H('SECTION 10: ECONOMIC FEASIBILITY AND VIABILITY ANALYSIS', 1)

H('10.1 Five-Year Financial Projection', 2)
CAP('TABLE 10.1: Projected Income Statement (INR Lakh)')
TBL(['Line Item', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'], [
    ['REVENUE', '', '', '', '', ''],
    ['Transaction commissions (3-5%)', '15', '95', '380', '720', '1,050'],
    ['Value-added processing margin', '0', '50', '290', '720', '1,200'],
    ['Buyer subscriptions', '5', '25', '90', '180', '250'],
    ['Financial services share', '0', '15', '45', '70', '90'],
    ['Data services', '0', '0', '20', '50', '110'],
    ['<b>Total Revenue</b>', '<b>20</b>', '<b>185</b>', '<b>825</b>', '<b>1,740</b>', '<b>2,700</b>'],
    ['', '', '', '', '', ''],
    ['OPERATING COSTS', '', '', '', '', ''],
    ['Personnel', '85', '180', '320', '480', '620'],
    ['Technology infrastructure', '40', '60', '85', '110', '135'],
    ['Marketing &amp; partnerships', '25', '50', '90', '140', '180'],
    ['Logistics &amp; cold chain', '15', '60', '180', '320', '420'],
    ['Cost of goods (processing)', '0', '40', '230', '575', '960'],
    ['Compliance, audit, legal', '10', '15', '25', '40', '55'],
    ['Member welfare programmes', '0', '20', '50', '95', '140'],
    ['<b>Total Operating Cost</b>', '<b>175</b>', '<b>425</b>', '<b>980</b>', '<b>1,760</b>', '<b>2,510</b>'],
    ['', '', '', '', '', ''],
    ['<b>OPERATING SURPLUS / (DEFICIT)</b>', '<b>(155)</b>', '<b>(240)</b>', '<b>(155)</b>', '<b>(20)</b>', '<b>+190</b>'],
    ['Cumulative cash flow (with grant)', '+30', '+50', '+80', '+90', '+280'],
])

P('The financial projection demonstrates the path to operational break-even, with operating surplus turning positive in Year 5 (Month 60), and cumulative cash position remaining positive throughout the projection period when grant inflows are incorporated. The pilot grant of INR 1.85 Crore plus follow-on Year 4-5 catalytic financing (estimated INR 2-3 Crore) covers the period of negative operating surplus, after which the platform sustains itself indefinitely on operational revenue.')

H('10.2 Break-Even Analysis', 2)
P('Break-even analysis at the unit-economics level reveals the platform achieves positive unit contribution from the first transaction onward. Per-transaction analysis: average transaction size INR 8,000, platform commission 4% = INR 320 revenue; variable transaction cost (payment gateway, logistics coordination, customer support) INR 95 = INR 225 unit contribution. Platform operating leverage emerges as transaction volume scales — fixed costs (technology infrastructure, core team) are amortized across growing transaction volumes. Aggregate break-even occurs at approximately INR 18-22 Crore annual transaction volume, projected to be reached in Year 4 of operations.')

H('10.3 Sensitivity Analysis', 2)
CAP('TABLE 10.2: Sensitivity Analysis &mdash; Year 5 Operating Surplus (INR Lakh)')
TBL(['Scenario', 'Producer Adoption Rate', 'Avg Transaction Volume', 'Year 5 Surplus', 'IRR'], [
    ['Pessimistic', '60% (3,000 active)', 'INR 150 Cr', '+45 lakh', '11%'],
    ['Base Case', '80% (4,000 active)', 'INR 250 Cr', '+190 lakh', '24%'],
    ['Optimistic', '95% (4,750 active)', 'INR 380 Cr', '+420 lakh', '38%'],
])

H('10.4 Return on Investment for Funders', 2)
P('From the funder perspective, PARVAT-SETU delivers extraordinary social return on investment. The grant investment of INR 1.85 Crore enables direct income increase of approximately INR 15-25 Crore annually for 5,000 households (35-50% increase on baseline median INR 1.2 lakh annual household income across 5,000 HH = INR 21 Crore baseline; 40% increase = INR 8.4 Crore annual income gain in conservative case, scaling to INR 15-20 Crore as platform fully matures by Year 5). On a Net Present Value basis at 8% social discount rate over 10 years, the income-uplift social return on investment ratio exceeds 60:1, before accounting for non-monetary co-benefits (gender empowerment, climate resilience, food sovereignty, biodiversity preservation through diversified production systems).')
BR()
print("Sections 9-10 added")

# ===================== SECTION 11: ECONOMIC UPLIFT MECHANISMS =====================
H('SECTION 11: ECONOMIC UPLIFT MECHANISMS &mdash; HOW INCOME ACTUALLY RISES', 1)
P('A persistent shortcoming of agricultural development projects is the failure to articulate the precise mechanisms by which producer incomes actually rise. PARVAT-SETU is structured around five explicit income-uplift mechanisms, each independently measurable and collectively additive.')

CAP('TABLE 11.1: Five Income-Uplift Mechanisms with Quantification')
TBL(['Mechanism', 'Causal Pathway', 'Expected Income Lift', 'Measurement Method'], [
    ['M1: Margin Capture', 'Eliminate 2-4 intermediaries between producer and end-buyer; capture margin differential', '+15-25% revenue', 'Compare farm-gate prices realized via platform vs control villages'],
    ['M2: Demand-Driven Crop Selection', 'AI-driven advisory shifts producers toward higher-value crops matching projected demand', '+10-15% revenue', 'Cropping pattern shift analysis pre/post platform'],
    ['M3: Premium-Market Access', 'Traceability + certification enables organic / single-origin / fair-trade premium pricing', '+25-40% on premium-channel sales', 'Price differential analysis by sales channel'],
    ['M4: Loss Reduction', 'Demand forecasting + cold chain reduces post-harvest loss', '+8-12% effective revenue', 'Loss audit pre-platform vs platform-mediated transactions'],
    ['M5: Cost Reduction', 'GIS-optimized logistics reduces per-unit transport cost; bulk input procurement reduces input cost', '-5-10% on cost base', 'Per-unit cost tracking via platform records'],
    ['<b>AGGREGATE</b>', '<b>Combined effect</b>', '<b>+35-50% net income</b>', '<b>Diff-in-Diff household survey</b>'],
])

H('11.1 Mechanism 1 &mdash; Margin Capture (Most Significant)', 2)
P('The single largest income-uplift mechanism is the elimination of intermediary margins. Current value chains for typical Garhwal smallholder produce involve 3-5 intermediary layers each capturing 8-25% margin, cumulating to 70-85% total margin extraction. PARVAT-SETU\'s direct producer-to-buyer architecture eliminates village commission agents (8-12% margin), district mandi traders (10-15% margin), and primary wholesalers (12-18% margin), enabling producers to capture this margin differential directly. Conservative modelling assumes only 50% of eliminated intermediary margin flows to producers (with 30-40% absorbed in platform commission and logistics, and 10-20% passed to buyers as price reduction enabling demand expansion), still yielding 15-25% revenue uplift on platform-mediated sales.')

H('11.2 Mechanism 2 &mdash; Demand-Driven Crop Selection', 2)
P('AI-driven advisory enables producers to shift from production-driven cropping (growing what is traditional or what fits local agronomy) toward demand-driven cropping (growing what specific buyers want, when they want it, at quality grades they will premium-price). The platform provides 6-month-ahead demand forecasts at district granularity, enabling producers to plan rabi or kharif sowing decisions with significantly better information than the price-volatile commodity-market signals they currently rely on. Empirical evidence from Microsoft AI Sowing App and similar interventions documents 10-15% revenue uplift purely from improved sowing decisions.')

H('11.3 Mechanism 3 &mdash; Premium-Market Access', 2)
P('Mountain-origin produce — apples, walnuts, kiwis, traditional millets, single-origin honey, medicinal herbs — commands 200-500% premium prices in metropolitan and export markets when properly certified, traced, and marketed. Smallholders currently cannot access these premium markets because they individually cannot meet certification requirements (organic certification costs INR 25,000-1 lakh per producer, prohibitive at smallholder scale), traceability requirements (no infrastructure for chain-of-custody documentation), or volume requirements (institutional buyers require committed weekly volumes). PARVAT-SETU solves all three: aggregating producers under group certification (reducing per-producer cost to INR 500-2,000), providing blockchain traceability automatically, and aggregating volume to meet institutional thresholds. Conservative modelling assumes that 40-60% of producer output channels through premium markets at 30-50% price premium over commodity-grade pricing, yielding 25-40% revenue uplift on the premium-channeled portion.')

H('11.4 Mechanism 4 &mdash; Post-Harvest Loss Reduction', 2)
P('Post-harvest losses for Garhwal perishables (apples, off-season vegetables, pears) currently average 28-40% by value, primarily due to delayed market access caused by transport disruptions, mismatched harvest-to-demand timing, and absence of cold-chain infrastructure. PARVAT-SETU reduces losses through three complementary channels: (i) DEMAND-SIDE COORDINATION via AI matching ensures that harvested produce is pre-sold before harvest with logistics pre-scheduled; (ii) COLD-CHAIN INFRASTRUCTURE at three cluster collection centres extends shelf life by 5-15 days for perishables; (iii) PROCESSING DIVERSION channels surplus production into value-added processing (dried/dehydrated/packaged) rather than allowing spoilage. Combined effect: post-harvest losses reduced from 30% baseline to 15-20% post-platform, equivalent to 10-15% effective revenue increase.')

H('11.5 Mechanism 5 &mdash; Cost Reduction', 2)
P('On the cost side, PARVAT-SETU enables 5-10% reduction in producer cost base through: (i) BULK INPUT PROCUREMENT for fertilizers, seeds, and packaging materials at 8-15% discount versus retail prices; (ii) GIS-OPTIMIZED LOGISTICS reducing per-unit transport cost by 30-45% through consolidated routing and back-haul utilization; (iii) FINANCIAL COST REDUCTION as formal credit at 9-12% interest replaces moneylender credit at 36-60%. While individually modest, these cost reductions compound across the production cycle and yield meaningful net-income enhancement.')

# ===================== SECTION 12: SUSTAINABILITY FRAMEWORK =====================
H('SECTION 12: SUSTAINABILITY FRAMEWORK', 1)
P('PARVAT-SETU\'s sustainability is engineered across four interconnected dimensions, each with explicit metrics and operational mechanisms.')

H('12.1 Environmental Sustainability', 2)
P('The platform actively promotes regenerative and climate-resilient agricultural practices through its advisory and incentive systems. (i) AGROECOLOGICAL CROP SELECTION: AI advisory prioritizes crops matching local agro-ecological zones, reducing input requirements and water dependence. (ii) ORGANIC TRANSITION SUPPORT: Group organic certification, premium market connection, and 3-year transition subsidies via PKVY convergence enable economically viable conversion from chemical-input agriculture. (iii) BIODIVERSITY PROMOTION: Premium pricing for traditional varieties (heritage millets, native vegetables, indigenous fruits) creates economic incentive for biodiversity conservation. (iv) CARBON CREDITS: Future integration with voluntary carbon markets (Verra, Gold Standard) for agroforestry and regenerative practices generates additional producer income while sequestering carbon. Target: 50% of participating producers transition to certified organic or natural farming by Year 5.')

H('12.2 Economic Sustainability', 2)
P('Operational financial sustainability is achieved through the diversified revenue model documented in Section 9.1, reaching break-even by Year 5 with 30-55% operating margin thereafter. Critically, NO EXTERNAL EQUITY DEPENDENCE exists in this model — surplus is retained within the producer cooperative for reinvestment, member welfare, and dividend distribution. This structural independence from venture capital cycles and grant renewal cycles provides resilience against external funding volatility that has destroyed many promising rural-development initiatives.')

H('12.3 Social Sustainability', 2)
P('Producer ownership ensures social sustainability by aligning governance authority with the population whose welfare the platform serves. Three-tier cooperative governance with mandatory women representation (35% on apex board, 60% participation across SHGs) institutionalizes inclusion. Annual general meetings, transparent financial reporting, and open audit of platform performance metrics build accountability. Grievance redressal protocols at SHG, cluster, and apex levels with documented response timelines ensure issues are addressed before escalating into systemic problems. Member education programmes on cooperative principles, financial literacy, and digital skills build the human capital necessary for self-governance over time.')

H('12.4 Institutional Sustainability', 2)
P('Multi-level institutional partnerships ensure that PARVAT-SETU is embedded within rather than parallel to existing rural development infrastructure. Partnerships: (i) UTTARAKHAND LIVELIHOODS MISSION (REAP) for SHG mobilization and convergence; (ii) NABARD for FPO ecosystem support and credit linkage; (iii) ICAR-NBSSLUP for agro-ecological zonation data; (iv) IMD for weather forecast integration; (v) UTTARAKHAND HORTICULTURE BOARD for market intelligence; (vi) KRISHI VIGYAN KENDRAS (KVKs) for extension and technology transfer; (vii) BANKING PARTNERS (Uttarakhand Gramin Bank, Bank of Baroda, NABARD-RIDF) for financial inclusion services. These embedded partnerships ensure that PARVAT-SETU continues operations with institutional support beyond the pilot grant period.')
BR()
print("Sections 11-12 added")

# ===================== SECTION 13: IMPLEMENTATION TIMELINE =====================
H('SECTION 13: IMPLEMENTATION PLAN AND GANTT CHART', 1)
CAP('DIAGRAM 5: 30-Month Implementation Gantt Chart')
MONO('''
================================================================================
                  PARVAT-SETU 30-MONTH GANTT CHART
================================================================================

ACTIVITY                          M1-3 M4-6 M7-9 M10-12 M13-15 M16-18 M19-21 M22-24 M25-27 M28-30
==============================================================================================

A. INCEPTION & MOBILIZATION
  A1. Team recruitment            ###
  A2. SDMA / FPO MoUs              ### ###
  A3. Baseline GIS mapping         ### ###
  A4. Baseline household survey         ### ###

B. TECHNOLOGY DEVELOPMENT
  B1. Mobile app dev (Phase 1)         ### ###
  B2. Backend API + DB setup           ### ###
  B3. AI model training                 ### ### ###
  B4. GIS layer integration                  ### ###
  B5. Blockchain traceability                      ###

C. PRODUCER ONBOARDING
  C1. SHG mobilization camps           ### ### ###
  C2. KYC + bank linkage                    ### ### ###
  C3. Production listing capture                  ### ### ###
  C4. Vernacular training                          ### ### ### ###

D. FINANCIAL INCLUSION
  D1. Banking partnerships              ###
  D2. Insurance partnerships            ###
  D3. Credit deployment                              ### ### ### ### ### ###
  D4. Insurance enrollment                                ### ### ### ###

E. MARKET LINKAGE & TRANSACTIONS
  E1. Buyer onboarding (B2B)                             ### ### ### ###
  E2. Cold-chain centres setup                ### ###
  E3. Cold-chain operations                           ### ### ### ### ### ###
  E4. D2C platform launch                                            ### ###
  E5. Transaction scaling                                 ### ### ### ### ### ###
  E6. Export certification                                             ### ###

F. M&E AND DOCUMENTATION
  F1. Quarterly progress reviews   ... ... ... ... ... ... ... ... ... ...
  F2. Mid-term evaluation                                  *(M15)
  F3. Endline survey                                                 ###
  F4. DiD impact analysis                                                ### ###
  F5. Replication playbook                                                    ###
  F6. Academic papers (3-4)                                              ### ### ### ###

  Legend: ### Active execution    ... Continuous/background    * Milestone
  TOTAL DURATION: 30 MONTHS (Fast-Track Pilot)
''')

# ===================== SECTION 14: STAKEHOLDER ENGAGEMENT =====================
H('SECTION 14: STAKEHOLDER MAPPING AND ENGAGEMENT PLAN', 1)
CAP('TABLE 14.1: Comprehensive Stakeholder Engagement Matrix')
TBL(['Stakeholder', 'Role / Interest', 'Influence', 'Engagement Strategy', 'Frequency'], [
    ['Smallholder Producers', 'Direct beneficiaries, platform users', 'High', 'SHG meetings, training camps, vernacular outreach', 'Weekly during onboarding, monthly thereafter'],
    ['Self-Help Groups (SHGs)', 'Mobilization channel, peer support', 'High', 'Federation meetings, cluster events', 'Monthly'],
    ['Farmer Producer Organizations (FPOs)', 'Mid-tier governance, aggregation', 'High', 'Board meetings, joint planning', 'Bi-monthly'],
    ['Uttarakhand Livelihoods Mission (REAP)', 'SHG ecosystem partner', 'High', 'Formal MoU, joint reviews', 'Quarterly'],
    ['NABARD', 'FPO support, credit linkage', 'High', 'Quarterly liaison, FPO co-funding', 'Quarterly'],
    ['Uttarakhand Gramin Bank', 'Banking partner, credit', 'High', 'Joint product development, credit reviews', 'Monthly'],
    ['Agriculture Insurance Co.', 'Crop insurance partner', 'Medium', 'Product design, claims SLA', 'Quarterly'],
    ['Uttarakhand Horticulture Board', 'Market intelligence', 'Medium', 'Data sharing, joint advisories', 'Monthly'],
    ['Krishi Vigyan Kendras', 'Extension, training', 'Medium', 'Co-delivered training, content development', 'Monthly'],
    ['District Magistrates (3 districts)', 'Administrative facilitation', 'High', 'Briefings, formal endorsements', 'Bi-annual'],
    ['Modern Retail Buyers', 'Demand-side, premium market', 'High', 'B2B portal onboarding, contract negotiations', 'Continuous'],
    ['Food Processors (FMCG)', 'Bulk buyers, value-added', 'High', 'Sourcing partnerships, traceability', 'Continuous'],
    ['D2C Consumers', 'Direct buyers, premium pricing', 'Medium', 'Marketing campaigns, ONDC integration', 'Continuous'],
    ['Export Buyers', 'Premium-segment demand', 'Medium', 'APEDA partnerships, trade fairs', 'Bi-annual'],
    ['Funder (NABARD/NITI/Foundation)', 'Grant provider, oversight', 'High', 'Quarterly progress reports, annual reviews', 'Quarterly'],
    ['Media (regional + national)', 'Awareness, advocacy', 'Medium', 'Press releases, success stories', 'Major milestones'],
    ['Academic Community', 'Knowledge exchange, validation', 'Low-Medium', 'Conference presentations, publications', 'Annual'],
    ['Other Himalayan FPOs', 'Replication audience', 'Low (initially)', 'Documentation sharing, study tours', 'Y2 onwards'],
])

# ===================== SECTION 15: RISK MANAGEMENT =====================
H('SECTION 15: COMPREHENSIVE RISK MANAGEMENT FRAMEWORK', 1)
CAP('TABLE 15.1: Risk Register with Mitigation Strategies')
TBL(['ID', 'Risk', 'P', 'I', 'Score', 'Mitigation Strategy'], [
    ['R1', 'Producer adoption below target', '3', '5', '15', 'Intensive on-ground mobilization; SHG-led peer onboarding; smartphone subsidy; vernacular UX testing'],
    ['R2', 'AI model accuracy below specification', '2', '4', '8', 'Multiple model architectures benchmarked; continuous retraining; expert validation panels'],
    ['R3', 'Connectivity / data unavailability', '4', '3', '12', 'Offline-first app architecture; LoRa fallback in core areas; SMS-based core functions'],
    ['R4', 'Banking partner reluctance to lend', '3', '4', '12', 'Multiple bank partnerships; AI scoring with human override; first-loss guarantee fund'],
    ['R5', 'Buyer-side commitment volatility', '3', '4', '12', 'Diversify across 50+ buyers; long-term contracts where feasible; D2C channel as buffer'],
    ['R6', 'Cold-chain logistics breakdown', '2', '4', '8', 'Maintenance contracts; backup generators; alternative-route planning'],
    ['R7', 'Currency/inflation impact on costs', '3', '2', '6', 'Annual budget revisions; bulk procurement to lock prices'],
    ['R8', 'Climate disasters disrupt operations', '4', '5', '20', 'Integrated insurance; emergency credit; alternative-route logistics; resilient cold chain'],
    ['R9', 'Political / regulatory changes', '2', '4', '8', 'Multi-state replication strategy; alignment with multiple government schemes; legal counsel'],
    ['R10', 'Data privacy / cybersecurity breach', '2', '5', '10', 'ISO 27001 compliance; DPDP Act 2023; encryption-at-rest/in-transit; security audits'],
    ['R11', 'Producer trust erosion (any failure)', '3', '5', '15', 'Transparent communication; rapid grievance redressal; community ombudsperson; over-deliver early'],
    ['R12', 'Competition from for-profit platforms', '3', '3', '9', 'Cooperative ownership as differentiator; superior gender focus; institutional partnerships'],
    ['R13', 'Team turnover (key personnel)', '3', '4', '12', 'Documentation protocols; cross-training; competitive retention; succession planning'],
    ['R14', 'Slower-than-projected revenue ramp', '3', '4', '12', 'Conservative budgeting; phased cost expansion; bridge funding identified pre-emptively'],
    ['R15', 'Geographic constraint (remote villages)', '4', '3', '12', 'Hub-and-spoke logistics; mobile collection vans; cluster-collection-centre strategy'],
])
P('Top 5 Critical Risks (Score &ge; 12) receive dedicated mitigation playbooks documented in the project risk management manual, with quarterly review cycles by the project Steering Committee. Each high-risk item has an assigned owner, defined trigger metrics, and pre-approved contingency budgets.')
BR()
print("Sections 13-15 added")

# ===================== SECTION 16: M&E FRAMEWORK =====================
H('SECTION 16: MONITORING, EVALUATION AND LEARNING FRAMEWORK', 1)
P('PARVAT-SETU implements a rigorous Monitoring, Evaluation, and Learning (MEL) framework combining real-time platform analytics (automatic capture of all transactions, user behavior, and outcome metrics) with periodic structured surveys (baseline, midline, endline) and qualitative process tracing. The framework is designed to satisfy three audiences: (i) operational management requiring real-time decision-support metrics; (ii) funders requiring quarterly progress reporting against contracted targets; (iii) academic and policy audiences requiring rigorous causal-attribution evidence of platform effects.')

CAP('TABLE 16.1: Outcome Indicators and Monitoring Methods')
TBL(['Indicator', 'Baseline', 'Y1 Target', 'Y2 Target', 'M30 Target', 'Method'], [
    ['Producers enrolled', '0', '2,000', '4,000', '5,000', 'Platform records'],
    ['Active monthly users (% of enrolled)', 'N/A', '40%', '65%', '80%', 'Platform analytics'],
    ['Average net income / household / yr', 'INR 1.2 L', '+15%', '+30%', '+40%', 'Diff-in-Diff survey'],
    ['Post-harvest losses (%)', '30%', '25%', '20%', '17%', 'Loss audit'],
    ['Bank account ownership (%)', '88%', '95%', '99%', '100%', 'KYC records'],
    ['Insurance coverage (%)', '14%', '50%', '80%', '100%', 'Insurance partner'],
    ['Working-capital credit access (%)', '33%', '50%', '70%', '85%', 'Bank records'],
    ['Women on platform (%)', '0', '50%', '58%', '60%+', 'Demographic data'],
    ['SC/ST participation (%)', '0', '30%', '33%', '35%+', 'Demographic data'],
    ['Aggregate transaction volume (INR Cr)', '0', '15', '95', '180', 'Platform records'],
    ['Cumulative credit disbursed (INR Cr)', '0', '0.5', '2.5', '5', 'Bank records'],
    ['Premium-channel share (%)', '0', '15%', '35%', '50%', 'Channel analytics'],
    ['Operational sustainability ratio', 'N/A', '11%', '44%', '85%', 'Financial reports'],
])

H('16.1 Impact Evaluation Methodology', 2)
P('The pilot uses a quasi-experimental difference-in-differences (DiD) design with matched control villages selected through propensity-score matching on baseline characteristics. Treatment group: 50 villages with active platform engagement. Control group: 50 matched villages with similar baseline demographics, agro-ecology, and infrastructure but no platform deployment. Baseline survey (Month 1-4): 2,000 households (1,000 treatment-area + 1,000 control). Endline survey (Month 27-30): same 2,000 households resurveyed using identical instruments. DiD estimator measures the causal effect of platform exposure on income, financial inclusion, and well-being indicators by comparing the change in treatment group to the change in control group. Standard errors clustered at village level account for spatial correlation. Robustness checks include placebo tests (treatment-equivalent outcomes that should not differ), heterogeneous treatment effects analysis (gender, caste, landholding), and instrumental-variable robustness checks.')

H('16.2 Real-Time Platform Analytics', 2)
P('Beyond the periodic survey-based evaluation, the platform automatically captures comprehensive operational metrics through Apache Superset dashboards: transaction volume, average ticket size, channel mix, geographic distribution, producer-level engagement scores, AI model performance metrics, credit portfolio quality, insurance claims experience, customer-support ticket volumes, and grievance-redressal time-to-resolution. These dashboards are accessible to project management (real-time), Steering Committee (quarterly summaries), and funders (quarterly portal access) — providing transparent, continuous accountability that no traditional development project achieves.')

# ===================== SECTION 17: BUDGET =====================
H('SECTION 17: DETAILED PROJECT BUDGET', 1)
CAP('TABLE 17.1: Comprehensive Budget Matrix &mdash; INR 1,85,00,000 over 30 Months')
TBL(['Code', 'Item', 'Amount (INR)', 'Year 1', 'Year 2', 'Year 3 (6mo)'], [
    ['A', 'TECHNOLOGY DEVELOPMENT &amp; INFRASTRUCTURE', '38,00,000', '20,00,000', '12,00,000', '6,00,000'],
    ['A1', 'Mobile app development (Android-lite)', '8,00,000', '6,00,000', '1,50,000', '50,000'],
    ['A2', 'Backend infrastructure (cloud, API)', '6,00,000', '3,00,000', '2,00,000', '1,00,000'],
    ['A3', 'AI/ML model development & training', '10,00,000', '5,00,000', '3,50,000', '1,50,000'],
    ['A4', 'GIS layer integration & data', '5,00,000', '3,00,000', '1,50,000', '50,000'],
    ['A5', 'Blockchain (Hyperledger setup)', '4,00,000', '2,00,000', '1,50,000', '50,000'],
    ['A6', 'Cybersecurity, audit, compliance', '5,00,000', '1,00,000', '2,00,000', '2,00,000'],
    ['B', 'HUMAN RESOURCES (TEAM)', '70,00,000', '24,00,000', '30,00,000', '16,00,000'],
    ['B1', 'PI honorarium (Dr. Nidhi Rawat)', '7,20,000', '2,40,000', '2,40,000', '2,40,000'],
    ['B2', 'Co-PI / Scholar (Raj Amritam, INR 35K/mo)', '10,50,000', '4,20,000', '4,20,000', '2,10,000'],
    ['B3', 'Tech Lead (full-time, 30 mo)', '18,00,000', '7,20,000', '7,20,000', '3,60,000'],
    ['B4', 'AI/ML Engineer (full-time)', '12,00,000', '4,80,000', '4,80,000', '2,40,000'],
    ['B5', 'GIS Specialist (full-time)', '9,00,000', '3,60,000', '3,60,000', '1,80,000'],
    ['B6', 'Field Coordinators (3, INR 25K/mo)', '13,30,000', '4,80,000', '6,00,000', '2,50,000'],
    ['C', 'COMMUNITY MOBILIZATION & TRAINING', '20,00,000', '8,00,000', '8,00,000', '4,00,000'],
    ['C1', 'SHG mobilization camps (50 villages)', '6,00,000', '3,00,000', '2,00,000', '1,00,000'],
    ['C2', 'Vernacular content development', '4,00,000', '2,50,000', '1,00,000', '50,000'],
    ['C3', 'Producer training programs', '6,00,000', '1,50,000', '3,00,000', '1,50,000'],
    ['C4', 'SHG honoraria & incentives', '4,00,000', '1,00,000', '2,00,000', '1,00,000'],
    ['D', 'MARKET INFRASTRUCTURE', '32,00,000', '5,00,000', '20,00,000', '7,00,000'],
    ['D1', 'Cluster collection centres (3)', '18,00,000', '3,00,000', '12,00,000', '3,00,000'],
    ['D2', 'Cold-chain equipment', '9,00,000', '0', '7,00,000', '2,00,000'],
    ['D3', 'Logistics setup & vehicles', '5,00,000', '2,00,000', '1,00,000', '2,00,000'],
    ['E', 'FINANCIAL SERVICES SETUP', '8,00,000', '3,00,000', '4,00,000', '1,00,000'],
    ['E1', 'Bank partnership setup costs', '2,00,000', '1,00,000', '50,000', '50,000'],
    ['E2', 'Credit guarantee / first-loss fund', '5,00,000', '1,50,000', '3,00,000', '50,000'],
    ['E3', 'Insurance product co-design', '1,00,000', '50,000', '50,000', '0'],
    ['F', 'M&amp;E AND RESEARCH', '8,00,000', '3,00,000', '2,50,000', '2,50,000'],
    ['F1', 'Baseline survey (2,000 HH)', '2,50,000', '2,50,000', '0', '0'],
    ['F2', 'Mid-line evaluation', '1,50,000', '0', '1,50,000', '0'],
    ['F3', 'Endline survey + DiD', '2,50,000', '0', '0', '2,50,000'],
    ['F4', 'Publications & dissemination', '1,50,000', '50,000', '1,00,000', '0'],
    ['G', 'TRAVEL, OVERHEADS & CONTINGENCY', '9,00,000', '3,00,000', '4,00,000', '2,00,000'],
    ['G1', 'In-state field travel', '4,00,000', '1,50,000', '1,50,000', '1,00,000'],
    ['G2', 'Conferences & dissemination', '2,00,000', '0', '1,50,000', '50,000'],
    ['G3', 'Institutional overheads', '1,50,000', '50,000', '50,000', '50,000'],
    ['G4', '10% Contingency reserve', '1,50,000', '1,00,000', '50,000', '0'],
    ['', '<b>GRAND TOTAL</b>', '<b>1,85,00,000</b>', '<b>66,00,000</b>', '<b>80,50,000</b>', '<b>38,50,000</b>'],
])

H('17.1 Budget Justification', 2)
P('The budget allocation reflects three strategic priorities: (i) HEAVY UPFRONT TECHNOLOGY INVESTMENT (A: 21% of budget) recognizes that platform quality determines long-term sustainability; (ii) DOMINANT HUMAN RESOURCES INVESTMENT (B: 38% of budget) ensures sustained, high-caliber team execution across the 30-month tenure; (iii) MEANINGFUL COMMUNITY MOBILIZATION (C: 11% of budget) ensures that technology deployment is matched by adequate human-centred onboarding and capacity building. The MARKET INFRASTRUCTURE allocation (D: 17% of budget) creates physical assets (cluster centres, cold chain) that anchor sustainability beyond the pilot. The financial services and M&amp;E budgets are right-sized to enable rigorous deployment without bloat.')

P('Cost-effectiveness analysis: At INR 1,85,00,000 total cost protecting 5,000 directly enrolled producers (with an additional 25,000 household members benefiting indirectly), the project achieves INR 3,700 per directly enrolled producer or INR 617 per total household-member-beneficiary. This compares favourably against benchmark intervention costs in agriculture-livelihood programmes which typically range INR 8,000-25,000 per beneficiary household for less integrated interventions.')
BR()
print("Sections 16-17 added")

# ===================== SECTION 18: LOGFRAME + ToC =====================
H('SECTION 18: LOGICAL FRAMEWORK MATRIX (LOGFRAME)', 1)
P('The Logical Framework Matrix articulates the hierarchy from Goal through Purpose to Outputs and Activities, providing the master accountability structure expected by international funders.')

CAP('TABLE 18.1: PARVAT-SETU Logical Framework Matrix')
TBL(['Level', 'Description', 'Indicators', 'Verification', 'Assumptions'], [
    ['GOAL (Impact)', 'Transform smallholder economic position across Indian Himalayan Region through producer-owned digital social enterprise', '5,00,000+ HH economic uplift by 2035; replicated across 13 IHR states', 'Multi-year impact studies; replication tracking', 'Sustained DPI evolution; cooperative-friendly policy'],
    ['PURPOSE (Outcome)', 'Demonstrate validated AI-GIS social enterprise platform delivering 35-50% income uplift, full financial inclusion, and operational sustainability for 5,000 Garhwal smallholders', '5,000 enrolled; 40% income uplift validated via DiD; trajectory to break-even', 'Endline household survey; financial audit', 'Producer adoption; market demand stable; partner cooperation'],
    ['OUTPUT 1', 'AI-GIS technology platform fully developed and deployed', 'Mobile app live; 4 AI models deployed at target accuracy; GIS layer operational', 'Platform analytics; A/B testing; user acceptance', 'Connectivity adequate; smartphone availability'],
    ['OUTPUT 2', '5,000 producers onboarded with active engagement', '5,000 enrolled; 80% monthly active users; 60% women; 35% SC/ST', 'KYC records; usage analytics; demographic data', 'SHG mobilization succeeds; trust established'],
    ['OUTPUT 3', 'Full financial inclusion achieved', '100% bank account; 100% insurance; 85% credit access; INR 5 Cr disbursed', 'Bank records; insurance partner data', 'Banking partner cooperation; AI scoring accepted'],
    ['OUTPUT 4', 'Cluster collection centres + cold-chain operational', '3 centres operational; >80% capacity utilization', 'Operations data; throughput records', 'Site availability; equipment delivery'],
    ['OUTPUT 5', 'Market linkage active across 4 channels', '50+ B2B buyers; 5+ retail chains; D2C live; export pipeline', 'Buyer contracts; transaction data', 'Buyer-side commitments; quality consistent'],
    ['OUTPUT 6', 'Documented replication playbook', 'Tech open-sourced; templates published; 3 SCIE papers', 'GitHub release; published documents', 'Time and quality permitted'],
    ['ACTIVITY 1.x', 'Tech development', 'Code commits; sprint completion', 'Project mgmt tools', 'Talent retention'],
    ['ACTIVITY 2.x', 'Onboarding', 'Camps held; KYC completed', 'Camp records', 'Producer interest'],
    ['ACTIVITY 3.x', 'Banking integration', 'MoUs signed; rails operational', 'Partner records', 'Bank cooperation'],
    ['ACTIVITY 4.x', 'Infrastructure', 'Centres built; equipment installed', 'Site visits', 'Site approvals'],
    ['ACTIVITY 5.x', 'Market linkage', 'Contracts signed; transactions flow', 'Sales data', 'Buyer demand'],
    ['ACTIVITY 6.x', 'M&amp;E', 'Surveys completed; analyses done', 'Reports', 'Field access'],
])

# ===================== SECTION 19: SDG ALIGNMENT =====================
H('SECTION 19: ALIGNMENT WITH UN SUSTAINABLE DEVELOPMENT GOALS (SDGs)', 1)
P('PARVAT-SETU directly contributes to seven SDGs through its integrated design.')
CAP('TABLE 19.1: SDG Contribution Matrix')
TBL(['SDG', 'Goal Title', 'Specific Contribution', 'Quantified Target'], [
    ['SDG 1', 'No Poverty', 'Income uplift for smallholder households below poverty line', '40% income increase for 5,000 HH'],
    ['SDG 2', 'Zero Hunger', 'Sustainable agriculture; biodiversity; food security', 'Traditional millet revival; 50% organic transition by Y5'],
    ['SDG 5', 'Gender Equality', 'Women-led SHG-cooperative model with gender-disaggregated outcomes', '60%+ women participation; equal income outcomes'],
    ['SDG 8', 'Decent Work &amp; Economic Growth', 'Dignified market participation; cooperative employment; financial inclusion', '5,000 dignified livelihoods; 30-45 jobs at centres'],
    ['SDG 10', 'Reduced Inequalities', 'Targeted SC/ST inclusion; rural-urban income gap reduction', '35%+ SC/ST participation; 40% income gap reduction'],
    ['SDG 12', 'Responsible Consumption', 'Traceable sourcing; reduced food loss; sustainable production', '25-35% post-harvest loss reduction'],
    ['SDG 13', 'Climate Action', 'Climate-resilient agriculture; insurance; carbon sequestration', '100% insurance coverage; agroforestry on 500+ ha'],
])

# ===================== SECTION 20: SCALING =====================
H('SECTION 20: SCALING AND REPLICATION STRATEGY', 1)
P('PARVAT-SETU is engineered as a replication-ready template from inception, not retrofitted for scaling after pilot success. The scaling strategy follows a deliberate three-phase trajectory designed to achieve geometric protection growth while maintaining quality and sustainability.')

CAP('DIAGRAM 6: Three-Phase Scaling Pathway')
MONO('''
================================================================================
                    PARVAT-SETU SCALING PATHWAY
================================================================================

  +----------------------------------------------------------+
  |  PHASE 1: PILOT (THIS PROJECT, M1-30)                     |
  |  ---------------------------------------------            |
  |  * 3 Garhwal districts (Tehri, Pauri, Chamoli)            |
  |  * 5,000 producers / 25,000 indirect HH                   |
  |  * INR 1.85 Cr investment                                 |
  |  * Technology + governance + evidence                     |
  +----------------------------------------------------------+
                            |
                            v Replication-ready playbook
  +----------------------------------------------------------+
  |  PHASE 2: UTTARAKHAND-WIDE (M31-66)                       |
  |  ---------------------------------------------            |
  |  * All 13 districts of Uttarakhand                        |
  |  * 30,000-40,000 producers / 1.5-2 lakh HH                |
  |  * INR 8-12 Cr investment                                 |
  |  * 50% per-unit cost reduction via standardization        |
  |  * Funder pathway: NABARD + State + CSR + multilateral    |
  +----------------------------------------------------------+
                            |
                            v Multi-state proof-of-concept
  +----------------------------------------------------------+
  |  PHASE 3: PAN-IHR (M67-120)                                |
  |  ---------------------------------------------            |
  |  * All 13 IHR states                                       |
  |  * 5,00,000+ producers / 25 lakh HH                        |
  |  * INR 80-150 Cr investment                                |
  |  * 65% per-unit cost reduction (full economies of scale)   |
  |  * Funder pathway: GCF, ADB, World Bank, large CSR         |
  |  * Operational sustainability: 70%+ self-funded            |
  +----------------------------------------------------------+
''')

# ===================== SECTION 21: REFERENCES =====================
H('SECTION 21: KEY REFERENCES', 1)
refs = [
    'Bhatt, E. (2006). We Are Poor But So Many: The Story of Self-Employed Women in India. Oxford University Press.',
    'DFID (1999). Sustainable Livelihoods Guidance Sheets. Department for International Development, UK.',
    'Government of India (2018-19). Situation Assessment of Agricultural Households. NSSO 77th Round.',
    'Government of India (2020). National Mission on Sustainable Agriculture, Operational Guidelines. MoA&FW.',
    'Government of India (2023). Digital Public Infrastructure for Agriculture (Agri Stack) Framework. MeitY-MoA.',
    'ICRIER (2024). State of Rural India: Smartphone Penetration and Digital Inclusion. Working Paper No. 412.',
    'IPCC AR6 WG2 (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability. Cambridge UP.',
    'Microsoft AI for Earth + ICRISAT (2017). AI Sowing App: Andhra Pradesh Pilot Results. Technical Report.',
    'NABARD (2023). FPO Status Report. National Bank for Agriculture and Rural Development.',
    'Niti Aayog (2023). Atmanirbhar Bharat: Agricultural Value Chain Modernization. Working Paper.',
    'One Acre Fund (2023). Annual Impact Report. East Africa Operations.',
    'RBI (2023). Account Aggregator Framework: Implementation Guidelines.',
    'SEWA (2023). Annual Report. Self Employed Women\'s Association.',
    'World Bank (2022). India: Strengthening Agricultural Markets. Country Diagnostic Report.',
    'Chen, J., & Yang, Q. (2024). AI for smallholder agriculture: A systematic review. AI &amp; Society, 39(2), 234-256.',
    'Kumar, P., et al. (2023). Digital platforms and rural livelihoods in India. World Development, 165, 106195.',
    'Suri, T., et al. (2021). Mobile money and the economic lives of the poor. Science, 372(6537), 1289-1290.',
    'Banerjee, A., Karlan, D., & Zinman, J. (2015). Six randomized evaluations of microcredit. Am. Econ. J. Applied 7(1).',
    'Aker, J. C., et al. (2020). The promise of digital agriculture for smallholders. Annual Review of Resource Economics, 12, 291-311.',
    'Reardon, T., et al. (2022). The processed food revolution in Indian agri-food systems. Food Policy, 105, 102166.',
]
for r in refs:
    P(r)

# ===================== DECLARATION =====================
BR()
H('DECLARATION', 1)
P('We hereby declare that this Project Funding Proposal represents original work. The proposed project does not duplicate any ongoing funded research. All budget items represent genuine estimated costs. The institutional infrastructure and human resources described are available and committed for the proposed project tenure. We commit to conducting this project with the highest standards of scientific integrity, community respect, gender sensitivity, and environmental responsibility. All technology developed will be open-sourced, all data anonymized for academic publication, and producer welfare prioritized in all governance decisions.')
SP(20)
sigtbl = Table([
    ['<b>Project Investigator:</b>', '<b>Co-Principal Investigator:</b>'],
    ['', ''],
    ['', ''],
    ['______________________', '______________________'],
    ['Dr. Nidhi Rawat', 'Raj Amritam'],
    ['Assistant Professor', 'PhD Research Scholar'],
    ['Dept. of Environmental Science', 'Dept. of Environmental Science'],
    ['DBS Global University, Dehradun', 'DBS Global University, Dehradun'],
], colWidths=[3.4*inch, 3.4*inch])
sigdata = []
for row in [
    ['Project Investigator:', 'Co-Principal Investigator:'],
    ['', ''],
    ['', ''],
    ['______________________', '______________________'],
    ['Dr. Nidhi Rawat', 'Raj Amritam'],
    ['Assistant Professor', 'PhD Research Scholar'],
    ['Dept. of Environmental Science', 'Dept. of Environmental Science'],
    ['DBS Global University, Dehradun', 'DBS Global University, Dehradun'],
]:
    sigdata.append([Paragraph(c, BNI) for c in row])
sigtbl = Table(sigdata, colWidths=[3.4*inch, 3.4*inch])
sigtbl.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
]))
story.append(sigtbl)

SP(20)
P('Date: ____________ &nbsp;&nbsp; | &nbsp;&nbsp; Place: Dehradun, Uttarakhand, India')
SP(15)
P('<b>Institutional Endorsement Stamp:</b>')
SP(10)
P('________________________________________')
P('(Vice-Chancellor / Registrar, DBS Global University)')


# ===================== ADDITIONAL SECTION 22: PRIOR WORK & PRECEDENT ANALYSIS =====================
H('SECTION 22: PRIOR WORK ANALYSIS &mdash; WHAT HAS ALREADY BEEN ATTEMPTED', 1)
P('A rigorous proposal must explicitly engage with prior interventions in the same problem space, identifying both validated success patterns and critical failure modes. PARVAT-SETU\'s design synthesizes lessons from over fifty documented interventions across India and internationally. This section provides detailed case-by-case analysis of the most relevant precedents.')

H('22.1 Indian Government Initiatives in Smallholder Aggregation', 2)

H('22.1.1 e-NAM (National Agriculture Market)', 3)
P('Launched April 2016 by Ministry of Agriculture and Farmers\' Welfare, e-NAM was conceived as a pan-India electronic trading portal networking existing APMC mandis. As of 2024, 1.7 crore farmers and 1.7 lakh traders are registered across 1,389 mandis in 23 states. Cumulative trade value crossed INR 2.5 lakh crore. However, critical evaluation reveals serious operational shortcomings: less than 8% of registered farmers transact monthly; only 11.7% of total trade value occurs across state borders (defeating the integration goal); price discovery improvements documented at only 0.7% to 3.1% versus traditional mandi auctions. PARVAT-SETU lessons: (i) registration without active engagement is meaningless; (ii) mandi-bound platforms fail to reach hill-state smallholders who lack mandi access; (iii) producer-controlled platforms outperform government-administered platforms in active engagement.')

H('22.1.2 FPO (Farmer Producer Organization) Scheme', 3)
P('SFAC and NABARD have facilitated formation of approximately 27,000 FPOs since 2014, with target of 10,000 additional FPOs by 2027 under the INR 6,865 crore Central Sector Scheme launched 2020. FPOs collectively serve approximately 30 lakh smallholder farmers. However, NABARD\'s own 2023 evaluation reveals that 60-70% of formed FPOs remain operationally weak — characterized by low membership engagement, insufficient working capital, absence of professional management, and minimal technology adoption. The structural problem: FPO formation is funded but FPO operationalization (technology, market linkage, working capital) is not. PARVAT-SETU directly addresses this gap by partnering with 12 existing or newly-formed FPOs in the pilot region, providing them precisely the technology stack, market connectivity, and operational capability they currently lack.')

H('22.1.3 Pradhan Mantri Vishwakarma Yojana', 3)
P('Launched September 2023 with INR 13,000 crore commitment, PM Vishwakarma targets 30 lakh artisans across 18 traditional crafts with skill training, toolkit grants, and credit access (INR 1 lakh first tranche, INR 2 lakh second tranche at 5% interest). The scheme provides direct convergence opportunity for PARVAT-SETU\'s women SHG handicraft producers — bamboo crafts, woollen weaving, traditional textiles — enabling stacked benefits: PMVY-funded skill development plus PARVAT-SETU\'s digital market linkage and aggregation.')

H('22.2 International Precedents &mdash; Comparative Analysis', 2)

H('22.2.1 One Acre Fund (East Africa)', 3)
P('Operating since 2006 across Kenya, Rwanda, Tanzania, Burundi, Uganda, Malawi, and Zambia, One Acre Fund has reached 1.5 million smallholder farmer households with bundled inputs (seeds, fertilizer), agricultural training, market access, and structured credit. Documented impact (independently evaluated): 40-50% income increase per participating farmer averaged across all geographies. Critical design lessons: (i) BUNDLING (inputs + credit + training + markets) outperforms single-service interventions by 3-5x; (ii) WORKING CAPITAL provision is non-negotiable for actual income outcomes; (iii) REPETITION across multiple seasons (2-3 years per farmer) is required for behaviour change to consolidate. PARVAT-SETU integrates all three principles.')

H('22.2.2 M-Pesa Mobile Money (Kenya)', 3)
P('Launched March 2007 by Safaricom, M-Pesa transformed financial inclusion in Kenya — reaching 96% of Kenyan adults by 2024. Independent academic studies (Suri & Jack 2016, Science) document that M-Pesa lifted approximately 2% of Kenyan households out of extreme poverty (194,000 households), primarily through enabling women\'s entry into business ownership and remittance-based risk smoothing. Critical lessons for PARVAT-SETU: (i) MOBILE MONEY UNLOCKS DOWNSTREAM INTERVENTIONS that depend on cash flow visibility; (ii) AGENT NETWORKS for cash-in/cash-out are critical for last-mile usability; (iii) WOMEN BENEFIT DISPROPORTIONATELY when mobile money expands their financial autonomy. India\'s UPI infrastructure provides equivalent capability without requiring separate platform — PARVAT-SETU directly leverages UPI rather than building parallel infrastructure.')

H('22.2.3 Grameen Bank Microcredit Model (Bangladesh)', 3)
P('Founded by Muhammad Yunus in 1976 (winning 2006 Nobel Peace Prize), Grameen Bank pioneered group-liability microcredit for poor women, reaching 9 million members with 97% women clients and historical repayment rates of 96-99%. Subsequent rigorous evaluations (Banerjee, Karlan, Zinman 2015) revealed that pure microcredit produces modest income effects (5-10% increases) but transformative effects on agency and women\'s decision-making power. Lessons for PARVAT-SETU: (i) GROUP-LIABILITY is more powerful than collateral for low-income lending; (ii) WOMEN-CENTRED design produces broader household welfare benefits; (iii) CREDIT ALONE IS INSUFFICIENT — must be paired with skill, market, and infrastructure interventions for transformative income effects.')

H('22.2.4 Microsoft AI for Agriculture (India)', 3)
P('Microsoft Research India in partnership with ICRISAT deployed AI-based sowing advisory in Devanakonda mandal, Andhra Pradesh, beginning 2017. The system uses weather data, soil moisture, and crop models to recommend optimal sowing dates by SMS in vernacular languages. Documented yield increases of 30% averaged across 175 participating farmers, validated through controlled comparison. Subsequent expansion to Karnataka, Maharashtra, and other states reached approximately 7,000 farmers by 2023. Critical lessons: (i) AI ADVISORY WORKS at the smallholder level when delivered in vernacular SMS format; (ii) WEATHER-BASED ADVISORY is the highest-impact AI use case for rainfed agriculture; (iii) INTEGRATION WITH EXTENSION SERVICES (KVKs, ATMA) is essential for advisory uptake.')

H('22.2.5 Esoko (Ghana, West Africa)', 3)
P('Founded 2005 in Ghana, Esoko provides SMS-based market price information and weather advisory to West African smallholders, currently reaching approximately 600,000 farmers across 10 countries. Independent evaluations document 10-15% price improvement for participating farmers. Critical limitation: Esoko remained an information service without integrated transaction capability, limiting its income impact. PARVAT-SETU\'s integrated transaction platform addresses this limitation directly.')

# ===================== SECTION 23: DETAILED BENEFICIARY PROFILES =====================
H('SECTION 23: DETAILED BENEFICIARY PROFILES AND USE CASES', 1)
P('To translate aggregate income targets into operational reality, the project has developed detailed beneficiary profiles representing the diversity of smallholder situations in the pilot region. Each profile captures current livelihood configuration, specific PARVAT-SETU intervention pathway, and quantified expected uplift. These profiles serve as the basis for tailoring outreach, training, and product offerings.')

H('23.1 Profile 1 &mdash; Sushila Devi, 42, Tehri Garhwal (SHG Member)', 2)
P('Sushila Devi is a 42-year-old female head of household in Pratapnagar block, Tehri Garhwal. Family of five (husband working as labourer in Mussoorie, three children in school). Owns 0.4 hectares of terraced land producing kharif rice and millets, rabi wheat and pulses, plus 200 sq metre kitchen garden. Three buffaloes producing 8-12 litres milk daily. Annual gross income: INR 1,15,000 (rice/wheat sale INR 35,000; pulse INR 18,000; milk to local trader INR 32,000; vegetable surplus INR 12,000; husband\'s remittance INR 18,000). Annual expenses: INR 92,000. Net annual surplus: INR 23,000. No bank account in her name (joint account with husband, husband-controlled), no insurance, no credit history. Member of Pratapnagar SHG (formed 2018 under NRLM Ajeevika).')
P('PARVAT-SETU Intervention Pathway: (i) Onboarding via SHG meeting; smartphone subsidy (existing 50% subsidized via PMKVY); (ii) Independent bank account in her name with Aadhaar-linked KYC; (iii) Direct milk sale via PARVAT-SETU dairy aggregator at INR 42/litre versus current INR 28/litre (+50% per litre, additional INR 16,800/year); (iv) Branded "Garhwal Mountain" millet sale at INR 95/kg versus current INR 35/kg, on 200 kg surplus (+INR 12,000/year); (v) Premium kitchen-garden vegetables to BigBasket via cluster aggregation (+INR 8,000/year); (vi) Bundled insurance (PMFBY + PMSBY); (vii) AI-scored credit access for buffalo upgrade (INR 30,000 working capital). Projected annual income post-PARVAT-SETU: INR 1,52,000 (+32% gross, +110% net surplus to INR 49,000).')

H('23.2 Profile 2 &mdash; Mohan Singh Negi, 51, Pauri Garhwal (Apple Farmer)', 2)
P('Mohan Singh Negi cultivates 0.6 hectares of apple orchard at 1,800m elevation in Khirsu block. Mature trees yield approximately 4 tonnes per year of mid-quality apples (Royal Delicious + local varieties). Currently sells entire crop to district commission agent at INR 22-30/kg averaging INR 1,00,000 annual revenue. Annual costs (fertilizer, plant protection, labor, transport): INR 65,000. Net annual income: INR 35,000. Has bank account (Punjab National Bank), holds Kisan Credit Card with INR 50,000 limit. No insurance.')
P('PARVAT-SETU Intervention Pathway: (i) Quality grading via mobile-app computer vision identifies premium-grade fraction (35% of crop); (ii) Premium fraction sold via PARVAT-SETU D2C channel at INR 110/kg versus INR 25/kg for commodity (+INR 1,19,000 on 1.4 tonnes premium); (iii) Standard fraction sold to institutional buyer (food processor for juice) at INR 35/kg versus INR 22/kg (+INR 33,800 on 2.6 tonnes); (iv) Reduction in transport cost by 35% via shared cluster logistics (savings INR 12,000); (v) Group organic certification (3-year transition) increases premium price by additional 25% in Year 4+. Projected post-PARVAT-SETU annual income: INR 2,52,000 gross / INR 1,35,000 net (+285% net income).')

H('23.3 Profile 3 &mdash; Anita and SHG-Cluster, Chamoli (Walnut + Honey)', 2)
P('Anita Bhandari leads the Devalsari Mahila SHG (15 women members) in Chamoli district, producing walnuts and honey from agroforestry plots and apiaries. Aggregate annual production: 1,200 kg in-shell walnuts and 480 kg multi-floral honey. Current sales: bulk to district trader at INR 250/kg walnut and INR 300/kg honey, generating INR 4,44,000 group annual revenue divided across 15 members (INR 29,600 per member).')
P('PARVAT-SETU Intervention Pathway: (i) Group organic certification (NPOP via APEDA-registered agency, group cost INR 35,000 versus individual cost INR 1.5 lakh+ per producer); (ii) Branded export-quality packaging for "Garhwal Single-Origin Honey" and "Himalayan Heritage Walnut"; (iii) Premium D2C and export-channel sales at INR 750/kg walnut (+200%) and INR 800/kg honey (+167%); (iv) Trade fair participation via APEDA-coordinated showcase; (v) Embedded GI tagging (Garhwal Honey GI in process). Projected post-PARVAT-SETU group revenue: INR 13,00,000 (+193%); per-member income INR 86,700 (+193%).')

# ===================== SECTION 24: AI USE-CASE DEEP DIVE =====================
H('SECTION 24: AI USE-CASE DEEP DIVE &mdash; HOW INTELLIGENCE TRANSLATES TO INCOME', 1)
P('PARVAT-SETU\'s AI integration is not generic — every model has been selected for its specific income-uplift contribution at smallholder scale. This section provides operational detail on each model\'s training, deployment, and expected impact.')

H('24.1 Demand Forecasting Model', 2)
P('ARCHITECTURE: Ensemble of LSTM (Long Short-Term Memory) deep neural network and Facebook Prophet seasonal decomposition model, weighted by recent-period accuracy (rolling 6-week MAPE). TRAINING DATA: Multi-year (2018-2024) AGMARKNET mandi prices for 50 commodities x 50 mandis (Hindi belt + Himalayan), supplemented by IMD weather grids, festival calendar (drives demand spikes for traditional foods), e-commerce search trends (Google Trends, BigBasket search volumes proxied), and macro food-price index. PERFORMANCE TARGET: Mean Absolute Percentage Error (MAPE) below 15% on 7-day forecasts and below 25% on 30-day forecasts. INCOME-UPLIFT MECHANISM: Producers receive crop-specific demand forecasts 6 months ahead of sowing decisions, enabling shifts toward demand-rising commodities (traditional millets, single-origin honey, organic walnut) and away from commodity-glut categories (generic potato, generic onion in oversupplied seasons). Documented similar interventions yield 10-15% revenue uplift from improved sowing decisions alone.')

H('24.2 Price Prediction Model', 2)
P('ARCHITECTURE: XGBoost gradient boosting ensemble with feature engineering capturing temporal lag, mandi-pair correlations, supply-chain disruption signals (transport strikes, weather events), and seasonality. Quantile regression provides prediction intervals (10th, 50th, 90th percentile forecasts) enabling risk-aware decisions. TRAINING DATA: Same as demand forecasting with addition of futures market data (where available) and import-export quantities. PERFORMANCE TARGET: R-squared above 0.75 on 7-day forecasts; coverage of true price within 80% prediction interval at advertised 80% level. INCOME-UPLIFT MECHANISM: Producers receive next-week price forecasts 24-48 hours before harvest decisions, enabling profit-maximizing timing. Combined with logistics availability information, this enables peak-price-window selling that documented evidence suggests captures 8-15% premium versus non-informed selling.')

H('24.3 Credit Scoring Model', 2)
P('ARCHITECTURE: Random Forest classifier with 200+ features spanning traditional financial indicators (where available), alternative data signals (SHG repayment history, transaction frequency, asset proxies via Census village data, weather exposure index, smartphone usage patterns), and platform-specific behaviour (engagement frequency, listing accuracy, dispute history). Probability calibration via isotonic regression ensures predicted probabilities are interpretable as actual default probabilities. TRAINING DATA: Initial model trained on partner bank historical loan data (consent-based, anonymized) augmented with simulated smallholder profiles; continuously retrained as platform-native data accumulates from actual loans disbursed and outcomes observed. PERFORMANCE TARGET: AUC above 0.78 on holdout set; default rate below 4% on disbursed loans over 24-month observation. INCOME-UPLIFT MECHANISM: Enables 70%+ of credit-history-less smallholders to access formal credit at 9-12% interest versus moneylender alternatives at 36-60% interest, generating direct interest-cost savings of INR 2,000-15,000 per producer-loan-cycle, and indirect benefit of timely working capital that prevents distress sales.')

H('24.4 Quality Grading Computer Vision Model', 2)
P('ARCHITECTURE: Convolutional Neural Network using MobileNetV3 or EfficientNet-Lite backbones (chosen for inference efficiency on low-end Android devices). Models are trained per-commodity (apple, walnut, vegetable basket) with separate quality classes (Premium / Standard / Sub-grade). Edge deployment via TensorFlow Lite achieves inference latency below 200ms on target hardware. Confidence-thresholded output flags low-confidence images for human-aggregator review. TRAINING DATA: Crowd-sourced labelled produce images (target 10,000 images per commodity x 3 quality classes), supplemented by synthetic data augmentation (rotation, lighting variation, partial occlusion). PERFORMANCE TARGET: Top-1 classification accuracy above 88% per commodity. INCOME-UPLIFT MECHANISM: Automated quality grading at point of harvest enables differentiated pricing (Premium fraction commands 30-60% price premium), creates transparent quality signals that buyers trust, and reduces dispute resolution costs by 70-80%.')

H('24.5 Vernacular Voice/Text Advisory', 2)
P('ARCHITECTURE: IndicTrans2 (AI4Bharat) for Hindi-Garhwali-Kumaoni translation, Indic-BERT for query understanding, retrieval-augmented generation (RAG) over curated content corpus (KVK extension materials, AGMARKNET advisories, weather forecasts, government scheme notifications). Voice input/output via Indic ASR/TTS models for low-literacy users. INCOME-UPLIFT MECHANISM: Enables producers to query in their natural language ("Mera tamatar kis bhaav par bechun?", "Mausam kaisa rahega?"), receiving precise actionable advice that previously required physical visits to KVK extension officers. Reduces information-asymmetry-driven decision errors estimated at 5-10% of annual revenue.')

# ===================== SECTION 25: GIS USE-CASE DEEP DIVE =====================
H('SECTION 25: GIS USE-CASE DEEP DIVE &mdash; SPATIAL INTELLIGENCE FOR LIVELIHOODS', 1)
P('GIS layers in PARVAT-SETU are not decorative maps — they are operational tools driving five specific income-uplift use cases.')

H('25.1 Producer Location Mapping &amp; Land Records Linkage', 2)
P('Each enrolled producer\'s geo-location is captured during onboarding, cross-referenced against Bhulekh land records to verify ownership claims, and linked to administrative boundaries (village, panchayat, block, district). This master spatial register enables: (i) targeted programme delivery (insurance, credit, advisory) based on precise location; (ii) catchment analysis for cluster collection centre placement; (iii) eligibility verification for government scheme convergence (PMFBY requires landholding documentation).')

H('25.2 Agro-Ecological Zonation for Crop Recommendation', 2)
P('Integrating ICAR-NBSSLUP soil maps, IMD climate zones, SRTM elevation, and ALOS PALSAR slope/aspect, the platform classifies each producer\'s land into agro-ecological micro-zones with empirically established crop suitability rankings. AI advisory recommends crops with high suitability + projected demand rather than generic "popular" crops, yielding 8-15% productivity improvement through agro-ecological matching alone.')

H('25.3 Climate-Risk Overlay for Insurance Pricing', 2)
P('Historical IMD precipitation grids, flood inundation maps, landslide susceptibility zones, and IPCC AR6 downscaled future projections are overlaid to produce parcel-level climate risk indices. This enables actuarially fair, location-specific insurance pricing — replacing the current uniform-rate insurance products that systematically over-charge low-risk locations and under-charge high-risk locations. Critical for insurance partner acceptance.')

H('25.4 Logistics Network Optimization', 2)
P('Google OR-Tools combined with constrained genetic algorithms solve the Vehicle Routing Problem with Time Windows (VRPTW) for daily produce collection. Inputs: producer locations (with harvest readiness), vehicle capacities (refrigerated and ambient), road network with elevation-aware travel time estimates (15-25% slower in mountain terrain than plains-equivalent distances), perishability constraints (apple max 24h ambient transit; honey 72h), and buyer delivery deadlines. Output: optimal routing reduces logistics cost by 30-45% versus naive routing.')

H('25.5 Market-Shed Analysis for Buyer Targeting', 2)
P('Reverse spatial analysis identifies optimal buyer locations: which urban centres are economically reachable from PARVAT-SETU producers within perishability windows? Mapping these "market sheds" against urban demand profiles (population density, per-capita income, demographic preferences, existing supplier coverage) identifies high-opportunity markets where PARVAT-SETU\'s mountain-origin product positioning faces lowest competition. This drives B2B buyer prioritization decisions.')

# ===================== SECTION 26: GENDER & EQUITY MAINSTREAMING =====================
H('SECTION 26: GENDER &amp; EQUITY MAINSTREAMING DEEP DIVE', 1)
P('Gender mainstreaming and equity inclusion are not afterthoughts in PARVAT-SETU — they are operational design parameters with measurable accountability throughout the platform architecture.')

H('26.1 Why Gender Focus Matters Economically', 2)
P('Decades of evidence (World Bank Gender Innovation Lab; SEWA cooperative tradition; OECD development reviews) consistently demonstrate that economic interventions targeting women yield 2-3x higher household-welfare outcomes than gender-blind interventions, because women in low-income households reinvest 90%+ of incremental income into household nutrition, child education, and health (versus 30-40% reinvestment rate for men). Women-focused interventions generate not only direct income increases for participating women but also intergenerational poverty reduction effects via improved child outcomes.')

H('26.2 Operational Gender Mainstreaming Mechanisms', 2)
B('<b>60% women participation target</b> embedded in onboarding criteria with monthly tracking and quarterly course-correction.')
B('<b>Women-only SHG cluster preference</b> in initial enrollment to build participation depth before mixed-gender expansion.')
B('<b>Independent bank accounts in women\'s names</b> (not joint accounts where male relatives control access) ensures women\'s direct economic agency.')
B('<b>Mandatory 35% women on apex Producer Company Board</b> ensuring governance representation matches participation.')
B('<b>Gender-disaggregated platform analytics</b> tracking transaction volume, income, credit access, and complaint patterns by gender to identify and address differential outcomes.')
B('<b>Crops/products selection bias toward women-led production</b>: dairy, kitchen gardens, traditional millets (women-managed), handicrafts (women-led), poultry — categories where women hold decision authority.')
B('<b>Vernacular content with women narrators</b> for training videos to enhance relatability and uptake.')
B('<b>Field coordinators include 50%+ women</b> ensuring women producers have same-gender support during onboarding and ongoing engagement.')

H('26.3 SC/ST Inclusion Mechanisms', 2)
P('Scheduled Caste and Scheduled Tribe communities in pilot districts (predominantly Jaunsari and Buxa STs in Tehri/Pauri; Bhotiya ST and Dalit communities in Chamoli) face compound disadvantages of geographic remoteness, historical land alienation, and reduced market access. PARVAT-SETU mainstreams SC/ST inclusion through: (i) 35% participation target with monthly tracking; (ii) targeted onboarding camps in SC/ST hamlet clusters; (iii) preference for SC/ST-led SHGs in cluster federation formation; (iv) reserved 25% representation on apex Board; (v) tailored credit products with first-loss guarantee for borrowers without collateral; (vi) priority cluster-collection-centre placement near SC/ST hamlets.')

# ===================== SECTION 27: INSTITUTIONAL ENDORSEMENT PATHWAY =====================
H('SECTION 27: INSTITUTIONAL ENDORSEMENT AND CONVERGENCE PATHWAY', 1)
P('PARVAT-SETU\'s success depends on systematic institutional endorsement and scheme convergence. Pre-project secured indicators of support and post-funding partnership commitments are documented below.')

H('27.1 Pre-Project Institutional Support (To Be Secured Pre-Disbursement)', 2)
B('Letter of support from Department of Rural Development, Government of Uttarakhand')
B('MoU framework with Uttarakhand Livelihoods Mission (REAP) for SHG ecosystem partnership')
B('Letter of partnership-intent from NABARD Uttarakhand Regional Office')
B('Preliminary commitment from Uttarakhand Gramin Bank for AI-scored credit pilot')
B('Endorsement from District Magistrates of Tehri Garhwal, Pauri Garhwal, Chamoli')
B('Institutional commitment from DBS Global University Vice-Chancellor for academic backing')
B('Technical collaboration agreement with KVK-Tehri and KVK-Pauri for extension co-delivery')
B('Letter from APEDA Regional Office for export-channel facilitation')

H('27.2 Government Scheme Convergence', 2)
P('PARVAT-SETU systematically converges with multiple existing government schemes, multiplying every grant rupee through complementary public investment:')
CAP('TABLE 27.1: Government Scheme Convergence Matrix')
TBL(['Scheme', 'Ministry', 'Convergence Mechanism', 'Estimated Value Add'], [
    ['NRLM Ajeevika', 'MoRD', 'SHG mobilization and capacity building', 'INR 8-12 lakh per SHG'],
    ['FPO Scheme (10K FPOs)', 'MoA&amp;FW', 'FPO formation grant + matching equity', 'INR 18 lakh per FPO'],
    ['PMFBY (Crop Insurance)', 'MoA&amp;FW', 'Subsidized crop insurance enrollment', '90% premium subsidy'],
    ['PM Vishwakarma', 'MSDE', 'Skill training + toolkit grant for artisans', 'INR 1-3 lakh per artisan'],
    ['MGNREGA', 'MoRD', 'Wage labor for collection-centre construction', 'Zero wage cost to project'],
    ['Agriculture Infrastructure Fund', 'MoA&amp;FW', 'Subsidized loan for cold-chain', '3% interest subvention'],
    ['NABARD-RIDF', 'NABARD', 'Rural infrastructure financing', 'Concessional rates'],
    ['PKVY (Organic Farming)', 'MoA&amp;FW', 'Organic certification cost subsidy', '50% subsidy on certification'],
    ['PMKVY', 'MSDE', 'Skill development for SHG members', 'Free training + placement support'],
    ['Atmanirbhar Bharat (FME)', 'MoFPI', 'Food processing micro-enterprises', 'INR 10 lakh / unit subsidy'],
])

# ===================== SECTION 28: EXIT STRATEGY =====================
H('SECTION 28: EXIT STRATEGY AND POST-PILOT TRANSITION', 1)
P('A frequently overlooked element of pilot project design is the exit strategy — what happens at Month 30 when the pilot funding concludes? PARVAT-SETU is structured for an explicit transition from grant-funded pilot to operationally self-sustaining cooperative enterprise, with documented hand-over protocols at each level.')

H('28.1 Technology Transition', 2)
P('All technology code is open-sourced on GitHub from the project inception under Apache 2.0 license, ensuring permanent accessibility independent of organizational continuity. Database backups, model artifacts, and configuration are exported in standard formats. Cloud infrastructure ownership transitions to the apex Producer Company at Month 30, with paid maintenance contracts established with technology partners (alternatively, the platform can migrate to NIC Cloud free-tier for the first three years post-pilot if budget constraints emerge).')

H('28.2 Governance Transition', 2)
P('The three-tier cooperative governance structure (SHG &rarr; FPO &rarr; Producer Company) is operational from Month 8 onwards, ensuring producer-led decision-making is the steady state rather than a transitional arrangement. By Month 30, the apex Board has 30 months of operational experience and full decision authority. Formal hand-over from project Steering Committee to Producer Company Board occurs at Month 28 with two-month parallel running for transition support.')

H('28.3 Financial Transition', 2)
P('At Month 30, the platform is generating revenue (commissions, processing margins, subscriptions) that covers approximately 50-70% of operating costs (per the financial projection in Section 10). The remaining gap (INR 2-3 Crore aggregate over Year 3-4) is bridged through: (i) follow-on grant from CSR partners (Tata Trusts, Bharti Foundation expressed interest); (ii) NABARD\'s working capital loan facility for FPOs (concessional rates); (iii) limited-period revenue partnerships with institutional buyers (advance contracts at slight discount for guaranteed multi-year supply). By Month 60, operational break-even achieved without grant dependence.')

H('28.4 Knowledge Transition', 2)
P('All operational knowledge is documented in three formats: (i) WRITTEN PLAYBOOKS covering technology, governance, partnerships, and operations; (ii) VIDEO TUTORIALS in vernacular languages for key processes; (iii) PEER-TO-PEER LEARNING NETWORKS connecting PARVAT-SETU FPOs with FPOs in subsequent replication geographies. The replication playbook is structured for direct deployment in any new district at 50-65% reduced cost.')

# ===================== SECTION 29: FUNDER VALUE PROPOSITION =====================
H('SECTION 29: FUNDER VALUE PROPOSITION SUMMARY', 1)
P('For prospective funders, PARVAT-SETU offers a unique combination of attributes that distinguishes it from typical project proposals.')

CAP('TABLE 29.1: Funder Value Proposition Matrix')
TBL(['Attribute', 'Typical Project', 'PARVAT-SETU', 'Funder Implication'], [
    ['Beneficiary Cost', 'INR 8,000-25,000/HH', 'INR 3,700/HH direct, INR 617/HH total', '4-7x more efficient'],
    ['Sustainability', 'Grant-dependent', 'Operational break-even Year 5', 'No perpetual subsidy needed'],
    ['Income Uplift', '5-15% (single intervention)', '35-50% (bundled)', '3x higher impact'],
    ['Replication Cost', 'Same as pilot or higher', '50-65% reduction per district', 'Funder leverage 3-5x'],
    ['Evidence Base', 'Often weak attribution', 'Diff-in-Diff with control group', 'Publishable, defensible'],
    ['Gender Mainstreaming', 'Often retrofit', '60% target operational', 'Attractive to gender-focused funders'],
    ['Tech Innovation', 'Often unspecified', 'AI-GIS-blockchain integrated', 'High visibility, photo-friendly'],
    ['Government Convergence', 'Standalone', 'Multiple scheme integration', 'Policy-aligned, low political risk'],
    ['Producer Ownership', 'External-led', 'Cooperative-owned', 'No "extraction" optics; ESG positive'],
    ['Climate Co-benefits', 'Often absent', 'Insurance, organic, agroforestry', 'Counts as climate finance'],
])

# ===================== BUILD =====================
doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4,
    rightMargin=0.7*inch, leftMargin=0.7*inch,
    topMargin=0.7*inch, bottomMargin=0.7*inch,
    title='PARVAT-SETU Pilot Project Proposal',
    author='Dr. Nidhi Rawat (PI), Raj Amritam (Co-PI)')
doc.build(story)

# Word count
import re
text = ''
def collect(elements):
    global text
    for el in elements:
        if hasattr(el, 'getPlainText'):
            text += ' ' + el.getPlainText()
        elif hasattr(el, 'text'):
            text += ' ' + str(el.text)
collect(story)
text = re.sub(r'<[^>]+>', '', text)
print(f"\nFinal PDF generated: {os.path.getsize(OUTPUT_PDF):,} bytes")
print(f"Approx word count: {len(text.split())} words")
