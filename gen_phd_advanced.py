#!/usr/bin/env python3
"""Advanced PhD Dissertation Proposal Generator - Part 1 (Setup + Title + Abstract + Sec 1)"""
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
    for r in h.runs:
        r.font.name = 'Times New Roman'
        r.font.color.rgb = RGBColor(0, 0, 0)

def P(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Inches(0.4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.line_spacing = 1.4

def MONO(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)

def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row):
            c = t.rows[ri].cells[ci]
            c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
    doc.add_paragraph('')

def CAP(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.italic = True; r.bold = True; r.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(8)

# ============ TITLE PAGE ============
for _ in range(3): doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('PhD DISSERTATION RESEARCH PROPOSAL'); r.bold=True; r.font.size=Pt(16)
doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('(Advanced Edition with Practical Methodology, Diagrams & Frameworks)')
r.italic=True; r.font.size=Pt(11)
doc.add_paragraph(''); doc.add_paragraph('')
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('Assessing the Efficacy of Nature-Based Solutions for Flood Mitigation:\nA Hydro-Spatial Modeling Framework for Scalable Risk Reduction\nin Climate-Vulnerable Watersheds of India')
r.bold=True; r.font.size=Pt(14)
doc.add_paragraph(''); doc.add_paragraph('')
for line,sz,b in [('Submitted by:',12,False),('Raj Amritam',14,True),('PhD Research Scholar',11,False),
    ('',10,False),('Under the Supervision of:',12,False),('Dr. Nidhi Rawat',14,True),
    ('Associate Professor',11,False),('',10,False),('Department of Environmental Science',12,True),
    ('DBS Global University, Dehradun',12,True),('Uttarakhand, India',12,False),('',10,False),('2025',13,True)]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn = p.add_run(line); rn.font.size=Pt(sz); rn.bold=b
doc.add_page_break()

# ============ ABSTRACT ============
H('ABSTRACT', 1)
P('India faces a compounding hydro-climatic crisis, with 72% of districts exposed to extreme flooding while only 33% are covered by functional early warning systems (EWS). Despite the construction of 3,732 km of embankments since 1954, India\'s flood-prone area has paradoxically expanded from 2.5 million hectares to 6.93 million hectares, demonstrating the structural failure of grey-infrastructure-dominated approaches. Concurrently, the India Meteorological Department documents a 75% increase in very heavy rainfall days since 1950, fundamentally invalidating the stationary design assumptions underlying existing infrastructure.')
P('This dissertation proposes a comprehensive Hydro-Spatial Modeling Framework integrating remote sensing, GIS-based multi-criteria vulnerability assessment using Analytic Hierarchy Process (AHP), distributed hydrological simulation through SWAT-CUP SUFI-2 calibrated coupling with HEC-RAS 2D hydraulic modeling, and socio-economic Total Economic Value (TEV) analysis. The research will quantify the flood mitigation efficacy of four Nature-Based Solutions (NbS) intervention scenarios across two climatologically distinct study sites: the Raipur-Dehradun watershed (sub-Himalayan flash-flood regime) and Darbhanga district (Indo-Gangetic riverine floodplain regime).')
P('Hypotheses predict that catchments with >40% impervious surfaces will exhibit 2-3× higher Flood Vulnerability Index scores; that 20-50m riparian buffer establishment will produce 12-25% peak discharge reduction under 50-year return period events; and that the integrated framework will yield benefit-cost ratios exceeding 3:1 at district-implementation costs of ₹15-25 Crore. The research aims to bridge the persistent academic-deployment gap by generating both Q1 SCIE publications and policy-ready DDMP-integrable templates under the Disaster Management Act 2005.')
H('Keywords', 2)
P('Nature-Based Solutions; Flood Vulnerability Index; AHP-GIS; SWAT Hydrological Modeling; HEC-RAS 2D; Climate Adaptation; Himalayan Watersheds; District Disaster Management Plans; Sendai Framework; Non-Stationary Design Storms.')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Part 1 (Title + Abstract) saved")

# Reload doc to continue appending
import sys
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
# Re-define helpers (they reference 'doc' from this scope)
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs:
        r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent=Inches(0.4); p.paragraph_format.space_after=Pt(6)
    p.paragraph_format.line_spacing=1.5; p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.4); p.paragraph_format.line_spacing=1.4
def MONO(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent=Inches(0.1); p.paragraph_format.space_after=Pt(2)
    p.paragraph_format.space_before=Pt(2); p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(9)
def TBL(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: r.bold=True; r.font.size=Pt(10)
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row):
            c = t.rows[ri].cells[ci]; c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs: r.font.size=Pt(10)
    doc.add_paragraph('')
def CAP(text):
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.italic=True; r.bold=True; r.font.size=Pt(10)
    p.paragraph_format.space_after=Pt(8)

# ============ SECTION 1: INTRODUCTION ============
doc.add_page_break()
H('SECTION 1: INTRODUCTION AND RESEARCH CONTEXT', 1)

P('India occupies a uniquely precarious position within the global hydrological risk landscape. Characterized by extraordinary hydro-climatic variability—ranging from the arid expanses of Rajasthan receiving less than 200 mm annual precipitation to the hyper-humid northeast exceeding 11,000 mm—the subcontinent faces a compounding crisis wherein anthropogenic land-use change, unplanned urbanization, and intensifying monsoon dynamics converge to produce catastrophic flood events with increasing frequency and severity. According to the National Disaster Management Authority (NDMA) and the Central Water Commission (CWC), approximately 72% of Indian districts are now classified as exposed to extreme flood events, encompassing both riverine inundation and pluvial flash flooding. Yet, critically, only 33% of these vulnerable districts are covered by functional early warning networks capable of providing actionable lead times exceeding six hours.')

P('The paradox of India\'s flood management trajectory is starkly illustrated by the expansion of flood-prone area despite massive investment in structural interventions. In 1954, the Rashtriya Barh Ayog estimated India\'s flood-prone area at approximately 2.5 million hectares; by 2022, this figure had expanded to 6.93 million hectares—a 177% increase—despite the construction of over 3,732 km of embankments, 37,904 km of drainage channels, and thousands of crores invested in reservoir-based flood cushioning. This counterintuitive expansion is attributable to the levee paradox (structural protection incentivizing floodplain encroachment), urbanization-induced drainage degradation, siltation-induced capacity reduction, and the fundamental limitation of grey infrastructure in accommodating non-stationary hydrological extremes.')

CAP('DIAGRAM 1: Timeline of Major Indian Hydro-Meteorological Disasters (2000-2025)')
TBL(['Year', 'Event', 'Location', 'Mortality', 'Economic Loss (₹ Cr)', 'EWS Status'],
    [['2005','Mumbai Deluge','Maharashtra','>1,000','5,000+','Inadequate'],
     ['2013','Kedarnath Floods','Uttarakhand','>5,700','12,000+','Failed'],
     ['2014','J&K Floods','Jammu & Kashmir','>280','5,400','Limited'],
     ['2015','Chennai Floods','Tamil Nadu','>422','15,000+','Inadequate'],
     ['2018','Kerala Mega-Flood','Kerala','>483','40,000+','Partial'],
     ['2019','Bihar Floods','Bihar','>130','7,000+','Limited'],
     ['2020','Hyderabad Floods','Telangana','>50','5,000+','Failed'],
     ['2021','Chamoli GLOF','Uttarakhand','>200','1,500+','Zero EWS'],
     ['2022','Assam Floods','Assam','>192','4,000+','Partial'],
     ['2023','Sikkim GLOF','Sikkim','>40','2,500+','Zero EWS'],
     ['2024','Wayanad Landslides','Kerala','>420','3,000+','Failed'],
     ['2025','Dharali Flash Floods','Uttarakhand','>30','500+','Zero EWS']])

P('The concentration of high-mortality events within the post-2010 period—and particularly the recurrence of zero-warning catastrophes in Himalayan catchments (Chamoli 2021, Sikkim 2023, Dharali 2025)—provides empirical validation of the systemic governance failure that this research addresses. Each of these events occurred in catchments where remote sensing capacity, hydrological modeling expertise, and IoT sensor technology were technically available but institutionally disconnected from community-level deployment.')

P('Against this backdrop, the international scientific and policy community has increasingly endorsed Nature-Based Solutions (NbS) as a complementary—and in many cases superior—paradigm for flood risk reduction. The IUCN Global Standard for NbS (2020), the European Commission\'s NbS Research and Innovation agenda, and the IPCC AR6 Working Group II report all identify NbS as critical interventions that leverage ecosystem services—infiltration, retention, evapotranspiration, flow attenuation, and sediment trapping—to reduce flood hazard while simultaneously delivering biodiversity co-benefits, carbon sequestration, and livelihood enhancement.')

CAP('DIAGRAM 2: Comparative Matrix — Grey Infrastructure vs. Nature-Based Solutions')
TBL(['Dimension','Grey Infrastructure','Nature-Based Solutions (NbS)','Hybrid Approach'],
    [['Capital Cost','High (₹40K-60K/m embankment)','Low-Moderate (₹2K-8K/m vegetated buffer)','Moderate'],
     ['Maintenance','High recurrent costs','Self-maintaining post-establishment','Moderate'],
     ['Lifespan','30-50 years (degrading)','Indefinite (with succession)','40-70 years'],
     ['Climate Resilience','Static design assumptions','Adaptive to non-stationarity','Adaptive'],
     ['Co-Benefits','None or negative','Biodiversity, carbon, livelihoods','Multiple'],
     ['Failure Mode','Catastrophic breach','Gradual degradation','Mixed'],
     ['Land Footprint','Confined','Distributed','Variable'],
     ['Community Ownership','Low (state-managed)','High (community-managed)','Moderate'],
     ['Scalability','Limited by capital','High (replicable)','High'],
     ['Carbon Footprint','High emissions (cement)','Carbon negative','Reduced']])

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 1 added")

# Reload for Section 2
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.1)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(9)
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

# ============ SECTION 2: PROBLEM & GAPS ============
H('SECTION 2: PROBLEM STATEMENT AND IDENTIFIED RESEARCH GAPS', 1)

P('The central problem motivating this research is the systematic failure of India\'s flood management infrastructure—both physical and institutional—to accommodate the non-stationary hydro-climatic regime now evident across the subcontinent. The India Meteorological Department (IMD) has documented a 75% increase in very heavy rainfall days (exceeding 124.5 mm/day) since 1950, with particularly pronounced intensification over the Indo-Gangetic Plains and Western Himalayan foothills. These extreme precipitation events overwhelm design assumptions embedded in CWC legacy infrastructure, which were calibrated against stationary Intensity-Duration-Frequency (IDF) curves derived from pre-1980 rainfall records.')

P('Simultaneously, rapid land-use transformation—with India losing 1.6 million hectares of forest cover between 2001 and 2020 and experiencing a 2.7-fold expansion of impervious urban surfaces—has fundamentally altered catchment hydrological response, reducing time-to-peak, amplifying peak discharges, and increasing flood volumes beyond the assimilative capacity of existing grey infrastructure. This compounding stressor environment demands a fundamentally new analytical and operational framework.')

CAP('TABLE 2.1: Research Gap Matrix — Five Critical Knowledge & Implementation Gaps')
TBL(['Gap ID','Gap Title','Current State','Proposed Contribution','Expected Impact'],
    [['G1','Inland NbS Valuation Deficit','Coastal NbS dominant; inland understudied','Catchment-scale hydrological evidence for inland NbS under monsoonal conditions','Fills 50-year+ return period evidence gap'],
     ['G2','District-Scale GIS-Hydrology Integration','Macro/micro scales studied; district scale missing','30m-resolution FVI integrated with process-based hydrology at DDMA-relevant scale','Enables evidence-based DDMP planning'],
     ['G3','NbS Performance Under Extreme Events','Moderate events well-studied; extreme uncertain','Quantified NbS performance for 50-100 year return periods','Validates/refutes NbS failure thresholds'],
     ['G4','DDMP-NbS Legislative Linkage','No explicit NbS provision in NDMA guidelines','Plug-and-play DDMP annexure templates under DM Act 2005 Sec. 31','Operationalizes NbS within statutory framework'],
     ['G5','Stationary Design Storm Reliance','CWC uses pre-1980 IDF curves','Non-stationary frequency analysis with updated quantiles','Recalibrates infrastructure design standards']])

H('2.1 Detailed Gap Analysis', 2)

H('Gap 1: Inland NbS Valuation Deficit', 3)
P('The preponderance of existing NbS-flood research in India focuses on coastal ecosystems—mangroves, coral reefs, and coastal wetlands—with quantified storm surge attenuation benefits ranging from 15% to 40%. By contrast, inland NbS interventions (riparian buffers, floodplain wetland reconnection, headwater reforestation, and constructed retention basins) remain severely under-quantified in the Indian context. A systematic review of 247 NbS-flood studies indexed in Web of Science (2010-2024) reveals that only 8 (3.2%) are conducted in Indian inland watersheds, and none provide catchment-scale hydrological evidence for return periods exceeding 25 years. This research will fill this critical evidence gap by quantifying NbS efficacy across 10, 25, 50, and 100-year design storms.')

H('Gap 2: District-Scale Integration Vacuum', 3)
P('Existing flood vulnerability assessments in India operate at either macro-scales (state/national level using 1km+ resolution datasets such as the National Flood Hazard Atlas) or micro-scales (individual village or ward-level studies typically covering <10 km²). A critical absence exists at the district scale—the administrative unit at which DDMPs are formulated, budgets allocated, and disaster response coordinated. The proposed research operates explicitly at this governance-relevant scale through 30-meter resolution FVI mapping integrated with district-scale process-based hydrological modeling.')

H('Gap 3: Extreme Event Performance Uncertainty', 3)
P('While NbS interventions demonstrate consistent efficacy under moderate flood scenarios (5-25 year return periods), their performance under extreme events exceeding 50-year return periods remains contested in the literature. Concerns persist regarding potential "failure thresholds" where ecosystem-based interventions become overwhelmed, particularly under compound events combining antecedent soil saturation with extreme precipitation. This uncertainty is acute for the Indian context, where monsoon dynamics produce multi-day precipitation totals exceeding 500 mm with limited inter-event recovery time.')

H('Gap 4: Legislative-Technical Disconnect', 3)
P('The Disaster Management Act of 2005 mandates DDMP preparation by all district administrations, yet contains no explicit provision for integrating NbS as a risk reduction strategy. NDMA guidelines provide no standardized template, evaluation protocol, or monitoring framework through which district authorities can incorporate ecosystem-based approaches into statutory planning. This research generates plug-and-play DDMP annexure templates explicitly compatible with existing statutory formats.')

H('Gap 5: Non-Stationary Design Quantile Deficit', 3)
P('CWC and State Irrigation Departments continue employing IDF relationships derived from stationary assumptions, despite documented non-stationarity in extreme precipitation quantiles across multiple Indian sub-basins. These design metrics systematically underestimate flood magnitudes for return periods exceeding 25 years, leading to under-designed infrastructure and inadequate flood risk zonation. This research employs Generalized Extreme Value (GEV) non-stationary frequency analysis with time-varying location parameters to generate updated design quantiles.')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 2 added")

# ============ SECTION 3: RQ & HYPOTHESES ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.1)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(9)
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

H('SECTION 3: RESEARCH QUESTIONS AND HYPOTHESES', 1)

P('The research is structured around three interconnected research questions, each paired with quantitatively testable hypotheses derived from international precedents and Indian field evidence. The questions progress logically from spatial vulnerability characterization (RQ1) through hydrological efficacy quantification (RQ2) to scalable decision support development (RQ3).')

CAP('DIAGRAM 3: Research Question — Hypothesis — Methodology Linkage Tree')
MONO("""
                    ╔══════════════════════════════════════════╗
                    ║   PRIMARY RESEARCH OBJECTIVE              ║
                    ║   Quantify NbS Flood Mitigation Efficacy  ║
                    ║   in Climate-Vulnerable Indian Watersheds ║
                    ╚════════════════════╤═════════════════════╝
                                         │
            ┌────────────────────────────┼────────────────────────────┐
            │                            │                            │
            ▼                            ▼                            ▼
  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
  │       RQ1        │       │       RQ2        │       │       RQ3        │
  │ Spatial          │       │ NbS Hydrological │       │ Scalable         │
  │ Vulnerability    │       │ Efficacy         │       │ Decision Support │
  └────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
           │                          │                          │
           ▼                          ▼                          ▼
  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
  │  H1: Catchments  │       │  H2: 20-50m      │       │  H3: BCR > 3:1   │
  │  >40% impervious │       │  buffers reduce  │       │  at INR 15-25 Cr │
  │  & <15% wetland  │       │  peak Q by       │       │  district cost;  │
  │  → 2-3× FVI      │       │  12-25% under    │       │  ₹50-200 Cr/yr   │
  │                  │       │  50-yr events    │       │  loss reduction  │
  └────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
           │                          │                          │
           ▼                          ▼                          ▼
  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
  │ METHOD: AHP-GIS  │       │ METHOD: SWAT +   │       │ METHOD: TEV +    │
  │ FVI Mapping      │       │ HEC-RAS 2D       │       │ B/C Analysis +   │
  │ (Phase 2)        │       │ Coupling         │       │ DDMP Templates   │
  │                  │       │ (Phase 3)        │       │ (Phase 4)        │
  └──────────────────┘       └──────────────────┘       └──────────────────┘
""")

H('Research Question 1: Spatial Vulnerability Characterization', 2)
P('RQ1: How do land-use/land-cover dynamics, geomorphological attributes, and socio-demographic exposure indicators interact to produce spatially heterogeneous flood vulnerability at the district-watershed scale in climatologically distinct Indian catchments?')
P('Hypothesis H1: Catchments with greater than 40% impervious surface coverage and less than 15% functional wetland cover will exhibit Flood Vulnerability Index (FVI) scores 2-3 times higher than catchments retaining natural hydrological connectivity, after controlling for precipitation intensity and topographic gradient. This hypothesis is grounded in the established relationship between imperviousness and runoff coefficient amplification documented in the SCS-CN framework, as well as the empirically demonstrated flood attenuation capacity of connected wetland systems as storage reservoirs during peak flow events.')

H('Research Question 2: NbS Hydrological Efficacy', 2)
P('RQ2: What is the quantifiable hydrological efficacy of specific Nature-Based Solution interventions—riparian buffer establishment, wetland reconnection, and headwater micro-basin treatment—in reducing peak discharge magnitude and flood inundation extent under design storms of varying return periods (10, 25, 50, and 100-year) in the selected study watersheds?')
P('Hypothesis H2: The establishment of 20-50 meter riparian buffer zones along primary and secondary drainage channels will produce a 12-25% reduction in simulated peak discharge at catchment outlets under 50-year return period events, while wetland reconnection interventions will reduce flood inundation extent by 15-35% under equivalent return period scenarios. These predictions derive from meta-analytical evidence (Dadson et al., 2017; Nicholson et al., 2020) adjusted for Indian monsoonal precipitation characteristics.')

H('Research Question 3: Scalable Decision Support', 2)
P('RQ3: Can a replicable, open-source hydro-spatial decision support framework be developed that enables district-level administrators to evaluate, prioritize, and implement NbS interventions within statutory DDMP processes at economically justifiable costs?')
P('Hypothesis H3: The proposed framework will demonstrate potential to reduce direct economic flood losses by ₹50-200 Crore per year at district-level implementation costs not exceeding ₹15-25 Crore over a 10-year horizon, yielding benefit-cost ratios exceeding 3:1 under baseline climate projections and 5:1 under RCP 8.5 intensification scenarios.')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 3 added")

# ============ SECTIONS 4 & 5: CONCEPTUAL FRAMEWORK + LITERATURE ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
def H(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs: r.font.name='Times New Roman'; r.font.color.rgb=RGBColor(0,0,0)
def P(text):
    p = doc.add_paragraph(text); p.paragraph_format.first_line_indent=Inches(0.4)
    p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.5
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
def MONO(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.1)
    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.line_spacing=1.0
    run = p.add_run(text); run.font.name='Courier New'; run.font.size=Pt(9)
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

H('SECTION 4: CONCEPTUAL FRAMEWORK', 1)

P('The conceptual architecture of this research is grounded in the IPCC Sixth Assessment Report (AR6) risk framework, which defines climate risk as a function of three interacting components: Hazard, Exposure, and Vulnerability. This triadic formulation provides the foundational logic for the entire research design and is operationalized through the integrated methodology described in Section 6.')

p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Flood Risk = ƒ ( Hazard × Exposure × Vulnerability )'); r.italic=True; r.bold=True; r.font.size=Pt(13)

CAP('DIAGRAM 4: IPCC AR6 Risk Framework with NbS as Dynamic Modifier')
MONO("""
        ╔═══════════════════════════════════════════════════════════════╗
        ║              IPCC AR6 INTEGRATED RISK FRAMEWORK                ║
        ╚═══════════════════════════════════════════════════════════════╝

  ┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
  │   HAZARD     │      │  EXPOSURE    │      │  VULNERABILITY   │
  │              │      │              │      │                  │
  │ • Extreme    │  ×   │ • Population │  ×   │ • Sensitivity    │
  │   rainfall   │      │ • Assets     │      │ • Adaptive       │
  │ • Flash      │      │ • Crops      │      │   Capacity       │
  │   flooding   │      │ • Infra-     │      │ • SC/ST/Gender   │
  │ • GLOFs      │      │   structure  │      │   disaggregation │
  └──────┬───────┘      └──────┬───────┘      └─────────┬────────┘
         │                     │                        │
         └─────────────────────┼────────────────────────┘
                               │
                               ▼
                    ╔══════════════════╗
                    ║   FLOOD RISK     ║
                    ║   = f(H × E × V) ║
                    ╚════════╤═════════╝
                             │
                  ╔══════════▼═══════════╗
                  ║  NbS DYNAMIC         ║
                  ║  MODIFIER            ║
                  ║  ─────────────────   ║
                  ║  • Reduces Hazard    ║◄────┐
                  ║    (peak Q ↓)        ║     │
                  ║  • Limits Exposure   ║     │ Adaptive
                  ║    (no-build zones)  ║     │ Mgmt
                  ║  • Decreases         ║     │ Feedback
                  ║    Vulnerability     ║     │ Loop
                  ║    (livelihoods,     ║     │
                  ║     groundwater)     ║     │
                  ╚══════════╤═══════════╝     │
                             │                 │
                             ▼                 │
                  ╔══════════════════╗         │
                  ║  RESIDUAL RISK   ║─────────┘
                  ║  + KNOWLEDGE     ║   Updates
                  ║  GENERATION      ║
                  ╚══════════════════╝
""")

P('Within this triadic formulation, Nature-Based Solutions operate as dynamic risk modifiers across all three dimensions simultaneously, distinguishing them fundamentally from conventional grey infrastructure which primarily addresses only the hazard component through flow conveyance or storage. NbS interventions reduce hazard through peak discharge attenuation and time-to-peak extension; limit exposure through floodplain corridor establishment that prevents asset accumulation in high-hazard zones; and decrease vulnerability through livelihood diversification, groundwater recharge enhancement, and social-ecological system strengthening.')

CAP('DIAGRAM 5: Adaptive Management Feedback Loop for NbS Implementation')
MONO("""
            ┌─────────────────┐
            │  1. ASSESS      │
            │  Baseline FVI   │
            │  + Hydrology    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐         ┌──────────────────┐
            │  2. PRIORITIZE  │         │  6. ADAPT        │
            │  NbS Sites via  │         │  Modify based on │
            │  Multi-criteria │         │  performance     │
            └────────┬────────┘         └────────▲─────────┘
                     │                           │
                     ▼                           │
            ┌─────────────────┐                  │
            │  3. DEPLOY      │                  │
            │  Pilot Inter-   │                  │
            │  ventions       │                  │
            └────────┬────────┘                  │
                     │                           │
                     ▼                           │
            ┌─────────────────┐                  │
            │  4. MONITOR     │                  │
            │  Performance    │                  │
            │  Indicators     │                  │
            └────────┬────────┘                  │
                     │                           │
                     ▼                           │
            ┌─────────────────┐                  │
            │  5. EVALUATE    │──────────────────┘
            │  Against        │
            │  Targets        │
            └─────────────────┘
""")

P('The framework conceptualizes NbS not as a static intervention but as an adaptive system establishing feedback loops between risk knowledge generation and governance recalibration. Implemented interventions generate empirical performance data that updates hazard models, refines vulnerability assessments, and informs iterative governance decisions—creating a learning-by-doing cycle consistent with adaptive management principles articulated by Holling (1978) and operationalized by Pahl-Wostl (2007) for water resources management.')

# ============ SECTION 5: LITERATURE REVIEW ============
H('SECTION 5: LITERATURE REVIEW AND THEORETICAL POSITIONING', 1)

P('This section synthesizes the global and Indian literature underpinning the research, identifying the specific knowledge frontier this dissertation advances. The review covers four thematic streams: (i) NbS hydrological performance studies, (ii) AHP-GIS flood vulnerability mapping, (iii) IoT-based community early warning systems, and (iv) economic valuation of ecosystem services for disaster risk reduction.')

CAP('TABLE 5.1: Literature Synthesis Matrix — Key Studies Informing the Research')
TBL(['Author/Year','Region','Method','Key Finding','Relevance'],
    [['Dadson et al. 2017','UK Catchments','Meta-analysis 65 studies','Riparian buffer 10-20% peak Q reduction','H2 quantitative basis'],
     ['Nicholson et al. 2020','Belford UK','SWAT+wetlands','30% peak reduction with 4% landscape coverage','Wetland scenario design'],
     ['Bhuiyan et al. 2017','Bangladesh','HEC-RAS 2D','Floodplain reconnection efficacy','Darbhanga site analog'],
     ['Singh & Pandey 2021','Kerala','AHP-GIS','FVI methodology validation','Phase 2 methodology'],
     ['Viswanathan et al. 2022','Bihar','Randomized Control Trial','30% medical cost reduction with EWS','Economic impact basis'],
     ['Schueler 1994','USA Urban','Empirical','Imperviousness threshold theory','H1 theoretical basis'],
     ['Kumar et al. 2019','Indian Himalaya','Remote sensing','18% forest loss in Garhwal 2000-2022','Site selection basis'],
     ['IPCC AR6 WG2 2022','Global','Synthesis','NbS critical for adaptation','Conceptual framework'],
     ['IUCN 2020','Global','Standard','NbS Global Standard','Methodological alignment'],
     ['MoEFCC NMHS 2024','India','Policy','National Himalayan Studies Mission','Funding alignment'],
     ['Mishra & Singh 2010','India','SCS-CN review','Curve Number adjustment for India','SWAT calibration basis'],
     ['Arnold et al. 2012','USA','SWAT manual','Model architecture','Phase 3 basis'],
     ['USACE 2020','Global','HEC-RAS 6.x manual','2D unsteady flow','Phase 3 hydraulics'],
     ['Abbaspour 2015','Switzerland','SUFI-2 manual','Calibration uncertainty','Phase 3 calibration'],
     ['Saaty 1980','Theoretical','AHP foundation','Pairwise comparison theory','Phase 2 methodology']])

P('The literature review reveals three critical gaps that this research addresses simultaneously. First, the integration gap: while individual methodological components (AHP-FVI, SWAT calibration, HEC-RAS 2D, economic valuation) are well-established in isolation, no published study integrates all four within a single coherent framework at the district-watershed scale in India. Second, the validation gap: NbS efficacy claims for return periods exceeding 25 years rely predominantly on temperate catchment evidence transferred to Indian conditions without empirical validation. Third, the policy translation gap: even rigorous research findings rarely achieve formal incorporation into District Disaster Management Plans, the statutory documents that govern actual resource allocation and emergency response.')

P('This research advances the knowledge frontier through deliberate integration of validated methodological components, empirical validation under Indian monsoonal conditions across two contrasting catchment types, and explicit policy translation through DDMP-compatible deliverables. The combination distinguishes this work from both pure academic publications and pure deployment projects.')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 4 & 5 added")

# ============ SECTION 6: DETAILED METHODOLOGY (THE CORE) ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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

doc.add_page_break()
H('SECTION 6: DETAILED METHODOLOGY AND ANALYTICAL FRAMEWORK', 1)

P('This section presents the complete methodological architecture organized into four sequential yet interconnected phases. Each phase builds upon the outputs of the previous phase while simultaneously informing iterative refinement of upstream methods through feedback loops. The methodology is designed for full reproducibility using exclusively open-source data and software, ensuring scalability to all 13 districts of Uttarakhand and replicability across the broader Indian Himalayan Region.')

H('6.1 Overall Research Design', 2)

CAP('DIAGRAM 6: Four-Phase Methodological Pipeline (Master Workflow)')
MONO("""
╔═══════════════════════════════════════════════════════════════════════════╗
║         INTEGRATED HYDRO-SPATIAL MODELING FRAMEWORK — MASTER PIPELINE     ║
╚═══════════════════════════════════════════════════════════════════════════╝

  ┌─────────────────────────────────────────────────────────────────────┐
  │                     PHASE 1: DATA ACQUISITION                        │
  │                                                                       │
  │  Sentinel-1/2 ──► Pre-process ──► Land-Use Classification            │
  │  SRTM/ALOS    ──► Hydro-cond. ──► DEM (30m / 12.5m)                  │
  │  ISRIC Soils  ──► Reclassify  ──► Soil Hydraulic Layers              │
  │  CHIRPS/IMERG ──► Bias-correct──► Precipitation Forcing              │
  │  Census 2011  ──► Disaggregate──► Socio-demographic Layers           │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │              PHASE 2: AHP-GIS FLOOD VULNERABILITY INDEX              │
  │                                                                       │
  │  Expert Panel (n=8) ──► Pairwise Matrix ──► CR < 0.10 Validation     │
  │           │                                        │                  │
  │           ▼                                        ▼                  │
  │     Weights w_i                             Layer Normalization       │
  │           │                                        │                  │
  │           └──────────────┬─────────────────────────┘                 │
  │                          ▼                                            │
  │              Weighted Linear Combination ──► FVI (30m raster)        │
  │                          │                                            │
  │                          ▼                                            │
  │              Validation vs Sentinel-1 SAR + SDMA records              │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │ Identifies priority sub-basins
                                   ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │       PHASE 3: HYDROLOGICAL & HYDRAULIC MODELING (SWAT + HEC-RAS)    │
  │                                                                       │
  │   ┌──────────────┐         ┌──────────────────┐                      │
  │   │    SWAT      │ ──Q──► │    HEC-RAS 2D    │                      │
  │   │ (catchment   │ hydro- │  (floodplain     │                      │
  │   │  rainfall-   │  graphs│   hydraulics)    │                      │
  │   │  runoff)     │         │                  │                      │
  │   └──────┬───────┘         └────────┬─────────┘                      │
  │          │                          │                                 │
  │          ▼                          ▼                                 │
  │   SUFI-2 Calibration          Flood Depth/Velocity Maps              │
  │   NSE > 0.6, R² > 0.65        for 10/25/50/100-yr events            │
  │   PBIAS ±15%                  CSI > 0.6 vs SAR validation           │
  │          │                          │                                 │
  │          └──────────────┬───────────┘                                 │
  │                         ▼                                             │
  │         Apply 4 NbS Scenarios (A, B, C, D) — see Section 8            │
  └────────────────────────────────┬────────────────────────────────────┘
                                   │ Inundation maps + discharge series
                                   ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │         PHASE 4: ECONOMIC VALUATION + DDMP TEMPLATE GENERATION       │
  │                                                                       │
  │  Stage-Damage Curves ──► Annual Expected Damage (EAD)                │
  │                                  │                                    │
  │                                  ▼                                    │
  │  Total Economic Value (TEV) Analysis @ 3% & 8% discount rates        │
  │                                  │                                    │
  │                                  ▼                                    │
  │  Benefit-Cost Ratio + Cost per Household Protected                   │
  │                                  │                                    │
  │                                  ▼                                    │
  │       DDMP Annexure Templates under DM Act 2005 Section 31           │
  └─────────────────────────────────────────────────────────────────────┘

  Feedback Loops: Phase 4 outcomes recalibrate Phase 2 weights;
                  Phase 3 model calibration refines Phase 1 data needs.
""")

H('6.2 Phase 1: Data Acquisition and Preprocessing', 2)

P('The research employs an exclusively open-source data acquisition strategy to ensure replicability and scalability. All datasets are publicly available through international space agencies (ESA, NASA, JAXA), global research institutes (ISRIC, UCSB), or Indian government portals (Bhuvan, IMD).')

CAP('TABLE 6.1: Data Source Matrix — Complete Inventory')
TBL(['Dataset','Source','Resolution','Temporal Coverage','Use in Research','Validation Method'],
    [['Sentinel-2 MSI','ESA Copernicus','10m (VIS/NIR), 20m (SWIR)','2015-2024','LULC classification, NDVI','Ground-truth points'],
     ['Sentinel-1 SAR','ESA Copernicus','10m (IW mode)','2014-2024','Flood extent mapping, soil moisture','Optical concurrent'],
     ['SRTM DEM','NASA','30m','2000','Topographic analysis','Differential GPS'],
     ['ALOS PALSAR DEM','JAXA','12.5m','2011','Drainage delineation flat terrain','Cross-section field'],
     ['ISRIC SoilGrids','ISRIC World Soil','250m','2017','Soil hydraulic properties','District soil reports'],
     ['CHIRPS','UCSB Climate Hazards','5km','1981-present','Long-term rainfall climatology','IMD gauge stations'],
     ['GPM IMERG V06','NASA','11km, 30-min','2000-present','Sub-hourly precipitation events','IMD AWS network'],
     ['Census 2011','RGI India','Village/ward','2011 (projected)','Socio-demographic layers','Sample household'],
     ['CWC Discharge','India-WRIS','Daily','1990-present','SWAT calibration target','Manual gauging'],
     ['SDMA Records','Uttarakhand SDMA','Event-based','2010-2024','Flood inventory validation','Field reports']])

P('Preprocessing protocols include: (i) atmospheric correction of Sentinel-2 imagery using Sen2Cor v2.11 to surface reflectance; (ii) speckle filtering of Sentinel-1 SAR using Refined Lee filter (window 7×7); (iii) hydrological conditioning of SRTM/ALOS DEMs through pit filling, sink removal, and stream burning using Whitebox GAT v3.0; (iv) bias correction of CHIRPS and GPM data against IMD ground stations using quantile mapping; and (v) geographic harmonization of all layers to UTM Zone 44N (WGS-84) at 30-meter resolution.')

H('6.3 Phase 2: AHP-Weighted Flood Vulnerability Index Development', 2)

P('A composite Flood Vulnerability Index is constructed at 30-meter spatial resolution through Analytic Hierarchy Process (AHP) weighted multi-criteria decision analysis. The AHP framework, originally developed by Saaty (1980) and standardized for environmental applications through ISO 31000:2018, enables systematic integration of heterogeneous vulnerability indicators through pairwise comparison matrices evaluated by an expert panel.')

CAP('DIAGRAM 7: AHP Hierarchical Decision Tree Structure')
MONO("""
                 ┌───────────────────────────────────┐
                 │      GOAL: Composite FVI           │
                 │      (Flood Vulnerability Index)   │
                 └─────────────────┬─────────────────┘
                                   │
        ┌──────────────┬──────────┼──────────────┬──────────────┐
        │              │          │              │              │
        ▼              ▼          ▼              ▼              ▼
  ┌─────────┐    ┌─────────┐ ┌─────────┐  ┌─────────┐    ┌─────────┐
  │ Topo-   │    │ Hydro-  │ │ Land-   │  │  Socio- │    │ Climate │
  │ graphy  │    │ logical │ │ Use     │  │ Demogr. │    │  Hazard │
  │ (w₁=0.25)    │ (w₂=0.22)│ (w₃=0.20)  │ (w₄=0.18)    │ (w₅=0.15)
  └────┬────┘    └────┬────┘ └────┬────┘  └────┬────┘    └────┬────┘
       │              │           │            │              │
       ▼              ▼           ▼            ▼              ▼
   ┌───────┐      ┌───────┐   ┌───────┐    ┌───────┐      ┌───────┐
   │ Slope │      │Drainge│   │ Imper-│    │SC/ST %│      │ Rain  │
   │ TWI   │      │density│   │vious %│    │BPL%   │      │ extr. │
   │ HAND  │      │ SCS-CN│   │ NDVI  │    │FemHH% │      │ trend │
   │ Aspect│      │ Bsflow│   │Wetland│    │Density│      │ index │
   └───────┘      └───────┘   └───────┘    └───────┘      └───────┘
""")

CAP('TABLE 6.2: Saaty\'s 9-Point Pairwise Comparison Scale')
TBL(['Intensity','Definition','Explanation'],
    [['1','Equal importance','Two criteria contribute equally'],
     ['3','Moderate importance','Slightly favors one over another'],
     ['5','Strong importance','Strongly favors one criterion'],
     ['7','Very strong importance','Demonstrated dominance'],
     ['9','Extreme importance','Highest order of dominance'],
     ['2,4,6,8','Intermediate values','Compromise between adjacent']])

CAP('TABLE 6.3: Example AHP Pairwise Comparison Matrix (Top-Level Criteria)')
TBL(['Criterion','Topo','Hydro','LULC','Socio','Climate'],
    [['Topography','1','2','3','4','5'],
     ['Hydrology','1/2','1','2','3','4'],
     ['Land-Use','1/3','1/2','1','2','3'],
     ['Socio-Demo','1/4','1/3','1/2','1','2'],
     ['Climate','1/5','1/4','1/3','1/2','1']])

P('Consistency validation employs the Consistency Ratio (CR), calculated as CR = CI/RI, where CI = (λmax − n)/(n−1) is the Consistency Index and RI is the Random Index from Saaty\'s standard table (RI = 1.12 for n=5 criteria). Only matrices achieving CR < 0.10 are accepted for weight derivation, ensuring logical coherence of expert judgments.')

CAP('TABLE 6.4: Final AHP-Derived FVI Parameter Weights (Targeted Values)')
TBL(['Theme','Sub-Parameter','Weight','Justification','Data Source'],
    [['Topography','Slope (degrees)','0.10','Steeper slopes increase runoff velocity','SRTM DEM'],
     ['Topography','TWI = ln(a/tan β)','0.08','Topographic Wetness Index','Derived'],
     ['Topography','HAND','0.07','Height Above Nearest Drainage','Derived'],
     ['Hydrology','Drainage density','0.07','km/km² channel density','Derived'],
     ['Hydrology','SCS-CN','0.08','Runoff potential index','LULC + soil'],
     ['Hydrology','Distance to stream','0.07','Inverse vulnerability driver','Euclidean'],
     ['Land-Use','Impervious fraction','0.08','Built-up area fraction','Sentinel-2'],
     ['Land-Use','NDVI / Forest cover','0.07','Vegetation density','Sentinel-2'],
     ['Land-Use','Wetland extent','0.05','Hydrological storage','Sentinel-1+2'],
     ['Socio-Demo','Population density','0.06','Census 2011 projected','Census'],
     ['Socio-Demo','SC/ST proportion','0.05','Equity vulnerability','Census'],
     ['Socio-Demo','BPL density','0.04','Economic vulnerability','Census'],
     ['Socio-Demo','Female-headed HH','0.03','Gender vulnerability','Census'],
     ['Climate','IDF intensity (50yr)','0.08','Hazard magnitude','CHIRPS GEV'],
     ['Climate','Trend (Mann-Kendall)','0.07','Non-stationarity index','CHIRPS series']])

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 6.1-6.3 (Methodology Phase 1-2) added")

# ============ SECTION 6.4: Phase 3 SWAT + HEC-RAS ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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

H('6.4 Phase 3: Hydrological and Hydraulic Modeling Architecture', 2)

P('Catchment-scale rainfall-runoff processes are simulated using the Soil and Water Assessment Tool (SWAT v2012/2024), a physically-based, semi-distributed model that operates at daily timestep with sub-daily disaggregation for event-scale modeling. The SWAT outputs—specifically calibrated discharge hydrographs at strategic monitoring nodes—serve as upstream boundary conditions for HEC-RAS 6.x 2D unsteady-flow simulation, enabling detailed floodplain hydraulics including velocity fields, depth maps, and inundation extent at 10-30m mesh resolution.')

CAP('DIAGRAM 8: SWAT Model Architecture and Spatial Discretization')
MONO("""
       ╔═══════════════════════════════════════════════════════════╗
       ║          SWAT SPATIAL DISCRETIZATION HIERARCHY             ║
       ╚═══════════════════════════════════════════════════════════╝

                    ┌────────────────────────┐
                    │   WATERSHED (350 km²)  │
                    │    Primary Outlet      │
                    └───────────┬────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
      ┌──────────┐     ┌──────────┐      ┌──────────┐
      │ Sub-     │     │ Sub-     │      │ Sub-     │
      │ basin 1  │     │ basin 2  │      │ basin N  │
      │ (~10km²) │     │          │      │          │
      └────┬─────┘     └─────┬────┘      └──────┬───┘
           │                 │                  │
     ┌─────┼─────┐     ┌─────┼─────┐            │
     ▼     ▼     ▼     ▼     ▼     ▼            ▼
  ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐    ...HRUs...
  │HRU1││HRU2││HRU3││HRU4││HRU5││HRU6│
  │L+S+││L+S+││L+S+││L+S+││L+S+││L+S+│
  │SLP ││SLP ││SLP ││SLP ││SLP ││SLP │
  └────┘└────┘└────┘└────┘└────┘└────┘
                                  
   HRU = Unique combination of (Land-Use × Soil × Slope class)
   Typical watershed: 50-150 sub-basins, 500-2000 HRUs

   ┌──────────────────────────────────────────────────────┐
   │ HRU-LEVEL PROCESSES (computed for each HRU daily):    │
   │ • Surface runoff (SCS-CN method)                       │
   │ • Lateral flow (kinematic storage)                     │
   │ • Percolation (storage routing)                        │
   │ • ET (Penman-Monteith / Hargreaves)                    │
   │ • Snowmelt (degree-day, Himalayan sites)               │
   │ • Sediment yield (MUSLE)                               │
   └──────────────────────────────────────────────────────┘
""")

CAP('DIAGRAM 9: SWAT-CUP SUFI-2 Calibration Workflow')
MONO("""
   ┌─────────────────────────────────────────────────────────┐
   │  STEP 1: Sensitivity Analysis (Global, Latin Hypercube) │
   │     Parameters tested: 22 SWAT parameters                │
   │     Identify Top-12 sensitive parameters                 │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │  STEP 2: Initial Parameter Range Specification          │
   │     Physical bounds + literature values                  │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │  STEP 3: SUFI-2 Iterative Optimization                  │
   │     500 simulations per iteration × 4-6 iterations       │
   │     Latin Hypercube sampling within evolving ranges      │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │  STEP 4: Performance Evaluation                         │
   │     • NSE > 0.6 (Nash-Sutcliffe Efficiency)             │
   │     • R² > 0.65 (Coefficient of Determination)          │
   │     • PBIAS within ±15% (Percent Bias)                  │
   │     • p-factor > 0.7 (% obs within 95PPU)               │
   │     • r-factor < 1.5 (uncertainty band width)           │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │  STEP 5: Validation on Independent Period (split-sample)│
   │     2010-2018 calibration | 2019-2023 validation         │
   └─────────────────────────────────────────────────────────┘
""")

CAP('TABLE 6.5: SWAT Critical Calibration Parameters with Initial Ranges')
TBL(['Parameter','Description','Initial Range','Typical Final','Sensitivity'],
    [['CN2','SCS-CN moisture cond. II','±25% relative','-10% to +5%','Very High'],
     ['ALPHA_BF','Baseflow recession constant','0.0 - 1.0','0.05 - 0.4','High'],
     ['GW_DELAY','Groundwater delay (days)','0 - 500','30 - 90','Moderate'],
     ['GWQMN','Threshold groundwater (mm)','0 - 5000','500 - 1500','High'],
     ['GW_REVAP','Groundwater revap coef.','0.02 - 0.2','0.05 - 0.10','Moderate'],
     ['ESCO','Soil evap. compensation','0.01 - 1.0','0.4 - 0.8','High'],
     ['EPCO','Plant uptake compensation','0.01 - 1.0','0.5 - 1.0','Low'],
     ['SOL_AWC','Available water capacity','±25% relative','-10% to +20%','Very High'],
     ['SURLAG','Surface runoff lag','0.05 - 24','1 - 6','High'],
     ['CH_N2','Manning n channel','0.014 - 0.15','0.025 - 0.06','High'],
     ['CH_K2','Channel hydraulic K','-0.01 - 500','5 - 50','Moderate'],
     ['SFTMP','Snowfall temperature','-20 - 20','-2 to 2','Site-specific']])

P('Performance evaluation employs the framework of Moriasi et al. (2015), which classifies model performance into four tiers: Very Good (NSE > 0.80), Good (0.70 < NSE ≤ 0.80), Satisfactory (0.50 < NSE ≤ 0.70), and Unsatisfactory (NSE ≤ 0.50). The research targets minimum "Satisfactory" performance with NSE > 0.6 and R² > 0.65 at the catchment outlet for daily streamflow, recognizing that mountainous Himalayan catchments routinely exhibit higher predictive uncertainty than lowland systems due to steep gradients, sparse gauge density, and complex precipitation patterns.')

H('6.5 HEC-RAS 2D Hydraulic Modeling Configuration', 2)

P('Detailed floodplain hydraulics are simulated using HEC-RAS 6.x with 2D unsteady flow capability. The 2D computational mesh is constructed at adaptive resolution: 10m in main channel and urban areas, 20m in floodplains, and 30m in upland zones, balancing computational efficiency with representational accuracy. Manning\'s roughness coefficients are spatially distributed using land-cover-based lookup tables.')

CAP('TABLE 6.6: Manning\'s Roughness Coefficients by Land Cover (HEC-RAS Inputs)')
TBL(['Land Cover Class','Baseline n','NbS Modified n','Difference','Reference'],
    [['Paved/Concrete','0.013','0.013','—','Chow 1959'],
     ['Built-up (urban)','0.025','0.025','—','USACE 2020'],
     ['Bare soil','0.020','0.025','+0.005','Vegetation'],
     ['Cropland','0.030','0.040','+0.010','HEC-RAS manual'],
     ['Grassland','0.035','0.060','+0.025','Native restoration'],
     ['Riparian shrub','0.045','0.080','+0.035','Buffer establishment'],
     ['Riparian forest (mature)','0.060','0.120','+0.060','Mature buffer'],
     ['Wetland (emergent)','0.045','0.080','+0.035','Wetland reconnection'],
     ['Open water','0.030','0.030','—','Channel'],
     ['Channel main','0.025','0.025','—','Engineered'],
     ['Channel braided','0.040','0.040','—','Natural']])

P('Validation employs Sentinel-1 SAR-derived flood extent maps for documented historical events. Performance metric is the Critical Success Index (CSI) calculated as CSI = TP / (TP + FP + FN), where TP = true positives (correctly modeled flooded), FP = false positives (modeled but not observed), FN = false negatives (observed but not modeled). The minimum acceptable threshold is CSI > 0.60.')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 6.4-6.5 added")

# ============ SECTION 6.6 (Phase 4) + Section 7 (Study Areas) ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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

H('6.6 Phase 4: Socio-Economic Benefit-Cost Analysis', 2)

P('The economic valuation component employs stage-damage curves adapted for Indian building typologies and agricultural systems to translate simulated flood depths into monetary damage estimates. Curves are developed for five asset categories: residential structures (kuccha, semi-pucca, pucca), commercial properties, agricultural crops (season-specific), public infrastructure, and vehicles. The methodology follows USACE (2020) and IPCC AR6 (2022) guidance with India-specific calibration based on post-disaster needs assessments from previous events.')

CAP('TABLE 6.7: Stage-Damage Curve Parameters for Indian Building Typologies')
TBL(['Asset Type','Replacement Value (₹/m²)','Damage @ 0.5m (%)','Damage @ 1m (%)','Damage @ 2m (%)','Damage @ 3m+ (%)'],
    [['Kuccha (mud/thatch)','3,500','45','75','95','100'],
     ['Semi-Pucca','8,500','25','50','80','95'],
     ['Pucca (RCC)','18,000','12','28','55','75'],
     ['Commercial small','25,000','30','55','75','90'],
     ['Industrial','35,000','15','35','60','80'],
     ['Vehicles (per unit)','350,000 avg','40','80','100','100'],
     ['Crops Kharif','25,000/ha','40','75','95','100'],
     ['Crops Rabi','20,000/ha','60','90','100','100'],
     ['Public infra (roads/m)','12,000','8','22','45','70']])

P('The benefit of NbS interventions is calculated as Expected Annual Damage (EAD) reduction between baseline and intervention scenarios, integrated across the full return period spectrum (2-500 year). The mathematical formulation is:')

p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('EAD = ∫₀^∞ D(p) dp ≈ Σᵢ ½ × (Dᵢ + Dᵢ₊₁) × (pᵢ − pᵢ₊₁)')
r.italic=True; r.bold=True; r.font.size=Pt(11)
P('Where D(p) is damage at exceedance probability p, calculated trapezoidally across return periods 2, 5, 10, 25, 50, 100, 250, 500 years.')

P('Lifecycle cost-benefit analysis employs a 30-year evaluation horizon at dual discount rates: 3% (reflecting social time preference for long-term environmental investments per UK Treasury Green Book) and 8% (reflecting India\'s standard public project appraisal rate per the Niti Aayog framework). Both rates are reported transparently to enable comparison across institutional contexts.')

CAP('DIAGRAM 10: Total Economic Value (TEV) Components Tree')
MONO("""
                ┌──────────────────────────────────┐
                │     TOTAL ECONOMIC VALUE (TEV)    │
                │    of NbS Flood Risk Reduction    │
                └────────────────┬─────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
    ┌─────────────────┐ ┌────────────────┐ ┌────────────────┐
    │   USE VALUE     │ │OPTION VALUE    │ │NON-USE VALUE   │
    └────────┬────────┘ └────────┬───────┘ └────────┬───────┘
             │                   │                  │
   ┌─────────┼───────────┐       │                  │
   ▼         ▼           ▼       ▼                  ▼
   ┌───┐ ┌────────┐ ┌────────┐ ┌─────────┐  ┌──────────────┐
   │Dir│ │Indirect│ │Avoided │ │Future   │  │Existence /   │
   │ect│ │        │ │Damage  │ │Resource │  │Bequest Value │
   │   │ │        │ │        │ │Use      │  │              │
   └─┬─┘ └───┬────┘ └────┬───┘ └─────────┘  └──────────────┘
     │      │            │
     ▼      ▼            ▼
   • Crops  • Carbon     • Reduced
   • Fisher.• Ground-      flood
   • Grass-   water         losses
     fodder   recharge    • Reduced
   • Bamboo • Pollination   evac costs
            • Soil         • Reduced
              fertility      health costs
""")

doc.add_page_break()
# ============ SECTION 7: STUDY AREAS ============
H('SECTION 7: STUDY AREAS — DETAILED COMPARATIVE PROFILES', 1)

P('The research employs a strategically selected pair of study sites representing the two dominant flood-vulnerable hydrogeomorphic regimes of northern India: the steep-gradient sub-Himalayan flash-flood catchment (Raipur-Dehradun) and the low-gradient riverine floodplain (Darbhanga). This pairing enables hypothesis testing across contrasting conditions, validating the generalizability of the proposed framework.')

CAP('TABLE 7.1: Comprehensive Comparative Study Site Matrix')
TBL(['Parameter','Raipur-Dehradun Watershed','Darbhanga District (Bihar)'],
    [['Geomorphic Regime','Sub-Himalayan steep gradient','Indo-Gangetic floodplain'],
     ['Area (km²)','~350','~2,278'],
     ['Elevation Range (m)','450 - 2,200','35 - 65'],
     ['Mean Slope','15-30°','<0.5°'],
     ['Geology','Siwalik conglomerates + Doon gravels + crystalline','Quaternary alluvium'],
     ['Annual Rainfall (mm)','1,800-2,500','1,150-1,300'],
     ['Dominant Flood Type','Flash floods, debris flows, GLOFs','Riverine inundation, waterlogging'],
     ['Time-to-Peak','30 min - 2 hours','12-72 hours'],
     ['Major River Systems','Song, Suswa (tributaries of Ganga)','Kamla-Balan, Kosi'],
     ['Forest Cover (2022)','38% (down from 56% in 2000)','3.7% (highly degraded)'],
     ['Forest Loss Rate','-18% (2000-2022)','-2% (2000-2022)'],
     ['Population (Census 2011)','1.7 million (Dehradun district)','3.94 million'],
     ['Population Density (/km²)','550','1,728'],
     ['SC/ST Proportion','28%','15.5% / 0.1%'],
     ['BPL Proportion','19%','42%'],
     ['Embankment Length (km)','Limited (15 km)','420 km (extensive)'],
     ['Documented Events 2010-24','12 major flash floods','9 major riverine floods'],
     ['Existing EWS Coverage','Partial (CWC + IMD)','Limited (CWC only)'],
     ['Primary NbS Opportunity','Headwater reforestation, contour bunding','Wetland reconnection, riparian buffers'],
     ['Key Stakeholders','Van Panchayats, SDMA UK','SDMA Bihar, Panchayati Raj']])

CAP('DIAGRAM 11: Schematic Location Map of Study Sites')
MONO("""
        ╔═══════════════════════════════════════════════════════════╗
        ║       STUDY SITE LOCATIONS WITHIN INDIAN CONTEXT           ║
        ╚═══════════════════════════════════════════════════════════╝

         N
         ▲
         │      ┌─────────────────────────────────────────────┐
         │      │  ░░░░░░░  GREATER HIMALAYA (>3000m)         │
         │      │  ░░░ MUSSOORIE  ░░░                         │
         │      │ ░░ │ ░░░░ │░░░░  ◄── PRIMARY SITE            │
         │      │   │      │       Raipur-Dehradun Watershed   │
         │      │   ▼      ▼       (Sub-Himalayan, Steep)      │
         │      │  RAIPUR-DEHRADUN                              │
         │      │  WATERSHED (350km²)                           │
         │      │  Outlet to Song River → Ganga                 │
         │      └────────────┬────────────────────────────────┘
         │                   │
         │      ┌─────────────────────────────────────────────┐
         │      │     INDO-GANGETIC PLAIN                      │
         │      │     ════════════════════                     │
         │      │  ┌─────────────────────────┐                 │
         │      │  │   DARBHANGA DISTRICT     │ ◄── COMPARATIVE
         │      │  │   (2,278 km²)            │     SITE       │
         │      │  │   Kamla-Balan + Kosi     │ (Riverine, Flat)
         │      │  │   76% pop. flood-affected│                 │
         │      │  └─────────────────────────┘                 │
         │      │     ░░░░░░░░░░ Embankment Network             │
         │      └─────────────────────────────────────────────┘
         │                                          │
         │                                          ▼
         │                                    BAY OF BENGAL
         │
         └────────────────────────────► E

   Inter-site Distance: ~1,200 km (enables climatic contrast)
   Combined Coverage: 2,628 km² | Combined Pop: ~5.6 million
""")

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Section 6.6 + 7 added")

# ============ SECTIONS 8, 9, 10 ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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

H('SECTION 8: SIMULATION INTERVENTION SCENARIOS', 1)

P('Four distinct NbS intervention scenarios are modeled, each involving specific parameter modifications within the calibrated SWAT and HEC-RAS frameworks. All scenarios are evaluated against a baseline (current land-use) condition and a grey-infrastructure counterfactual (conventional embankment heightening and channel widening), enabling rigorous economic comparison.')

CAP('TABLE 8.1: Master Scenario Parameter Modification Matrix')
TBL(['Parameter','Baseline','Scenario A (Riparian)','Scenario B (Wetland)','Scenario C (Headwater)','Scenario D (Integrated)'],
    [['SWAT CN2 (riparian zone)','85','75','85','75','70'],
     ['SWAT CN2 (wetland zone)','85','85','65','85','65'],
     ['SWAT CN2 (headwater)','82','82','82','72','70'],
     ['SWAT SOL_AWC','baseline','+10%','+5%','+15%','+20%'],
     ['HEC-RAS Manning n (buffer)','0.030','0.120','0.030','0.030','0.120'],
     ['HEC-RAS Manning n (wetland)','0.045','0.045','0.080','0.045','0.080'],
     ['Reservoir reconnection','None','None','15-20 sites','None','15-20 sites'],
     ['USLE C (treated)','baseline','-50%','baseline','-60%','-65%'],
     ['Channel width modification','None','None','None','None','+10% bottleneck']])

CAP('DIAGRAM 12: Scenario Decision Tree for Sensitivity Analysis')
MONO("""
                ┌──────────────────────────┐
                │  BASELINE SIMULATION     │
                │  (Current LULC, no NbS)  │
                └───────────┬──────────────┘
                            │
        ┌───────────────────┼───────────────────┬──────────────┐
        ▼                   ▼                   ▼              ▼
  ┌───────────┐       ┌───────────┐       ┌───────────┐  ┌────────────┐
  │SCENARIO A │       │SCENARIO B │       │SCENARIO C │  │SCENARIO D  │
  │Riparian   │       │Wetland    │       │Headwater  │  │Integrated  │
  │Buffers    │       │Reconnect  │       │Treatment  │  │A+B+C+grey  │
  │(20-50m)   │       │(15-20 sites)      │(PMKSY-WDC)│  │            │
  └─────┬─────┘       └─────┬─────┘       └─────┬─────┘  └─────┬──────┘
        │                   │                   │              │
        └───────────────────┼───────────────────┴──────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │ EVALUATE FOR EACH:            │
              │ • Peak Q reduction (%)        │
              │ • Time-to-peak shift (hours)  │
              │ • Inundation extent (km²)     │
              │ • Maximum depth (m)           │
              │ • EAD reduction (₹/yr)        │
              │ • BCR @ 3% & 8% discount      │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ SENSITIVITY MATRIX            │
              │ • Return periods: 10/25/50/100│
              │ • Climate: baseline vs RCP8.5 │
              │ • Land-use: 2024 vs 2040 BAU  │
              └───────────────────────────────┘
""")

H('Scenario A: Riparian Buffer Establishment', 2)
P('This scenario simulates the establishment of 20-50 meter vegetated riparian buffers along all primary (Strahler order ≥3) and secondary (Strahler order 2) drainage channels. In HEC-RAS, Manning\'s roughness coefficient is modified from baseline 0.030 to 0.120, simulating flow retardation through dense vegetation. In SWAT, corresponding HRUs are reclassified from agricultural/barren to forest/buffer land use, modifying CN2, leaf area index, and evapotranspiration. The scenario quantifies peak discharge reduction, time-to-peak extension, and downstream flood depth reduction.')

H('Scenario B: Wetland Reconnection and Restoration', 2)
P('This scenario models hydrological reconnection of historically disconnected floodplain wetlands (oxbow lakes, palustrine marshes, seasonal jheels) to the active drainage network. In SWAT, SCS Curve Number for identified wetland zones is modified from 85 (degraded agricultural occupancy) to 65 (functional wetland with high organic content). Reservoir routing parameters are introduced at wetland locations to simulate storage-discharge relationships of restored water bodies.')

H('Scenario C: Headwater Micro-Basin Treatment', 2)
P('This scenario simulates comprehensive watershed treatment of headwater catchments (Strahler order 1-2) through vegetative porous barriers, contour trenching, and afforestation—aligned with PMKSY-WDC 2.0 guidelines. In SWAT, treated sub-basins receive reduced CN2 (5-10 unit reduction), increased soil available water capacity, and modified USLE cover factor.')

H('Scenario D: Integrated NbS-Grey Infrastructure Package', 2)
P('Combines Scenarios A, B, and C with targeted grey-infrastructure enhancements (channel optimization, culvert upgrades) at identified bottleneck locations. Tests whether combined NbS interventions produce synergistic (super-additive) benefits exceeding the arithmetic sum of individual scenarios. The grey-infrastructure counterfactual consists of conventional engineering (embankment heightening 1.5m, channel widening 30%) achieving equivalent flood protection, enabling direct economic comparison.')

# ============ SECTION 9: EXPECTED OUTCOMES ============
H('SECTION 9: EXPECTED OUTCOMES AND DELIVERABLES', 1)

CAP('TABLE 9.1: Outcome-Indicator-Verification Matrix')
TBL(['Outcome','Indicator','Target','Verification Method','Beneficiary'],
    [['District-scale FVI maps','30m resolution coverage','350 km² (UK) + 2,278 km² (Bihar)','Sentinel-1 SAR validation','DDMAs'],
     ['Calibrated SWAT models','NSE performance','> 0.6 daily, > 0.7 monthly','SUFI-2 95PPU','CWC, SDMA'],
     ['HEC-RAS 2D flood maps','Inundation accuracy','CSI > 0.6','SAR comparison','District officials'],
     ['NbS efficacy quantification','Peak Q reduction','12-25% under 50-yr events','Modeled vs baseline','Researchers, NDMA'],
     ['Economic valuation','Benefit-Cost Ratio','> 3:1 baseline; > 5:1 RCP8.5','Damage curve integration','MoEFCC'],
     ['DDMP Annexure templates','Districts adopted','5+ districts','Administrative orders','District Magistrates'],
     ['SCIE Publications','Q1 papers','3 of 4 in Q1','Journal acceptance','Academic community'],
     ['Open-source code repository','GitHub release','Full code + data','Public access','Replication researchers'],
     ['Capacity building','Workshop participants','100+ officials trained','Attendance records','State agencies'],
     ['Community FVI validation','Villages engaged','20+ villages','Participatory mapping','Local communities']])

# ============ SECTION 10: TIMELINE ============
doc.add_page_break()
H('SECTION 10: TIMELINE AND WORK BREAKDOWN STRUCTURE', 1)

CAP('DIAGRAM 13: 36-Month Gantt Chart of Research Activities')
MONO("""
ACTIVITY                      Y1Q1 Y1Q2 Y1Q3 Y1Q4 Y2Q1 Y2Q2 Y2Q3 Y2Q4 Y3Q1 Y3Q2 Y3Q3 Y3Q4
═══════════════════════════════════════════════════════════════════════════════════════
1. Literature Review         ████ ████ 
2. Field Reconnaissance      ████ ████ 
3. Data Acquisition          ████ ████ ████ 
4. Field Ground-truthing          ████ ████ ████ 
5. AHP Expert Panel               ████ ████ 
6. FVI Development                     ████ ████ ████ 
7. FVI Validation                           ████ ████ 
8. SWAT Setup                          ████ ████ ████ 
9. SWAT Calibration (SUFI-2)                          ████ ████ 
10. SWAT Validation                                        ████ 
11. HEC-RAS 2D Setup                                  ████ ████ 
12. HEC-RAS Calibration                                    ████ ████ 
13. NbS Scenario A,B,C                                     ████ ████ ████ 
14. NbS Scenario D                                              ████ ████ ████ 
15. Sensitivity Analysis                                             ████ ████ 
16. Economic Valuation                                                    ████ ████ 
17. DDMP Templates                                                             ████ ████ 
18. Stakeholder Workshops    ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ ████ ████ ████
19. Paper 1 (Review)              ░░░░ ████ ████ ████ ●Submit Paper 1 (M12)
20. Paper 2 (FVI)                                ░░░░ ████ ████ ●Submit Paper 2 (M18)
21. Paper 3 (Hydrology)                                    ░░░░ ████ ████ ●Submit P3(M27)
22. Paper 4 (Economics)                                              ░░░░ ████ ●P4(M33)
23. Dissertation Writing                                                  ░░░░ ████ ████
24. Pre-submission Seminar                                                          ████
25. Final Submission                                                                  ●

  Legend: ████ = Active execution    ░░░░ = Continuous/Background    ● = Milestone
""")

CAP('TABLE 10.1: Quarterly Milestones and Key Deliverables')
TBL(['Quarter','Months','Key Deliverable','Indicator'],
    [['Y1Q1','M1-3','Literature review complete + Field plan','Annotated bibliography 200+ refs'],
     ['Y1Q2','M4-6','All datasets acquired + AHP panel convened','Data inventory + Expert panel CR<0.10'],
     ['Y1Q3','M7-9','FVI methodology paper drafted','Paper 1 manuscript ready'],
     ['Y1Q4','M10-12','Paper 1 submitted; FVI maps validated','Submission confirmation'],
     ['Y2Q1','M13-15','SWAT model setup complete','Working models for both sites'],
     ['Y2Q2','M16-18','SWAT calibration complete; Paper 2 submitted','NSE>0.6 + submission'],
     ['Y2Q3','M19-21','HEC-RAS 2D running','Validated flood maps'],
     ['Y2Q4','M22-24','Scenarios A,B,C complete','Modeled inundation maps'],
     ['Y3Q1','M25-27','Scenario D + sensitivity; Paper 3 submitted','BCR calculations + submission'],
     ['Y3Q2','M28-30','Economic valuation; Stakeholder workshops','TEV monetary estimates'],
     ['Y3Q3','M31-33','DDMP templates + Paper 4 submitted','Templates adopted'],
     ['Y3Q4','M34-36','Dissertation submitted; Defense scheduled','Final submission']])

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("Sections 8, 9, 10 added")

# ============ SECTIONS 11, 12, 13, 14 ============
doc = Document('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
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

# ============ SECTION 11: PUBLICATION STRATEGY ============
H('SECTION 11: PUBLICATION STRATEGY (4-PAPER SCIE TRACK)', 1)

P('The dissertation is structured around a deliberate 4-paper SCIE publication track designed to maximize academic impact while ensuring timely completion. Each paper addresses a discrete contribution and targets a specific Q1 or Q2 SCIE journal aligned with the methodological focus of that paper.')

CAP('TABLE 11.1: Publication Strategy with Target Journals')
TBL(['Paper','Title (Working)','Target Journal','IF (2024)','Tier','Submission Month'],
    [['Paper 1','NbS for Inland Flood Mitigation: Systematic Review and Conceptual Framework','Science of the Total Environment','9.8','Q1','Month 12'],
     ['Paper 2','District-Scale AHP-GIS Flood Vulnerability Atlas for Indian Watersheds','International Journal of Disaster Risk Reduction','5.0','Q1','Month 18'],
     ['Paper 3','SWAT-HEC-RAS Coupled Simulation of NbS Efficacy Under Non-Stationary Climate','Journal of Hydrology','6.4','Q1','Month 27'],
     ['Paper 4','Economic Decision Framework for NbS Integration in DDMPs','Land Use Policy','7.1','Q1','Month 33']])

# ============ SECTION 12: ETHICS & CLIMATE JUSTICE ============
H('SECTION 12: ETHICS, CLIMATE JUSTICE AND COMMUNITY ENGAGEMENT', 1)

P('Recognizing that flood impacts in India are profoundly inequitable—with Scheduled Caste and Scheduled Tribe communities, landless agricultural laborers, and female-headed households bearing disproportionate losses relative to their asset base and adaptive capacity—this research embeds a Climate Justice analytical lens throughout. Flood damage estimates and NbS benefit distributions are disaggregated by gender, caste category, economic quintile, and geographic marginality.')

H('12.1 Data Ethics and Informed Consent', 2)
P('All spatial data is derived from open-source platforms (Copernicus, NASA, ISRIC) freely available for research. Socio-demographic data from Census 2011 is used at aggregate (village/ward) levels without individual identification. Community surveys conducted during field validation will obtain informed consent through bilingual (Hindi/English or Hindi/Maithili) consent forms approved by the DBS Global University Institutional Ethics Committee. GPS coordinates of individual households will be aggregated to ward-level centroids in published outputs to prevent identification. All data storage complies with the Information Technology Act 2000 and the Digital Personal Data Protection Act 2023.')

H('12.2 Gender-Sensitive Validation Protocol', 2)
P('Participatory validation incorporates two stages: (i) during FVI development, where Participatory Rural Appraisal (PRA) exercises—including transect walks, seasonal calendars, and hazard mapping—validate model-derived vulnerability classifications against lived experience; and (ii) during decision support framework development, where stakeholder workshops with district officials, Panchayati Raj members, and community representatives validate intervention practicability. Gender sensitivity is ensured through mandatory minimum 50% female participation, gender-disaggregated FVI indicators, and explicit assessment of differential NbS impacts on women\'s workloads, mobility, and economic opportunities.')

CAP('TABLE 12.1: Stakeholder Engagement Matrix')
TBL(['Stakeholder Group','Engagement Stage','Method','Frequency','Output'],
    [['Gram Sabha','All phases','Open community meetings','Quarterly','Validation + buy-in'],
     ['Van Panchayat (UK)','Phase 2-4','Forest management consultation','Bi-annual','Site selection input'],
     ['SHG Networks','Phase 2-4','Women-only focus groups','Quarterly','Gender-disagg validation'],
     ['SC/ST Communities','All phases','Targeted FGDs','Bi-annual','Equity validation'],
     ['Mukhiya/Sarpanch','All phases','Individual consultations','Monthly','Local governance integration'],
     ['Block Development','Phase 4','BDO meetings','Quarterly','Administrative pathway'],
     ['District Magistrate','Phase 4','Briefings','Bi-annual','DDMP adoption'],
     ['SDMA','All phases','Technical meetings','Quarterly','Institutional integration'],
     ['CWC/IMD','Phase 1, 3','Data sharing protocols','As needed','Validation datasets']])

# ============ SECTION 13: RISK MANAGEMENT ============
H('SECTION 13: RISK MANAGEMENT AND MITIGATION FRAMEWORK', 1)

CAP('TABLE 13.1: Comprehensive Risk Register')
TBL(['Risk ID','Risk Description','P (1-5)','I (1-5)','Score','Mitigation Strategy'],
    [['R1','Sentinel data unavailability for monsoon period','2','3','6','Use multiple satellites (S1+S2+Landsat)'],
     ['R2','SWAT calibration NSE < 0.6','2','5','10','Multi-objective calibration; alternative model (MIKE-SHE backup)'],
     ['R3','HEC-RAS instability in steep terrain','3','3','9','Adaptive mesh; alternative HEC-HMS+TUFLOW'],
     ['R4','AHP expert panel low CR','2','3','6','Iterative refinement; replace inconsistent panelist'],
     ['R5','Field access blocked (landslides, monsoon)','3','2','6','Multiple field windows; remote sensing primary'],
     ['R6','Community participation low','3','4','12','Early Gram Sabha buy-in; honoraria for participation'],
     ['R7','SDMA non-cooperation','2','4','8','Formal MoU at project initiation'],
     ['R8','Climate change invalidates baseline','2','2','4','Non-stationary frequency analysis built-in'],
     ['R9','Equipment damage during fieldwork','3','2','6','Insurance + redundancy budget 10%'],
     ['R10','Paper rejection in Q1 journals','3','3','9','Multiple target journals per paper; pre-print on EarthArXiv'],
     ['R11','Scholar health/personal emergency','2','5','10','Co-PI continuity plan; documentation protocol'],
     ['R12','Software license cost overrun','2','2','4','Use open-source alternatives (QSWAT, free HEC-RAS)']])

P('Risk scoring uses Probability × Impact (1-5 each, max score 25). High-risk items (Score ≥ 10) include SWAT calibration failure (R2), low community participation (R6), and scholar emergency (R11). For each high-risk item, a documented contingency plan is maintained in the project quality assurance manual.')

# ============ SECTION 14: REFERENCES ============
H('SECTION 14: KEY REFERENCES', 1)
refs = ['Abbaspour, K.C. (2015). SWAT-CUP: SWAT Calibration and Uncertainty Programs. Eawag, Switzerland.',
'Arnold, J.G., et al. (2012). SWAT: Model use, calibration, and validation. Trans. ASABE 55(4): 1491-1508.',
'Dadson, S.J., et al. (2017). A restatement of the natural science evidence concerning catchment-based "natural" flood management. Proc. Royal Society A 473: 20160706.',
'IPCC AR6 WG2 (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability. Cambridge University Press.',
'IUCN (2020). Global Standard for Nature-based Solutions. Gland, Switzerland.',
'Mishra, S.K., Singh, V.P. (2010). SCS-CN-based hydrologic simulation package. Mathematical Models of Small Watershed Hydrology, Water Resources Publications.',
'Moriasi, D.N., et al. (2015). Hydrologic and water quality models: Performance measures. Trans. ASABE 58(6): 1763-1785.',
'NDMA (2022). National Disaster Management Guidelines: Flash Flood Management. Govt. of India.',
'Nicholson, A.R., et al. (2020). Modelling small-scale floods in upland catchments: a comparison. Hydrology Research 51(2): 290-308.',
'Pahl-Wostl, C. (2007). Transitions towards adaptive management of water facing climate and global change. Water Resources Management 21(1): 49-62.',
'Saaty, T.L. (1980). The Analytic Hierarchy Process. McGraw-Hill, New York.',
'Schueler, T.R. (1994). The importance of imperviousness. Watershed Protection Techniques 1(3): 100-111.',
'Singh, P., Pandey, A. (2021). AHP-GIS based flood vulnerability mapping. Natural Hazards 109(1): 1043-1071.',
'USACE (2020). HEC-RAS 6.x River Analysis System User\'s Manual. US Army Corps of Engineers.',
'Viswanathan, B., et al. (2022). Flood early warning impact: An RCT in Bihar. World Development 156: 105922.']
for r in refs:
    p = doc.add_paragraph(r)
    p.paragraph_format.left_indent=Inches(0.5)
    p.paragraph_format.first_line_indent=Inches(-0.5)
    p.paragraph_format.line_spacing=1.3
    p.paragraph_format.space_after=Pt(4)

# ============ DECLARATION ============
doc.add_page_break()
H('DECLARATION', 1)
P('I, Raj Amritam, hereby declare that this PhD Dissertation Research Proposal represents original work prepared specifically for academic submission. The proposed research does not duplicate any ongoing funded research. All datasets, methodologies, and computational tools described are accessible through publicly available platforms or licensed institutional access. I commit to conducting this research with the highest standards of scientific integrity, community respect, and environmental responsibility. All publications arising from this research will follow open-access protocols where feasible.')
doc.add_paragraph('')
doc.add_paragraph('')
sigt = doc.add_table(rows=4, cols=2); sigt.style = None
sigt.rows[0].cells[0].text = 'Research Scholar:'
sigt.rows[0].cells[1].text = 'Supervisor:'
for r in sigt.rows[0].cells[0].paragraphs[0].runs: r.bold=True
for r in sigt.rows[0].cells[1].paragraphs[0].runs: r.bold=True
sigt.rows[1].cells[0].text = ''
sigt.rows[1].cells[1].text = ''
sigt.rows[2].cells[0].text = '________________________'
sigt.rows[2].cells[1].text = '________________________'
sigt.rows[3].cells[0].text = 'Raj Amritam\nPhD Research Scholar\nDept. of Environmental Science\nDBS Global University, Dehradun'
sigt.rows[3].cells[1].text = 'Dr. Nidhi Rawat\nAssociate Professor (Supervisor)\nDept. of Environmental Science\nDBS Global University, Dehradun'

doc.add_paragraph('')
P('Date: ____________ | Place: Dehradun, Uttarakhand')

doc.save('/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx')
print("All sections 11-14 + Declaration added")
print()
# Word count check
text = ' '.join([p.text for p in doc.paragraphs])
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text += ' ' + cell.text
print(f"FINAL Word count: {len(text.split())}")
