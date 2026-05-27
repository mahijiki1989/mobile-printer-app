#!/usr/bin/env python3
"""Advanced Grant Project Proposal Generator with Diagrams, Logframe, ToC"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.4); p.paragraph_format.line_spacing=1.4
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ TITLE PAGE ============
for _ in range(3): doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('GRANT PROJECT FUNDING PROPOSAL'); r.bold=True; r.font.size=Pt(16)
doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('(Advanced Edition with Theory of Change, Logical Framework, M&E & Implementation Diagrams)')
r.italic=True; r.font.size=Pt(10)
doc.add_paragraph(''); doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('Developing an Integrated Hydro-Spatial Framework for\nEco-Safe Himalayan Catchments:\n\nA Hybrid Academic-Deployment Strategy for\nNature-Based Flood Mitigation, IoT-Enabled Early Warning Systems\n& Community Climate Resilience')
r.bold=True; r.font.size=Pt(13)
doc.add_paragraph(''); doc.add_paragraph('')
for line,sz,b in [('Submitted to:',12,False),
    ('National Mission on Himalayan Studies (NMHS) /',12,True),
    ('DST-NMSHE / National Adaptation Fund for Climate Change (NAFCC)',12,True),
    ('',10,False),('Submitted by:',12,False),
    ('Department of Environmental Science',13,True),
    ('DBS Global University, Dehradun',13,True),
    ('Uttarakhand, India',12,False),('',10,False),
    ('Principal Investigator: Dr. Nidhi Rawat',12,True),
    ('Co-PI / Research Scholar: Raj Amritam',12,True),
    ('',10,False),('2025',13,True)]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn = p.add_run(line); rn.font.size=Pt(sz); rn.bold=b
doc.add_page_break()

# ============ SECTION 1: METADATA ============
H('SECTION 1: PROJECT IDENTIFICATION AND METADATA', 1)
TBL(['Field','Information'],
    [['Project Title','Developing an Integrated Hydro-Spatial Framework for Eco-Safe Himalayan Catchments: A Hybrid Academic-Deployment Strategy for Nature-Based Flood Mitigation, IoT-Enabled Early Warning Systems & Community Climate Resilience'],
     ['Proposed Tenure','36 Months (3-Year Fast-Track Strategy)'],
     ['Total Financial Request','INR 28,50,000 (Twenty-Eight Lakhs Fifty Thousand Only)'],
     ['Targeted Field Region','Garhwal Himalayan Region, Uttarakhand, India'],
     ['Direct Institutional Affiliation','Department of Environmental Science, DBS Global University, Dehradun'],
     ['Principal Investigator','Dr. Nidhi Rawat, Associate Professor'],
     ['Co-PI / Research Scholar','Raj Amritam, PhD Research Scholar'],
     ['Strategic Alignment','Sendai Framework Targets A, B, C, D, G; WMO Early Warnings for All (EW4All); NAPCC National Water Mission'],
     ['Institutional Mandate','DM Act 2005 (Sec. 30-31); SDMA Uttarakhand Guidelines; NDMA Flash Flood Management Guidelines 2022'],
     ['Direct Beneficiaries','2,500 households (~12,500 individuals) in Year 1-3 pilot'],
     ['Indirect Beneficiaries','500,000+ households via state-wide replication pathway'],
     ['Total SCIE Publications','4 Q1/Q2 papers within tenure'],
     ['CSR/Multilateral Pipeline','INR 100-500 Crore programs (post-pilot)']])

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Title + Section 1 saved")

# ============ SECTION 2: EXECUTIVE SUMMARY + Section 3: Theory of Change ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.4); p.paragraph_format.line_spacing=1.4
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

H('SECTION 2: EXECUTIVE SUMMARY AND STRATEGIC RATIONALE', 1)

P('The Garhwal Himalayan region of Uttarakhand represents one of the most acutely climate-vulnerable geographies on the Indian subcontinent. Characterized by extreme orographic precipitation gradients (1,200 mm in the Doon Valley to over 3,500 mm in mid-elevation cloudforest zones), tectonically active substrate (the Main Central Thrust and Main Boundary Thrust systems), and rapidly degrading forest cover (-18% during 2000-2022 in Garhwal alone), the region has witnessed an unprecedented acceleration of catastrophic hydro-meteorological events. The Chamoli disaster of February 2021 (>200 dead, two hydropower installations destroyed) and the Dharali flash floods of August 2025 (three villages inundated with zero prior warning) collectively underscore a systemic governance failure: the near-complete absence of functional early warning infrastructure in catchments experiencing rapid hazard intensification.')

P('This proposal presents a strategically integrated response designed for multi-year climate funding bodies seeking demonstrable community-level impact within compressed timelines. The core value proposition is the explicit dual-structure architecture bridging the persistent gap between academic computational research ("The Brain") and immediate, cost-effective on-ground community deployment ("The Body") within a single 36-month execution window. Unlike conventional academic projects (publications without operational outcomes) or development projects (infrastructure without scientific rigor), this initiative deliberately fuses both paradigms—producing simultaneously a validated hydro-spatial modeling framework (publishable in Q1 SCIE journals) AND a functioning early warning system protecting minimum 2,500 directly vulnerable households.')

P('The strategic rationale draws upon demonstrated international precedents. The Netherlands\' Room for the River program (2006-2019) achieved sustained 35 cm peak water level reduction across 39 intervention sites through nature-based engineering—proving ecosystem-based approaches deliver quantifiable hydraulic benefits at operational scales. ICIMOD\'s transboundary flood EWS across the HKH belt have proven low-cost sensor networks combined with community-based last-mile dissemination provide actionable lead times of 3-8 hours. The Bihar flood-forecasting RCT (Viswanathan et al., 2022) demonstrated that targeted early warnings yielded 30% reduction in post-flood household medical expenditures and 22% reduction in livestock mortality—establishing rigorous evidence base for economic returns of community-level flood preparedness investments.')

P('This project targets the institutional sweet-spot where academic innovation meets deployment readiness: INR 28,50,000 over 36 months (~INR 1,140 per protected household) delivering a replicable, open-source template scalable across 13 districts of Uttarakhand and 25+ Himalayan districts of Himachal Pradesh, Sikkim, Arunachal Pradesh. The initiative directly serves the National Mission on Himalayan Studies (NMHS) priority areas, DST-NMSHE adaptation goals, and NAFCC implementation mandates while generating a pipeline of larger multilateral programs (GCF, ADB, GFDRR portfolios in INR 20-500 Crore range).')

# ============ SECTION 3: THEORY OF CHANGE ============
doc.add_page_break()
H('SECTION 3: THEORY OF CHANGE', 1)

P('The project employs a rigorous Theory of Change framework articulating the causal pathway from inputs through activities to long-term impact. Each transition includes explicit assumptions and risks, enabling adaptive management when assumptions prove false.')

CAP('DIAGRAM 1: Theory of Change — Causal Pathway with Assumptions')
MONO("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  THEORY OF CHANGE: HIMALAYAN FLOOD RESILIENCE             ║
╚═══════════════════════════════════════════════════════════════════════════╝

  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
  │    INPUTS      │ ──► │   ACTIVITIES   │ ──► │    OUTPUTS     │
  │                │     │                │     │                │
  │ • INR 28.5 L   │     │ • FVI Atlas    │     │ • 30m FVI maps │
  │ • PI/Co-PI/JRF │     │ • NbS Pilot    │     │ • 2-ha NbS site│
  │ • IoT sensors  │     │ • IoT EW deploy│     │ • 3 sensors+AWS│
  │ • Software     │     │ • Community    │     │ • SHG cadres   │
  │ • Institutional│     │   training     │     │ • DDMP annexes │
  │   linkages     │     │ • DDMP drafting│     │                │
  └────────────────┘     └────────────────┘     └────────┬───────┘
                                                         │
                                                         ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ ASSUMPTION ZONE 1: Data quality sufficient + Community accepts   │
  │ RISK ZONE 1: Sensor failure, AHP CR>0.10, low community uptake  │
  └─────────────────────────────────────────────────────────────────┘
                                                         │
                                                         ▼
  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
  │SHORT-TERM      │     │MEDIUM-TERM     │     │  LONG-TERM     │
  │OUTCOMES (Y1-2) │ ──► │OUTCOMES (Y3-5) │ ──► │  IMPACT (Y6+)  │
  │                │     │                │     │                │
  │• 95% sensor    │     │• 5+ districts  │     │• State-wide   │
  │  uptime        │     │  adopt template│     │  rollout       │
  │• 45-min lead   │     │• 30% damage    │     │• 500K HH       │
  │  time achieved │     │  reduction     │     │  protected     │
  │• 80% comprehen-│     │• Rev. pipeline │     │• Replication   │
  │  sion in alerts│     │  unlocked (CSR │     │  to other      │
  │• 100+ trained  │     │  + multilateral│     │  Himalayan     │
  │• NbS perform.  │     │  + Data-as-a-  │     │  states        │
  │  validated     │     │  Service)      │     │• Mortality red.│
  │                │     │                │     │  in target dist│
  └────────────────┘     └────────────────┘     └────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   ASSUMPTION 2:         ASSUMPTION 3:           ASSUMPTION 4:
   IoT operational       SDMA cooperation        Climate trends
   continuity            sustained               match RCP4.5/8.5
   RISK 2: tech          RISK 3: budget          RISK 4: extreme
   failure mid-          regime change           events overwhelm
   project                                       NbS thresholds
""")

