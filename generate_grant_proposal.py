#!/usr/bin/env python3
"""Generate Grant Funding Proposal as .docx file."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)

def add_h(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs:
        r.font.name = 'Times New Roman'
        r.font.color.rgb = RGBColor(0, 0, 0)

def add_p(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5

def add_b(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.line_spacing = 1.5

# === TITLE PAGE ===
for _ in range(3):
    doc.add_paragraph('')
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('ON-GROUND PROJECT / GRANT FUNDING PROPOSAL')
r.bold = True; r.font.size = Pt(14)
doc.add_paragraph('')
s = doc.add_paragraph()
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run('Developing an Integrated Hydro-Spatial Framework for Eco-Safe Himalayan Catchments:\nA Hybrid Academic-Deployment Strategy for Nature-Based Flood Mitigation,\nIoT-Enabled Early Warning Systems & Community Climate Resilience')
r.bold = True; r.font.size = Pt(13)
doc.add_paragraph('')
doc.add_paragraph('')
for line in ['Submitted to:', 'National Mission on Himalayan Studies (NMHS) /','DST-NMSHE / National Adaptation Fund for Climate Change (NAFCC)','','Submitted by:','Department of Environmental Science','DBS Global University, Dehradun','Uttarakhand, India','','Principal Investigator: Dr. Nidhi Rawat','Co-PI / Research Scholar: Raj Amritam','','2025']:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(line).font.size = Pt(12)
doc.add_page_break()

# === SECTION 1 ===
add_h('1. PROJECT IDENTIFICATION AND METADATA', level=1)
tbl = doc.add_table(rows=9, cols=2)
tbl.style = 'Table Grid'
data = [
    ('Project Title', 'Developing an Integrated Hydro-Spatial Framework for Eco-Safe Himalayan Catchments: A Hybrid Academic-Deployment Strategy for Nature-Based Flood Mitigation, IoT-Enabled Early Warning Systems & Community Climate Resilience'),
    ('Proposed Tenure', '36 Months (3-Year Fast-Track Strategy)'),
    ('Total Financial Request', 'INR 28,50,000 (Twenty-Eight Lakhs Fifty Thousand Only)'),
    ('Targeted Field Region', 'Garhwal Himalayan Region, Uttarakhand, India'),
    ('Direct Institutional Affiliation', 'Department of Environmental Science, DBS Global University, Dehradun'),
    ('Principal Investigator', 'Dr. Nidhi Rawat, Associate Professor'),
    ('Co-PI / Research Scholar', 'Raj Amritam, PhD Research Scholar'),
    ('Strategic Alignment', 'Sendai Framework Targets A, B, C, D, and G; WMO Early Warnings for All (EW4All) Initiative; NAPCC National Water Mission'),
    ('Institutional Mandate', 'DM Act 2005 (Sec. 30-31); SDMA Uttarakhand Guidelines; NDMA Flash Flood Management Guidelines 2022'),
]
for i, (k, v) in enumerate(data):
    tbl.rows[i].cells[0].text = k
    tbl.rows[i].cells[1].text = v
    for p in tbl.rows[i].cells[0].paragraphs:
        for run in p.runs:
            run.bold = True
doc.add_paragraph('')

# === SECTION 2 ===
add_h('2. EXECUTIVE SUMMARY AND STRATEGIC RATIONALE', level=1)
add_p('The Garhwal Himalayan region of Uttarakhand represents one of the most acutely climate-vulnerable geographies on the Indian subcontinent. Characterized by extreme orographic precipitation gradients (ranging from 1,200 mm in the Doon Valley to over 3,500 mm at mid-elevation cloudforest zones), tectonically active substrate (the Main Central Thrust and Main Boundary Thrust systems), and rapidly degrading forest cover due to encroachment and infrastructure development, the region has witnessed an unprecedented acceleration of catastrophic hydro-meteorological events over the past decade. The Chamoli disaster of February 2021\u2014wherein a glacial-rock avalanche triggered a devastating flood pulse killing over 200 individuals and destroying two hydropower installations\u2014and the Dharali flash floods of August 2025 that inundated three villages with zero prior warning, collectively underscore a systemic governance failure: the near-complete absence of functional early warning infrastructure in precisely those catchments experiencing the most rapid hazard intensification.')
add_p('This proposal presents a strategically integrated response to this crisis, designed specifically for multi-year climate funding bodies seeking demonstrable community-level impact within compressed timelines. The project\'s core value proposition is its explicit dual-structure architecture that bridges the persistent gap between academic computational research ("The Brain") and immediate, cost-effective on-ground community deployment ("The Body") within a single 36-month execution window. Unlike conventional academic projects that generate publications without operational outcomes, or conventional development projects that deploy infrastructure without scientific rigor, this initiative deliberately fuses both paradigms\u2014producing simultaneously a validated hydro-spatial modeling framework (publishable in Q1 SCIE journals) AND a functioning early warning system protecting a minimum of 2,500 directly vulnerable households.')
add_p('The strategic rationale for this integrated approach draws upon demonstrated international precedents. The Netherlands\' \'Room for the River\' program (2006\u20132019) achieved a sustained 35 cm peak water level reduction across 39 intervention sites through precisely the kind of nature-based engineering interventions proposed here\u2014demonstrating that ecosystem-based approaches can deliver quantifiable hydraulic benefits at operational scales. ICIMOD\'s transboundary flood early warning systems across the Hindu Kush-Himalayan belt have proven that low-cost sensor networks combined with community-based last-mile dissemination can provide actionable lead times of 3\u20138 hours in mountain flash-flood contexts. Most compellingly, the Bihar flood-forecasting randomized controlled trial (Viswanathan et al., 2022) demonstrated that targeted early warnings\u2014even in resource-constrained, low-literacy contexts\u2014yielded a 30% reduction in post-flood household medical expenditures and a 22% reduction in livestock mortality, establishing a rigorous evidence base for the economic returns of community-level flood preparedness investments.')
add_p('This project targets the institutional sweet-spot where academic innovation meets deployment readiness: a total investment of INR 28,50,000 over 36 months\u2014approximately INR 1,140 per protected household\u2014to deliver a replicable, open-source template that can be scaled across the 13 districts of Uttarakhand and subsequently adapted for the 25+ Himalayan districts of Himachal Pradesh, Sikkim, and Arunachal Pradesh without requiring additional foundational research.')

# === SECTION 3 ===
add_h('3. DUAL-STRUCTURE LINKAGE MATRIX AND SCOPE OF WORK', level=1)
add_p('The project operationalizes its dual-structure philosophy through three integrated deployment tasks, each designed to generate both academic outputs (publications, datasets, validated methodologies) and tangible community-level outcomes (infrastructure, capacity, institutional embedding) simultaneously.')

add_h('3.1 Task 1: Digital Flood Vulnerability Atlas \u2014 Resource Deployment', level=2)
add_p('The foundational analytical task constructs an open-access Digital Flood Vulnerability Atlas operating at unprecedented administrative granularity\u2014the Gram Panchayat and Block Development level\u2014across the target Garhwal Himalayan watersheds. This atlas transcends conventional hazard mapping by integrating multi-dimensional vulnerability indicators into a composite Flood Vulnerability Index (FVI) at 30-meter spatial resolution, enabling precise identification of high-priority micro-watersheds for intervention targeting.')
add_b('Analytical Architecture: Employs Analytic Hierarchy Process (AHP) weighted multi-criteria analysis integrating topographic (slope, TWI, HAND), hydrological (drainage density, SCS-CN), land-use (impervious fraction, forest cover loss), and socio-demographic (SC/ST population proportion, female-headed households, BPL density) indicators.')
add_b('Data Sources: Sentinel-2 multispectral (10m), SRTM/ALOS PALSAR DEM (30m/12.5m), ISRIC SoilGrids, CHIRPS rainfall, GPM IMERG sub-hourly precipitation, Census 2011 socio-economic layers.')
add_b('Output Deliverables: Interactive web-based GIS portal (hosted on institutional servers with open API access); Ward-level vulnerability classification maps for minimum 150 Gram Panchayats; Priority micro-watershed ranking for NbS intervention deployment.')
add_b('Governance Integration: Atlas outputs formatted as direct annexures to Block-level DDMPs under DM Act 2005 Section 31, requiring zero legislative modification for institutional adoption by District Magistrate offices.')

add_h('3.2 Task 2: Ecological Engineering \u2014 Physical NbS Pilot Deployment', level=2)
add_p('The second task translates vulnerability analytics into physical landscape intervention through a 2-hectare pilot ecological engineering site in a selected high-priority micro-watershed. The pilot is designed for maximum replicability using locally available materials, indigenous knowledge systems, and convergence with existing government labor programs\u2014specifically MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) wage labor and Van Panchayat community forest management institutions.')
add_b('Site Specifications: 2-hectare treatment area within a Strahler order 1-2 headwater sub-catchment exhibiting active erosion, degraded riparian zones, and documented flash-flood damage history. Site selection validated through FVI atlas outputs and ground-truthing.')
add_b('Intervention Package: Locally fabricated bamboo check structures (using Dendrocalamus strictus sourced from Van Panchayat community forests); vegetative barriers using Vetiver grass (Chrysopogon zizanioides) and Napier grass hedgerows; contour stone bunding with live vegetation stakes; and riparian buffer planting using native species (Alnus nepalensis, Grewia optiva, Celtis australis).')
add_b('Performance Targets: Minimum 20% flow velocity reduction at pilot outlet (measured via float method and calibrated against installed pressure transducer data); minimum 30% topsoil conservation (measured via sediment traps and Revised Universal Soil Loss Equation modeling); documented infiltration enhancement of minimum 15% (measured via ring infiltrometer tests at 6-month intervals).')
add_b('Labor Convergence: All manual labor for structure construction coordinated through MGNREGA job cards, ensuring zero additional wage cost to the project while generating 450-600 person-days of documented employment for marginalized community members. Van Panchayat institutional engagement ensures long-term maintenance responsibility beyond the project period.')

add_h('3.3 Task 3: IoT Telemetry System \u2014 Community Early Warning Deployment', level=2)
add_p('The third task establishes a functional, community-embedded flood early warning system comprising automated sensing, intelligent processing, and multi-modal last-mile dissemination\u2014designed to operate autonomously during the critical June\u2013September monsoon window when institutional response capacity is most constrained.')
add_b('Sensor Array: 3 automated river-level sensors (ultrasonic/pressure-based, solar-powered, GPRS/LoRa telemetry) deployed at strategic upstream monitoring points identified through hydraulic modeling. 1 automated micro-meteorological weather station (AWS) recording rainfall intensity, temperature, humidity, wind speed, and barometric pressure at 5-minute intervals.')
add_b('Communication Gateway: Automated alert dissemination via WhatsApp Business API and SMS gateway (Exotel/Knowlarity IVR platform) triggered when water levels exceed pre-defined threshold stages (Alert/Warning/Danger). Multi-language support (Hindi/Garhwali). Escalating alert cascade: automated message \u2192 mukhiya volunteer phone call \u2192 manual siren activation.')
add_b('Operational Targets: >45-minute flash-flood warning lead time (validated against historical event reconstruction); >95% sensor uptime during monsoon season (June\u2013September); >80% message comprehension rate across marginalized groups (validated through post-monsoon household surveys with minimum 100 respondent sample including SC/ST, women, and elderly populations).')
add_b('Institutional Embedding: All sensor data feeds automatically to the SDMA Uttarakhand Emergency Operations Center dashboard. Alert protocols integrated into DDMP Standard Operating Procedures. Annual pre-monsoon calibration conducted jointly with district administration and community volunteers.')

# === SECTION 4 ===
add_h('4. THE FOUR-PILLAR EW4ALL OPERATIONAL ARCHITECTURE', level=1)
add_p('The project\'s technical deployment maps directly and comprehensively to the World Meteorological Organization\'s (WMO) Early Warnings for All (EW4All) architecture\u2014the global standard framework endorsed by the UN Secretary-General\'s Executive Action Plan (2022). This alignment ensures international best-practice compliance while maximizing the project\'s eligibility for follow-on multilateral climate finance.')

add_h('4.1 Pillar 1: Disaster Risk Knowledge', level=2)
add_p('Risk knowledge generation is driven by the AHP-weighted spatial GIS vulnerability layers constituting the Digital Flood Vulnerability Atlas (Task 1). The atlas produces quantified, spatially explicit risk information at governance-relevant scales\u2014enabling evidence-based resource allocation by district and block-level disaster management authorities. Historical event inventories are compiled from SDMA records, satellite-derived flood extent maps (Sentinel-1 SAR), and community-sourced damage reports to validate and continuously update risk assessments. The risk knowledge base explicitly disaggregates vulnerability by gender, caste category, and economic quintile\u2014ensuring that preparedness investments target the most marginalized and least-resilient populations.')

add_h('4.2 Pillar 2: Detection, Observation, Monitoring, and Forecasting', level=2)
add_p('Detection and monitoring capabilities are provided by the physical IoT sensor array (3 river-level gauges + 1 micro-AWS) deployed at strategically selected upstream monitoring points. The sensor network operates continuously during the monsoon season with 5-minute data transmission intervals, enabling real-time water level tracking and rainfall-intensity monitoring. A threshold-based forecasting algorithm\u2014calibrated against historically reconstructed flood events using the HEC-RAS hydraulic model\u2014translates observed water levels and rainfall intensities into probabilistic flood warnings with quantified lead times and uncertainty bounds. The system architecture is designed for graceful degradation: even with single-sensor failure, remaining sensors provide redundant warning capability through the monitoring network\'s spatial distribution.')

add_h('4.3 Pillar 3: Warning Dissemination and Communication', level=2)
add_p('Warning dissemination employs multi-modal communication pathways engineered for maximum penetration across diverse literacy levels, technological access patterns, and linguistic contexts. The primary automated pathway utilizes WhatsApp Business API and SMS broadcasting via the Exotel/Knowlarity IVR gateway\u2014reaching smartphone and feature-phone users simultaneously. The secondary pathway activates a trained mukhiya (village head) volunteer network who receive priority alerts and are responsible for person-to-person notification of households without phone access. The tertiary pathway comprises manually activated community sirens positioned at strategic village gathering points. All warning messages are issued in both Hindi and Garhwali languages, using pre-tested simplified formats validated for >80% comprehension across marginalized demographic groups including non-literate individuals, women in purdah/restricted mobility contexts, and elderly populations with hearing impairment.')

add_h('4.4 Pillar 4: Preparedness and Response Capability', level=2)
add_p('Community preparedness is institutionalized through structured annual programming: 2 full-scale community disaster drills per year (one pre-monsoon in May and one mid-monsoon in August), conducted in coordination with the Block Development Officer and SDMA representatives. Drills incorporate realistic scenarios based on modeled flood extents and include complete alert-to-evacuation sequences. Gender-inclusive Self-Help Group (SHG) Emergency Task Forces are established in each target village\u2014comprising minimum 50% women membership\u2014trained in first aid, evacuation route management, livestock protection protocols, and post-disaster needs assessment. Task force members receive annual refresher training and are integrated into the DDMP institutional structure as recognized community disaster management volunteers under Section 41 of the DM Act 2005.')

# === SECTION 5 ===
add_h('5. ITEMIZED BUDGETARY AND FINANCIAL REQUEST MATRIX', level=1)
add_p('The total project budget of INR 28,50,000 is structured across four expenditure heads distributed over the 36-month implementation timeline. The budget reflects principles of cost-effectiveness, institutional sustainability, and maximum deployment impact per rupee invested.')
doc.add_paragraph('')

# Budget table
bt = doc.add_table(rows=19, cols=4)
bt.style = 'Table Grid'
headers = ['S.No.', 'Budget Head / Item Description', 'Amount (INR)', 'Timeline']
for i, h in enumerate(headers):
    bt.rows[0].cells[i].text = h
    for p in bt.rows[0].cells[i].paragraphs:
        for run in p.runs:
            run.bold = True

budget_items = [
    ('', 'A. CAPITAL & ANALYTICAL EQUIPMENT', '4,50,000', 'Year 1'),
    ('A1', 'IoT River-Level Sensors (3 units @ INR 75,000 each)', '2,25,000', 'Year 1 Q1-Q2'),
    ('A2', 'Micro-Meteorological AWS (1 unit, complete station)', '1,25,000', 'Year 1 Q1'),
    ('A3', 'High-Throughput GIS Laboratory Workstation (64GB RAM, RTX GPU)', '1,00,000', 'Year 1 Q1'),
    ('', 'B. OPERATIONAL & MATERIAL ASSETS', '8,50,000', 'Year 2'),
    ('B1', 'Vegetative matrices, bamboo materials, Vetiver grass procurement', '2,50,000', 'Year 2 Q1-Q2'),
    ('B2', 'Community workshops, training materials, SHG capacity building', '1,50,000', 'Years 1-3'),
    ('B3', 'API server hosting, Exotel/Knowlarity IVR subscription (36 months)', '1,80,000', 'Years 1-3'),
    ('B4', 'Satellite data processing credits (Google Earth Engine Pro)', '70,000', 'Years 1-2'),
    ('B5', 'Field instrumentation (infiltrometers, sediment traps, float kits)', '1,00,000', 'Year 1-2'),
    ('B6', 'Pilot site civil works (stone bunding, contour trenching labor tools)', '1,00,000', 'Year 2'),
    ('', 'C. MANPOWER & INSTITUTIONAL FELLOWSHIP', '13,00,000', 'Years 1-3'),
    ('C1', 'JRF/SRF Fellowship (1 scholar @ INR 35,000/month x 36 months)', '12,60,000', 'Years 1-3'),
    ('C2', 'Field Surveyors & Data Collection Specialists (seasonal, 2 persons)', '40,000', 'Monsoon seasons'),
    ('', 'D. TRAVEL, DIAGNOSTICS & CONTINGENCY', '2,50,000', 'Years 1-3'),
    ('D1', 'In-state field travel (vehicle hire, fuel, accommodation)', '1,20,000', 'Years 1-3'),
    ('D2', 'Conference presentations (2 national + 1 international)', '80,000', 'Years 2-3'),
    ('D3', 'Institutional overheads & 10% contingency reserve', '50,000', 'Years 1-3'),
]
for i, (sno, desc, amt, timeline) in enumerate(budget_items, start=1):
    bt.rows[i].cells[0].text = sno
    bt.rows[i].cells[1].text = desc
    bt.rows[i].cells[2].text = amt
    bt.rows[i].cells[3].text = timeline
    if sno == '':
        for p in bt.rows[i].cells[1].paragraphs:
            for run in p.runs:
                run.bold = True

doc.add_paragraph('')
# Total row
tp = doc.add_paragraph()
tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = tp.add_run('TOTAL PROJECT BUDGET: INR 28,50,000 (Twenty-Eight Lakhs Fifty Thousand Only)')
r.bold = True; r.font.size = Pt(12)
doc.add_paragraph('')

add_p('The budget allocation reflects a deliberate emphasis on community-facing deployment (Tasks 2 and 3 collectively representing 46% of total expenditure) over purely academic infrastructure, ensuring that the majority of invested resources translate directly into observable community-level protection outcomes. The JRF/SRF fellowship component (45.6% of total) represents the single largest investment, reflecting the labor-intensive nature of integrated field research combining remote sensing analysis, hydrological modeling, sensor deployment, community engagement, and multi-stakeholder coordination within a compressed 36-month timeline.')

# === SECTION 6 ===
add_h('6. INSTITUTIONAL SUSTAINABILITY, POLICY INTEGRATION AND FEASIBILITY MODEL', level=1)

add_h('6.1 Legislative Integration Under DM Act 2005', level=2)
add_p('The project is architecturally designed for seamless integration into India\'s existing disaster management legislative framework without requiring any modifications to current law or policy. Under the Disaster Management Act of 2005, District Disaster Management Authorities (DDMAs) are mandated (Section 30) to prepare District Disaster Management Plans (DDMPs) incorporating hazard identification, vulnerability assessment, and preparedness measures. The project outputs\u2014specifically the Digital Flood Vulnerability Atlas, the IoT early warning system operational protocols, and the NbS pilot site design templates\u2014are formatted as direct plug-and-play annexures to existing DDMPs, requiring only a District Magistrate\'s administrative order for formal incorporation into statutory planning documents.')
add_p('This design philosophy eliminates the single largest barrier to research-to-policy translation in India: the requirement for legislative or regulatory change. The project provides district administrations with turnkey technical content that they can immediately adopt within their existing mandated planning processes. The template format is standardized to enable replication across all 13 districts of Uttarakhand (and subsequently across 25+ Himalayan districts in other states) without additional foundational research investment\u2014each new district requiring only localized data ingestion and calibration within the established methodological framework.')

add_h('6.2 Post-Project Financial Sustainability Model', level=2)
add_p('The project is designed not merely as a time-bound research initiative but as an institutional capability-building exercise that generates self-sustaining revenue pathways beyond the grant period. The research outputs function as an unlocked commercial asset pipeline enabling multiple monetization channels:')
add_b('Corporate CSR Consultancies: The validated methodology and demonstrated pilot outcomes position the institutional team to provide fee-for-service flood vulnerability assessments and NbS design services to corporate clients with ESG obligations and CSR mandates (Companies Act 2013 Section 135). Estimated revenue potential: INR 5-15 lakhs per assignment for industrial site vulnerability assessments and NbS design.')
add_b('SDMA Implementation Grants: Demonstrated operational success of the pilot IoT-EWS positions the team as preferred implementing partners for state-level SDMA programs seeking to scale early warning coverage across additional districts. The Uttarakhand SDMA\'s current 5-year action plan includes INR 47 Crore allocation for early warning system expansion\u2014representing a directly addressable market for the project team\'s proven capabilities.')
add_b('Multilateral Project Preparation Facilities: The combination of rigorous academic validation (SCIE publications), demonstrated field deployment (operational IoT-EWS), and quantified economic returns (benefit-cost analysis) positions the institutional team to access large-scale multilateral climate finance as technical preparation consultants. Specifically, the Green Climate Fund (GCF), Asian Development Bank (ADB) Climate Investment Funds, and World Bank\'s Global Facility for Disaster Reduction and Recovery (GFDRR) routinely commission project preparation studies valued at INR 20-500 Crore for full-scale national flood resilience programs. The outputs of this INR 28.5 lakh investment provide precisely the evidence base and technical credibility required to access these significantly larger funding envelopes.')
add_b('Data-as-a-Service: The Digital Flood Vulnerability Atlas and real-time sensor data streams represent monetizable digital assets. Insurance companies (crop insurance under PMFBY, property insurance), real estate developers, and infrastructure planning agencies represent potential subscription clients for regularly updated vulnerability intelligence products.')

add_h('6.3 Scalability and Replication Pathway', level=2)
add_p('The project\'s replication pathway is designed for geometric scaling: Year 1-3 establishes proof-of-concept in a single micro-watershed (protecting ~2,500 households); Years 4-5 (through follow-on SDMA/NDMA funding) expands to 5 additional micro-watersheds within Uttarakhand (protecting ~12,500 households); Years 6-8 (through multilateral project preparation) enables state-wide and multi-state scaling across the entire Indian Himalayan Region (potential protection of 500,000+ households). Each scaling stage reduces marginal cost-per-household-protected by approximately 40% due to methodological standardization, reusable analytical frameworks, and institutional learning effects.')

add_h('6.4 Risk Management and Mitigation Strategy', level=2)
add_p('The proposal acknowledges and proactively addresses key implementation risks:')
add_b('Sensor Failure Risk: Mitigated through redundant sensor placement (3 units providing overlapping coverage), solar-battery hybrid power systems designed for 72-hour autonomous operation during cloudy periods, and quarterly preventive maintenance protocols.')
add_b('Community Engagement Risk: Mitigated through early-stage Van Panchayat and Gram Sabha institutional buy-in (formal resolutions), integration with existing SHG networks, and MGNREGA wage convergence ensuring direct economic benefits to participating households.')
add_b('Climate Variability Risk: The project\'s non-stationary analytical framework explicitly accounts for intensifying precipitation trends. Sensor alert thresholds are recalibrated annually using updated frequency analysis, preventing obsolescence under changing climate conditions.')
add_b('Institutional Transition Risk: All technical knowledge is documented in open-access manuals, all code is published on GitHub/institutional repositories, and all sensor maintenance protocols are transferred to trained community volunteers\u2014ensuring continuity independent of individual researcher availability.')

doc.add_page_break()
add_h('DECLARATION', level=1)
add_p('We hereby declare that this proposal represents original work prepared specifically for submission to the identified funding body. The proposed activities do not duplicate any ongoing funded research. All budget items represent genuine estimated costs. The institutional infrastructure and human resources described are available and committed for the proposed project tenure.')
doc.add_paragraph('')
doc.add_paragraph('')

sig1 = doc.add_paragraph()
sig1.add_run('_________________________\t\t\t_________________________').font.size = Pt(11)
sig2 = doc.add_paragraph()
sig2.add_run('Dr. Nidhi Rawat\t\t\t\t\tRaj Amritam').font.size = Pt(11)
sig3 = doc.add_paragraph()
sig3.add_run('Principal Investigator\t\t\t\t\tCo-PI / PhD Research Scholar').font.size = Pt(11)
sig4 = doc.add_paragraph()
sig4.add_run('Department of Environmental Science\t\t\tDBS Global University, Dehradun').font.size = Pt(11)

# Save
output = '/projects/sandbox/mobile-printer-app/Grant_Funding_Proposal_Raj_Amritam.docx'
doc.save(output)
print(f"Document saved: {output}")
print(f"File size: {os.path.getsize(output)} bytes")
