#!/usr/bin/env python3
"""
Generate Grant Funding Proposal .docx file
Output: Grant_Funding_Proposal_Raj_Amritam.docx
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
import os

def set_cell_format(cell, text, bold=False, size=12):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold

def add_paragraph(doc, text, bold=False, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, font_size=12):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.bold = bold
    return p

def add_heading_custom(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.line_spacing = 1.5
    for run in h.runs:
        run.font.name = 'Times New Roman'
    return h

def create_document():
    doc = Document()
    
    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5


    # ==================== TITLE PAGE ====================
    add_paragraph(doc, "ON-GROUND PROJECT / GRANT FUNDING PROPOSAL", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=14)
    add_paragraph(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    title_text = ("Developing an Integrated Hydro-Spatial Framework for Eco-Safe Himalayan Catchments: "
                  "A Hybrid Academic-Deployment Strategy for Nature-Based Flood Mitigation, "
                  "IoT-Enabled Early Warning Systems & Community Climate Resilience")
    add_paragraph(doc, title_text, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=13)
    add_paragraph(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Submitted to:", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "NMHS / DST-NMSHE / NAFCC", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Submitted by:", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Department of Environmental Science", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "DBS Global University, Dehradun", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Principal Investigator: Dr. Nidhi Rawat, Associate Professor", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Co-Principal Investigator: Raj Amritam, PhD Research Scholar", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "Year: 2025", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    doc.add_page_break()


    # ==================== SECTION 1: PROJECT IDENTIFICATION ====================
    add_heading_custom(doc, "Section 1: Project Identification & Metadata", level=1)
    
    table_data = [
        ("Project Title", "Developing an Integrated Hydro-Spatial Framework for Eco-Safe Himalayan Catchments: A Hybrid Academic-Deployment Strategy for Nature-Based Flood Mitigation, IoT-Enabled Early Warning Systems & Community Climate Resilience"),
        ("Proposed Tenure", "36 Months (3-Year Fast-Track Strategy)"),
        ("Total Financial Request", "INR 28,50,000 (Twenty-Eight Lakhs Fifty Thousand Only)"),
        ("Targeted Field Region", "Garhwal Himalayan Region, Uttarakhand, India"),
        ("Direct Institutional Affiliation", "Department of Environmental Science, DBS Global University, Dehradun"),
        ("Principal Investigator", "Dr. Nidhi Rawat, Associate Professor, Department of Environmental Science, DBS Global University"),
        ("Co-PI / Research Scholar", "Raj Amritam, PhD Research Scholar, Department of Environmental Science, DBS Global University"),
        ("Strategic Alignment", "Sendai Framework Targets A, B, C, D, and G; WMO Early Warnings for All (EW4All) Initiative; NAPCC National Water Mission"),
        ("Institutional Mandate", "DM Act 2005 (Sec. 30-31); SDMA Uttarakhand Guidelines; NDMA Flash Flood Management Guidelines 2022"),
    ]
    
    table = doc.add_table(rows=len(table_data), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, (field, value) in enumerate(table_data):
        set_cell_format(table.rows[i].cells[0], field, bold=True)
        set_cell_format(table.rows[i].cells[1], value)
    
    doc.add_paragraph()


    # ==================== SECTION 2: EXECUTIVE SUMMARY ====================
    add_heading_custom(doc, "Section 2: Executive Summary & Strategic Rationale", level=1)
    
    exec_para1 = (
        "The Garhwal Himalayan region of Uttarakhand represents one of the most climatically vulnerable "
        "mountain territories in the global South, characterized by extreme orographic precipitation ranging "
        "from 1,200 mm in the lower Shiwalik foothills to over 3,500 mm in the Greater Himalayan zones. "
        "This precipitation regime, intensified by anthropogenic climate change and shifting monsoon dynamics, "
        "operates upon a geological substrate defined by the Main Central Thrust (MCT) and Main Boundary Thrust (MBT) "
        "tectonic systems, producing inherently unstable slope conditions across inhabited territory. "
        "The degradation of forest cover—accelerated by road construction, hydropower development, and changing "
        "agricultural patterns—has removed critical natural buffering capacity, resulting in a documented acceleration "
        "of hydro-meteorological disasters including flash floods, debris flows, and glacial lake outburst floods (GLOFs). "
        "The Indian Meteorological Department records indicate that extreme rainfall events (>100 mm/day) have increased "
        "by approximately 40% in the Central Himalayan region over the past three decades. The intersection "
        "of tectonic instability, extreme precipitation variability, rapid land-use transformation, and growing "
        "population pressure in valley floors creates a compounding risk environment that demands fundamentally "
        "new approaches to disaster risk reduction."
    )
    add_paragraph(doc, exec_para1)
    
    exec_para2 = (
        "The catastrophic Chamoli disaster of February 2021 stands as a stark illustration of these compounding "
        "vulnerabilities. A massive glacial-rock avalanche originating from the Ronti Peak area triggered a "
        "devastating debris flow that traveled over 15 kilometers through the Rishiganga and Dhauliganga valleys, "
        "destroying two hydropower projects (the 13.2 MW Rishiganga and the under-construction 520 MW Tapovan Vishnugad), "
        "killing over 200 individuals, and displacing thousands of families. The disaster revealed catastrophic "
        "failures in India's early warning architecture: no sensor detected the initial avalanche, no automated "
        "warning reached downstream communities, and evacuation began only after visual confirmation by workers "
        "at the Rishiganga plant—by which point the debris flow was already upon downstream settlements. "
        "More recently, the Dharali flash floods of August 2025 inundated three villages in the Bhagirathi "
        "catchment with zero prior warning, despite the affected area falling within the operational jurisdiction "
        "of multiple state and national monitoring agencies. These events are not anomalies but rather symptoms "
        "of a systemic failure: India possesses substantial scientific capacity in hydrology, remote sensing, "
        "and climate science, yet this capacity remains disconnected from the communities most at risk. "
        "The institutional architecture that separates research from deployment, academia from governance, "
        "and technology from community practice ensures that scientific advances remain confined to journal "
        "publications while vulnerable populations continue to face unmitigated risk."
    )
    add_paragraph(doc, exec_para2)


    exec_para3 = (
        "This proposal presents a fundamentally different paradigm: a dual-structure 'Brain + Body' approach "
        "that integrates rigorous academic computational research (the 'Brain') with on-ground community deployment "
        "infrastructure (the 'Body') within a single 36-month project window. The 'Brain' component encompasses "
        "advanced GIS-based vulnerability mapping using Analytical Hierarchy Process multi-criteria decision analysis, "
        "hydrological modeling through SWAT and HEC-RAS frameworks, satellite-derived change detection using "
        "Sentinel-2 multispectral and Sentinel-1 SAR data, and IoT-based telemetry system design. The 'Body' "
        "component delivers tangible community protection through ecological engineering interventions (Nature-Based "
        "Solutions), automated early warning dissemination via WhatsApp and SMS platforms, community capacity building "
        "through Self-Help Group (SHG) emergency task forces, and institutional integration through District Disaster "
        "Management Plan (DDMP) annexures. This dual structure ensures that every computational advance directly "
        "informs a deployment decision, and every deployment outcome feeds back into model calibration and validation. "
        "The project thus generates simultaneously SCIE-indexed publishable academic outputs—including vulnerability "
        "atlases, NbS performance assessments, and EWS efficacy evaluations—AND functioning community-level protection "
        "infrastructure that operates independently beyond the project period."
    )
    add_paragraph(doc, exec_para3)
    
    exec_para4 = (
        "Conventional academic research projects in India's disaster risk reduction space typically produce "
        "publications, conference presentations, and technical reports that accumulate citations but rarely "
        "translate into reduced mortality or economic losses at the community level. Conversely, development "
        "projects funded through government schemes often deploy infrastructure—check dams, retaining walls, "
        "warning sirens—without the rigorous baseline assessment, monitoring protocols, or adaptive management "
        "frameworks necessary to ensure long-term effectiveness. This proposal explicitly bridges this divide "
        "by embedding academic rigor within a deployment framework and constraining deployment decisions within "
        "evidence-based parameters. The Analytical Hierarchy Process vulnerability assessment, for example, "
        "does not merely produce a research paper; it directly determines the spatial targeting of NbS interventions "
        "and IoT sensor placement. The ecological engineering pilot does not merely reduce erosion; it generates "
        "calibration data for the SWAT hydrological model while simultaneously creating MGNREGA employment "
        "and strengthening Van Panchayat institutional capacity. Every project activity thus serves dual purposes: "
        "advancing scientific understanding while delivering measurable community protection outcomes."
    )
    add_paragraph(doc, exec_para4)
    
    exec_para5 = (
        "International precedents validate this integrated approach. The Netherlands' 'Room for the River' program "
        "(2006-2019) demonstrated that nature-based flood management could achieve 35 cm peak water level reduction "
        "across 39 intervention sites while simultaneously enhancing ecological connectivity and recreational value—all "
        "at costs comparable to conventional grey infrastructure. ICIMOD's transboundary early warning systems across "
        "Nepal and India have demonstrated that community-embedded IoT networks can achieve 3-8 hour flash flood lead "
        "times in Himalayan catchments, sufficient for evacuation of valley-floor settlements. A rigorous randomized "
        "controlled trial of flood forecasting in Bihar demonstrated that even basic early warning (24-48 hour lead time) "
        "reduced medical expenditures by 30%, livestock mortality by 22%, and crop losses by 18% among recipient "
        "households compared to control villages—representing benefit-cost ratios exceeding 10:1. These precedents "
        "establish that integrated hydro-spatial frameworks combining computational modeling, nature-based interventions, "
        "and community-embedded warning systems can deliver transformative protection outcomes at costs far below "
        "conventional engineering approaches."
    )
    add_paragraph(doc, exec_para5)


    exec_para6 = (
        "The proposed project budget of INR 28,50,000 over 36 months translates to approximately INR 1,140 per "
        "protected household across the 2,500 households in the target micro-watershed cluster—a figure that compares "
        "extraordinarily favorably against conventional flood protection infrastructure (typically INR 15,000-50,000 "
        "per household for gabion walls and concrete embankments) while delivering superior long-term sustainability "
        "through self-maintaining ecological systems and community-owned warning infrastructure. The framework is "
        "designed for replication across all 13 districts of Uttarakhand and potentially 25+ Himalayan districts "
        "in Himachal Pradesh, Sikkim, Arunachal Pradesh, and Jammu & Kashmir, representing a scalable template "
        "for India's broader climate adaptation strategy. The project directly addresses the fundamental disconnect "
        "between India's considerable scientific capacity in earth sciences and its persistently inadequate deployment "
        "capacity in disaster risk reduction—a disconnect that costs hundreds of lives and billions of rupees annually "
        "in preventable losses. By demonstrating that a single integrated project can generate SCIE publications, "
        "functioning early warning systems, ecological infrastructure, community capacity, and policy-ready "
        "institutional frameworks within a 36-month window and INR 28.5 lakh budget, this proposal establishes "
        "a replicable model for transforming India's approach to Himalayan disaster risk reduction from reactive "
        "response to proactive, science-informed, community-embedded resilience building."
    )
    add_paragraph(doc, exec_para6)


    # ==================== SECTION 3: DUAL-STRUCTURE LINKAGE MATRIX ====================
    add_heading_custom(doc, "Section 3: Dual-Structure Linkage Matrix & Scope of Work", level=1)
    
    # 3.1 Task 1
    add_heading_custom(doc, "3.1 Task 1: Digital Flood Vulnerability Atlas — Resource Deployment", level=2)
    
    task1_para1 = (
        "The Digital Flood Vulnerability Atlas constitutes the foundational analytical layer upon which all subsequent "
        "project interventions are spatially targeted and prioritized. This atlas will be developed as an open-access, "
        "web-hosted Geographic Information System portal providing vulnerability assessments at the Gram Panchayat "
        "and Block Development level—the administrative scales at which disaster management planning and resource "
        "allocation actually occur in India's federal governance structure. The atlas covers over 150 Gram Panchayats "
        "within the Garhwal Himalayan study region, providing ward-level vulnerability classifications that enable "
        "District Disaster Management Authorities to identify priority intervention areas with unprecedented spatial "
        "precision. The analytical methodology employs Analytical Hierarchy Process (AHP) weighted multi-criteria "
        "analysis integrating four thematic dimensions: topographic parameters (slope gradient, Topographic Wetness "
        "Index, Height Above Nearest Drainage), hydrological characteristics (drainage density, SCS Curve Number "
        "runoff potential), land-use dynamics (impervious surface fraction, decadal forest cover loss rates), and "
        "socio-demographic vulnerability indicators (Scheduled Caste/Scheduled Tribe population proportion, "
        "female-headed household density, Below Poverty Line concentration). Each parameter is derived from "
        "publicly available datasets ensuring reproducibility and long-term updatability: Sentinel-2 multispectral "
        "imagery at 10-meter resolution for land-use classification, SRTM and ALOS PALSAR Digital Elevation Models "
        "at 30-meter and 12.5-meter resolution respectively for terrain analysis, ISRIC SoilGrids for infiltration "
        "parameters, CHIRPS and GPM IMERG for precipitation characterization, and Census 2011 data for demographic "
        "vulnerability layers."
    )
    add_paragraph(doc, task1_para1)
    
    task1_para2 = (
        "The AHP weight determination process follows a structured expert panel methodology designed to minimize "
        "subjectivity while incorporating domain expertise. A panel of eight specialists—comprising hydrologists, "
        "geomorphologists, remote sensing scientists, social vulnerability researchers, and disaster management "
        "practitioners—will conduct pairwise comparison of all criteria using Saaty's fundamental scale (1-9). "
        "The resulting comparison matrices will be tested for logical consistency using the Consistency Ratio (CR), "
        "with only matrices achieving CR < 0.10 accepted for weight derivation. This threshold ensures that expert "
        "judgments are internally coherent and do not contain circular preference patterns. The derived weights "
        "are then applied to normalized indicator layers using weighted linear combination in a GIS environment, "
        "producing composite vulnerability indices at 30-meter pixel resolution that are subsequently aggregated "
        "to administrative boundaries. Validation employs historical flood inventory data compiled from three "
        "independent sources: SDMA Uttarakhand official disaster records (2010-2024), Sentinel-1 SAR-derived "
        "flood extent maps for major events, and community-reported flood histories collected through participatory "
        "mapping exercises in 20 validation villages. The concordance between modeled high-vulnerability zones "
        "and documented flood occurrences provides quantitative validation metrics (Area Under ROC Curve > 0.75 "
        "target). The atlas outputs are formatted as direct annexures to District Disaster Management Plans under "
        "Section 31 of the DM Act 2005, requiring no legislative change for immediate operational adoption by "
        "District Magistrates through administrative order. Priority micro-watershed ranking enables targeted "
        "allocation of limited resources to areas of maximum vulnerability and population exposure, transforming "
        "disaster management from reactive response to evidence-based proactive planning."
    )
    add_paragraph(doc, task1_para2)


    # 3.2 Task 2
    add_heading_custom(doc, "3.2 Task 2: Ecological Engineering — Physical NbS Pilot Deployment", level=2)
    
    task2_para1 = (
        "The ecological engineering component deploys a 2-hectare Nature-Based Solutions (NbS) pilot in the "
        "highest-priority micro-watershed identified through the vulnerability atlas analysis. This intervention "
        "represents a deliberate departure from conventional grey infrastructure approaches (concrete check dams, "
        "gabion walls, RCC retaining structures) that dominate India's current flood management expenditure. "
        "The pilot site is selected through overlay analysis of vulnerability scores, population exposure, "
        "accessibility for monitoring, and institutional readiness (presence of active Van Panchayat and Self-Help "
        "Groups). The intervention design integrates multiple complementary ecological engineering techniques: "
        "bamboo check structures constructed from locally harvested Dendrocalamus strictus sourced through Van "
        "Panchayat forest management agreements, Vetiver grass (Chrysopogon zizanioides) contour hedgerows for "
        "slope stabilization and sediment interception, Napier grass (Pennisetum purpureum) buffer strips along "
        "drainage lines for velocity reduction and nutrient capture, contour stone bunding using locally available "
        "materials for overland flow interception, and riparian buffer plantation using indigenous species—Alnus "
        "nepalensis (Utis) for nitrogen fixation and rapid biomass production, Grewia optiva (Bhimal) for soil "
        "binding and fodder value, and Celtis australis (Khirak) for deep-rooted slope anchoring. This multi-species, "
        "multi-technique approach ensures functional redundancy: if any single intervention underperforms due to "
        "site-specific conditions, the remaining elements maintain aggregate protective function."
    )
    add_paragraph(doc, task2_para1)
    
    task2_para2 = (
        "A critical innovation in this deployment strategy is the convergence with existing government employment "
        "and forest governance programs to achieve zero wage cost and long-term maintenance sustainability. All "
        "physical labor for site preparation, planting, bunding, and structure construction is implemented through "
        "MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act), generating 450-600 person-days of "
        "employment for local households while imposing no wage burden on the project budget. Van Panchayat "
        "coordination ensures bamboo and other materials are sustainably harvested under existing community forest "
        "management plans, while simultaneously building institutional ownership that ensures maintenance beyond "
        "the project period. The monitoring protocol establishes quantitative performance targets: minimum 20% "
        "flow velocity reduction measured through float method transit times and continuous pressure transducer "
        "records at upstream and downstream stations; minimum 30% topsoil conservation quantified through paired "
        "sediment trap measurements and cross-validated against Revised Universal Soil Loss Equation (RUSLE) "
        "modeling; and minimum 15% infiltration enhancement measured through double-ring infiltrometer tests "
        "conducted at 6-month intervals across treated and control plots. These monitoring data serve dual purposes: "
        "validating NbS performance for academic publication in journals such as Ecological Engineering and "
        "Catena, while simultaneously providing calibration parameters for the SWAT hydrological model that "
        "underlies the vulnerability atlas. Indigenous knowledge integration occurs through structured elicitation "
        "workshops with elderly community members, documenting traditional land management practices (such as "
        "chaal-khal water harvesting and ban panchayat rotational forest management) that inform intervention "
        "design and ensure cultural acceptability of deployed solutions."
    )
    add_paragraph(doc, task2_para2)


    # 3.3 Task 3
    add_heading_custom(doc, "3.3 Task 3: IoT Telemetry System — Community Early Warning", level=2)
    
    task3_para1 = (
        "The IoT-based community early warning system deploys a network of three automated river-level monitoring "
        "sensors and one micro-Automatic Weather Station (micro-AWS) across the target micro-watershed, connected "
        "through a hybrid GPRS/LoRa communication architecture to a cloud-based alert generation and dissemination "
        "platform. Each river-level sensor combines ultrasonic distance measurement (primary) with submersible "
        "pressure transducer (backup) to ensure measurement continuity across the extreme conditions encountered "
        "during Himalayan monsoon floods—conditions that routinely destroy single-sensor installations through "
        "debris impact, submersion, or bank erosion. The sensors are solar-powered with lithium iron phosphate "
        "(LiFePO4) battery banks providing 72-hour autonomous operation during extended cloud cover periods, "
        "housed in IP67-rated enclosures mounted on reinforced concrete piers positioned above documented maximum "
        "flood levels. The micro-AWS measures rainfall (tipping bucket, 0.2mm resolution), temperature, relative "
        "humidity, wind speed and direction, and barometric pressure at 5-minute intervals, providing the "
        "meteorological forcing data necessary for real-time threshold-based alert generation. Data transmission "
        "occurs via GPRS (primary) with LoRa mesh relay (backup) to a cloud server running threshold comparison "
        "algorithms calibrated against HEC-RAS hydraulic modeling of the target reaches."
    )
    add_paragraph(doc, task3_para1)
    
    task3_para2 = (
        "The alert dissemination architecture employs a three-tier cascade designed to reach all community members "
        "regardless of technology access, literacy level, or physical mobility. The primary tier uses WhatsApp "
        "Business API integrated with the cloud server for automated message generation and delivery to registered "
        "community WhatsApp groups, supplemented by SMS alerts via Exotel/Knowlarity IVR (Interactive Voice Response) "
        "platforms for households without smartphones or reliable internet connectivity. All messages are generated "
        "in bilingual format (Hindi and Garhwali) using pre-tested templates validated for greater than 80% "
        "comprehension across demographic groups including non-literate individuals, women in restricted mobility "
        "situations, and elderly persons with hearing impairment. The secondary tier activates trained mukhiya "
        "(village head) volunteers who receive priority alerts and are responsible for door-to-door notification "
        "in their assigned sectors, ensuring reach to households that may not receive or comprehend digital messages. "
        "The tertiary tier employs manually-activated sirens positioned at strategic locations for mass notification "
        "during extreme events when digital infrastructure may be compromised. Performance targets include greater "
        "than 45-minute flash-flood lead time (validated against sensor-to-impact travel time for the target reaches), "
        "greater than 95% sensor uptime during the critical June-September monsoon season, and greater than 80% "
        "message comprehension validated through a 100+ respondent post-alert survey conducted after each monsoon "
        "season. The threshold calibration methodology uses HEC-RAS one-dimensional unsteady flow modeling of "
        "the target river reaches, with rating curves developed from manual discharge measurements during the "
        "first monsoon season providing the stage-discharge relationships necessary for translating sensor readings "
        "into flood severity classifications. The graceful degradation architecture ensures that failure of any "
        "single component—sensor, communication link, server, or dissemination channel—does not result in complete "
        "warning system failure: LoRa backup maintains data flow if GPRS fails, pressure transducers continue "
        "measuring if ultrasonic sensors are damaged, SMS reaches households if WhatsApp is unavailable, and "
        "mukhiya volunteers provide human backup if all digital channels fail simultaneously. Annual pre-monsoon "
        "calibration protocol includes sensor cleaning, solar panel maintenance, battery replacement assessment, "
        "threshold review based on channel morphology changes, and communication system end-to-end testing with "
        "SDMA dashboard integration verification."
    )
    add_paragraph(doc, task3_para2)


    # ==================== SECTION 4: FOUR-PILLAR EW4ALL ====================
    add_heading_custom(doc, "Section 4: Four-Pillar EW4All Operational Architecture", level=1)
    
    add_heading_custom(doc, "4.1 Pillar 1: Risk Knowledge", level=2)
    pillar1 = (
        "The Risk Knowledge pillar establishes the comprehensive understanding of hazard patterns, exposure "
        "concentrations, and vulnerability distributions that underpins all subsequent early warning operations. "
        "This pillar integrates three primary knowledge streams: the AHP-GIS vulnerability layers generated through "
        "Task 1 (providing static vulnerability characterization at 30-meter resolution), historical event inventories "
        "compiled from SDMA official records, Sentinel-1 SAR-derived flood extent maps, and systematically collected "
        "community flood narratives (providing empirical validation and temporal pattern recognition), and continuously "
        "updated demographic vulnerability data disaggregated by gender, caste, economic status, age, and disability "
        "to ensure that warning systems explicitly account for differential vulnerability within communities. The "
        "gender and caste disaggregation is particularly critical in the Himalayan context where women's restricted "
        "mobility during certain periods, Scheduled Caste settlements' frequent location in flood-prone valley floors "
        "due to historical land allocation patterns, and elderly populations' limited capacity for rapid evacuation "
        "create differential risk profiles that uniform warning approaches fail to address. The continuous updating "
        "protocol ensures that risk knowledge evolves with changing conditions: post-monsoon assessment incorporates "
        "new flood events, land-use change detection updates vulnerability layers annually, and community feedback "
        "identifies emerging risk concentrations not captured by remote sensing alone. This dynamic risk knowledge "
        "base feeds directly into Pillar 2 threshold calibration and Pillar 3 message targeting, creating an "
        "adaptive system that becomes more effective with each monsoon season of operation."
    )
    add_paragraph(doc, pillar1)
    
    add_heading_custom(doc, "4.2 Pillar 2: Detection & Forecasting", level=2)
    pillar2 = (
        "The Detection and Forecasting pillar encompasses the IoT sensor array, data transmission infrastructure, "
        "and threshold-based alert generation algorithms that transform raw environmental observations into actionable "
        "flood warnings. The sensor network transmits data at 5-minute intervals during monsoon season (reduced to "
        "15-minute intervals during dry season to conserve battery and communication resources), providing the temporal "
        "resolution necessary for flash flood detection in steep Himalayan catchments where time-to-peak can be as "
        "short as 30-45 minutes. The threshold-based forecasting system operates on three alert levels—Yellow (advisory), "
        "Orange (warning), and Red (emergency)—calibrated against HEC-RAS hydraulic modeling of the target river reaches. "
        "Each threshold corresponds to specific stage levels at sensor locations that correlate with documented inundation "
        "of particular settlement zones downstream. Probabilistic uncertainty bounds are incorporated through ensemble "
        "threshold ranges that account for measurement uncertainty and channel morphology changes. The graceful degradation "
        "design ensures continued warnings under component failure: if the primary ultrasonic sensor fails, the backup "
        "pressure transducer maintains measurement; if GPRS fails, LoRa mesh relay maintains data flow; if the cloud "
        "server experiences downtime, edge computing enables local threshold comparison and direct alert triggering. "
        "This redundancy is calibrated against documented 20-40% component failure rates of previous Himalayan "
        "installations during extreme events. The system integrates with IMD nowcast data when available but operates "
        "independently of external data streams to ensure warning capability during communication disruption."
    )
    add_paragraph(doc, pillar2)


    add_heading_custom(doc, "4.3 Pillar 3: Warning Dissemination & Communication", level=2)
    pillar3 = (
        "The Warning Dissemination pillar translates automated sensor-derived alerts into comprehensible, actionable "
        "messages reaching every individual within the protected population, regardless of their technology access, "
        "literacy level, language preference, or physical capabilities. The primary dissemination channel utilizes "
        "WhatsApp Business API for smartphone-equipped households (estimated 60-70% penetration in target communities) "
        "and SMS via Exotel/Knowlarity IVR platforms for feature phone users. All automated messages are generated "
        "in bilingual Hindi and Garhwali formats, using vocabulary and sentence structures pre-tested through focus "
        "group discussions with representative community members including non-literate women, elderly persons, and "
        "individuals with hearing or visual impairments. Message templates follow the Common Alerting Protocol (CAP) "
        "structure: WHAT is happening, WHERE it will impact, WHEN it will arrive, and WHAT ACTION to take—expressed "
        "in directive language validated for greater than 80% comprehension across all demographic groups. The secondary "
        "channel activates trained mukhiya volunteers organized in a geographic sector system. Each volunteer covers "
        "15-25 households, receives priority alerts 5 minutes before general notification, and conducts door-to-door "
        "verification. This human layer reaches elderly persons who keep phones switched off, women whose phone "
        "access is mediated by male household members, persons with disabilities, and households in cellular dead "
        "zones. The tertiary channel employs manually-activated sirens at three locations providing audible coverage "
        "to the entire settlement cluster, activated upon Red-level alert confirmation. This three-tier architecture "
        "ensures no single point of failure results in unwarned populations."
    )
    add_paragraph(doc, pillar3)
    
    add_heading_custom(doc, "4.4 Pillar 4: Preparedness & Response Capacity", level=2)
    pillar4 = (
        "The Preparedness pillar builds community capacity to translate received warnings into effective protective "
        "action through trained human resources, practiced evacuation procedures, pre-positioned supplies, and "
        "institutionalized response protocols. Two mandatory evacuation drills are conducted annually (May pre-monsoon "
        "and August mid-monsoon) simulating the complete alert cascade from sensor detection through community "
        "evacuation, with drill performance metrics including time-to-complete-evacuation, coverage of vulnerable "
        "populations, and communication chain completion rates feeding into system improvement protocols. Self-Help "
        "Group (SHG) Emergency Task Forces are established with minimum 50% women membership, trained in first aid "
        "(including snakebite management critical in monsoon conditions), search and rescue techniques appropriate "
        "for flood conditions, evacuation route management including livestock protection protocols (livestock "
        "representing 30-50% of household asset value in target communities), and post-disaster rapid needs "
        "assessment using standardized SPHERE-compliant assessment formats. These SHG Task Forces serve as the "
        "permanent community institution for disaster preparedness, operating year-round for risk awareness, "
        "seasonal preparedness activities, and emergency response. Evacuation routes are mapped, signposted, "
        "cleared annually, and validated through drill exercises to ensure accessibility for wheelchair users, "
        "elderly persons with mobility limitations, and families with young children. Post-disaster needs assessment "
        "protocols enable rapid damage documentation for insurance claims, SDRF/NDRF assistance applications, and "
        "compensation processing—addressing the documented failure of post-disaster support systems to reach "
        "marginalized households that lack documentation capacity. Recognition under DM Act Section 41 for volunteer "
        "organizations provides legal framework and insurance coverage for task force members during emergency "
        "operations. The four pillars operate as a continuous feedback loop: risk knowledge informs detection "
        "thresholds, detection triggers dissemination, dissemination activates preparedness, and preparedness "
        "outcomes (drill performance, response effectiveness) feed back into risk knowledge updates and system "
        "refinement, creating an adaptive architecture that improves with each cycle of operation."
    )
    add_paragraph(doc, pillar4)


    # ==================== SECTION 5: BUDGET ====================
    add_heading_custom(doc, "Section 5: Itemized Budgetary & Financial Request Matrix", level=1)
    
    budget_data = [
        ("Code", "Item Description", "Amount (INR)", "Timeline"),
        ("A", "Capital & Analytical Equipment", "4,50,000", "Year 1"),
        ("A1", "IoT River-Level Sensors (3 units × 75,000)", "2,25,000", "Year 1 Q1-Q2"),
        ("A2", "Micro-Automatic Weather Station (1 unit)", "1,25,000", "Year 1 Q1"),
        ("A3", "GIS Workstation (64GB RAM, RTX GPU)", "1,00,000", "Year 1 Q1"),
        ("B", "Operational & Material Assets", "8,50,000", "Year 2"),
        ("B1", "Vegetative/Bamboo NbS Materials", "2,50,000", "Year 2 Q1-Q2"),
        ("B2", "Community Workshops & SHG Training", "1,50,000", "Years 1-3"),
        ("B3", "API Server & IVR Subscription", "1,80,000", "Years 1-3"),
        ("B4", "Satellite Processing Credits (GEE/AWS)", "70,000", "Years 1-2"),
        ("B5", "Field Instrumentation (Infiltrometers, Sediment Traps)", "1,00,000", "Years 1-2"),
        ("B6", "Civil Works & Tools for NbS Deployment", "1,00,000", "Year 2"),
        ("C", "Manpower & Fellowship", "13,00,000", "Years 1-3"),
        ("C1", "JRF/SRF Fellowship (35,000/month × 36 months)", "12,60,000", "Years 1-3"),
        ("C2", "Field Surveyors (Seasonal Monsoon Support)", "40,000", "Monsoon Season"),
        ("D", "Travel & Contingency", "2,50,000", "Years 1-3"),
        ("D1", "Field Travel (Fuel, Vehicle Hire, Per Diem)", "1,20,000", "Years 1-3"),
        ("D2", "Conference Participation & Dissemination", "80,000", "Years 2-3"),
        ("D3", "Institutional Overheads + 10% Contingency", "50,000", "Years 1-3"),
        ("", "GRAND TOTAL", "28,50,000", "36 Months"),
    ]
    
    budget_table = doc.add_table(rows=len(budget_data), cols=4)
    budget_table.style = 'Table Grid'
    budget_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, row_data in enumerate(budget_data):
        for j, cell_text in enumerate(row_data):
            bold = (i == 0 or i == len(budget_data) - 1 or row_data[0] in ['A', 'B', 'C', 'D'])
            set_cell_format(budget_table.rows[i].cells[j], cell_text, bold=bold, size=10)
    
    doc.add_paragraph()


    budget_rationale1 = (
        "The budget allocation reflects a deliberate strategic prioritization of human capital and community engagement "
        "over capital equipment, recognizing that sustainable disaster risk reduction outcomes depend primarily on "
        "institutional capacity and community ownership rather than technology alone. The largest single allocation "
        "(Category C, INR 13,00,000, representing 45.6% of total budget) supports the Junior/Senior Research Fellowship "
        "that enables full-time dedicated research effort across all three project tasks—a recognition that integrated "
        "projects spanning computational analysis, field deployment, and community engagement require sustained human "
        "commitment rather than periodic consultancy inputs. The IoT and AWS equipment (Category A, INR 4,50,000, "
        "15.8%) represents carefully selected instrumentation at the minimum specification necessary for reliable "
        "Himalayan monsoon operation, avoiding the common trap of over-specifying equipment that subsequently proves "
        "impossible to maintain in remote field conditions. Operational costs (Category B, INR 8,50,000, 29.8%) "
        "cover the actual deployment of NbS materials, community engagement activities, and digital infrastructure "
        "that constitute the project's tangible community-facing outputs."
    )
    add_paragraph(doc, budget_rationale1)
    
    budget_rationale2 = (
        "The cost-per-household analysis reveals extraordinary value-for-money compared to conventional alternatives. "
        "At INR 28,50,000 total cost protecting approximately 2,500 households (directly through early warning and "
        "NbS flood mitigation), the project achieves INR 1,140 per protected household—a figure that represents "
        "less than 3% of the cost of conventional grey infrastructure flood protection (gabion walls and concrete "
        "embankments typically cost INR 40,000-60,000 per linear meter, translating to INR 15,000-50,000 per "
        "protected household depending on settlement density). Moreover, unlike grey infrastructure that requires "
        "ongoing government maintenance budgets and typically degrades to non-functionality within 5-10 years in "
        "Himalayan conditions, the NbS and community-based early warning approaches are designed for self-sustaining "
        "operation through ecological succession (vegetative interventions become self-maintaining within 3-5 years) "
        "and community institutional ownership (SHG Task Forces and Van Panchayat management continue indefinitely). "
        "The Bihar flood forecasting RCT documented benefit-cost ratios exceeding 10:1 for basic early warning systems; "
        "given that this project additionally provides flood mitigation through NbS, the anticipated benefit-cost "
        "ratio is conservatively estimated at 15:1 to 25:1, representing one of the highest-return public investments "
        "available in India's climate adaptation portfolio."
    )
    add_paragraph(doc, budget_rationale2)
    
    budget_rationale3 = (
        "The budget explicitly excludes wage costs for physical NbS deployment labor (estimated INR 3-5 lakhs "
        "equivalent) by leveraging MGNREGA convergence, and excludes vegetative material costs for bamboo and "
        "timber by leveraging Van Panchayat forest produce rights. This convergence strategy effectively doubles "
        "the project's deployment capacity without additional financial requirement, while simultaneously generating "
        "rural employment and strengthening community forest governance institutions. The 10% contingency allocation "
        "under D3 provides buffer for the unpredictable cost variations inherent in Himalayan field operations "
        "(road closures requiring alternative transport, equipment damage during extreme weather, price inflation "
        "in remote procurement markets), ensuring project completion is not jeopardized by routine operational "
        "disruptions that are endemic to mountain research environments."
    )
    add_paragraph(doc, budget_rationale3)


    # ==================== SECTION 6: SUSTAINABILITY ====================
    add_heading_custom(doc, "Section 6: Institutional Sustainability, Policy Integration & Feasibility", level=1)
    
    # 6.1
    add_heading_custom(doc, "6.1 Legislative Integration Under DM Act 2005", level=2)
    legis_para1 = (
        "The project's institutional sustainability strategy is anchored in the Disaster Management Act 2005, which "
        "provides a comprehensive legislative framework for integrating project outputs into routine government "
        "operations without requiring any legislative amendment, policy change, or new institutional creation. "
        "Section 30 of the DM Act mandates every District Disaster Management Authority to prepare a District "
        "Disaster Management Plan (DDMP), while Section 31 specifies the minimum contents of such plans including "
        "vulnerability assessment, capacity assessment, and response procedures. The project's vulnerability atlas "
        "outputs are specifically formatted as plug-and-play annexures to existing DDMPs, requiring only an "
        "administrative order from the District Magistrate (who serves as Chair of the DDMA) for formal adoption. "
        "This design eliminates the most common barrier to research-to-policy translation in India: the requirement "
        "for new policy formulation, legislative amendment, or institutional restructuring that typically delays "
        "adoption by 3-7 years. The early warning system SOPs are formatted as appendices to DDMP response protocols, "
        "specifying trigger thresholds, communication chains, evacuation procedures, and inter-agency coordination "
        "mechanisms in the standardized format used by Uttarakhand SDMA across all 13 districts."
    )
    add_paragraph(doc, legis_para1)
    
    legis_para2 = (
        "The specific DDMP sections that project outputs directly map to include: Hazard and Vulnerability Assessment "
        "(Chapter 3 in standard DDMP format)—receiving the GIS vulnerability atlas layers and micro-watershed priority "
        "rankings; Early Warning System Protocol (Chapter 7)—receiving IoT sensor specifications, threshold parameters, "
        "communication SOPs, and escalation procedures; Community Preparedness (Chapter 8)—receiving SHG Task Force "
        "composition, drill protocols, evacuation route maps, and volunteer training curricula; and Resource Inventory "
        "(Chapter 9)—receiving equipment registers, sensor locations, and maintenance schedules. This mapping ensures "
        "that project outputs do not exist as standalone documents requiring separate institutional champions but "
        "rather integrate directly into the document that District Magistrates are legally mandated to implement. "
        "The replicability across all 13 districts of Uttarakhand is ensured by using standardized DDMP formats "
        "prescribed by SDMA, meaning that vulnerability atlas methodology, EWS protocols, and community preparedness "
        "frameworks developed for the pilot district can be adopted by other districts through simple administrative "
        "adaptation rather than fundamental redesign. Extension to 25+ Himalayan districts in other states (Himachal "
        "Pradesh, Sikkim, Meghalaya, Arunachal Pradesh) requires only substitution of state-specific DEM, land-use, "
        "and demographic data into the established analytical framework—a process documentable in standard operating "
        "procedures accessible to district-level GIS operators."
    )
    add_paragraph(doc, legis_para2)


    # 6.2
    add_heading_custom(doc, "6.2 Post-Project Financial Sustainability Model", level=2)
    sustain_para1 = (
        "The project's financial sustainability beyond the 36-month funding period is ensured through four distinct "
        "revenue and institutional support pathways that collectively guarantee continued operation and scaling without "
        "dependence on renewed grant funding. The first pathway leverages India's Corporate Social Responsibility "
        "mandate under Section 135 of the Companies Act 2013, which requires companies above specified profit "
        "thresholds to allocate 2% of average net profits to CSR activities including disaster management and "
        "environmental sustainability. The project team's demonstrated expertise in community-based disaster risk "
        "reduction—validated through published research, functioning field infrastructure, and DDMP integration—positions "
        "it to secure CSR consultancy assignments valued at INR 5-15 lakhs per assignment for companies seeking "
        "to fulfil CSR obligations in the disaster management and climate resilience domains. Companies operating "
        "hydropower, tourism, and infrastructure projects in Uttarakhand represent a particularly receptive market "
        "given their direct exposure to Himalayan flood risk and regulatory requirements for environmental and "
        "social safeguards."
    )
    add_paragraph(doc, sustain_para1)
    
    sustain_para2 = (
        "The second pathway accesses SDMA implementation grants through Uttarakhand SDMA's recently announced "
        "INR 47 Crore allocation for early warning system expansion across the state—a program that explicitly "
        "requires demonstrated proof-of-concept installations as prerequisites for large-scale deployment funding. "
        "This project's functioning EWS pilot, complete with performance data, community validation, and DDMP "
        "integration documentation, positions it as the leading candidate for scale-up funding across multiple "
        "districts. The third pathway involves multilateral climate finance through Green Climate Fund (GCF), "
        "Asian Development Bank (ADB), and Global Facility for Disaster Reduction and Recovery (GFDRR) programs "
        "that typically range from INR 20-500 Crore for state-wide or regional implementation of proven disaster "
        "risk reduction approaches. These multilateral programs require extensive proof-of-concept documentation, "
        "community validation evidence, and institutional framework demonstrations—precisely the outputs this "
        "project generates. The pathway from this INR 28.5 lakh investment to accessing INR 100+ Crore multilateral "
        "programs follows a documented progression: pilot demonstration (this project) → state government endorsement "
        "(through DDMP integration and SDMA partnership) → national implementing entity engagement (NABARD for GCF, "
        "DEA for ADB) → multilateral project preparation grant → full program proposal. This progression typically "
        "requires 2-3 years beyond pilot completion, making the project timeline optimally positioned for multilateral "
        "funding cycles beginning 2028-2029."
    )
    add_paragraph(doc, sustain_para2)
    
    sustain_para3 = (
        "The fourth pathway develops Data-as-a-Service revenue from the continuous environmental monitoring data "
        "generated by the IoT sensor network. Potential clients include agricultural insurance providers (particularly "
        "PMFBY implementing companies requiring micro-scale rainfall data for claim verification), real estate "
        "developers requiring flood risk certification for new construction in Himalayan towns, infrastructure "
        "planning agencies requiring hydrological baseline data for road, bridge, and hydropower design, and "
        "academic researchers requiring calibration data for hydrological and climate models. A conservative "
        "estimate of INR 2-5 lakhs annual revenue from data services is sufficient to cover the recurring costs "
        "of sensor maintenance, communication subscriptions, and server hosting that constitute the primary "
        "post-project operational expenditure. Together, these four pathways ensure that the early warning system "
        "continues operating, the vulnerability atlas remains updated, community preparedness capacity is sustained, "
        "and the institutional framework persists and expands well beyond the initial 36-month project period—transforming "
        "a time-limited research project into a permanent institutional capability."
    )
    add_paragraph(doc, sustain_para3)


    # 6.3
    add_heading_custom(doc, "6.3 Scalability and Replication Pathway", level=2)
    scale_para = (
        "The project's scalability pathway follows a structured three-phase expansion strategy designed to achieve "
        "state-wide coverage within 8 years while maintaining quality and institutional sustainability at each stage. "
        "Phase 1 (Years 1-3, this project) establishes the proof-of-concept across one micro-watershed cluster "
        "protecting approximately 2,500 households, generating the performance data, institutional frameworks, "
        "and replication documentation necessary for expansion. Phase 2 (Years 4-5, post-project scaling through "
        "SDMA and multilateral funding) extends the framework to 5 additional micro-watersheds across 3 districts, "
        "reaching approximately 12,500 households while achieving 40% marginal cost reduction through shared "
        "infrastructure (single GIS workstation serving multiple watersheds, bulk sensor procurement, trained "
        "personnel covering larger areas, established community engagement protocols requiring less intensive "
        "facilitation). Phase 3 (Years 6-8, state-wide deployment through GCF/ADB program) achieves coverage "
        "across all high-risk micro-watersheds in Uttarakhand's 13 districts, protecting 500,000+ households "
        "with a further 40% marginal cost reduction through full institutionalization within SDMA operational "
        "budgets, district-level GIS capacity, and self-sustaining community institutions. This progression "
        "from INR 28.5 lakhs to state-wide coverage represents a demonstrated scaling pathway that multilateral "
        "funders require before committing large-scale resources."
    )
    add_paragraph(doc, scale_para)
    
    # 6.4
    add_heading_custom(doc, "6.4 Risk Management", level=2)
    risk_para = (
        "Comprehensive risk management protocols address the four primary risk categories identified through "
        "systematic pre-project risk assessment. First, sensor and equipment failure risk is mitigated through "
        "redundant measurement systems (dual ultrasonic and pressure transducer), solar-battery hybrid power "
        "with 72-hour autonomous operation capacity, IP67-rated environmental protection, quarterly preventive "
        "maintenance schedules, and strategic spare parts inventory at district headquarters ensuring replacement "
        "within 48 hours of failure detection. Historical failure rate analysis of similar Himalayan installations "
        "indicates 15-25% annual component failure rates, which the redundancy architecture reduces to less than "
        "5% system-level failure probability. Second, community engagement risk—the possibility that target "
        "communities may not participate meaningfully in preparedness activities—is mitigated through Van Panchayat "
        "and Gram Sabha institutional buy-in secured during the project inception phase, SHG integration that "
        "leverages existing women's collective action infrastructure, MGNREGA wage linkage that provides direct "
        "economic incentive for participation in NbS deployment, and progressive engagement design that begins "
        "with tangible visible benefits (employment, seedlings, training) before requesting behavioral changes "
        "(evacuation compliance, drill participation). Third, climate variability risk—the possibility that "
        "non-stationary climate trends may invalidate static threshold parameters—is addressed through a "
        "non-stationary analytical framework that assumes hydrological parameters will shift over time, with "
        "annual threshold recalibration protocols incorporating each monsoon season's data into updated "
        "stage-discharge relationships and alert trigger levels. Fourth, institutional transition risk—the "
        "possibility that project knowledge and systems may not successfully transfer to permanent institutional "
        "management—is addressed through open-access documentation of all methodologies, GitHub-hosted code "
        "repositories with comprehensive documentation, trained community volunteer cadres capable of basic "
        "system operation, and formal Memorandum of Understanding with SDMA Uttarakhand for post-project "
        "system adoption. Together, these risk management protocols ensure project resilience against the "
        "operational uncertainties inherent in Himalayan field research and community engagement."
    )
    add_paragraph(doc, risk_para)


    # ==================== DECLARATION PAGE ====================
    doc.add_page_break()
    add_heading_custom(doc, "Declaration", level=1)
    
    declaration_text = (
        "We, the undersigned, hereby declare that the information provided in this grant funding proposal is "
        "true, accurate, and complete to the best of our knowledge and belief. We confirm that the proposed "
        "project has not received duplicate funding from any other source for the same activities described herein. "
        "We undertake to utilize the sanctioned funds exclusively for the purposes outlined in this proposal and "
        "to maintain proper accounts and records of all expenditures in accordance with the financial guidelines "
        "of the funding agency. We further declare that all necessary institutional approvals, ethical clearances, "
        "and administrative permissions will be obtained prior to commencement of field activities. We commit to "
        "submitting periodic progress reports, financial statements, and utilization certificates as required by "
        "the funding agency, and to making all project outputs (data, publications, tools, and frameworks) "
        "available in open-access formats for maximum societal benefit. We affirm our commitment to conducting "
        "this research with the highest standards of scientific integrity, community respect, and environmental "
        "responsibility."
    )
    add_paragraph(doc, declaration_text)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Signature blocks
    sig_table = doc.add_table(rows=4, cols=2)
    set_cell_format(sig_table.rows[0].cells[0], "Principal Investigator:", bold=True)
    set_cell_format(sig_table.rows[0].cells[1], "Co-Principal Investigator:", bold=True)
    set_cell_format(sig_table.rows[1].cells[0], "")
    set_cell_format(sig_table.rows[1].cells[1], "")
    set_cell_format(sig_table.rows[2].cells[0], "________________________")
    set_cell_format(sig_table.rows[2].cells[1], "________________________")
    set_cell_format(sig_table.rows[3].cells[0], "Dr. Nidhi Rawat\nAssociate Professor\nDept. of Environmental Science\nDBS Global University, Dehradun")
    set_cell_format(sig_table.rows[3].cells[1], "Raj Amritam\nPhD Research Scholar\nDept. of Environmental Science\nDBS Global University, Dehradun")
    
    add_paragraph(doc, "")
    add_paragraph(doc, "Date: _______________", alignment=WD_ALIGN_PARAGRAPH.LEFT)
    add_paragraph(doc, "Place: Dehradun, Uttarakhand", alignment=WD_ALIGN_PARAGRAPH.LEFT)
    
    # Save document
    output_path = '/projects/sandbox/mobile-printer-app/Grant_Funding_Proposal_Raj_Amritam.docx'
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_document()