H('3.1 Causal Logic Articulation', 2)
P('The chain begins with INPUTS (financial, human, technological, institutional resources) which feed ACTIVITIES (vulnerability mapping, ecological engineering pilot, IoT deployment, community capacity building, policy translation). These activities generate OUTPUTS (validated FVI atlas, functioning NbS pilot site, operational EWS, trained SHG cadres, DDMP annexures). Outputs translate into SHORT-TERM OUTCOMES (operational performance metrics achieved within 36 months) which compound into MEDIUM-TERM OUTCOMES (multi-district adoption, revenue pipeline activation) and ultimately LONG-TERM IMPACT (state-wide rollout, mortality reduction, replication).')

H('3.2 Critical Assumptions and Mitigation', 2)
B('Assumption 1: Open-source Sentinel/SRTM data quality remains sufficient. Mitigation: Multi-satellite fusion + manual ground-truthing budget.')
B('Assumption 2: IoT sensors remain operational under monsoon conditions. Mitigation: Redundant sensors (3 units) + 72-hr battery backup + quarterly maintenance.')
B('Assumption 3: SDMA Uttarakhand sustains cooperation across project tenure. Mitigation: Formal MoU at inception + DM Act statutory alignment ensures institutional continuity.')
B('Assumption 4: Climate trends remain within RCP4.5-8.5 envelope. Mitigation: Non-stationary frequency analysis with annual recalibration.')
B('Assumption 5: Community willingness to participate in drills/training. Mitigation: Honoraria + Gram Sabha resolutions + integration with MGNREGA wages.')

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 2-3 added")

# ============ SECTION 4: LOGFRAME + Section 5: Scope ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.4); p.paragraph_format.line_spacing=1.4
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ SECTION 4: LOGFRAME ============
doc.add_page_break()
H('SECTION 4: LOGICAL FRAMEWORK MATRIX (LFM)', 1)

P('The Logical Framework Matrix provides the master accountability structure for the project, articulating the hierarchy from Goal through Purpose to Outputs and Activities, with measurable indicators, verification means, and explicit assumptions at each level. This is the standard format expected by international funders (GCF, ADB, World Bank, UNDP).')

CAP('TABLE 4.1: Master Logical Framework Matrix')
TBL(['Hierarchy Level','Description','Verifiable Indicators','Means of Verification','Critical Assumptions'],
    [['GOAL (Impact)','Reduce flood-induced mortality and economic losses in climate-vulnerable Indian Himalayan watersheds through integrated science-deployment frameworks','• 30-50% mortality reduction in pilot zones over 5 years\n• 40% reduction in economic losses\n• Replication to 25+ districts','• SDMA disaster records\n• Census/economic surveys\n• State adoption documents','• Climate trends within projection envelope\n• Political stability\n• Sustained funding'],
     ['PURPOSE (Outcome)','Develop and demonstrate a replicable Hydro-Spatial Framework integrating NbS, IoT-EWS, and DDMP integration in the Garhwal Himalaya','• Operational EWS protecting 2,500 HH\n• 4 Q1 SCIE publications\n• DDMP adoption in 1 district','• EWS performance logs\n• Journal acceptances\n• DDMP gazette notifications','• SDMA cooperation\n• Community participation'],
     ['OUTPUT 1','Digital Flood Vulnerability Atlas at 30m resolution covering 150+ Gram Panchayats','• FVI maps published online\n• AUC > 0.75 vs historical floods\n• Open API access','• GitHub repository\n• Validation report\n• User analytics','• Sentinel data continuity\n• Census data accessible'],
     ['OUTPUT 2','Functioning 2-hectare NbS ecological engineering pilot with quantified performance','• ≥20% velocity reduction\n• ≥30% topsoil conservation\n• ≥15% infiltration enhancement','• Float+ADCP measurements\n• Sediment trap data\n• Infiltrometer logs','• Van Panchayat coop.\n• MGNREGA convergence\n• No major landslide damage'],
     ['OUTPUT 3','Community-embedded IoT-EWS with multi-modal alert dissemination','• >95% sensor uptime (Jun-Sep)\n• >45-min lead time\n• >80% message comprehension','• Server uptime logs\n• Event reconstructions\n• Post-monsoon survey','• Solar power adequacy\n• Cellular coverage\n• Community phone access'],
     ['OUTPUT 4','DDMP annexure templates adopted by district administration','• 1 district administrative order\n• Template documentation\n• Training delivered','• Gazette notification\n• Workshop records\n• MoU with SDMA','• DM administrative will\n• No political disruption'],
     ['ACTIVITY 1.1','Acquire & preprocess Sentinel/SRTM/Census data','Data acquisition log','Project records','Data accessibility'],
     ['ACTIVITY 1.2','Convene AHP expert panel & derive FVI weights','CR<0.10 achieved','AHP matrix records','Expert availability'],
     ['ACTIVITY 1.3','Generate FVI raster + validate vs SDMA records','AUC>0.75','Validation report','Historical records access'],
     ['ACTIVITY 2.1','Site selection + Van Panchayat MoU','MoU signed','Signed agreement','Van Panchayat consent'],
     ['ACTIVITY 2.2','MGNREGA convergence for labor mobilization','450-600 person-days','MGNREGA records','MGNREGA functioning'],
     ['ACTIVITY 2.3','Deploy NbS interventions + monitor','Interventions installed','Site photos+monitoring','No catastrophic event'],
     ['ACTIVITY 3.1','Procure & install 3 sensors + 1 micro-AWS','Hardware operational','Installation report','Equipment delivery'],
     ['ACTIVITY 3.2','Configure WhatsApp/SMS gateway + thresholds','System operational','Test alert logs','Server provider stability'],
     ['ACTIVITY 3.3','Train SHG Emergency Task Forces','100+ trained','Training records','Community participation'],
     ['ACTIVITY 4.1','Draft DDMP annexure templates','Draft completed','Document','SDMA technical input'],
     ['ACTIVITY 4.2','Stakeholder workshops for adoption','3+ workshops','Workshop records','Stakeholder availability'],
     ['ACTIVITY 4.3','Secure DM administrative order','Order issued','Gazette notification','Political continuity']])

# ============ SECTION 5: SCOPE OF WORK ============
doc.add_page_break()
H('SECTION 5: DETAILED SCOPE OF WORK (3-TASK ARCHITECTURE)', 1)

P('The project operationalizes its dual-structure philosophy through three integrated deployment tasks, each generating both academic outputs (publications, datasets, validated methodologies) and tangible community-level outcomes (infrastructure, capacity, institutional embedding) simultaneously.')

