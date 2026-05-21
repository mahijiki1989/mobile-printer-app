#!/usr/bin/env python3
"""
Generate PhD Dissertation Proposal as .docx file.
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

# Set margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)

# --- TITLE PAGE ---
for _ in range(4):
    doc.add_paragraph('')

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('PhD DISSERTATION PROPOSAL')
run.bold = True
run.font.size = Pt(14)
doc.add_paragraph('')

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run(
    'Assessing the Efficacy of Nature-Based Solutions for Flood Mitigation:\n'
    'A Hydro-Spatial Modeling Framework for Scalable Risk Reduction\n'
    'in Climate-Vulnerable Watersheds of India'
)
run.bold = True
run.font.size = Pt(13)


doc.add_paragraph('')
doc.add_paragraph('')

scholar = doc.add_paragraph()
scholar.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = scholar.add_run('Submitted by:\nRaj Amritam\nPhD Research Scholar')
run.font.size = Pt(12)

doc.add_paragraph('')

supervisor = doc.add_paragraph()
supervisor.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = supervisor.add_run('Under the Supervision of:\nDr. Nidhi Rawat')
run.font.size = Pt(12)

doc.add_paragraph('')

affiliation = doc.add_paragraph()
affiliation.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = affiliation.add_run(
    'Department of Environmental Science\n'
    'DBS Global University, Dehradun\n'
    'Uttarakhand, India'
)
run.font.size = Pt(12)

doc.add_paragraph('')
year = doc.add_paragraph()
year.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = year.add_run('2025')
run.font.size = Pt(12)

doc.add_page_break()


# --- HELPER FUNCTION ---
def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    return p

def add_bullet(text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5 + level * 0.25)
    p.paragraph_format.line_spacing = 1.5
    return p

# --- SECTION 1: INTRODUCTION & RESEARCH CONTEXT ---
add_heading_styled('1. INTRODUCTION AND RESEARCH CONTEXT', level=1)

add_body(
    'India occupies a uniquely precarious position within the global hydrological risk landscape. '
    'Characterized by extraordinary hydro-climatic variability—ranging from the arid expanses of Rajasthan '
    'receiving less than 200 mm annual precipitation to the hyper-humid northeast exceeding 11,000 mm—the '
    'subcontinent faces a compounding crisis wherein anthropogenic land-use change, unplanned urbanization, '
    'and intensifying monsoon dynamics converge to produce catastrophic flood events with increasing frequency '
    'and severity. According to the National Disaster Management Authority (NDMA) and the Central Water '
    'Commission (CWC), approximately 72% of Indian districts are now classified as exposed to extreme flood '
    'events, encompassing both riverine inundation and pluvial flash flooding. Yet, critically, only 33% of '
    'these vulnerable districts are covered by functional early warning networks capable of providing actionable '
    'lead times exceeding six hours. This coverage deficit constitutes a governance failure of the first order, '
    'rendering millions of citizens—disproportionately from Scheduled Caste, Scheduled Tribe, and economically '
    'weaker sections—vulnerable to recurrent displacement, asset loss, and mortality.'
)


add_body(
    'The paradox of India\'s flood management trajectory is starkly illustrated by the expansion of flood-prone '
    'area despite massive investment in structural interventions. In 1954, the Rashtriya Barh Ayog (National '
    'Flood Commission) estimated India\'s flood-prone area at approximately 2.5 million hectares. By 2022, this '
    'figure had expanded to 6.93 million hectares—a 177% increase—despite the construction of over 3,732 km of '
    'embankments, 37,904 km of drainage channels, and thousands of crores invested in reservoir-based flood '
    'cushioning. This counterintuitive expansion is attributable to multiple factors: the levee paradox wherein '
    'structural protection incentivizes floodplain encroachment; the degradation of natural drainage pathways '
    'through urbanization; siltation-induced capacity reduction in existing infrastructure; and the fundamental '
    'limitation of grey infrastructure in accommodating non-stationary hydrological extremes driven by '
    'anthropogenic climate change.'
)

add_body(
    'Against this backdrop, the international scientific and policy community has increasingly endorsed '
    'Nature-Based Solutions (NbS) as a complementary—and in many cases superior—paradigm for flood risk '
    'reduction. The IUCN Global Standard for NbS (2020), the European Commission\'s NbS Research and Innovation '
    'agenda, and the IPCC AR6 Working Group II report all identify NbS as critical interventions that leverage '
    'ecosystem services—infiltration, retention, evapotranspiration, flow attenuation, and sediment trapping—to '
    'reduce flood hazard while simultaneously delivering biodiversity co-benefits, carbon sequestration, and '
    'livelihood enhancement. However, the operationalization of NbS within India\'s institutional framework '
    'remains nascent, hampered by inadequate hydrological evidence at district scales, absence of integration '
    'with statutory District Disaster Management Plans (DDMPs), and a persistent technocratic preference for '
    'engineered solutions among implementing agencies such as the CWC and State Irrigation Departments.'
)

add_body(
    'This dissertation proposes to bridge this critical implementation gap through the development and validation '
    'of a Hydro-Spatial Modeling Framework that integrates remote sensing, GIS-based multi-criteria vulnerability '
    'assessment, distributed hydrological simulation, and socio-economic cost-benefit analysis to quantify the '
    'flood mitigation efficacy of NbS interventions across two climatologically distinct yet equally vulnerable '
    'Indian watersheds. The research aspires not merely to academic contribution but to the generation of '
    'actionable, policy-ready decision support tools deployable within the existing governance architecture of '
    'the Disaster Management Act, 2005.'
)


# --- SECTION 2: PROBLEM STATEMENT & RESEARCH GAPS ---
add_heading_styled('2. PROBLEM STATEMENT AND IDENTIFIED RESEARCH GAPS', level=1)

add_body(
    'The central problem motivating this research is the systematic failure of India\'s flood management '
    'infrastructure—both physical and institutional—to accommodate the non-stationary hydro-climatic regime '
    'now evident across the subcontinent. The India Meteorological Department (IMD) has documented a 75% '
    'increase in very heavy rainfall days (exceeding 124.5 mm/day) since 1950, with particularly pronounced '
    'intensification over the Indo-Gangetic Plains and Western Himalayan foothills. These extreme precipitation '
    'events overwhelm design assumptions embedded in the CWC\'s legacy infrastructure, which were calibrated '
    'against stationary Intensity-Duration-Frequency (IDF) curves derived from pre-1980 rainfall records. '
    'Simultaneously, rapid land-use transformation—with India losing 1.6 million hectares of forest cover '
    'between 2001 and 2020 and experiencing a 2.7-fold expansion of impervious urban surfaces—has fundamentally '
    'altered catchment hydrological response, reducing time-to-peak, amplifying peak discharges, and increasing '
    'flood volumes beyond the assimilative capacity of existing grey infrastructure.'
)

add_body(
    'This research identifies five distinct, interconnected research gaps that collectively impede the '
    'evidence-based adoption of Nature-Based Solutions for flood mitigation in India:'
)

add_heading_styled('Gap 1: Inland NbS Valuation Deficit', level=2)
add_body(
    'The preponderance of existing NbS-flood research in India focuses on coastal ecosystems—mangroves, '
    'coral reefs, and coastal wetlands—with quantified storm surge attenuation benefits. By contrast, '
    'inland NbS interventions (riparian buffers, floodplain wetland reconnection, headwater reforestation, '
    'and constructed retention basins) remain severely under-quantified in the Indian context. No peer-reviewed '
    'study has, to date, provided catchment-scale hydrological evidence for inland NbS efficacy under '
    'Indian monsoonal conditions with return periods exceeding 25 years.'
)

add_heading_styled('Gap 2: Lack of District-Scale GIS-Hydrology Integration', level=2)
add_body(
    'Existing flood vulnerability assessments in India typically operate at either macro-scales (state or '
    'national level using coarse-resolution datasets) or micro-scales (individual village or ward-level studies). '
    'A critical absence exists at the district scale—the administrative unit at which DDMPs are formulated and '
    'disaster response is coordinated. No operational framework currently integrates high-resolution (30m) '
    'GIS-derived vulnerability indices with process-based hydrological models at this governance-relevant scale.'
)


add_heading_styled('Gap 3: Uncertain NbS Performance Under Extreme Climate Events', level=2)
add_body(
    'While NbS interventions demonstrate consistent efficacy under moderate flood scenarios (5-25 year return '
    'periods), their performance under extreme events exceeding 50-year return periods remains contested in the '
    'literature. Concerns persist regarding the potential for NbS "failure thresholds" where ecosystem-based '
    'interventions become overwhelmed, particularly under compound events combining antecedent soil saturation '
    'with extreme precipitation. This uncertainty is particularly acute for the Indian context, where monsoon '
    'dynamics can produce multi-day precipitation totals exceeding 500 mm with limited inter-event recovery time.'
)

add_heading_styled('Gap 4: Missing DDMP-NbS Legislative Linkages', level=2)
add_body(
    'The Disaster Management Act of 2005 mandates the preparation of District Disaster Management Plans (DDMPs) '
    'by all district administrations. However, the current DDMP framework—as operationalized by the NDMA '
    'guidelines—contains no explicit provision for integrating NbS as a risk reduction strategy. There exists '
    'no standardized template, evaluation protocol, or monitoring framework through which district authorities '
    'can incorporate ecosystem-based approaches into their statutory planning obligations. This legislative-'
    'technical gap effectively excludes NbS from the formal disaster risk reduction architecture despite '
    'India\'s commitments under the Sendai Framework for Disaster Risk Reduction 2015-2030.'
)

add_heading_styled('Gap 5: Reliance on Outdated Stationary Design Storm Metrics', level=2)
add_body(
    'The Central Water Commission and State Irrigation Departments continue to employ Intensity-Duration-'
    'Frequency (IDF) relationships and design storm hyetographs derived from stationary assumptions—typically '
    'calibrated against historical rainfall records spanning 1950-1990. Under conditions of documented '
    'non-stationarity (evidenced by trend analyses showing statistically significant increases in extreme '
    'precipitation quantiles across multiple Indian sub-basins), these design metrics systematically '
    'underestimate flood magnitudes for return periods exceeding 25 years, leading to under-designed '
    'infrastructure and inadequate flood risk zonation. This research will employ non-stationary frequency '
    'analysis to generate updated design quantiles against which NbS efficacy is evaluated.'
)


# --- SECTION 3: RESEARCH QUESTIONS & HYPOTHESES ---
add_heading_styled('3. RESEARCH QUESTIONS AND HYPOTHESES', level=1)

add_heading_styled('Research Question 1: Spatial Vulnerability Characterization', level=2)
add_body(
    'RQ1: How do land-use/land-cover dynamics, geomorphological attributes, and socio-demographic '
    'exposure indicators interact to produce spatially heterogeneous flood vulnerability at the '
    'district-watershed scale in climatologically distinct Indian catchments?'
)
add_body(
    'Hypothesis H1: Catchments with greater than 40% impervious surface coverage and less than 15% '
    'functional wetland cover will exhibit Flood Vulnerability Index (FVI) scores 2-3 times higher '
    'than catchments retaining natural hydrological connectivity, after controlling for precipitation '
    'intensity and topographic gradient. This hypothesis is grounded in the established relationship '
    'between imperviousness and runoff coefficient amplification (documented in the SCS-CN framework), '
    'as well as the empirically demonstrated flood attenuation capacity of connected wetland systems '
    'as storage reservoirs during peak flow events.'
)

add_heading_styled('Research Question 2: NbS Hydrological Efficacy', level=2)
add_body(
    'RQ2: What is the quantifiable hydrological efficacy of specific Nature-Based Solution '
    'interventions—riparian buffer establishment, wetland reconnection, and headwater micro-basin '
    'treatment—in reducing peak discharge magnitude and flood inundation extent under design storms '
    'of varying return periods (10, 25, 50, and 100-year) in the selected study watersheds?'
)
add_body(
    'Hypothesis H2: The establishment of 20-50 meter riparian buffer zones along primary and '
    'secondary drainage channels will produce a 12-25% reduction in simulated peak discharge at '
    'catchment outlets under 50-year return period events, while wetland reconnection interventions '
    '(restoring hydrological connectivity to historically disconnected floodplain depressions) will '
    'reduce flood inundation extent by 15-35% under equivalent return period scenarios. These '
    'quantitative predictions are derived from meta-analytical evidence from temperate catchments '
    '(Dadson et al., 2017; Nicholson et al., 2020) adjusted for Indian monsoonal precipitation '
    'characteristics and soil hydraulic properties.'
)

add_heading_styled('Research Question 3: Scalable Decision Support', level=2)
add_body(
    'RQ3: Can a replicable, open-source hydro-spatial decision support framework be developed that '
    'enables district-level administrators to evaluate, prioritize, and implement NbS interventions '
    'within statutory DDMP processes at economically justifiable costs?'
)
add_body(
    'Hypothesis H3: The proposed framework, when deployed as a standardized template incorporating '
    'GIS vulnerability mapping, hydrological simulation outputs, and economic valuation protocols, '
    'will demonstrate potential to reduce direct economic flood losses by ₹50-200 Crore per year at '
    'district-level implementation costs not exceeding ₹15-25 Crore over a 10-year horizon, yielding '
    'benefit-cost ratios exceeding 3:1 under baseline climate projections and 5:1 under RCP 8.5 '
    'intensification scenarios. This hypothesis positions NbS as economically superior to equivalent '
    'grey-infrastructure investments when ecosystem co-benefits (carbon sequestration, biodiversity '
    'enhancement, groundwater recharge) are monetized within a Total Economic Value framework.'
)


# --- SECTION 4: CONCEPTUAL FRAMEWORK ---
add_heading_styled('4. CONCEPTUAL FRAMEWORK', level=1)

add_body(
    'The conceptual architecture of this research is grounded in the IPCC Sixth Assessment Report (AR6) '
    'risk framework, which defines climate risk as a function of three interacting components: Hazard, '
    'Exposure, and Vulnerability. Formally expressed as:'
)

eq = doc.add_paragraph()
eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = eq.add_run('Flood Risk = f (Hazard × Exposure × Vulnerability)')
run.italic = True
run.font.size = Pt(12)

add_body(
    'Within this triadic formulation, Nature-Based Solutions operate as dynamic risk modifiers across '
    'all three dimensions simultaneously, distinguishing them fundamentally from conventional grey '
    'infrastructure, which primarily addresses only the hazard component through flow conveyance or '
    'storage. Specifically:'
)

add_bullet(
    'Hazard Modification: NbS interventions (riparian buffers, headwater reforestation, wetland storage) '
    'directly reduce flood hazard by attenuating peak discharges, extending time-to-peak, and reducing '
    'total flood volumes through enhanced infiltration, interception, and surface roughness.'
)
add_bullet(
    'Exposure Limitation: Strategic NbS placement in floodplain corridors creates "no-build" ecological '
    'zones that inherently limit the expansion of assets and populations into high-hazard areas, thereby '
    'reducing exposure without requiring restrictive zoning regulations.'
)
add_bullet(
    'Vulnerability Reduction: NbS enhances community adaptive capacity through diversified livelihood '
    'opportunities (fisheries in restored wetlands, agroforestry in riparian buffers), improved '
    'groundwater recharge for drought resilience, and strengthened social-ecological systems that '
    'buffer against compound climate stresses.'
)

add_body(
    'Crucially, this framework conceptualizes NbS not as a static intervention but as an adaptive system '
    'that establishes feedback loops between risk knowledge generation and governance recalibration. As NbS '
    'interventions are implemented and monitored, they generate empirical performance data that updates '
    'hazard models, refines vulnerability assessments, and informs iterative governance decisions—creating '
    'a learning-by-doing cycle consistent with adaptive management principles. This feedback architecture '
    'is operationalized through the proposed Decision Support Framework (RQ3), which embeds monitoring '
    'protocols and performance thresholds triggering governance review and intervention modification.'
)

add_body(
    'The framework further incorporates the concept of "hybrid" or "green-grey" infrastructure portfolios, '
    'recognizing that optimal flood risk reduction in most Indian catchments will require synergistic '
    'combinations of NbS and engineered infrastructure rather than wholesale substitution. The research '
    'will quantify these synergistic interactions through Scenario D (Integrated Package), testing whether '
    'combined interventions yield non-linear (super-additive) benefits exceeding the sum of individual '
    'NbS and grey-infrastructure components.'
)


# --- SECTION 5: METHODOLOGICAL PIPELINE & STUDY AREAS ---
add_heading_styled('5. METHODOLOGICAL PIPELINE AND STUDY AREAS', level=1)

add_heading_styled('5.1 Study Area Selection and Geographical Profiles', level=2)

add_heading_styled('Primary Site: Raipur-Dehradun Watershed, Uttarakhand', level=3)
add_body(
    'The Raipur-Dehradun watershed, a sub-Himalayan catchment of approximately 350 km² situated within '
    'the Doon Valley intermontane basin, represents a rapidly urbanizing landscape experiencing acute '
    'hydro-geomorphic stress. The watershed drains southward through the Song River system into the '
    'Ganges, traversing a geological sequence from the Mussoorie syncline (Greater Himalayan crystallines) '
    'through the Siwalik Group (unconsolidated conglomerates and sandstones) to the Doon gravels—a '
    'stratigraphy that produces extreme variability in infiltration capacity and mass-wasting susceptibility. '
    'The catchment is subject to flash floods triggered by cloudbursts (localized convective events producing '
    '>100 mm/hour), debris flows mobilized by antecedent saturation of Siwalik slopes, and potential Glacial '
    'Lake Outburst Floods (GLOFs) from upstream glacial systems. Remote sensing analysis documents an 18% loss '
    'of forest cover between 2000 and 2022, replaced predominantly by built-up area and agricultural expansion, '
    'fundamentally altering catchment hydrological response. The selection of this site enables investigation '
    'of NbS efficacy under steep-gradient, high-intensity precipitation regimes characteristic of the '
    'sub-Himalayan belt.'
)

add_heading_styled('Comparative Site: Darbhanga District, North Bihar', level=3)
add_body(
    'Darbhanga District in North Bihar represents the archetypal riverine floodplain landscape of the '
    'Indo-Gangetic Plains, dominated by the Kamla-Balan and Kosi river systems whose hydrology is '
    'fundamentally shaped by Himalayan snowmelt, monsoon precipitation, and sediment dynamics. The district '
    'exemplifies the "embankment trap"—a condition wherein extensive levee systems (constructed post-1954) '
    'have confined rivers, eliminated natural floodplain storage, and paradoxically increased flood depths '
    'and durations within protected areas when breaches occur. Approximately 76% of the district\'s '
    'population (predominantly agricultural communities of lower economic quintiles) resides within the '
    'documented flood-affected zone. The flat topography (average slope <0.5%), heavy clay soils with low '
    'infiltration capacity, inadequate drainage infrastructure, and high water tables create conditions of '
    'prolonged waterlogging that conventional engineering approaches have failed to resolve. This site '
    'enables investigation of NbS efficacy under low-gradient, prolonged-inundation regimes where wetland '
    'reconnection and drainage restoration represent primary intervention pathways.'
)


add_heading_styled('5.2 Methodological Pipeline', level=2)

add_heading_styled('Phase 1: Open-Source Spatial Data Ingestion and Preprocessing', level=3)
add_body(
    'The research employs an exclusively open-source data acquisition strategy to ensure replicability '
    'and scalability. Sentinel-2 multispectral imagery (10m visible/NIR, 20m SWIR) provides land-use/land-'
    'cover classification through supervised Random Forest algorithms trained on ground-truth points collected '
    'during field campaigns. Sentinel-1 C-band SAR imagery enables flood extent mapping during active events '
    'and soil moisture estimation through change detection algorithms. Topographic characterization utilizes '
    'SRTM 30m DEM supplemented by ALOS PALSAR 12.5m DEM for enhanced drainage delineation in flat terrain '
    '(critical for the Darbhanga site). Soil hydraulic properties (saturated hydraulic conductivity, water '
    'holding capacity, bulk density) are derived from ISRIC SoilGrids 250m global predictions, validated '
    'against available district soil survey reports. Precipitation forcing employs CHIRPS daily rainfall '
    '(0.05° resolution) for long-term climatological analysis and GPM IMERG V06 half-hourly data for '
    'event-scale hydrological modeling, validated against IMD rain gauge observations.'
)

add_heading_styled('Phase 2: Multi-Criteria Flood Vulnerability Index (FVI) Development', level=3)
add_body(
    'A composite Flood Vulnerability Index is constructed at 30m spatial resolution through an Analytic '
    'Hierarchy Process (AHP) weighted multi-criteria decision analysis. The AHP framework enables systematic '
    'integration of heterogeneous vulnerability indicators through pairwise comparison matrices evaluated by '
    'an expert panel (minimum 7 domain experts from hydrology, geomorphology, disaster management, and '
    'ecology). A strict Consistency Ratio (CR) threshold of <0.10 is enforced to ensure logical coherence '
    'of expert judgments. The FVI integrates the following parameter categories:'
)

add_bullet('Topographic Parameters: Slope gradient (degrees), Topographic Wetness Index (TWI = ln(a/tan β)), '
           'Height Above Nearest Drainage (HAND), flow accumulation, and curvature.')
add_bullet('Hydrological Parameters: Drainage density, distance to nearest stream channel, SCS Curve Number, '
           'and baseflow index.')
add_bullet('Land-Use Parameters: Impervious surface fraction, NDVI-based vegetation density, wetland extent, '
           'and riparian buffer width.')
add_bullet('Socio-Demographic Parameters: Population density (Census 2011 updated with growth projections), '
           'housing quality index, infrastructure exposure, and social vulnerability indicators '
           '(SC/ST proportion, female-headed households, Below Poverty Line proportion).')

add_body(
    'The resulting FVI maps are validated against historical flood event inventories compiled from the '
    'Disaster Management Division records, SDMA reports, and Sentinel-1 derived flood extent maps for '
    'documented events (minimum 5 events per study site spanning 2015-2024).'
)


add_heading_styled('Phase 3: Hydrological and Hydraulic Modeling', level=3)
add_body(
    'Catchment-scale rainfall-runoff processes are simulated using the Soil and Water Assessment Tool (SWAT), '
    'a physically-based, semi-distributed model operating at daily timestep with sub-daily disaggregation for '
    'event modeling. The SWAT model is configured with Hydrological Response Units (HRUs) defined by unique '
    'combinations of land use, soil type, and slope class. Model calibration and uncertainty analysis employ '
    'the SWAT-CUP SUFI-2 (Sequential Uncertainty Fitting version 2) algorithm, which uses Latin Hypercube '
    'sampling to explore parameter space and quantify 95% prediction uncertainty bands (95PPU). Calibration '
    'targets include daily streamflow at available CWC gauge stations, with performance criteria requiring '
    'Nash-Sutcliffe Efficiency (NSE) > 0.6, coefficient of determination (R²) > 0.65, and Percent Bias '
    '(PBIAS) within ±15% for both calibration and validation periods.'
)

add_body(
    'For detailed floodplain hydraulics and inundation mapping, the calibrated SWAT discharge hydrographs '
    'serve as upstream boundary conditions for 2D unsteady-flow simulation in HEC-RAS 6.x (Hydrologic '
    'Engineering Center\'s River Analysis System). The 2D computational mesh is constructed at 10-30m '
    'resolution (adaptive, with refinement in channel and urban areas) using the SRTM/ALOS terrain model '
    'supplemented by bathymetric cross-sections where available. Manning\'s roughness coefficients are '
    'spatially distributed based on land-cover classification, with values ranging from 0.025 (paved '
    'surfaces) to 0.15 (dense riparian forest). Model validation employs Sentinel-1 SAR-derived flood '
    'extent maps with Critical Success Index (CSI) > 0.6 as the minimum acceptable performance threshold.'
)

add_heading_styled('Phase 4: Socio-Economic Benefit-Cost Analysis', level=3)
add_body(
    'The economic valuation component employs stage-damage (depth-damage) curves adapted for Indian building '
    'typologies and agricultural systems to translate simulated flood depths into monetary damage estimates. '
    'Curves are developed for five asset categories: residential structures (kuccha, semi-pucca, pucca), '
    'commercial properties, agricultural crops (season-specific), public infrastructure, and vehicles. '
    'The benefit of NbS interventions is calculated as the Expected Annual Damage (EAD) reduction between '
    'baseline and intervention scenarios, integrated across the full return period spectrum (2-500 year). '
    'Lifecycle cost-benefit analysis employs a 30-year evaluation horizon at dual discount rates: 3% '
    '(reflecting social time preference for long-term environmental investments) and 8% (reflecting '
    'India\'s standard public project appraisal rate per the Niti Aayog framework). Total Economic Value '
    '(TEV) incorporates non-market benefits including carbon sequestration (valued at $50/tCO₂e), '
    'groundwater recharge, biodiversity habitat provision, and recreational amenity values estimated '
    'through benefit transfer from comparable Indian valuation studies.'
)


# --- SECTION 6: SIMULATION INTERVENTION SCENARIOS ---
add_heading_styled('6. SIMULATION INTERVENTION SCENARIOS', level=1)

add_body(
    'Four distinct NbS intervention scenarios are modeled, each involving specific parameter modifications '
    'within the calibrated SWAT and HEC-RAS modeling frameworks. All scenarios are evaluated against a '
    'baseline (current land-use) condition and a grey-infrastructure counterfactual (conventional embankment '
    'heightening and channel widening).'
)

add_heading_styled('Scenario A: Riparian Buffer Establishment', level=2)
add_body(
    'This scenario simulates the establishment of 20-50 meter vegetated riparian buffers along all '
    'primary (Strahler order ≥3) and secondary (Strahler order 2) drainage channels within the study '
    'watersheds. In HEC-RAS, Manning\'s roughness coefficient (n) is modified from the baseline value '
    'of 0.03 (representing existing degraded/agricultural riparian zones) to 0.12 (representing mature '
    'mixed riparian forest with understory), simulating the hydraulic effect of flow retardation through '
    'dense vegetation. In SWAT, the corresponding HRUs are reclassified from agricultural/barren land '
    'use to forest/buffer land use, modifying infiltration parameters, leaf area index, and '
    'evapotranspiration rates accordingly. The scenario evaluates the resulting reduction in peak '
    'discharge, extension of time-to-peak, and reduction in downstream flood depths.'
)

add_heading_styled('Scenario B: Wetland Reconnection and Restoration', level=2)
add_body(
    'This scenario models the hydrological reconnection of historically disconnected floodplain wetlands '
    '(oxbow lakes, palustrine marshes, and seasonal jheels) to the active drainage network, restoring '
    'their function as off-stream stormwater retention basins. In SWAT, the SCS Curve Number for '
    'identified wetland restoration zones is modified from the current degraded value of 85 (representing '
    'compacted, poorly-drained agricultural land occupying former wetland basins) to 65 (representing '
    'functional wetland with high organic content, ponding storage, and saturated hydraulic connectivity). '
    'Additionally, reservoir routing parameters are introduced at wetland locations to simulate the '
    'storage-discharge relationship of restored water bodies. The scenario quantifies off-stream storage '
    'volumes, peak discharge attenuation at downstream locations, and the temporal lag introduced into '
    'the flood hydrograph.'
)

add_heading_styled('Scenario C: Headwater Micro-Basin Treatment', level=2)
add_body(
    'This scenario simulates comprehensive watershed treatment of headwater catchments (Strahler order 1-2) '
    'through vegetative porous barriers (loose boulder check structures with living vegetation), contour '
    'trenching, and afforestation—interventions aligned with the Pradhan Mantri Krishi Sinchayee Yojana '
    'Watershed Development Component 2.0 (PMKSY-WDC 2.0) guidelines. In SWAT, treated sub-basins receive '
    'modified parameters including reduced Curve Numbers (5-10 unit reduction reflecting enhanced '
    'infiltration), increased soil available water capacity (representing improved soil structure), and '
    'modified USLE cover factor reflecting vegetation establishment. The scenario evaluates cumulative '
    'downstream impacts of distributed headwater interventions on catchment-outlet hydrographs.'
)

add_heading_styled('Scenario D: Integrated NbS-Grey Infrastructure Package', level=2)
add_body(
    'The final scenario combines Scenarios A, B, and C simultaneously, with the addition of targeted '
    'grey-infrastructure enhancements (channel optimization, culvert upgrades) at identified bottleneck '
    'locations. This integrated scenario tests whether combined NbS interventions produce synergistic '
    '(super-additive) flood reduction benefits exceeding the arithmetic sum of individual scenario outcomes. '
    'The grey-infrastructure counterfactual consists of conventional engineering interventions (embankment '
    'heightening by 1.5m, channel widening by 30%) designed to achieve equivalent flood protection levels, '
    'enabling direct economic comparison of NbS-hybrid versus pure grey-infrastructure approaches under '
    'identical design storm conditions.'
)


# --- SECTION 7: TIMELINE, PUBLICATION TRACK & ETHICAL CONSIDERATIONS ---
add_heading_styled('7. TIMELINE, SCIE PUBLICATION TRACK, AND ETHICAL CONSIDERATIONS', level=1)

add_heading_styled('7.1 Research Timeline: 36-Month Fast-Track Pipeline', level=2)

add_body('The research is structured as a 36-month accelerated PhD program with the following phase-wise timeline:')

add_bullet('Months 1-6: Comprehensive literature review, study area reconnaissance, field data collection '
           '(ground-truth points, cross-sections, community surveys), and data procurement/preprocessing.')
add_bullet('Months 7-12: FVI development, AHP expert elicitation, vulnerability mapping, and validation. '
           'Submission of Paper 1 (Systematic Review and Conceptual Framework) to a Q1 SCIE journal.')
add_bullet('Months 13-18: SWAT model setup, calibration (SUFI-2), and validation for both study sites. '
           'Submission of Paper 2 (GIS-Based Flood Vulnerability Atlas) to a Q1/Q2 SCIE journal.')
add_bullet('Months 19-27: HEC-RAS 2D model development, scenario simulations (A through D), sensitivity '
           'analysis, and uncertainty quantification. Submission of Paper 3 (Hydrological Simulation of '
           'NbS Efficacy) to a Q1 SCIE journal (e.g., Journal of Hydrology, Water Resources Research).')
add_bullet('Months 28-33: Economic valuation, benefit-cost analysis, decision support framework development, '
           'and stakeholder validation workshops. Submission of Paper 4 (Economic Decision Framework for '
           'NbS-DDMP Integration) to a Q1/Q2 SCIE journal.')
add_bullet('Months 34-36: Dissertation compilation, internal review, pre-submission seminar, and final '
           'submission to the university examination system.')

add_heading_styled('7.2 SCIE Publication Track (4-Paper Model)', level=2)

# Publication table
table = doc.add_table(rows=5, cols=4)
table.style = 'Table Grid'
headers = ['Paper', 'Title/Focus', 'Target Timeline', 'Target Journal Tier']
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

papers = [
    ['Paper 1', 'Systematic Review: NbS for Inland Flood Mitigation in South Asia', 'Month 12', 'Q1 SCIE'],
    ['Paper 2', 'District-Scale Flood Vulnerability Atlas Using AHP-GIS Integration', 'Month 18', 'Q1/Q2 SCIE'],
    ['Paper 3', 'SWAT-HEC-RAS Simulation of NbS Scenarios Under Non-Stationary Climate', 'Month 27', 'Q1 SCIE'],
    ['Paper 4', 'Economic Decision Framework for NbS Integration in DDMPs', 'Month 33', 'Q1/Q2 SCIE'],
]
for row_idx, paper in enumerate(papers, start=1):
    for col_idx, val in enumerate(paper):
        table.rows[row_idx].cells[col_idx].text = val

doc.add_paragraph('')


add_heading_styled('7.3 Ethical Considerations', level=2)

add_heading_styled('Data Ethics and Privacy', level=3)
add_body(
    'All spatial data employed in this research is derived from open-source platforms (Copernicus, NASA, ISRIC) '
    'freely available for research purposes. Socio-demographic data from Census 2011 is used at aggregate '
    '(village/ward) levels without individual identification. Community surveys conducted during field validation '
    'will obtain informed consent through bilingual (Hindi/English or Hindi/Maithili) consent forms approved by '
    'the DBS Global University Institutional Ethics Committee. GPS coordinates of individual households will be '
    'aggregated to ward-level centroids in published outputs to prevent identification of specific properties. '
    'All data storage complies with the Information Technology Act, 2000, and emerging data protection norms '
    'under the Digital Personal Data Protection Act, 2023.'
)

add_heading_styled('Participatory and Gender-Sensitive Community Validation', level=3)
add_body(
    'The research incorporates participatory validation at two stages: (1) during FVI development, where '
    'community-level Participatory Rural Appraisal (PRA) exercises—including transect walks, seasonal '
    'calendars, and hazard mapping—validate model-derived vulnerability classifications against lived '
    'experience; and (2) during decision support framework development, where stakeholder workshops with '
    'district officials, Panchayati Raj Institution members, and community representatives validate the '
    'practicability and acceptability of proposed NbS interventions. Gender sensitivity is ensured through: '
    'mandatory minimum 50% female participation in community validation exercises; gender-disaggregated '
    'vulnerability indicators within the FVI; and explicit assessment of how proposed NbS interventions '
    'differentially impact women\'s workloads, mobility, and economic opportunities.'
)

add_heading_styled('Climate Justice Framework', level=3)
add_body(
    'Recognizing that flood impacts in India are profoundly inequitable—with Scheduled Caste and Scheduled '
    'Tribe communities, landless agricultural laborers, and female-headed households bearing disproportionate '
    'losses relative to their asset base and adaptive capacity—this research embeds a Climate Justice '
    'analytical lens throughout. Flood damage estimates and NbS benefit distributions are disaggregated by: '
    'gender (male-headed vs. female-headed households); caste category (General, OBC, SC, ST); economic '
    'quintile (based on housing quality and landholding proxies); and geographic marginality (distance from '
    'administrative centers and service infrastructure). The research explicitly evaluates whether proposed '
    'NbS interventions reduce or exacerbate existing inequities in flood risk distribution, ensuring that '
    'vulnerable communities are positioned as primary beneficiaries rather than bearing additional costs '
    '(e.g., land acquisition for buffer zones displacing marginal farmers). This equity analysis directly '
    'informs the DDMP integration framework, embedding distributional justice criteria within the '
    'prioritization algorithm for NbS site selection.'
)

# --- SAVE DOCUMENT ---
output_path = '/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Raj_Amritam.docx'
doc.save(output_path)
print(f"Document saved successfully to: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