H('5.1 Task 1: Digital Flood Vulnerability Atlas — Resource Deployment', 2)

CAP('DIAGRAM 2: Task 1 Atlas Development Workflow')
MONO("""
   ┌─────────────────────────────────────────────────────────────────┐
   │                    TASK 1 WORKFLOW                                │
   └─────────────────────────────────────────────────────────────────┘

   Step 1: DATA ACQUISITION (Months 1-4)
   ┌──────────────────────────────────────────────────────┐
   │ • Sentinel-2 (10m LULC)                              │
   │ • SRTM/ALOS DEM (30m/12.5m)                          │
   │ • Census 2011 socio-demographic                      │
   │ • CHIRPS rainfall climatology                        │
   │ • SDMA historical flood inventory                    │
   └──────────────────────┬───────────────────────────────┘
                          │
                          ▼
   Step 2: AHP EXPERT ELICITATION (Months 4-6)
   ┌──────────────────────────────────────────────────────┐
   │ Panel: 8 experts (hydro/geo/RS/social/practitioner)  │
   │ Pairwise comparison matrix generation                │
   │ CR<0.10 validation iteratively                       │
   │ Output: Weight vector w_i for 15 indicators          │
   └──────────────────────┬───────────────────────────────┘
                          │
                          ▼
   Step 3: FVI COMPUTATION (Months 6-9)
   ┌──────────────────────────────────────────────────────┐
   │ Per-pixel: FVI = Σᵢ wᵢ × normalized_indicator_i      │
   │ Resolution: 30m                                      │
   │ Output: Continuous FVI raster + classified zones     │
   │   (Very Low, Low, Moderate, High, Very High)         │
   └──────────────────────┬───────────────────────────────┘
                          │
                          ▼
   Step 4: VALIDATION (Months 9-11)
   ┌──────────────────────────────────────────────────────┐
   │ vs Sentinel-1 SAR derived flood extents (5 events)   │
   │ vs SDMA reported affected villages                   │
   │ Performance: ROC AUC > 0.75 (target)                 │
   └──────────────────────┬───────────────────────────────┘
                          │
                          ▼
   Step 5: PUBLICATION + DEPLOYMENT (Months 11-14)
   ┌──────────────────────────────────────────────────────┐
   │ • Web-based GIS portal (open API)                    │
   │ • DDMP annexure formatting                           │
   │ • SDMA briefing + adoption pathway                   │
   │ • Paper 2 submission (target Q1 SCIE)                │
   └──────────────────────────────────────────────────────┘
""")

CAP('TABLE 5.1: Task 1 Sub-Activities and Deliverables')
TBL(['Activity','Months','Responsible','Deliverable','Verification'],
    [['Data acquisition (Sentinel/SRTM)','M1-3','JRF','Raw datasets, 100+ GB','Inventory log'],
     ['Field reconnaissance + GPS points','M2-4','PI+JRF+Field staff','GCP database (300+)','GPS logs'],
     ['LULC supervised classification','M3-5','JRF','30m LULC map','Accuracy >85% (kappa>0.80)'],
     ['DEM hydrological conditioning','M3-4','JRF','Pit-filled DEMs','QA report'],
     ['AHP expert panel convening','M4-5','PI','Pairwise matrices','CR<0.10'],
     ['FVI weight derivation','M5-6','PI+JRF','Weight vector','Sensitivity check'],
     ['Indicator layer normalization','M6-7','JRF','15 normalized rasters','Statistical summary'],
     ['Weighted overlay computation','M7-8','JRF','FVI raster','GIS log'],
     ['Validation vs SAR floods','M8-10','JRF','AUC values','Validation report'],
     ['Web portal development','M10-12','JRF+contractor','Live portal','Public URL'],
     ['DDMP annexure formatting','M12-14','PI+SDMA','Template document','SDMA review'],
     ['Paper 2 submission','M18','PI+JRF','Submitted manuscript','Submission ID']])

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 4-5.1 added")

# ============ Tasks 5.2 & 5.3 ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

H('5.2 Task 2: Ecological Engineering — 2-Hectare NbS Pilot Site', 2)

P('The ecological engineering task translates vulnerability analysis into physical landscape intervention through a 2-hectare pilot site in the highest-priority micro-watershed identified via Task 1. The pilot is designed for maximum replicability using locally available materials, indigenous knowledge systems, and convergence with MGNREGA wage labor and Van Panchayat institutions—ensuring zero wage cost to the project while generating documented employment.')

CAP('DIAGRAM 3: NbS Pilot Site Layout (Schematic)')
MONO("""
   ╔══════════════════════════════════════════════════════════════════╗
   ║         2-HECTARE NBS PILOT SITE (Headwater Sub-catchment)        ║
   ║                                                                    ║
   ║   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
   ║   ░ Forested Headwater (afforestation patch) - native species ░    ║
   ║   ░ • Alnus nepalensis (Utis - N-fixing)                       ░    ║
   ║   ░ • Grewia optiva (Bhimal - fodder)                          ░    ║
   ║   ░ • Celtis australis (Khirak - deep-rooted)                  ░    ║
   ║   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
   ║       ║                                                            ║
   ║       ▼  Stream flow direction                                     ║
   ║   ┌───────────────────────────────────────────────────────┐       ║
   ║   │ ▓▓▓ Contour Stone Bunding (every 10m vertical drop)   │       ║
   ║   │     with live Vetiver grass stakes                     │       ║
   ║   └───────────────────────────────────────────────────────┘       ║
   ║       ║                                                            ║
   ║       ▼                                                            ║
   ║   ┌───────────────────────────────────────────────────────┐       ║
   ║   │ ╳╳╳ Bamboo Check Structures (Dendrocalamus strictus)  │       ║
   ║   │     5-7 structures across primary drainage line        │       ║
   ║   │     spaced 30-50m apart                                │       ║
   ║   └───────────────────────────────────────────────────────┘       ║
   ║       ║                                                            ║
   ║       ▼                                                            ║
   ║   ┌───────────────────────────────────────────────────────┐       ║
   ║   │ ●●● Vetiver Grass Hedgerows (along stream banks)      │       ║
   ║   │ ●●● Napier Grass Buffer Strip (15m wide)               │       ║
   ║   └───────────────────────────────────────────────────────┘       ║
   ║       ║                                                            ║
   ║       ▼                                                            ║
   ║   ┌───────────────────────────────────────────────────────┐       ║
   ║   │ ◊◊◊ MONITORING STATION (downstream outlet):           │       ║
   ║   │     • Pressure transducer (water level)                │       ║
   ║   │     • Sediment trap                                    │       ║
   ║   │     • Velocity measurements (float method)             │       ║
   ║   │     • Ring infiltrometer locations (5 points)          │       ║
   ║   └───────────────────────────────────────────────────────┘       ║
   ║                                                                    ║
   ║   Total area: 2 hectares                                           ║
   ║   MGNREGA labor: 450-600 person-days                               ║
   ║   Targets: ≥20% velocity ↓, ≥30% topsoil cons., ≥15% infiltration ║
   ╚══════════════════════════════════════════════════════════════════╝
""")

CAP('TABLE 5.2: NbS Bill of Quantities (Pilot Site)')
TBL(['Item','Quantity','Unit Cost (₹)','Total (₹)','Source'],
    [['Bamboo poles (Dendrocalamus strictus)','500 nos.','120','60,000','Van Panchayat'],
     ['Vetiver grass slips','5,000 slips','5','25,000','Local nursery'],
     ['Napier grass cuttings','2,500 cuttings','3','7,500','MGNREGA nursery'],
     ['Native saplings (Alnus, Grewia, Celtis)','1,500 saplings','30','45,000','Forest Dept nursery'],
     ['Stone for bunding','25 cu.m','1,200','30,000','Local quarry'],
     ['Coir matting (geotextile)','500 sq.m','60','30,000','Coir Board'],
     ['Compost/manure','5 tonnes','3,000','15,000','Local'],
     ['Fencing (temporary protection)','200 m','150','30,000','Iron market'],
     ['Tools/implements (basic)','Lump sum','—','15,000','—'],
     ['Site supervision (technical)','3 visits','—','25,000','Project staff'],
     ['Monitoring instruments setup','Lump sum','—','18,000','Phase 1 budget'],
     ['MGNREGA labor (450-600 PD)','525 avg PD','220 (state rate)','MGNREGA-funded','State scheme'],
     ['','','TOTAL (project-funded)','3,00,500','—']])

H('5.3 Task 3: IoT Telemetry & Community Early Warning System', 2)

P('The IoT-based community EWS deploys 3 automated river-level sensors and 1 micro-Automatic Weather Station connected through hybrid GPRS/LoRa to a cloud-based threshold algorithm and multi-modal dissemination platform. The architecture is engineered for graceful degradation under monsoon stress and last-mile reach to non-literate, mobility-restricted, and elderly populations.')

CAP('DIAGRAM 4: IoT System Architecture (End-to-End)')
MONO("""
╔══════════════════════════════════════════════════════════════════════════╗
║          IoT-BASED COMMUNITY EARLY WARNING SYSTEM ARCHITECTURE             ║
╚══════════════════════════════════════════════════════════════════════════╝

   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │  SENSOR 1    │    │  SENSOR 2    │    │  SENSOR 3    │
   │  Upstream    │    │  Mid-reach   │    │  Downstream  │
   │  ────────    │    │  ────────    │    │  ────────    │
   │  Ultrasonic  │    │  Ultrasonic  │    │  Ultrasonic  │
   │  + Pressure  │    │  + Pressure  │    │  + Pressure  │
   │  Solar+72hr  │    │  Solar+72hr  │    │  Solar+72hr  │
   │  GPRS/LoRa   │    │  GPRS/LoRa   │    │  GPRS/LoRa   │
   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
          │                   │                   │
          │   ┌───────────────────────────────┐  │
          │   │       MICRO-AWS               │  │
          │   │  Rainfall + T + RH + Wind     │  │
          │   │  + Pressure (5-min interval)  │  │
          │   └───────────────┬───────────────┘  │
          │                   │                  │
          └───────────┬───────┴──────────────────┘
                      ▼
            ┌─────────────────────────┐
            │   GPRS/LoRa GATEWAY     │
            │   (Local relay)          │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │     CLOUD SERVER             │
            │   ─────────────────          │
            │   • Threshold Algorithm     │
            │     (HEC-RAS calibrated)    │
            │   • Yellow/Orange/Red       │
            │     alert generation         │
            │   • Edge computing fallback │
            │   • SDMA dashboard feed     │
            └────────────┬────────────────┘
                         │
                         ▼ ALERT TRIGGERED
        ┌────────────────┼─────────────────┐
        │                │                  │
        ▼                ▼                  ▼
  ┌──────────┐   ┌──────────────┐   ┌──────────────┐
  │ TIER 1   │   │ TIER 2       │   │ TIER 3       │
  │ AUTOMATED│   │ HUMAN RELAY  │   │ MASS         │
  │ DIGITAL  │   │              │   │ NOTIFICATION │
  │ ──────── │   │ ────────     │   │ ──────────   │
  │WhatsApp  │   │Mukhiya phone │   │Manual sirens │
  │Business  │   │call (priority│   │at 3 strategic│
  │API +     │   │alert 5 min   │   │locations     │
  │SMS via   │   │before public │   │(IP67 weather │
  │Exotel/   │   │+ door-to-door│   │ proof)       │
  │Knowlarity│   │notification  │   │              │
  │IVR       │   │for non-phone │   │              │
  │          │   │HHs           │   │              │
  └──────────┘   └──────────────┘   └──────────────┘

   PERFORMANCE TARGETS:
   • >45-min flash flood lead time (Yellow→Red)
   • >95% sensor uptime June-September
   • >80% message comprehension across demographic groups
""")

CAP('TABLE 5.3: IoT Hardware Specifications')
TBL(['Component','Specification','Quantity','Unit Cost (₹)','Total (₹)'],
    [['River level sensor (Ultrasonic+Pressure)','5m range, ±1cm accuracy, IP68','3','75,000','2,25,000'],
     ['Micro-AWS','Rain TB, T, RH, wind, pressure','1','1,25,000','1,25,000'],
     ['Solar panel + LiFePO4 battery','100W panel, 100Ah battery (per site)','4 sites','12,500','50,000'],
     ['Communication module','GPRS+LoRa hybrid','4','8,500','34,000'],
     ['Enclosure (IP67) + mounting','Mounting brackets, RCC piers','4','15,000','60,000'],
     ['Cloud server (annual)','AWS/Azure tier, 36 months','1','60,000','60,000'],
     ['SMS/IVR gateway (Exotel/Knowlarity)','Per message + base 36mo','—','40,000','40,000'],
     ['WhatsApp Business API','Setup + messaging','—','20,000','20,000'],
     ['Sirens (manual)','100W power, weatherproof','3','15,000','45,000']])

CAP('TABLE 5.4: Alert Threshold Matrix')
TBL(['Alert Level','Sensor Stage Threshold','Lead Time','Trigger Conditions','Recommended Action'],
    [['Yellow (Advisory)','60% of bank-full','45-60 min','Rising trend + IMD watch','Awareness; check movable assets'],
     ['Orange (Warning)','80% of bank-full','30-45 min','Sustained rise + heavy rain','Evacuate vulnerable persons; livestock to higher ground'],
     ['Red (Emergency)','95% of bank-full','15-30 min','Imminent overflow','Full evacuation; activate sirens']])

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 5.2-5.3 added")

# ============ SECTIONS 6, 7, 8 ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ SECTION 6: EW4ALL ============
doc.add_page_break()
H('SECTION 6: FOUR-PILLAR EW4ALL OPERATIONAL ARCHITECTURE', 1)

P('The project\'s technical deployment maps directly to the World Meteorological Organization\'s Early Warnings for All (EW4All) framework—the global standard endorsed by the UN Secretary-General\'s Executive Action Plan (2022). This alignment ensures international best-practice compliance while maximizing eligibility for follow-on multilateral climate finance.')

CAP('DIAGRAM 5: Four-Pillar EW4All Architecture (Project Mapping)')
MONO("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EW4ALL FOUR-PILLAR INTEGRATED ARCHITECTURE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
  │   PILLAR 1     │  │   PILLAR 2     │  │   PILLAR 3     │  │   PILLAR 4     │
  │ Risk Knowledge │  │   Detection    │  │ Dissemination  │  │  Preparedness  │
  │                │  │  & Forecasting │  │ & Communication│  │   & Response   │
  ├────────────────┤  ├────────────────┤  ├────────────────┤  ├────────────────┤
  │                │  │                │  │                │  │                │
  │• AHP-GIS FVI   │  │• 3 IoT sensors │  │• WhatsApp API  │  │• 2 drills/year │
  │  layers        │  │• 1 micro-AWS   │  │• SMS via Exotel│  │  (May, Aug)    │
  │                │  │                │  │  IVR           │  │                │
  │• Historical    │  │• 5-min interval│  │                │  │• SHG Emergency │
  │  flood records │  │  transmission  │  │• Hindi+Garhwali│  │  Task Forces   │
  │                │  │                │  │  bilingual     │  │  (≥50% women)  │
  │• Sentinel-1    │  │• HEC-RAS       │  │                │  │                │
  │  SAR derived   │  │  calibrated    │  │• Pre-tested for│  │• First aid +   │
  │  flood extents │  │  thresholds    │  │  >80% comp.    │  │  search-rescue │
  │                │  │                │  │                │  │                │
  │• Gender/caste/ │  │• Yellow/Orange/│  │• Mukhiya       │  │• Evacuation    │
  │  economic      │  │  Red levels    │  │  volunteer     │  │  routes mapped │
  │  disaggregation│  │                │  │  network       │  │                │
  │                │  │• Graceful      │  │                │  │• Livestock     │
  │• Continuous    │  │  degradation   │  │• Manual sirens │  │  protocols     │
  │  updating      │  │  architecture  │  │  (3 locations) │  │                │
  │                │  │                │  │                │  │• DM Act Sec 41 │
  │                │  │                │  │                │  │  recognition   │
  │                │  │                │  │                │  │                │
  └───────┬────────┘  └───────┬────────┘  └────────┬───────┘  └────────┬───────┘
          │                   │                    │                   │
          └───────────────────┼────────────────────┼───────────────────┘
                              │                    │
                              ▼                    ▲
                          ┌─────────────────────────┐
                          │  CONTINUOUS FEEDBACK     │
                          │  Performance data → Risk │
                          │  Knowledge updates →     │
                          │  Threshold recalibration │
                          └─────────────────────────┘
""")

CAP('TABLE 6.1: Project Component → EW4All Pillar Mapping')
TBL(['Project Output','EW4All Pillar','Specific Contribution','Performance Target'],
    [['FVI Atlas (Task 1)','Pillar 1: Risk Knowledge','Spatial vulnerability characterization','30m resolution, AUC>0.75'],
     ['Historical inventory','Pillar 1','Pattern recognition','5+ events documented'],
     ['Disaggregation analysis','Pillar 1','Equity-aware risk profile','Gender/caste/quintile splits'],
     ['IoT sensors (Task 3)','Pillar 2: Detection','Real-time water level','>95% uptime monsoon'],
     ['Micro-AWS','Pillar 2','Rainfall intensity monitoring','5-min resolution'],
     ['Threshold algorithm','Pillar 2','Alert level generation','>45 min lead time'],
     ['WhatsApp/SMS gateway','Pillar 3: Dissemination','Smartphone+feature phone reach','>80% comprehension'],
     ['Mukhiya volunteer network','Pillar 3','Last-mile reach','100% household coverage'],
     ['Manual sirens','Pillar 3','Mass notification','3 strategic locations'],
     ['SHG Task Forces','Pillar 4: Preparedness','Trained volunteer cadres','100+ trained'],
     ['Annual drills','Pillar 4','Practiced response','2 per year'],
     ['DDMP integration','Pillar 4','Institutional embedding','1+ district adoption']])

# ============ SECTION 7: GANTT ============
doc.add_page_break()
H('SECTION 7: IMPLEMENTATION PLAN AND GANTT CHART', 1)

CAP('DIAGRAM 6: 36-Month Implementation Gantt Chart')
MONO("""
TASK / ACTIVITY               Y1Q1 Y1Q2 Y1Q3 Y1Q4 Y2Q1 Y2Q2 Y2Q3 Y2Q4 Y3Q1 Y3Q2 Y3Q3 Y3Q4
═══════════════════════════════════════════════════════════════════════════════════════
A. PROJECT INCEPTION
  A1. Site selection         ████ 
  A2. SDMA MoU               ████ 
  A3. Inception workshop     ████ 

B. TASK 1: FVI ATLAS  
  B1. Data acquisition       ████ ████ 
  B2. AHP expert panel            ████ ████ 
  B3. FVI computation                  ████ ████ 
  B4. Validation                            ████ ████ 
  B5. Web portal launch                           ████ 

C. TASK 2: NbS PILOT
  C1. Site MoU+VanPanchayat        ████ 
  C2. MGNREGA mobilization              ████ 
  C3. Plant nursery raising             ████ ████ 
  C4. Civil works (bunds)                    ████ ████ 
  C5. Plantation                                  ████ 
  C6. Monitoring (continuous)                     ████ ████ ████ ████ ████ ████

D. TASK 3: IoT EWS
  D1. Equipment procurement        ████ 
  D2. Sensor installation               ████ 
  D3. Server+threshold setup                 ████ 
  D4. Community sensitization                ████ ████ 
  D5. Drills (May 2026, 2027)                            ████      ████
  D6. Drills (Aug 2026, 2027, 2028)                             ████      ████      ████

E. SHG TASK FORCE FORMATION
  E1. Identification & training              ████ ████ 
  E2. Refresher training                                    ████      ████

F. DDMP INTEGRATION
  F1. Annexure drafting                                ████ ████ 
  F2. Stakeholder workshops                                 ████ ████ 
  F3. Administrative order pursuit                                    ████ ████

G. M&E
  G1. Quarterly progress reviews ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░
  G2. Mid-term evaluation                                  ●(M18)
  G3. End-term evaluation                                                          ●(M36)

H. PUBLICATIONS
  H1. Paper 1 (Review)            ████ ████ ████ ●Submit M12
  H2. Paper 2 (FVI)                          ░░░░ ████ ████ ●Submit M18
  H3. Paper 3 (Hydrology)                                  ░░░░ ████ ●Submit M27
  H4. Paper 4 (Economics)                                            ░░░░ ████ ●Submit M33

  Legend: ████ Active   ░░░░ Background   ● Milestone
""")

# ============ SECTION 8: STAKEHOLDER MAPPING ============
H('SECTION 8: STAKEHOLDER MAPPING AND ENGAGEMENT', 1)

CAP('DIAGRAM 7: Power-Interest Grid for Stakeholder Strategy')
MONO("""
                              HIGH INTEREST
                                   ▲
                                   │
           ┌──────────────────┬────┴────┬──────────────────┐
           │  KEEP SATISFIED  │         │  MANAGE CLOSELY  │
           │  ─────────────   │         │  ─────────────   │
           │                  │         │                  │
           │ • IMD            │         │ • SDMA Uttarakhand│
           │ • CWC            │         │ • DDMA Dehradun  │
           │ • NMHS Secretariat│        │ • Van Panchayat   │
           │                  │         │ • Gram Sabha      │
           │                  │         │ • SHG Networks    │
           │                  │         │ • Mukhiya volunt. │
   LOW ◄──┼──────────────────┼─────────┼──────────────────┼──► HIGH
   POWER  │                  │         │                  │   POWER
           │  MONITOR         │         │  KEEP INFORMED   │
           │  ─────────       │         │  ─────────────   │
           │                  │         │                  │
           │ • Tourist        │         │ • Block Develop. │
           │   operators      │         │   Officer        │
           │ • Media          │         │ • State media    │
           │ • General public │         │ • State minister │
           │                  │         │ • DM (briefings) │
           └──────────────────┴────┬────┴──────────────────┘
                                   │
                              LOW INTEREST
""")

CAP('TABLE 8.1: Stakeholder Engagement Matrix')
TBL(['Stakeholder','Role','Influence','Engagement Strategy','Frequency'],
    [['SDMA Uttarakhand','Institutional anchor + adoption','High','Formal MoU + technical meetings','Quarterly'],
     ['DDMA Dehradun','District-level adoption','High','Briefings + DDMP drafting collab.','Bi-monthly'],
     ['District Magistrate','Administrative authorization','High','Strategic briefings','Bi-annual'],
     ['Block Development Officer','Implementation supervision','Medium','Operational meetings','Monthly'],
     ['Van Panchayat','Forest mgmt + bamboo source','High','MoU + community meetings','Monthly'],
     ['Gram Sabha','Community consent','High','Open meetings + resolutions','Quarterly'],
     ['SHG Networks','Task Force formation','High','Training + women-only FGDs','Monthly'],
     ['Mukhiya volunteers','Last-mile alert relay','High','Recruitment + training','Continuous'],
     ['SC/ST representatives','Equity validation','Medium','Targeted FGDs','Bi-annual'],
     ['IMD','Met data + validation','Medium','Data sharing protocols','As needed'],
     ['CWC','Hydrological data','Medium','Formal data request','As needed'],
     ['NMHS Secretariat','Funder oversight','High','Progress reports','Quarterly'],
     ['MGNREGA officials','Labor convergence','Medium','Operational coordination','Monthly during deploy.'],
     ['Tourist operators','Local economy','Low','Awareness sessions','Annual'],
     ['State media','Public awareness','Medium','Press releases','Major milestones']])

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 6-8 added")

# ============ SECTIONS 9, 10, 11 ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ SECTION 9: BUDGET ============
doc.add_page_break()
H('SECTION 9: DETAILED BUDGET MATRIX', 1)

CAP('TABLE 9.1: Comprehensive Project Budget — 36 Months')
TBL(['Code','Item Description','Amount (INR)','Year 1','Year 2','Year 3','Justification'],
    [['A','CAPITAL & ANALYTICAL EQUIPMENT','4,50,000','4,50,000','-','-','Front-loaded'],
     ['A1','IoT River-Level Sensors (3 × 75K)','2,25,000','2,25,000','-','-','One-time procurement'],
     ['A2','Micro-Automatic Weather Station','1,25,000','1,25,000','-','-','Single AWS unit'],
     ['A3','GIS Workstation (64GB RAM, RTX GPU)','1,00,000','1,00,000','-','-','Hydro modeling needs'],
     ['B','OPERATIONAL & MATERIAL ASSETS','8,50,000','2,00,000','5,50,000','1,00,000','Year 2 deployment heavy'],
     ['B1','Vegetative/Bamboo materials','2,50,000','-','2,50,000','-','NbS pilot Year 2'],
     ['B2','Community workshops & SHG training','1,50,000','50,000','60,000','40,000','Continuous engagement'],
     ['B3','API server hosting + IVR (36 months)','1,80,000','60,000','60,000','60,000','Ongoing infrastructure'],
     ['B4','Satellite processing credits','70,000','40,000','30,000','-','GEE/AWS during analysis'],
     ['B5','Field instrumentation','1,00,000','50,000','50,000','-','Infiltrometers, traps'],
     ['B6','Civil works & tools','1,00,000','-','1,00,000','-','Bunding/check structures'],
     ['C','MANPOWER & FELLOWSHIP','13,00,000','4,32,000','4,32,000','4,36,000','Largest single category'],
     ['C1','JRF/SRF Fellowship (₹35K × 36mo)','12,60,000','4,20,000','4,20,000','4,20,000','Full-time scholar'],
     ['C2','Field Surveyors (seasonal)','40,000','12,000','12,000','16,000','Monsoon support'],
     ['D','TRAVEL & CONTINGENCY','2,50,000','83,000','83,000','84,000','Distributed'],
     ['D1','In-state field travel','1,20,000','40,000','40,000','40,000','Site visits'],
     ['D2','Conference participation','80,000','-','40,000','40,000','Y2-Y3 dissemination'],
     ['D3','Overheads + 10% contingency','50,000','17,000','17,000','16,000','Buffer'],
     ['','GRAND TOTAL','28,50,000','11,65,000','10,65,000','6,20,000','Target']])

H('9.1 Cost-per-Household Analysis', 2)
P('At INR 28,50,000 total cost protecting 2,500 households directly, the project achieves INR 1,140 per protected household—a figure that compares extraordinarily favorably against conventional grey infrastructure. Concrete embankments and gabion walls typically cost INR 40,000-60,000 per linear meter, translating to INR 15,000-50,000 per protected household depending on settlement density. Therefore, this project achieves equivalent protection at approximately 3-7% of the cost of conventional alternatives, while additionally providing co-benefits (carbon sequestration, biodiversity, livelihoods) absent from grey infrastructure.')

CAP('TABLE 9.2: Cost-Benefit Comparison — Grey vs. Hybrid Approach')
TBL(['Metric','Grey Infrastructure (Conventional)','This Project (Hybrid NbS+EWS)','Ratio'],
    [['Total cost (HH protected)','₹15,000-50,000/HH','₹1,140/HH','13-44× cheaper'],
     ['Annual maintenance','~10% of capital','<2% of capital','5× cheaper'],
     ['Lifespan','30-50 yrs (degrading)','Indefinite (succession)','>2× longer'],
     ['Climate adaptability','Static design','Adaptive recalibration','Superior'],
     ['Co-benefits monetized','None','Carbon ₹2.5K/HH/yr + biodiversity','+ benefits'],
     ['Expected BCR','1.5-2.5','15-25 (incl. co-benefits)','7-10× higher']])

# ============ SECTION 10: M&E ============
doc.add_page_break()
H('SECTION 10: MONITORING & EVALUATION (M&E) FRAMEWORK', 1)

CAP('DIAGRAM 8: M&E Cycle')
MONO("""
                    ┌─────────────────┐
                    │  1. PLAN        │
                    │  Baseline data  │
                    │  + indicators   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │  2. MONITOR  │ │  3. ASSESS   │ │  4. REPORT   │
     │  Continuous  │ │  Performance │ │  Quarterly   │
     │  data        │ │  vs targets  │ │  + Annual +  │
     │  collection  │ │              │ │  Mid-term +  │
     │              │ │              │ │  End-term    │
     └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  5. ADAPT       │
                    │  Course-correct │
                    │  if deviation   │
                    │  > threshold    │
                    └────────┬────────┘
                             │
                             ▼ (back to step 1)
""")

CAP('TABLE 10.1: M&E Indicator Matrix')
TBL(['Indicator','Baseline','Target','Frequency','Method','Responsible'],
    [['FVI maps generated','0','Full coverage','Once','GIS audit','JRF + PI'],
     ['AHP CR achieved','N/A','<0.10','Once','Calculation','PI'],
     ['SWAT NSE','N/A','>0.6','Once + valid.','SUFI-2','JRF'],
     ['HEC-RAS CSI','N/A','>0.6','Once','SAR comparison','JRF'],
     ['Sensors operational','0','3 + AWS','Continuous','Server logs','JRF'],
     ['Sensor uptime monsoon','N/A','>95%','Per monsoon','Telemetry','JRF'],
     ['Alert lead time','N/A','>45 min','Per event','Reconstruction','PI'],
     ['Alert message comprehension','N/A','>80%','Annual survey','Field survey','PI+JRF'],
     ['NbS velocity reduction','Baseline','≥20%','Quarterly','Float method','Field staff'],
     ['NbS topsoil conservation','Baseline','≥30%','Bi-annual','Sediment traps','Field staff'],
     ['MGNREGA person-days','0','450-600','Once','MGNREGA records','BDO'],
     ['SHG members trained','0','100+','Annual','Training records','PI'],
     ['Drills conducted','0','2/year','Annual','Drill reports','SHG+PI'],
     ['DDMP annexure adoption','0','1+ district','Once','Gazette','SDMA'],
     ['SCIE papers submitted','0','4','Per paper','Submission ID','PI'],
     ['Workshops held','0','8+','Quarterly','Records','PI']])

# ============ SECTION 11: RISK MGMT ============
doc.add_page_break()
H('SECTION 11: RISK MANAGEMENT FRAMEWORK', 1)

CAP('TABLE 11.1: Comprehensive Risk Register (Probability × Impact)')
TBL(['ID','Risk','P(1-5)','I(1-5)','Score','Category','Mitigation','Owner'],
    [['R1','Sensor hardware failure','3','4','12','Technical','Redundant 3 sensors + spare parts','JRF'],
     ['R2','Solar power inadequate (cloud)','3','3','9','Technical','LiFePO4 72-hr battery','JRF'],
     ['R3','GPRS/cellular outage','3','4','12','Technical','LoRa mesh backup','JRF'],
     ['R4','Cloud server downtime','2','4','8','Technical','Edge computing fallback','Vendor'],
     ['R5','Community participation low','3','5','15','Social','Honoraria + Gram Sabha buy-in','PI'],
     ['R6','Van Panchayat non-cooperation','2','5','10','Institutional','Early MoU + alt site identified','PI'],
     ['R7','SDMA staff turnover','3','3','9','Institutional','Multi-level MoU + documentation','PI'],
     ['R8','MGNREGA delays','3','3','9','Operational','Direct labor budget standby (₹1L)','PI'],
     ['R9','Extreme event damages NbS pilot','2','5','10','Climate','Insurance + redundant design','PI'],
     ['R10','Climate trends exceed projection','2','3','6','Climate','Non-stationary analysis built-in','JRF'],
     ['R11','Scholar (JRF) attrition','2','5','10','HR','Co-PI continuity + comprehensive docs','PI'],
     ['R12','Paper rejection in Q1','3','3','9','Academic','Multi-target journals + preprint','PI'],
     ['R13','DDMP adoption blocked politically','2','4','8','Political','Multiple districts + Sec 31 alignment','PI'],
     ['R14','Equipment delivery delays','3','3','9','Procurement','Order Y1Q1 + advance procurement','PI'],
     ['R15','Currency fluctuation (imports)','2','2','4','Financial','Lock prices via advance order','PI']])

CAP('DIAGRAM 9: Risk Heat Map (5×5 Grid)')
MONO("""
                              IMPACT (Severity)
                  1          2          3          4          5
              ┌─────────┬─────────┬─────────┬─────────┬─────────┐
            5 │   LOW   │  MEDIUM │  HIGH   │ CRITICAL│ CRITICAL│
              │   (5)   │   (10)  │   (15)  │   (20)  │   (25)  │
              │         │         │         │         │   R5    │
              ├─────────┼─────────┼─────────┼─────────┼─────────┤
            4 │   LOW   │  MEDIUM │  HIGH   │  HIGH   │ CRITICAL│
   PROB-      │   (4)   │   (8)   │   (12)  │   (16)  │   (20)  │
   ABILITY    │         │         │   R3    │         │         │
              ├─────────┼─────────┼─────────┼─────────┼─────────┤
            3 │   LOW   │  LOW    │ MEDIUM  │  HIGH   │  HIGH   │
              │   (3)   │   (6)   │   (9)   │   (12)  │   (15)  │
              │         │         │R7,R8,R12│   R1    │         │
              │         │         │R14      │         │         │
              ├─────────┼─────────┼─────────┼─────────┼─────────┤
            2 │   LOW   │   LOW   │ MEDIUM  │ MEDIUM  │  HIGH   │
              │   (2)   │   (4)   │   (6)   │   (8)   │   (10)  │
              │         │  R15    │  R10    │  R4,R13 │R6,R9,R11│
              ├─────────┼─────────┼─────────┼─────────┼─────────┤
            1 │   LOW   │   LOW   │   LOW   │   LOW   │ MEDIUM  │
              │   (1)   │   (2)   │   (3)   │   (4)   │   (5)   │
              └─────────┴─────────┴─────────┴─────────┴─────────┘

  Score Categories:
  LOW (1-5): Accept   |   MEDIUM (6-10): Monitor   |   HIGH (11-19): Mitigate   |   CRITICAL (20-25): Treat urgently

  Top Risks Requiring Active Management:
  • R5 (Score 15): Community participation - Mitigation in progress
  • R1, R3 (Score 12): Sensor failures - Redundancy designed
  • R6, R9, R11 (Score 10): Institutional/Climate/HR - Active monitoring
""")

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 9-11 added")

# ============ SECTIONS 12, 13, 14, 15 + DECLARATION ============
doc = Document('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.4); p.paragraph_format.line_spacing=1.4
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.05)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(8)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri,row in enumerate(rows,1):
        for ci,val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ SECTION 12: SUSTAINABILITY ============
doc.add_page_break()
H('SECTION 12: SUSTAINABILITY AND SCALING PATHWAY', 1)

P('The project is designed not as a time-bound research initiative but as an institutional capability-building exercise generating self-sustaining revenue pathways and replication mechanisms beyond the 36-month grant period. Sustainability is achieved through four reinforcing strategies.')

CAP('DIAGRAM 10: Geometric Scaling Pyramid')
MONO("""
                                          ╔═══════════════════════╗
                                          ║   PHASE 3 (Y6-Y8)      ║
                                          ║   STATE-WIDE SCALING   ║
                                          ║   500,000+ HH          ║
                                          ║   (GCF/ADB/GFDRR)      ║
                                         ║   ₹100-500 Cr program  ║
                                       ╚═══════════════════════╝
                              ╔═════════════════════════════════════╗
                              ║   PHASE 2 (Y4-Y5)                    ║
                              ║   MULTI-DISTRICT EXPANSION           ║
                              ║   12,500 HH across 5 micro-watersheds║
                              ║   (SDMA + Multi-state replication)   ║
                              ║   ₹15-25 Cr per district             ║
                              ╚═════════════════════════════════════╝
                  ╔═══════════════════════════════════════════════════════╗
                  ║   PHASE 1 (Y1-Y3) — THIS PROJECT                       ║
                  ║   PROOF-OF-CONCEPT                                      ║
                  ║   2,500 HH in 1 micro-watershed cluster                 ║
                  ║   (NMHS / DST-NMSHE / NAFCC)                            ║
                  ║   ₹28.5 lakh investment                                 ║
                  ╚═══════════════════════════════════════════════════════╝

   Cost Reduction per Phase (marginal cost-per-household):
   • Phase 1: ₹1,140/HH (proof-of-concept)
   • Phase 2: ₹680/HH (40% reduction via shared infra, learning effects)
   • Phase 3: ₹400/HH (additional 40% reduction via scale economies)
""")

H('12.1 Four Revenue Pathways for Post-Grant Sustainability', 2)

CAP('TABLE 12.1: Sustainability Revenue Model')
TBL(['Pathway','Description','Revenue Estimate (Annual)','Activation Timeline','Probability'],
    [['CSR Consultancies','Vulnerability assessments + NbS design for hydropower, tourism, infrastructure firms (Companies Act Sec 135)','₹15-30 lakh','Y2 onwards','High (CSR mandatory)'],
     ['SDMA Implementation Grants','Scaling of demonstrated EWS across UK districts (₹47 Cr SDMA EWS allocation)','₹50 lakh - ₹2 Cr','Y3 onwards','Very High'],
     ['Multilateral Project Preparation','GCF/ADB/GFDRR consultancy for state-wide Himalayan resilience programs','₹1 Cr - ₹5 Cr per project','Y4 onwards','Medium-High (proven proof needed)'],
     ['Data-as-a-Service','Subscription access to FVI atlas + sensor data for insurance, real estate, planners','₹5-15 lakh','Y2 onwards','Medium (market development)'],
     ['','','TOTAL POTENTIAL','₹2-8 Cr/year','—']])

H('12.2 Replication Pathway Detail', 2)
P('The project deliberately produces replication-ready outputs at every stage: (i) Open-source code on GitHub with comprehensive documentation enables any district GIS officer to replicate the FVI methodology with localized data; (ii) Standardized DDMP annexure templates require only data substitution (not redesign) for other districts; (iii) IoT system designs use commodity hardware and open-source software stack (Python, PostgreSQL, MQTT) with vendor-agnostic specifications; (iv) Training curricula for SHG Task Forces are documented in bilingual format for direct deployment.')

H('12.3 Plug-and-Play DDMP Integration', 2)
P('Under DM Act 2005 Section 30, every District Disaster Management Authority must prepare a DDMP. The project deliberately formats all outputs to slot into existing DDMP chapter structures: Hazard Assessment chapter receives FVI atlas; Early Warning chapter receives IoT-EWS protocols; Community Preparedness chapter receives SHG Task Force frameworks. This eliminates the largest barrier to research-to-policy translation in India: requirement for new policy creation. District Magistrates can adopt project outputs through simple administrative orders within existing statutory frameworks.')

# ============ SECTION 13: INSTITUTIONAL SETUP ============
doc.add_page_break()
H('SECTION 13: INSTITUTIONAL SETUP AND GOVERNANCE', 1)

CAP('DIAGRAM 11: Project Organogram')
MONO("""
            ╔═══════════════════════════════════════════════════╗
            ║       PROJECT STEERING COMMITTEE                    ║
            ║  • DBS Global University (Chair)                    ║
            ║  • Funding Agency Representative (NMHS/DST/NAFCC)   ║
            ║  • SDMA Uttarakhand                                 ║
            ║  • External Expert (NIDM/IIRS/IIT)                  ║
            ╚════════════════════════╤══════════════════════════╝
                                     │
                                     ▼
            ┌─────────────────────────────────────────────┐
            │  PRINCIPAL INVESTIGATOR (PI)                 │
            │  Dr. Nidhi Rawat, Associate Professor        │
            │  Dept. of Environmental Science, DBSGU       │
            │  Role: Overall scientific & administrative   │
            │        responsibility, funder liaison        │
            └────────────┬────────────────────────────────┘
                         │
                         ▼
            ┌─────────────────────────────────────────────┐
            │  CO-PI / RESEARCH SCHOLAR                    │
            │  Raj Amritam, PhD Research Scholar           │
            │  Role: Day-to-day execution, field work,     │
            │        publications, community engagement    │
            └────────────┬────────────────────────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
  ┌──────────┐    ┌─────────────┐    ┌──────────────┐
  │  JRF/SRF │    │ Field       │    │ External     │
  │ (full-   │    │ Surveyors   │    │ Consultants  │
  │  time)   │    │ (seasonal)  │    │ (as needed)  │
  └──────────┘    └─────────────┘    └──────────────┘

  COMMUNITY-LEVEL GOVERNANCE:
  ┌──────────────────────────────────────────────┐
  │ • Gram Sabha (consultative role)              │
  │ • Van Panchayat (forest mgmt collaboration)  │
  │ • SHG Task Forces (operational implementation)│
  │ • Mukhiya Volunteers (alert relay)            │
  │ • Community Liaison Committee (5-7 members)  │
  └──────────────────────────────────────────────┘

  LIAISON ARRANGEMENTS:
  ┌──────────────────────────────────────────────┐
  │ • SDMA Uttarakhand (formal MoU)              │
  │ • DDMA Dehradun (technical collaboration)    │
  │ • Block Development Office (operational)     │
  │ • IMD/CWC (data sharing protocols)           │
  └──────────────────────────────────────────────┘
""")

CAP('TABLE 13.1: RACI Matrix — Roles & Responsibilities')
TBL(['Activity','PI','Co-PI/Scholar','JRF','SDMA','Community','Funder'],
    [['Overall direction','A','R','C','I','I','I'],
     ['Scientific quality','A','R','R','C','—','I'],
     ['Field deployment','C','A','R','I','C','I'],
     ['Community engagement','C','A','R','I','R','I'],
     ['SDMA liaison','A','R','C','R','I','I'],
     ['Publications','A','R','R','—','—','I'],
     ['Financial mgmt','A','C','—','—','—','I'],
     ['Reporting','A','R','C','I','—','R'],
     ['DDMP adoption','C','R','—','A','C','I'],
     ['Risk management','A','R','C','C','C','I']])
P('Legend: R = Responsible | A = Accountable | C = Consulted | I = Informed')

# ============ SECTION 14: COMPLIANCE ============
H('SECTION 14: COMPLIANCE, APPROVALS AND ETHICAL CLEARANCE', 1)

CAP('TABLE 14.1: Compliance Checklist')
TBL(['Compliance Area','Specific Requirement','Status','Verification'],
    [['DM Act 2005','Sec 30/31 alignment for DDMP integration','Built into design','Sec 31 referenced'],
     ['Sendai Framework','Targets A, B, C, D, G alignment','All 5 addressed','Logframe mapping'],
     ['NAPCC','National Water Mission alignment','Direct contribution','Mission docs'],
     ['Companies Act 2013 Sec 135','CSR pathway compatibility','Designed in','Pathway documented'],
     ['IT Act 2000 + DPDP 2023','Data privacy, anonymization','Aggregate data only','Protocol documented'],
     ['Institutional Ethics','DBSGU IEC clearance','To be obtained M1','Application drafted'],
     ['Forest Conservation','No FCA clearance needed (no diversion)','Confirmed','Site analysis'],
     ['Wildlife Protection Act','No PA clearance needed','Confirmed','Site outside PAs'],
     ['Local consent','Gram Sabha resolutions','To be obtained M1-3','Format prepared'],
     ['Foreign exchange','No foreign funds; no FCRA','N/A','Domestic funder']])

P('All required clearances will be secured during the project inception phase (Months 1-3) before any field intervention begins. The PI maintains a compliance register reviewed quarterly by the Steering Committee. The Institutional Ethics Committee at DBS Global University will review research protocols involving human subjects (community surveys, FGDs, validation workshops).')

# ============ SECTION 15: ANNEXURES REFERENCE ============
H('SECTION 15: ANNEXURES (Reference List)', 1)
P('The following annexures accompany this proposal as separate documents (available on request):')
B('Annexure A: Curriculum Vitae of Principal Investigator (Dr. Nidhi Rawat)')
B('Annexure B: Curriculum Vitae of Co-PI (Raj Amritam)')
B('Annexure C: Institutional Endorsement Letter from DBS Global University')
B('Annexure D: Letter of Support from SDMA Uttarakhand (in process)')
B('Annexure E: Equipment Quotations from approved vendors')
B('Annexure F: Detailed AHP Expert Panel CVs (8 experts)')
B('Annexure G: Sample Community Consent Forms (Hindi/English bilingual)')
B('Annexure H: Detailed Bill of Quantities for NbS Pilot')
B('Annexure I: Software License Documentation (open-source primarily)')
B('Annexure J: Risk Management Detailed Protocols')
B('Annexure K: Publication Pipeline with Target Journals & Editorial Boards')
B('Annexure L: Letters of Collaboration (Van Panchayat, Gram Sabha, SHGs - to be secured)')

# ============ DECLARATION ============
doc.add_page_break()
H('DECLARATION AND SIGNATURES', 1)

P('We, the undersigned, hereby declare that the information provided in this Grant Project Funding Proposal is true, accurate, and complete to the best of our knowledge and belief. We confirm that:')
B('The proposed project has not received duplicate funding from any other source for the same activities.')
B('All budget items represent genuine estimated costs verified through current market quotations.')
B('The institutional infrastructure and human resources described are available and committed.')
B('Funds will be utilized exclusively for the purposes outlined in this proposal.')
B('Proper accounts and records will be maintained per funding agency guidelines.')
B('Necessary institutional approvals, ethical clearances, and administrative permissions will be obtained before commencing field activities.')
B('Periodic progress reports, financial statements, and utilization certificates will be submitted as required.')
B('All project outputs (data, publications, tools, frameworks) will be made available in open-access formats for maximum societal benefit.')
B('The research will be conducted with the highest standards of scientific integrity, community respect, and environmental responsibility.')

doc.add_paragraph('')
doc.add_paragraph('')
sigt = doc.add_table(rows=4, cols=2)
sigt.rows[0].cells[0].text = 'Principal Investigator:'
sigt.rows[0].cells[1].text = 'Co-Principal Investigator:'
for r in sigt.rows[0].cells[0].paragraphs[0].runs: r.bold=True
for r in sigt.rows[0].cells[1].paragraphs[0].runs: r.bold=True
sigt.rows[1].cells[0].text = ''
sigt.rows[1].cells[1].text = ''
sigt.rows[2].cells[0].text = '________________________'
sigt.rows[2].cells[1].text = '________________________'
sigt.rows[3].cells[0].text = 'Dr. Nidhi Rawat\nAssociate Professor\nDept. of Environmental Science\nDBS Global University, Dehradun'
sigt.rows[3].cells[1].text = 'Raj Amritam\nPhD Research Scholar\nDept. of Environmental Science\nDBS Global University, Dehradun'

doc.add_paragraph('')
doc.add_paragraph('')
P('Date: ____________ | Place: Dehradun, Uttarakhand, India')
doc.add_paragraph('')
P('Institutional Endorsement Stamp:')
doc.add_paragraph('')
P('________________________________________')
P('(Vice-Chancellor / Registrar, DBS Global University)')

doc.save('/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx')
print("All sections + declaration added")
print()
text = ' '.join([p.text for p in doc.paragraphs])
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text += ' ' + cell.text
print(f"FINAL Word count: {len(text.split())}")
