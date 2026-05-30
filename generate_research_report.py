#!/usr/bin/env python3
"""Generate comprehensive Research Report on NbS for Flood Mitigation."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def set_cell_shading(cell, color):
    shading_elm = parse_xml('<w:shd {} w:fill="{}"/>'.format(nsdecls("w"), color))
    cell._tc.get_or_add_tcPr().append(shading_elm)


def add_para(doc, text, bold=False, italic=False, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    p.alignment = alignment
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    return p


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 51, 102)
    return h


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        set_cell_shading(cell, "003366")
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(cell_text)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
            if r_idx % 2 == 0:
                set_cell_shading(cell, "F0F4F8")
    doc.add_paragraph()
    return table


def add_flowchart(doc, title, lines):
    add_para(doc, "FLOWCHART: " + title, bold=True, font_size=11)
    p = doc.add_paragraph()
    run = p.add_run("\n".join(lines))
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    p.paragraph_format.line_spacing = 1.0
    doc.add_paragraph()


def create_document():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # TITLE PAGE
    for _ in range(4):
        doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("RESEARCH REPORT")
    run.font.name = "Times New Roman"
    run.font.size = Pt(28)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    doc.add_paragraph()
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Nature-Based Solutions for Flood Mitigation:\nAn AI and GIS Integrated Hydro-Spatial Modeling Framework")
    run.font.name = "Times New Roman"
    run.font.size = Pt(18)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 80, 120)
    for _ in range(3):
        doc.add_paragraph()
    info_lines = [
        ("Author:", "Raj Amritam, PhD Research Scholar"),
        ("Supervisor:", "Dr. Nidhi Rawat, Assistant Professor"),
        ("Department:", "Department of Environmental Science"),
        ("Institution:", "DBS Global University, Dehradun, Uttarakhand"),
        ("Date:", "January 2025"),
        ("Document Type:", "Comprehensive Research Report"),
    ]
    for label, value in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run1 = p.add_run(label + " ")
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(12)
        run1.bold = True
        run2 = p.add_run(value)
        run2.font.name = "Times New Roman"
        run2.font.size = Pt(12)
    doc.add_page_break()

    # TABLE OF CONTENTS
    add_heading_styled(doc, "TABLE OF CONTENTS", level=1)
    toc_items = [
        "1. Executive Overview - What Is This Research About?",
        "2. Key Terms and Definitions Glossary",
        "3. The Problem - Why This Research Is Needed",
        "4. The Solution - What Are Nature-Based Solutions?",
        "5. AI Integration - Where, When, and How AI Is Used",
        "6. GIS Integration - Where, When, and How GIS Is Used",
        "7. The Complete Methodology - Step-by-Step Guide",
        "8. Study Areas - Detailed Profile",
        "9. AI + GIS Integration Timeline",
        "10. Expected Results",
        "11. How This Helps India",
        "12. References",
        "13. Appendix: Software and Tools Needed",
    ]
    for item in toc_items:
        add_para(doc, item, font_size=11)
    doc.add_page_break()

    return doc


def add_executive_overview(doc):
    add_heading_styled(doc, "1. EXECUTIVE OVERVIEW - What Is This Research About?", level=1)
    add_para(doc, "In Simple Terms: This research is about finding smarter, nature-friendly ways to reduce flood damage in India using advanced computer tools like Artificial Intelligence (AI) and Geographic Information Systems (GIS).", bold=True, italic=True, font_size=11)
    
    paragraphs = [
        "India faces devastating floods every year. In 2023 alone, floods affected over 30 million people and caused damages exceeding Rs. 50,000 crores. Despite spending thousands of crores on embankments, dams, and drainage systems (called 'grey infrastructure'), the flood-affected area in India has actually INCREASED from 5 million hectares in the 1950s to over 40 million hectares today. This tells us something critically important: our current approach of building only concrete structures is not working well enough. We need a fundamentally different strategy.",
        
        "Nature-Based Solutions (NbS) offer that different approach. NbS means using natural ecosystems - forests, wetlands, floodplains, riparian zones (areas along riverbanks) - to reduce flood risk. Think of it this way: a forest acts like a giant sponge that soaks up rainwater before it rushes into rivers. A wetland works like a natural reservoir that stores excess water during heavy rains. Riparian vegetation (plants growing along river edges) slows down water flow and traps sediment. These natural systems have been managing water for millions of years - we just need to understand them scientifically and protect or restore them strategically.",
        
        "But here is the key challenge: How do we scientifically PROVE that planting trees along a river will reduce flooding by, say, 30%? How do we identify exactly WHERE to restore wetlands for maximum benefit? How do we predict what happens under future climate conditions when rainfall patterns change dramatically? How do we convince government officials to allocate budget for something they cannot see working immediately? This is where Artificial Intelligence (AI) and Geographic Information Systems (GIS) become absolutely essential tools in our research toolkit.",
        
        "Artificial Intelligence (AI) in this research means using computer algorithms (step-by-step mathematical instructions for computers) that can learn patterns from data and make accurate predictions without being explicitly programmed for every scenario. For example, AI can analyze 20 years of satellite images covering thousands of square kilometers and automatically detect how land use has changed - precisely where forests were cut down, where urbanization expanded, where wetlands were drained or filled. This analysis would take a team of human analysts several months of tedious work; AI accomplishes it in hours with greater accuracy and consistency. AI also helps us calibrate (fine-tune) our hydrological models by testing thousands of parameter combinations to find the best match with observed real-world data.",
        
        "Geographic Information Systems (GIS) means digital mapping and spatial analysis technology that can layer multiple types of geographic information on top of each other and perform complex spatial calculations. Imagine transparent maps stacked together - one showing terrain elevation, one showing soil type, one showing average rainfall, one showing population density, one showing existing drainage infrastructure. GIS lets us combine all these layers mathematically to answer complex spatial questions like: 'Which specific areas with clay soil, elevation below 200 meters, population density above 500 per square km, and proximity to rivers within 2 km are most vulnerable to flooding?' No human could answer this question across an entire district without GIS.",
        
        "This research combines NbS with AI and GIS to create a complete scientific framework (a structured, reproducible system) for flood risk reduction. We will study two very different locations - Raipur-Dehradun in Uttarakhand (hilly terrain with flash floods caused by sudden heavy rainfall on steep slopes) and Darbhanga in Bihar (flat alluvial plains with river flooding caused by water overflow from the Kosi and Kamla-Balan rivers). By studying these contrasting environments, we demonstrate that our integrated framework works across different geographic, climatic, and socioeconomic settings across India.",
        
        "The final outputs of this research will include: (1) Detailed flood vulnerability maps showing which specific areas and communities are most at risk, classified into Very High, High, Moderate, Low, and Very Low vulnerability zones; (2) Scientific evidence quantifying exactly how much NbS interventions can reduce peak flood discharge, flood extent, and flood duration under various rainfall scenarios; (3) Rigorous cost-benefit analysis proving that NbS is financially worthwhile with Benefit-Cost Ratios expected to range from 2.5 to 4.8; (4) Ready-to-use templates for District Disaster Management Plans (DDMPs) that government officials can directly implement without needing to hire consultants; and (5) A prototype AI-powered monitoring system concept for real-time flood early warning using IoT sensors and satellite data.",
        
        "Who benefits from this research? Directly: communities living in flood-prone areas who will have better early warning and natural protection systems. Government agencies (NDMA, SDMA, District administrations) who will have scientific data and ready frameworks to make better resource allocation decisions. Farmers whose crops valued at thousands of crores are destroyed every monsoon season. Indirectly: the entire nation benefits, because research shows that every rupee spent on flood prevention saves Rs. 7-10 in post-disaster relief, reconstruction, and economic losses. This research provides the scientific basis for that preventive investment, moving India from a reactive disaster response model to a proactive disaster risk reduction model aligned with global frameworks like the Sendai Framework for Disaster Risk Reduction 2015-2030.",
    ]
    
    for para in paragraphs:
        add_para(doc, para)
    
    doc.add_page_break()



def add_glossary(doc):
    add_heading_styled(doc, "2. KEY TERMS AND DEFINITIONS GLOSSARY", level=1)
    add_para(doc, "In Simple Terms: Before we dive into the details of this research, here is a comprehensive dictionary of every technical term you will encounter. Each term is explained in plain language so that anyone with basic science knowledge can understand the full research report.", bold=True, italic=True, font_size=11)
    add_para(doc, "This glossary contains 40+ terms organized in a table format. Each entry provides the term abbreviation, its full form, a simple definition that anyone can understand, and its specific role in this research project.")
    
    glossary_data = [
        ("NbS", "Nature-Based Solutions", "Using natural ecosystems (forests, wetlands, rivers) to solve human problems like flooding. Instead of building concrete walls, we use or restore natural features that already know how to manage water.", "The core concept of this research - we are proving scientifically that nature can reduce floods better and cheaper than concrete alone."),
        ("FVI", "Flood Vulnerability Index", "A number (0 to 1) that tells us how likely an area is to be badly affected by floods. Higher number = more vulnerable. It combines physical factors (terrain, drainage) with social factors (population, poverty).", "We create FVI maps for both study areas using GIS, combining 18 different factors to identify which specific villages and wards need the most help."),
        ("AHP", "Analytic Hierarchy Process", "A mathematical method for making complex decisions. It is like a structured voting system where experts rate which factors matter most for flooding - is slope more important than soil type? Is drainage density more critical than land use? AHP converts expert opinions into mathematical weights.", "We use AHP to assign importance weights to each vulnerability factor. For example, if experts say elevation matters twice as much as soil type, AHP converts this into precise numerical weights (e.g., 0.18 vs 0.09)."),
        ("GIS", "Geographic Information System", "Computer software that works with digital maps. It can store, analyze, and display geographic data in layers. Think of Google Maps but with the ability to perform complex scientific calculations on the map data.", "GIS is used throughout this research for mapping vulnerability, visualizing flood extent, selecting NbS sites, and creating outputs for government planning documents."),
        ("AI", "Artificial Intelligence", "Computer programs that can learn patterns from data and make predictions or decisions without being explicitly programmed for every situation. In simple terms (samajhne ke liye): computers that learn from experience, like humans do.", "AI is used for satellite image classification, flood prediction, model calibration optimization, and damage estimation in this research."),
        ("ML", "Machine Learning", "A subset of AI where computers learn patterns from data. Instead of telling the computer exact rules, we show it examples and it figures out the rules itself. For example, we show it 1000 satellite images labeled 'flood' and 'no flood' and it learns to distinguish them.", "ML algorithms (Random Forest, Support Vector Machine) are used for land-use classification from satellite imagery and for flood extent mapping from radar data."),
        ("Remote Sensing", "Remote Sensing", "Collecting information about the Earth from a distance, usually from satellites or aircraft. The satellites take pictures of Earth in different wavelengths of light (visible, infrared, microwave) that reveal different features.", "We use satellite remote sensing data (Sentinel-1, Sentinel-2, Landsat) to map land use, detect floods, measure vegetation health, and monitor changes over time across our study areas."),
        ("DEM", "Digital Elevation Model", "A 3D computer model of the Earth's surface showing the height of every point. It is like a digital relief map where each pixel has an elevation value in meters. This tells us where water will flow (downhill) and where it will collect (in valleys).", "DEM is the foundation of our hydrological modeling. From DEM we extract slope, flow direction, drainage networks, watersheds, and the Topographic Wetness Index."),
        ("SRTM", "Shuttle Radar Topography Mission", "A NASA mission that used radar from the Space Shuttle to map elevation of nearly the entire Earth at 30-meter and 90-meter resolution. This free dataset is widely used for terrain analysis worldwide.", "We use SRTM 30m DEM as our primary elevation dataset for terrain analysis, watershed delineation, and as input to both SWAT and HEC-RAS models."),
        ("Sentinel-1", "Sentinel-1 (ESA Satellite)", "A European Space Agency satellite carrying SAR (radar) that can see through clouds and work at night. It sends microwave signals to Earth and records what bounces back. Water surfaces appear dark in SAR images because water reflects radar away from the satellite.", "Sentinel-1 SAR data is critical for flood extent mapping because it can image floods even during heavy cloud cover when optical satellites cannot see the ground. We use AI change detection on Sentinel-1 to map exact flood boundaries."),
        ("Sentinel-2", "Sentinel-2 (ESA Satellite)", "A European Space Agency satellite that takes high-resolution optical images (like a very powerful camera) in 13 different color bands including visible light and infrared. Resolution is 10 meters - meaning each pixel represents a 10m x 10m area on ground.", "We use Sentinel-2 for land-use land-cover (LULC) classification using AI algorithms. The multiple spectral bands allow us to distinguish forests from cropland from urban areas from water bodies with high accuracy."),
        ("NDVI", "Normalized Difference Vegetation Index", "A number between -1 and +1 that tells us how green and healthy vegetation is. Calculated from satellite images using red and near-infrared light. Healthy plants absorb red light for photosynthesis but reflect near-infrared strongly. NDVI close to +1 means dense healthy vegetation; close to 0 means bare soil; negative means water.", "NDVI helps us map vegetation density, identify forests and riparian zones suitable for NbS, assess vegetation health before and after NbS implementation, and detect deforestation that increases flood risk."),
        ("SAR", "Synthetic Aperture Radar", "A type of radar imaging that creates detailed images by combining multiple radar signals as the satellite moves. Unlike cameras that need sunlight and clear skies, SAR works day or night, rain or shine, because it creates its own microwave illumination.", "SAR (from Sentinel-1) is our primary tool for flood mapping because floods typically happen during cloudy, rainy conditions when optical satellites cannot see. SAR penetrates clouds and clearly shows water surfaces."),
        ("SWAT", "Soil and Water Assessment Tool", "A computer model that simulates how water moves through a watershed (river basin). It tracks rainfall from the moment it hits the ground - how much soaks in, how much runs off, how much plants use, how fast it reaches the river. It divides the watershed into small units and calculates water balance for each.", "SWAT is our primary hydrological model. We use it to simulate current flood conditions and then test NbS scenarios - changing land use parameters to represent forests, wetlands, and riparian buffers, then seeing how much peak flood flow decreases."),
        ("HEC-RAS", "Hydrologic Engineering Center River Analysis System", "A computer model that simulates water flowing IN rivers and over floodplains. While SWAT tells us how much water reaches the river, HEC-RAS tells us how deep and wide the flooding will be at any specific point along the river. It uses equations of fluid dynamics.", "HEC-RAS takes SWAT output (river discharge) and converts it into flood inundation maps showing exact flood depth, extent, and velocity at every point. This is critical for damage estimation and identifying which buildings and farms will be flooded."),
        ("HRU", "Hydrological Response Units", "Small subdivisions of a watershed in the SWAT model that have uniform land use, soil type, and slope. Each HRU responds to rainfall in a similar way. For example, a flat area with clay soil and paddy cultivation would be one HRU; a steep area with sandy soil and forest would be another.", "SWAT divides our study watersheds into hundreds of HRUs. When we simulate NbS scenarios, we change the land use parameter of specific HRUs (e.g., converting 'degraded land' to 'riparian forest') and observe how the overall watershed response changes."),
        ("NSE", "Nash-Sutcliffe Efficiency", "A statistical measure of how well our model's predictions match real-world observed data. NSE = 1 means perfect match; NSE > 0.5 is considered acceptable; NSE > 0.75 is very good. It is like a grade for our model's accuracy.", "We use NSE as the primary criterion to evaluate whether our SWAT and HEC-RAS models are accurate enough to be trusted for making flood predictions and testing NbS scenarios."),
        ("SCS-CN", "SCS Curve Number", "A number (0 to 100) developed by the US Soil Conservation Service that represents how much rainfall becomes surface runoff for a given land cover and soil type. Low CN (like 30) means most rain soaks in (forest on sandy soil). High CN (like 95) means most rain runs off (concrete parking lot).", "Curve Numbers are a key parameter in our hydrological modeling. When we simulate NbS, we reduce CN values to represent increased infiltration - for example, converting degraded land (CN=82) to healthy forest (CN=55) shows how much runoff decreases."),
        ("Manning n", "Manning's Roughness Coefficient", "A number that represents how much resistance a surface provides to water flowing over it. Smooth concrete channel has low n (0.013) so water flows fast. Dense floodplain forest has high n (0.15) so water flows slowly. Higher roughness = slower water = more time for water to spread and soak in.", "Manning's n is critical in HEC-RAS modeling. NbS interventions like riparian forests increase roughness, which slows flood wave travel time, reduces peak discharge downstream, and increases floodplain storage. We modify n values in our NbS scenarios."),
        ("TWI", "Topographic Wetness Index", "A number calculated from elevation data that predicts which areas tend to accumulate water. Flat areas at the bottom of large drainage areas have high TWI (tend to be wet/flooded). Steep hilltops have low TWI (water runs off quickly). Calculated as: ln(upstream area / slope).", "TWI is one of our vulnerability assessment factors. Areas with high TWI are naturally prone to waterlogging and flooding. We also use TWI to identify potential wetland restoration sites where water naturally accumulates."),
        ("HAND", "Height Above Nearest Drainage", "The vertical height difference between any point on the landscape and the nearest river or stream. Low HAND values (0-5 meters) mean you are close to river level and highly flood-prone. High HAND values mean you are elevated well above the river.", "HAND is a powerful flood vulnerability indicator in our FVI mapping. Areas with HAND less than 3 meters in our study areas are classified as Very High vulnerability zones because even moderate river rise will inundate them."),
        ("EAD", "Expected Annual Damage", "The average amount of flood damage (in rupees) expected every year when you account for floods of different sizes and probabilities. Small floods happen often (causing small damage frequently) while big floods are rare (but cause massive damage occasionally). EAD combines all these into one annual number.", "EAD is our primary economic metric. We calculate EAD under current conditions and under NbS scenarios. The difference (reduction in EAD) represents the annual economic benefit of NbS interventions, which we compare against implementation costs."),
        ("BCR", "Benefit-Cost Ratio", "The ratio of total benefits to total costs over the project lifetime. BCR > 1 means benefits exceed costs (good investment). BCR of 3 means for every Rs. 1 spent, Rs. 3 in benefits are received. This is the key metric that convinces government officials to fund a project.", "We calculate BCR for each NbS scenario. We expect BCR between 2.5 and 4.8, meaning nature-based flood management is an excellent economic investment even before counting non-monetary benefits like biodiversity and carbon sequestration."),
        ("TEV", "Total Economic Value", "The complete economic value of an ecosystem including: direct use value (timber, fish), indirect use value (flood control, water purification), option value (future potential uses), and existence value (people value knowing it exists even if they never visit).", "TEV framework helps us capture the FULL benefits of NbS, not just flood reduction. A restored wetland provides flood control, water filtration, fish habitat, carbon storage, recreation, and biodiversity. TEV captures all these in economic terms."),
        ("Return Period", "Return Period (Recurrence Interval)", "The average time between flood events of a certain size. A '100-year flood' does NOT mean it happens once every 100 years exactly - it means there is a 1% chance of it happening in ANY given year. A '25-year flood' has a 4% annual chance. Climate change is making formerly rare floods more frequent.", "We design and test our NbS for multiple return periods: 10-year, 25-year, 50-year, and 100-year floods. This shows how effective NbS is for both common floods and extreme events, and how climate change shifts return periods."),
        ("NSFA", "Non-Stationary Frequency Analysis", "Traditional flood frequency analysis assumes the climate is stable (stationary) - that a 100-year flood stays a 100-year flood forever. NSFA recognizes that climate change is making extreme rainfall more frequent, so what was a 100-year flood in 1980 might be a 50-year flood by 2050.", "We use NSFA to calculate future design storms under climate change scenarios (RCP 4.5 and RCP 8.5). This ensures our NbS recommendations are designed for future conditions, not just historical patterns that no longer apply."),
        ("DDMP", "District Disaster Management Plan", "An official government planning document that every district in India must prepare under the Disaster Management Act 2005. It outlines the district's hazard profile, vulnerability assessment, risk reduction measures, preparedness, response plan, and resource inventory.", "Our research directly feeds into DDMPs. We create ready-to-use NbS modules with maps, prioritized interventions, cost estimates, and implementation timelines that district officials can insert directly into their DDMPs without needing additional technical expertise."),
        ("DM Act 2005", "Disaster Management Act 2005", "Indian legislation that created the institutional framework for disaster management at national, state, and district levels. It established NDMA (National), SDMA (State), and DDMA (District) authorities and mandated disaster management plans at all levels.", "The DM Act 2005 mandates district disaster management plans and provides the legal framework within which our research outputs (NbS-integrated DDMPs) will be implemented. It gives authority to district collectors to implement our recommended measures."),
        ("Sendai Framework", "Sendai Framework for DRR 2015-2030", "An international agreement signed by 187 countries including India, committing to reduce disaster risk and losses. It has 4 priorities: understanding risk, strengthening governance, investing in resilience, and enhancing preparedness. It explicitly encourages nature-based approaches.", "Our research aligns with Sendai Framework Priority 1 (understanding flood risk through AI-GIS mapping) and Priority 3 (investing in NbS for resilience). This international alignment strengthens the policy relevance of our work."),
        ("IPCC AR6", "Intergovernmental Panel on Climate Change 6th Assessment Report", "The most comprehensive scientific assessment of climate change, published in 2021-2023 by thousands of scientists worldwide. AR6 confirms that human-caused climate change is increasing the frequency and intensity of extreme rainfall events globally.", "IPCC AR6 provides the scientific basis for our climate change scenarios. It confirms that extreme rainfall in India has increased 75% since 1950 and will continue increasing, making our NbS research urgently necessary."),
        ("RCP 4.5", "Representative Concentration Pathway 4.5", "A climate change scenario where greenhouse gas emissions peak around 2040 and then decline (moderate mitigation). Global temperature rises about 1.8 degrees C by 2100. Represents a world where countries implement some climate policies but not aggressively.", "We use RCP 4.5 as our 'moderate' future climate scenario to test NbS effectiveness. It represents what happens if the world makes reasonable efforts to reduce emissions."),
        ("RCP 8.5", "Representative Concentration Pathway 8.5", "A climate change scenario where greenhouse gas emissions continue rising throughout the 21st century (no mitigation / business as usual). Global temperature rises about 4.3 degrees C by 2100. Represents the worst-case scenario if no climate action is taken.", "We use RCP 8.5 as our 'worst case' future climate scenario. If NbS works even under RCP 8.5, it proves the approach is robust and worthwhile regardless of how much climate change occurs."),
        ("Riparian Buffer", "Riparian Buffer Zone", "A strip of natural vegetation (trees, shrubs, grasses) maintained along both sides of a river or stream. Typically 30-100 meters wide. These vegetated strips filter pollutants from runoff, stabilize river banks, provide wildlife habitat, and critically - slow down and absorb floodwater.", "Riparian buffers are one of our primary NbS interventions. In our modeling, we simulate establishing 50m and 100m riparian buffers along key river reaches and measure the resulting reduction in peak flood discharge and flood extent downstream."),
        ("Wetland Reconnection", "Wetland Reconnection/Restoration", "Many natural wetlands have been disconnected from rivers by embankments or filled in for agriculture/development. Reconnection means removing barriers so the wetland can again receive and store floodwater during high flows, acting as a natural sponge and reservoir.", "Wetland reconnection is our second major NbS intervention. We identify former wetlands using historical satellite images and model the flood reduction benefit of reconnecting them to the river system."),
        ("Check Structures", "Check Dams / Check Structures", "Small barriers built across small streams and gullies (nalas) that slow down water flow, trap sediment, and promote groundwater recharge. They are typically 1-3 meters tall and made of local stone, gabions, or brushwood. They reduce the speed and erosive power of runoff.", "Check structures in upper catchments are our third NbS intervention category. In hilly Uttarakhand, strategically placed check structures in sub-watersheds can reduce peak discharge by 15-25% by slowing runoff and promoting infiltration."),
        ("MGNREGA", "Mahatma Gandhi National Rural Employment Guarantee Act", "India's largest rural employment program guaranteeing 100 days of paid work per year to every rural household. Many MGNREGA works involve land and water conservation - building check dams, farm ponds, contour trenches, and plantation activities.", "MGNREGA is the key implementation mechanism for NbS. Most NbS interventions (planting trees, building check dams, digging farm ponds, restoring wetlands) can be implemented through MGNREGA, providing employment while reducing flood risk."),
        ("Van Panchayat", "Van Panchayat (Forest Council)", "Community-managed forest governance system unique to Uttarakhand, where local village councils manage and protect designated forest areas. These are democratic institutions with legal authority over forest resources.", "Van Panchayats are critical for NbS implementation and maintenance in our Uttarakhand study site. Community ownership through Van Panchayats ensures long-term sustainability of forest-based NbS interventions."),
        ("IoT", "Internet of Things", "A network of physical sensors and devices connected to the internet that collect and share data automatically. In flood monitoring: water level sensors in rivers, rain gauges, soil moisture sensors - all sending real-time data to a central computer system.", "We propose an IoT-based monitoring system for NbS effectiveness - sensors measuring soil moisture, water levels, and flow rates before and after NbS implementation, connected to an AI system that issues flood early warnings."),
        ("EWS", "Early Warning System", "A system that detects approaching hazards and alerts communities before damage occurs. For floods: combines rainfall monitoring, river level sensors, and computer models to predict flooding hours or days in advance, giving people time to evacuate or protect assets.", "Our research integrates NbS with EWS design - showing how NbS interventions upstream extend the warning time available downstream by slowing the flood wave, giving communities more time to respond to warnings."),
        ("SUFI-2", "Sequential Uncertainty Fitting version 2", "An algorithm used in SWAT-CUP software for calibrating the SWAT model. It systematically tests thousands of parameter combinations using Latin Hypercube Sampling (a smart way to explore many possibilities efficiently) to find which parameter values make the model best match observed data.", "SUFI-2 is our model calibration algorithm. It uses AI-like optimization to find the best SWAT model parameters, testing 500-1000 simulations per iteration until the model achieves NSE > 0.7 against observed river discharge data."),
        ("CR", "Consistency Ratio", "A mathematical check in AHP that verifies whether expert judgments are logically consistent. If an expert says A is more important than B, and B is more important than C, they should also say A is more important than C. CR must be less than 0.10 (10%) for the weights to be accepted.", "We calculate CR for all our AHP weight matrices to ensure the vulnerability factor weights are logically consistent and scientifically defensible. If CR exceeds 0.10, we must revise the pairwise comparisons."),
        ("CSI", "Critical Success Index", "A validation metric for flood maps that measures how well our predicted flood extent matches the actual observed flood extent. It accounts for hits (correctly predicted flooded areas), misses (flooded areas we missed), and false alarms (areas we predicted as flooded but were not).", "CSI is used to validate our HEC-RAS flood inundation maps against Sentinel-1 SAR observed flood extents. We target CSI > 0.65 which indicates good agreement between modeled and observed flood boundaries."),
    ]
    
    headers = ["Term", "Full Form", "Simple Definition", "Role in This Research"]
    rows = [(t[0], t[1], t[2], t[3]) for t in glossary_data]
    add_table(doc, headers, rows)
    
    doc.add_page_break()



def add_problem_section(doc):
    add_heading_styled(doc, "3. THE PROBLEM - Why This Research Is Needed", level=1)
    add_para(doc, "In Simple Terms: India is one of the most flood-affected countries in the world. Every year, millions of people lose their homes, crops, and livelihoods. Despite billions spent on flood control, the problem is getting WORSE, not better. Climate change is making extreme rainfall more frequent and intense. We urgently need new approaches.", bold=True, italic=True, font_size=11)
    
    paragraphs = [
        "India's Flood Crisis in Numbers: India ranks as the most flood-affected country in Asia and the second most flood-affected country globally after China. According to the Central Water Commission (CWC) and National Disaster Management Authority (NDMA), approximately 72% of Indian districts (over 520 out of 718 districts) are exposed to flood hazards of varying severity. The average annual flood damage in India has increased from Rs. 1,805 crores in the 1950s to over Rs. 50,000 crores in recent years - a 27-fold increase even after adjusting for inflation. Between 2015 and 2023, floods in India killed over 12,000 people, displaced over 200 million (cumulative), and destroyed crops on over 50 million hectares of agricultural land.",
        
        "The Paradox of Increasing Flood Damage Despite Massive Investment: India has invested over Rs. 1,00,000 crores in structural flood control measures since independence - building over 36,000 km of embankments, 32,000 km of drainage channels, and numerous large dams and barrages. Yet the flood-affected area has increased from 5 million hectares (1950s average) to 40+ million hectares (recent average). This paradox reveals a fundamental flaw in the grey infrastructure approach: embankments give a false sense of security, encouraging encroachment into floodplains; when they breach (as they inevitably do), the damage is catastrophic because more people and assets are now in the flood path. Dams have finite storage capacity that gets reduced by sedimentation over time. Drainage channels get clogged with waste and encroachment in urban areas.",
        
        "Why Grey Infrastructure Alone Fails - The Engineering Limitations: Embankments (bandh) prevent lateral flow of flood water into natural storage areas (floodplains and wetlands), forcing all water to travel downstream in a narrow channel. This INCREASES peak flood levels downstream. When an embankment breaches under extreme pressure, the resulting flood is far more destructive than natural flooding would have been because the water bursts out with enormous force into areas that were unprepared. Furthermore, embankments prevent normal sediment deposition on floodplains, depriving agricultural land of natural fertility replenishment. The long-term result: downstream floods become MORE severe, not less.",
        
        "Climate Change is Making Everything Worse: According to IPCC AR6 and India Meteorological Department (IMD) data, extreme rainfall events (defined as daily rainfall exceeding 150mm) in India have increased by approximately 75% since 1950. The frequency of very heavy rainfall days has increased while moderate rainfall days have decreased - meaning rainfall is becoming more concentrated in fewer, more intense bursts. This is exactly the worst pattern for flooding: sudden heavy downpours overwhelm drainage capacity before water can gradually infiltrate or be stored. Climate projections under RCP 4.5 and RCP 8.5 scenarios indicate this trend will intensify through the 21st century, with extreme rainfall events potentially doubling by 2100.",
        
        "Early Warning System Coverage Gap: Despite India's advanced meteorological capabilities, only about 33% of flood-vulnerable communities have access to effective Early Warning Systems (EWS). In remote tribal and hill communities of Uttarakhand and Bihar, EWS coverage drops to below 15%. Even when warnings are issued, the lead time is often insufficient for effective evacuation - sometimes just 2-3 hours for flash floods in hilly terrain. NbS can extend this warning window by slowing flood waves.",
        
        "Recent Devastating Disasters That Underscore the Need: Uttarakhand 2013 (Kedarnath disaster) - Over 5,700 people killed, 4,200 villages affected, Rs. 12,000 crores damage. Caused by extreme rainfall on already saturated, deforested slopes triggering massive debris flows. Deforestation in upper catchments was a major amplifying factor. Kerala 2018 - 483 deaths, 1.4 million displaced, Rs. 40,000 crores economic loss. All 14 districts affected simultaneously when unprecedented rainfall combined with unplanned dam releases. Loss of natural wetlands and paddy fields (which act as water storage) in previous decades magnified the impact. Chamoli 2021 - Rock-ice avalanche triggered a devastating flood wave in the Rishi Ganga and Dhauli Ganga valleys, killing over 200 people including 134 workers trapped in underground tunnels of two hydropower projects. Showed vulnerability of infrastructure in Himalayan valleys. Wayanad 2024 - Massive landslides triggered by extreme rainfall killing over 400 people in what was formerly considered a relatively safe hilly area. Deforestation, monoculture plantations replacing natural forest, and quarrying activities destabilized slopes.",
        
        "The Common Thread: In every recent disaster, loss or degradation of natural ecosystems (forests, wetlands, floodplains, riparian zones) was identified as a significant amplifying factor. Nature-Based Solutions address this root cause directly, rather than trying to resist floods with ever-higher concrete walls in an escalating battle that nature always eventually wins.",
        
        "The Policy Gap: While India has excellent policies on paper (National Disaster Management Plan, State Action Plans on Climate Change, District Disaster Management Plans), these plans lack specific, scientifically-backed NbS prescriptions. They acknowledge the importance of ecosystems but do not provide: (a) quantified evidence of NbS effectiveness; (b) specific site selection criteria; (c) cost-benefit analyses; (d) implementation timelines; or (e) monitoring protocols. This research fills exactly these gaps.",
    ]
    
    for para in paragraphs:
        add_para(doc, para)
    
    doc.add_page_break()



def add_solution_section(doc):
    add_heading_styled(doc, "4. THE SOLUTION - What Are Nature-Based Solutions?", level=1)
    add_para(doc, "In Simple Terms: Nature-Based Solutions (NbS) means working WITH nature instead of AGAINST it to solve flood problems. Forests absorb rainwater like sponges. Wetlands store floodwater like natural reservoirs. Riverbank vegetation slows down rushing water. These natural services are free, self-maintaining, and often more effective than concrete structures.", bold=True, italic=True, font_size=11)
    
    paragraphs = [
        "Definition and Concept: Nature-Based Solutions (NbS) is defined by the International Union for Conservation of Nature (IUCN) as 'actions to protect, sustainably manage, and restore natural or modified ecosystems that address societal challenges effectively and adaptively, simultaneously providing human well-being and biodiversity benefits.' In the context of flood risk reduction, NbS involves using ecosystem services - the benefits that healthy natural systems provide to humans - to reduce flood hazard, exposure, and vulnerability. Unlike grey infrastructure that fights against natural water processes, NbS works by enhancing the landscape's natural capacity to absorb, store, slow down, and filter water.",
        
        "How NbS Reduces Flood Risk - The Four Mechanisms: (1) INFILTRATION ENHANCEMENT - Forests and vegetated areas have deep root systems that create channels in the soil, allowing rainwater to seep into the ground rather than running off the surface. Healthy forest soil can absorb 10-20 times more water than compacted bare or urban soil. This means less water reaches rivers during storms. (2) STORAGE - Wetlands, floodplains, and farm ponds physically store excess water during peak flows, releasing it slowly after the flood peak passes. A single hectare of functioning wetland can store 10,000-15,000 cubic meters of water. (3) FLOW RETARDATION - Vegetation along rivers and on floodplains increases surface roughness, physically slowing down the speed of flood waves. Slower water means the peak arrives later at downstream locations (more warning time) and with less destructive force. (4) SEDIMENT AND DEBRIS TRAPPING - Natural vegetation traps sediment and woody debris that would otherwise clog drainage infrastructure downstream. Riparian forests prevent bank erosion that adds sediment to flood flows.",
        
        "Types of NbS Interventions for Flood Reduction:",
    ]
    
    for para in paragraphs:
        add_para(doc, para)
    
    # NbS types table
    headers = ["NbS Type", "Description", "How It Reduces Floods", "Where Applicable", "Example Scale"]
    rows = [
        ("Riparian Buffer Restoration", "Planting native trees and vegetation along riverbanks in strips 30-100m wide", "Increases bank stability, filters runoff, slows overbank flow, increases roughness", "Along degraded river reaches in both study sites", "50-100m width, several km length"),
        ("Wetland Restoration/Creation", "Reconnecting or creating wetlands in low-lying areas near rivers", "Stores floodwater (10,000-15,000 m3/ha), reduces peak flow, delays flood peak", "Former wetland sites in Bihar floodplain, low-lying areas in Dehradun", "10-500 hectares per site"),
        ("Catchment Reforestation", "Planting native tree species on degraded upper catchment slopes", "Increases infiltration by 60-80%, reduces surface runoff, stabilizes soil", "Degraded hill slopes in Uttarakhand upper catchments", "100-5000 hectares"),
        ("Check Structures (Bio-engineering)", "Small vegetated barriers across gullies and small streams", "Slows runoff velocity, traps sediment, promotes infiltration, reduces peak flow", "First and second order streams in Uttarakhand", "1-3m height, every 50-200m along gullies"),
        ("Floodplain Reconnection", "Removing or lowering embankments to allow controlled flooding of designated areas", "Provides massive storage volume, reduces downstream peak by 10-30%", "Bihar study site where embankments trap water", "500-5000 hectares per site"),
        ("Urban Green Infrastructure", "Rain gardens, bioswales, permeable pavements, green roofs in urban areas", "Reduces urban runoff by 30-50%, delays time of concentration", "Dehradun urban and peri-urban areas", "Multiple small installations across city"),
        ("Farm Ponds and Bunds", "Small water harvesting structures on agricultural land", "Stores rainwater locally, reduces field runoff contribution to river flooding", "Agricultural areas in both study sites", "0.1-1 hectare per pond, community-scale"),
        ("Mangrove/Riparian Agroforestry", "Integrating trees with crops along waterways", "Combines livelihood with flood control, increases soil organic matter and infiltration", "River margins in Bihar, stream margins in Uttarakhand", "Along waterways, 20-50m strips"),
    ]
    add_table(doc, headers, rows)
    
    # Comparison table
    add_para(doc, "NbS vs Grey Infrastructure - Comparison:", bold=True)
    headers2 = ["Parameter", "Grey Infrastructure (Embankments, Dams)", "Nature-Based Solutions (Forests, Wetlands)"]
    rows2 = [
        ("Initial Cost", "Very High (Rs. 1-5 crores/km for embankments)", "Moderate to Low (Rs. 10-50 lakhs/hectare for restoration)"),
        ("Maintenance Cost", "High and ongoing (10-15% of capital annually)", "Low after establishment (self-maintaining after 5 years)"),
        ("Lifespan", "25-50 years with maintenance, then needs replacement", "Permanent and self-renewing if protected"),
        ("Failure Mode", "Catastrophic - sudden breach causes devastating damage", "Gradual degradation, no catastrophic failure mode"),
        ("Effectiveness Under Climate Change", "Decreases (designed for historical extremes)", "Increases (ecosystems adapt to changing conditions)"),
        ("Co-benefits", "Minimal - serves only flood control purpose", "Multiple: biodiversity, carbon storage, water purification, livelihoods, recreation"),
        ("Community Acceptance", "Often causes social conflict (land acquisition, displacement)", "High acceptance - provides income and ecosystem services to communities"),
        ("Employment Generation", "Limited to construction period", "Ongoing through MGNREGA, eco-tourism, sustainable harvesting"),
        ("Ecosystem Impact", "Negative - disrupts natural river processes, harms fish migration", "Positive - restores ecosystem health and biodiversity"),
        ("Scalability", "Limited by budget and land acquisition constraints", "Highly scalable through community participation and MGNREGA"),
        ("Downstream Effect", "Often transfers flood risk downstream", "Reduces flood risk system-wide"),
        ("Carbon Footprint", "High (concrete production is major CO2 source)", "Negative (absorbs CO2 through vegetation growth)"),
    ]
    add_table(doc, headers2, rows2)
    
    add_para(doc, "International Success Stories: The Netherlands has implemented 'Room for the River' program, deliberately lowering or removing embankments and restoring floodplains along the Rhine and Meuse rivers. Result: flood levels reduced by up to 1.5 meters while creating valuable wetland habitats and recreation areas. The United Kingdom's Natural Flood Management program in Yorkshire demonstrated that strategic tree planting and leaky woody dams in upper catchments reduced downstream flood peaks by 15-20%. Australia's Brisbane River catchment restoration after devastating 2011 floods showed that for every dollar invested in catchment revegetation, $4.30 in flood damage was avoided over 30 years.")
    
    add_para(doc, "Why NbS is Perfect for India: India has several unique advantages for NbS implementation: (1) MGNREGA provides labor force and funding mechanism - NbS activities like tree planting, check dam construction, wetland restoration perfectly align with MGNREGA work categories; (2) Traditional water management knowledge (talabs, johads, ahar-pyne systems) provides cultural foundation; (3) Large degraded areas available for restoration without displacing communities; (4) High biodiversity value means NbS provides exceptional co-benefits; (5) Climate vulnerability makes the need urgent and political will increasingly available; (6) Community forest management institutions (Van Panchayats, JFM committees) provide governance framework for sustainable maintenance.")
    
    doc.add_page_break()



def add_ai_integration(doc):
    add_heading_styled(doc, "5. AI INTEGRATION - Where, When, and How AI Is Used", level=1)
    
    # 5.1
    add_heading_styled(doc, "5.1 What is AI/ML in This Context?", level=2)
    add_para(doc, "In Simple Terms: Artificial Intelligence means making computers smart enough to perform tasks that normally require human intelligence - like recognizing patterns in satellite images, making predictions about future floods, or finding the best combination of model settings from millions of possibilities.", bold=True, italic=True, font_size=11)
    
    paragraphs_51 = [
        "Artificial Intelligence (AI) is the broad field of making machines capable of intelligent behavior. In our research context, AI does NOT mean robots or sentient computers - it means mathematical algorithms (sets of step-by-step instructions) that can learn patterns from data and apply those patterns to new situations. Think of it like this: a human expert can look at a satellite image and say 'this green area is forest, that brown area is bare soil, that blue area is water.' AI does the same thing, but for millions of pixels across thousands of square kilometers, with greater speed and consistency.",
        
        "Machine Learning (ML) is a subset of AI where the computer learns from examples rather than being explicitly programmed with rules. There are three main types relevant to our research: (1) SUPERVISED LEARNING - We show the computer labeled examples ('this is forest,' 'this is urban,' 'this is water') and it learns the patterns that distinguish each category. Then it can classify new, unlabeled images. We use this for land-use mapping. (2) OPTIMIZATION ALGORITHMS - These find the best solution from a vast space of possibilities. SUFI-2 in our model calibration tests thousands of parameter combinations to find which ones make the model best match reality. (3) STATISTICAL LEARNING - Advanced statistical methods that can identify non-linear relationships in data. We use these for non-stationary frequency analysis of extreme rainfall.",
        
        "Deep Learning is a further subset of ML using artificial neural networks (inspired by brain structure) with many layers. While we primarily use classical ML (Random Forest, SVM), we reference deep learning potential for future enhanced flood prediction using temporal satellite sequences.",
        
        "Why is AI Needed in This Research? Without AI: (a) Classifying land use across 5,000+ sq km from satellite images would take a trained analyst 6-8 months of manual work. With AI: 2-3 days including validation. (b) Calibrating a SWAT model by manual trial-and-error might require testing 50-100 parameter combinations (missing the optimal solution). With AI optimization: 5,000+ combinations tested systematically, finding globally optimal parameters. (c) Mapping flood extent from multiple SAR images manually is subjective and inconsistent between analysts. With AI: objective, reproducible, consistent thresholding and classification. (d) Analyzing non-stationary climate trends requires detecting subtle shifts in extreme value distributions. With AI statistical methods: robust detection of trends that human visual inspection would miss.",
    ]
    for para in paragraphs_51:
        add_para(doc, para)
    
    # 5.2
    add_heading_styled(doc, "5.2 AI Applications in This Research - Detailed Matrix", level=2)
    add_para(doc, "The following table provides a complete mapping of where, when, and how AI/ML techniques are deployed throughout this research:", bold=True)
    
    headers = ["Application", "AI/ML Technique", "Input Data", "Output", "When Used (Phase)", "Why Better Than Manual"]
    rows = [
        ("Land-Use/Land-Cover Classification", "Random Forest (RF) algorithm - an ensemble of 500+ decision trees that vote on the best classification", "Sentinel-2 multispectral imagery (10 bands), training samples from field visits and Google Earth", "LULC maps with 10+ classes at 10m resolution. Overall accuracy target: >85%", "Phase 1-2 (Months 2-6)", "Manual digitization of LULC for 5000 sq km would take 6 months. RF does it in days with higher consistency and reproducibility across time periods"),
        ("Flood Extent Mapping", "Change Detection with Otsu thresholding and ML-enhanced classification on SAR backscatter", "Sentinel-1 SAR pre-flood and during-flood images (VV and VH polarization)", "Binary flood maps showing exact extent of inundation for validation of HEC-RAS outputs", "Phase 3 (Months 10-14)", "Manual flood boundary delineation is subjective. AI provides consistent, reproducible boundaries. Critical for model validation (CSI calculation)"),
        ("Vulnerability Factor Weighting", "AHP with consistency optimization - iterative adjustment of pairwise comparison matrices using eigenvalue method", "Expert survey responses (pairwise comparisons of 18 vulnerability factors)", "Normalized weight vector with CR < 0.10 for each factor in FVI calculation", "Phase 2 (Months 5-7)", "Without mathematical optimization, expert opinions may be inconsistent. AHP algorithm ensures logical consistency and provides defensible weights"),
        ("Hydrological Model Calibration", "SUFI-2 algorithm using Latin Hypercube Sampling - a sophisticated optimization that explores parameter space efficiently", "Observed daily river discharge data (10+ years), SWAT model parameter ranges (26 parameters)", "Optimized parameter set achieving NSE > 0.7, R-squared > 0.7, PBIAS within +/-25%", "Phase 3 (Months 9-13)", "Manual calibration tests ~50 combinations. SUFI-2 tests 500-1000 per iteration across 3-5 iterations = 2500-5000 combinations. Finds global optimum, not just local"),
        ("Flood Damage Estimation", "Stage-damage function fitting using regression ML and Monte Carlo simulation for uncertainty", "Historical flood damage records, building survey data, flood depth-damage relationships from literature", "Spatially distributed damage estimates (Rs/m2) for each flood depth class", "Phase 5 (Months 22-25)", "Manual damage estimation is highly uncertain. ML can learn complex non-linear relationships between flood characteristics and actual damages from historical data"),
        ("Non-Stationary Frequency Analysis", "GEV distribution fitting with time-varying parameters using Maximum Likelihood Estimation and Bayesian inference", "Long-term daily rainfall records (50+ years), climate projection data (CMIP6 models)", "Climate-adjusted design storms for 10, 25, 50, 100-year return periods under RCP 4.5 and RCP 8.5", "Phase 3 (Months 8-10)", "Traditional frequency analysis assumes stable climate (stationary). AI-enhanced statistical methods detect trends and project future extremes accurately"),
        ("Pattern Recognition in Historical Floods", "Spatial clustering (K-means, DBSCAN) and temporal pattern analysis on historical flood records", "50+ years of flood records, historical satellite imagery, gazetted flood reports", "Identification of flood-prone hotspots, recurrence patterns, and changing flood characteristics over time", "Phase 1 (Months 2-4)", "Human analysis of 50 years of records across large areas misses subtle spatial-temporal patterns. Clustering algorithms reveal hidden patterns and trends"),
    ]
    add_table(doc, headers, rows)
    
    # 5.3
    add_heading_styled(doc, "5.3 AI Tools and Software Used", level=2)
    
    ai_tools_paras = [
        "Python Programming Language with Scientific Libraries: Python is the primary programming language for AI/ML implementation in this research. Key libraries include: scikit-learn (for Random Forest classification, clustering, and regression), NumPy and Pandas (for data manipulation), SciPy (for statistical analysis and distribution fitting), matplotlib and seaborn (for visualization). Python is free, open-source, and has the largest ecosystem of geospatial and ML libraries available.",
        
        "Google Earth Engine (GEE): A cloud-based platform by Google that provides free access to petabytes of satellite imagery and powerful computing infrastructure. GEE allows us to run ML classification algorithms on decades of satellite data without downloading anything to local computers. We use GEE for: multi-temporal LULC classification, NDVI time series analysis, large-scale change detection, and SAR-based flood mapping. The advantage is processing speed - analysis that would take weeks on a desktop runs in minutes on Google's servers.",
        
        "R Statistical Software: Used specifically for advanced statistical analysis including non-stationary frequency analysis (packages: extRemes, eva, nsRFA), Bayesian inference (packages: R2jags, rstan), and spatial statistics. R has the most mature and validated implementations of extreme value theory methods needed for our climate-adjusted flood frequency analysis.",
        
        "SWAT-CUP with SUFI-2: SWAT Calibration and Uncertainty Programs (SWAT-CUP) is specialized software for calibrating the SWAT hydrological model. SUFI-2 (Sequential Uncertainty Fitting version 2) within SWAT-CUP uses Latin Hypercube Sampling - a stratified random sampling method that efficiently explores the multi-dimensional parameter space. In each iteration, it runs 500-1000 simulations with different parameter combinations, evaluates performance against observed data, and progressively narrows the parameter ranges toward optimal values. This is essentially an AI optimization process applied to hydrological modeling.",
        
        "TensorFlow Lite (Future Enhancement): While not the primary AI tool in the current research, TensorFlow Lite represents a future enhancement pathway. It enables running trained ML models on mobile devices and IoT sensors for real-time flood detection and early warning. This aligns with our proposed IoT-based NbS monitoring system where edge computing (processing data at the sensor location rather than sending everything to a central server) enables faster response times.",
    ]
    for para in ai_tools_paras:
        add_para(doc, para)
    
    # AI Flowchart
    add_flowchart(doc, "AI Integration Points in the Research", [
        "+------------------------------------------------------------------+",
        "|            AI INTEGRATION POINTS IN RESEARCH WORKFLOW             |",
        "+------------------------------------------------------------------+",
        "|                                                                    |",
        "|  PHASE 1: DATA COLLECTION                                         |",
        "|  +------------------+     +-------------------+                   |",
        "|  | Satellite Images |---->| AI Classification |---> LULC Maps     |",
        "|  | (Sentinel-1 & 2) |     | (Random Forest)   |                   |",
        "|  +------------------+     +-------------------+                   |",
        "|                                                                    |",
        "|  PHASE 2: VULNERABILITY MAPPING                                   |",
        "|  +------------------+     +-------------------+                   |",
        "|  | Expert Surveys   |---->| AHP Optimization  |---> FVI Weights   |",
        "|  | (Pairwise Matrix)|     | (Eigenvalue+CR)   |                   |",
        "|  +------------------+     +-------------------+                   |",
        "|                                                                    |",
        "|  PHASE 3: HYDROLOGICAL MODELING                                   |",
        "|  +------------------+     +-------------------+                   |",
        "|  | Observed Q Data  |---->| SUFI-2 Algorithm  |---> Calibrated    |",
        "|  | + SWAT Params    |     | (Latin Hypercube) |     SWAT Model    |",
        "|  +------------------+     +-------------------+                   |",
        "|                                                                    |",
        "|  +------------------+     +-------------------+                   |",
        "|  | SAR Flood Images |---->| Change Detection  |---> Flood Maps    |",
        "|  | (Sentinel-1)     |     | (ML Threshold)    |     (Validation)  |",
        "|  +------------------+     +-------------------+                   |",
        "|                                                                    |",
        "|  PHASE 4-5: ANALYSIS                                              |",
        "|  +------------------+     +-------------------+                   |",
        "|  | Rainfall Records |---->| GEV Fitting (MLE) |---> Design Storms |",
        "|  | (50+ years)      |     | Non-Stationary    |     (Future)      |",
        "|  +------------------+     +-------------------+                   |",
        "|                                                                    |",
        "|  +------------------+     +-------------------+                   |",
        "|  | Flood Depth +    |---->| Regression ML     |---> Damage Maps   |",
        "|  | Asset Data       |     | (Stage-Damage)    |     (Rs/sq.m)     |",
        "|  +------------------+     +-------------------+                   |",
        "+------------------------------------------------------------------+",
    ])
    
    doc.add_page_break()



def add_gis_integration(doc):
    add_heading_styled(doc, "6. GIS INTEGRATION - Where, When, and How GIS Is Used", level=1)
    
    # 6.1
    add_heading_styled(doc, "6.1 What is GIS?", level=2)
    add_para(doc, "In Simple Terms: GIS (Geographic Information System) is like a super-powered digital map that can store many types of information in layers and perform calculations to answer spatial questions. Imagine stacking transparent sheets - one showing rivers, one showing elevation, one showing soil type, one showing population - and being able to mathematically combine them to find answers like 'where are the most flood-vulnerable areas?'", bold=True, italic=True, font_size=11)
    
    gis_intro = [
        "A Geographic Information System (GIS) is computer-based technology for capturing, storing, analyzing, managing, and displaying geographic (spatial) data. Unlike a simple map that just shows locations, GIS connects geographic features (points, lines, areas) with attribute information (data about those features). For example, a river in GIS is not just a blue line on a map - it is a feature with attached data: its name, length, average discharge, flood frequency, water quality parameters, bank condition, and riparian vegetation status.",
        
        "The LAYERS Concept Explained: GIS works with data organized in layers (also called themes or coverages). Each layer represents one type of geographic information. In our flood research, key layers include: (1) ELEVATION layer showing height of terrain at every point; (2) SLOPE layer showing steepness; (3) DRAINAGE layer showing rivers and streams; (4) SOIL layer showing soil types and infiltration capacity; (5) LAND USE layer showing what covers the ground (forest, urban, agriculture); (6) RAINFALL layer showing precipitation patterns; (7) POPULATION layer showing where people live; (8) INFRASTRUCTURE layer showing roads, buildings, hospitals. The power of GIS lies in OVERLAY ANALYSIS - combining multiple layers mathematically to create new information that no single layer could provide alone.",
        
        "Why GIS is Essential for Flood Research: Floods are fundamentally SPATIAL phenomena - they happen in specific geographic locations determined by terrain, drainage patterns, rainfall distribution, and land characteristics. Without GIS, we cannot: (a) Identify which specific areas will flood (requires terrain + hydrology analysis); (b) Determine who is affected (requires overlaying flood extent with population data); (c) Select optimal NbS sites (requires multi-criteria spatial analysis); (d) Create maps for disaster management plans (requires cartographic output); (e) Communicate results to policymakers (maps are far more powerful than tables of numbers).",
    ]
    for para in gis_intro:
        add_para(doc, para)
    
    # 6.2
    add_heading_styled(doc, "6.2 GIS Applications in This Research - Detailed Matrix", level=2)
    
    headers = ["Application", "GIS Operation", "Software", "Input Layers", "Output Product", "When Used (Phase)"]
    rows = [
        ("Terrain Analysis", "DEM processing: slope calculation, aspect derivation, flow direction, flow accumulation, drainage network extraction, hill-shade generation", "QGIS + GRASS GIS + WhiteboxTools", "SRTM 30m DEM, ALOS PALSAR DEM (12.5m for Uttarakhand)", "Slope map, Aspect map, Flow direction grid, Drainage density map, TWI map, HAND map", "Phase 1 (Months 1-3)"),
        ("Watershed Delineation", "Automated catchment boundary extraction from DEM using D8 flow algorithm, sub-watershed division, stream ordering (Strahler method)", "QGIS with GRASS GIS r.watershed module", "Filled DEM, pour point locations (gauging stations)", "Watershed boundary polygons, sub-basin boundaries, stream network with Strahler orders", "Phase 1 (Month 2-3)"),
        ("FVI Mapping (Vulnerability)", "Multi-Criteria Evaluation: weighted overlay of 18 normalized layers using AHP-derived weights. Reclassification into 5 vulnerability classes.", "QGIS + Python (rasterio, numpy)", "18 raster layers: DEM, slope, TWI, HAND, drainage density, rainfall, soil, LULC, NDVI, population, road density, distance to river, historical flood frequency, poverty index, etc.", "Flood Vulnerability Index map (0-1 continuous) reclassified into Very High/High/Moderate/Low/Very Low zones", "Phase 2 (Months 5-8)"),
        ("Flood Inundation Mapping", "Converting HEC-RAS 2D model output (water surface elevation grid) to GIS layers. Flood depth = Water Surface Elevation minus Ground Elevation. Flood extent = areas where depth > 0.", "QGIS + HEC-RAS Mapper + RAS2FIM tools", "HEC-RAS water surface elevation output, DEM, cross-section data", "Flood depth maps, flood extent polygons, flood duration maps, velocity maps - for each return period (10, 25, 50, 100-yr)", "Phase 3 (Months 12-16)"),
        ("Land-Use Change Detection", "Multi-temporal comparison of classified satellite images (2000, 2010, 2015, 2020, 2024). Change matrix generation, transition mapping.", "Google Earth Engine + QGIS", "Classified LULC maps from multiple years (output of AI classification)", "Change detection maps showing where forest was lost, wetlands were filled, urbanization expanded over 24 years. Quantified area of each transition.", "Phase 1-2 (Months 3-6)"),
        ("NbS Site Selection (Suitability)", "Multi-Criteria Suitability Analysis: Boolean and weighted overlay of constraint layers (slope, soil, land use, land ownership, accessibility) to identify optimal NbS locations.", "QGIS + Python scripting", "Slope, soil infiltration capacity, current land use, land ownership (revenue maps), distance to settlements, distance to water, historical flood extent, elevation above river", "NbS suitability maps showing optimal locations for: riparian buffers, wetland restoration, reforestation, check structures. Each pixel rated as Highly Suitable / Suitable / Marginal / Unsuitable", "Phase 4 (Months 16-18)"),
        ("DDMP Map Integration", "Cartographic output production: creating standardized map layouts with legend, scale bar, north arrow, coordinate grid suitable for government planning documents at district/block/village level.", "QGIS Print Composer", "All analysis outputs: FVI maps, flood maps, NbS maps, infrastructure layers, administrative boundaries", "Publication-ready maps at multiple scales for insertion into District Disaster Management Plans. Includes risk zone maps, evacuation route maps, NbS implementation area maps.", "Phase 6 (Months 26-30)"),
        ("Climate Risk Overlay", "Combining hazard layers (flood extent under climate scenarios) with exposure layers (population, assets) and vulnerability layers (FVI) to create integrated climate risk maps.", "QGIS + Python (rasterstats for zonal statistics)", "Future flood extent maps (under RCP 4.5 and RCP 8.5), population grids, building footprints, agricultural land maps, FVI layers", "Climate Risk Index maps showing which areas face increasing risk under climate change. Essential for long-term planning and climate adaptation strategies.", "Phase 4-5 (Months 18-24)"),
    ]
    add_table(doc, headers, rows)
    
    # 6.3
    add_heading_styled(doc, "6.3 GIS Tools and Software", level=2)
    
    gis_tools = [
        "QGIS (Quantum GIS) - Version 3.x: Our PRIMARY GIS software. QGIS is free, open-source, and professional-grade. It handles all standard GIS operations: data visualization, layer management, spatial analysis, map production. QGIS has a powerful plugin ecosystem with specialized tools for hydrology (QSWAT plugin for SWAT model setup), terrain analysis (WhiteboxTools plugin), and remote sensing (Semi-Automatic Classification Plugin). Being free and open-source means our methodology is accessible to any researcher or government agency without expensive license fees, promoting replicability.",
        
        "GRASS GIS (Geographic Resources Analysis Support System): Integrated within QGIS as a processing backend. GRASS GIS has exceptionally powerful raster processing capabilities essential for hydrology: r.watershed (watershed delineation), r.terraflow (flow routing), r.water.outlet (drainage extraction), r.mapcalc (raster algebra). Its 40+ year development history means algorithms are thoroughly tested and scientifically validated.",
        
        "Google Earth Engine (GEE): Cloud-based geospatial analysis platform. GEE provides: (a) Free access to the entire Landsat archive (1972-present), Sentinel archive (2014-present), MODIS, and hundreds of other datasets; (b) Cloud computing infrastructure - no need to download terabytes of data; (c) JavaScript and Python APIs for scripting analysis; (d) Built-in ML classifiers. We use GEE for all satellite image processing and classification because it eliminates the data download and storage bottleneck that would otherwise require multiple terabytes of hard drive space.",
        
        "PostGIS (Spatial Database Extension for PostgreSQL): For managing large spatial datasets. When dealing with thousands of features across multiple years, a proper spatial database provides: efficient queries ('find all villages within 2km of rivers in high vulnerability zones'), data integrity, multi-user access, and integration with web mapping for visualization and sharing results with stakeholders.",
        
        "HEC-RAS Mapper (integrated with HEC-RAS 6.x): Specifically for hydraulic model visualization and flood inundation mapping. HEC-RAS Mapper converts 1D and 2D hydraulic model results into GIS-compatible flood maps, creates flood depth grids, generates flood boundary polygons, and produces flood animation sequences showing how inundation progresses over time during a flood event.",
    ]
    for para in gis_tools:
        add_para(doc, para)
    
    # 6.4 Data Inventory
    add_heading_styled(doc, "6.4 GIS Data Sources - Complete Inventory", level=2)
    
    headers2 = ["Dataset", "Source Agency", "Resolution/Scale", "What It Shows", "How We Use It"]
    rows2 = [
        ("SRTM DEM", "NASA/USGS (free download from EarthExplorer)", "30m horizontal, ~5m vertical accuracy", "Terrain elevation across entire study area", "Base layer for all terrain analysis: slope, flow direction, watershed delineation, TWI, HAND calculation"),
        ("ALOS PALSAR DEM", "JAXA (free from ASF DAAC)", "12.5m horizontal", "Higher resolution terrain for Uttarakhand hilly area", "Enhanced terrain analysis for steep slopes where 30m SRTM may miss narrow valleys and ridges"),
        ("Sentinel-2 MSI", "ESA Copernicus (free via GEE or Copernicus Hub)", "10m (VNIR), 20m (SWIR)", "Multispectral optical imagery in 13 bands", "Land use classification, NDVI calculation, vegetation health monitoring, change detection"),
        ("Sentinel-1 SAR", "ESA Copernicus (free via GEE or Copernicus Hub)", "10m (IW mode)", "Radar backscatter intensity (works through clouds)", "Flood extent mapping during actual flood events, soil moisture estimation, change detection"),
        ("Landsat 5/7/8/9", "NASA/USGS (free via GEE or EarthExplorer)", "30m multispectral", "Historical optical imagery from 1984 to present", "Long-term land use change analysis (40 years), historical NDVI trends, wetland mapping"),
        ("Soil Map", "NBSS&LUP (National Bureau of Soil Survey)", "1:250,000 to 1:50,000 scale", "Soil types, texture, depth, drainage class, infiltration capacity", "Input to SWAT model (soil parameters), FVI mapping, NbS site selection (soil suitability)"),
        ("Rainfall Data", "IMD (India Meteorological Department)", "0.25 degree gridded + station data", "Daily rainfall 1951-present", "Input to SWAT model, frequency analysis, design storm calculation"),
        ("River Discharge", "CWC (Central Water Commission)", "Daily at gauging stations", "Observed daily river flow (cumecs)", "SWAT model calibration and validation, flood frequency analysis"),
        ("Census Data", "Census of India 2011 (+ projections)", "Village/ward level", "Population, housing, amenities, occupation", "Exposure and vulnerability mapping, damage estimation, benefit distribution analysis"),
        ("LULC (reference)", "NRSC Bhuvan LULC", "1:50,000 scale", "Official land use land cover maps", "Validation of our AI-classified LULC maps, identification of land use change trajectories"),
        ("Administrative Boundaries", "Survey of India", "Village/block/district level", "Political and administrative boundaries", "Aggregation of results by administrative unit, DDMP integration at district and block level"),
        ("Road Network", "OpenStreetMap + NHAI", "Detailed mapping", "All roads including rural roads (PMGSY)", "Accessibility analysis for NbS sites, evacuation route planning, FVI factor"),
        ("Building Footprints", "Google Open Buildings + Survey", "Individual building level", "Location and area of all buildings", "Exposure mapping, damage estimation, identifying structures in flood zones"),
        ("Historical Flood Maps", "NRSC/ISRO Flood Monitoring + CWC", "Variable (30m-250m)", "Recorded flood extents from past events", "HEC-RAS validation, flood frequency mapping, identifying recurring flood zones"),
        ("Climate Projections", "CMIP6 models via CORDEX-SA", "0.25 to 0.5 degree", "Future temperature, rainfall under RCP 4.5, 8.5", "Non-stationary frequency analysis, future flood scenarios, climate risk assessment"),
    ]
    add_table(doc, headers2, rows2)
    
    # GIS Layer Stacking Flowchart
    add_flowchart(doc, "GIS Layer Stacking Concept for FVI Mapping", [
        "+================================================================+",
        "|        GIS LAYER STACKING FOR FLOOD VULNERABILITY INDEX        |",
        "+================================================================+",
        "|                                                                  |",
        "|  Layer 1 (Top):     Land Use/Land Cover     [Weight: 0.14]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 2:           Elevation (DEM)          [Weight: 0.12]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 3:           Slope                    [Weight: 0.11]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 4:           Drainage Density         [Weight: 0.10]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 5:           TWI                      [Weight: 0.09]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 6:           HAND                     [Weight: 0.09]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 7:           Rainfall Intensity       [Weight: 0.08]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 8:           Soil Type                [Weight: 0.07]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 9:           NDVI (Vegetation)        [Weight: 0.06]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 10:          Distance to River        [Weight: 0.05]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 11:          Population Density       [Weight: 0.04]      |",
        "|  -----------------------------------------------------------------",
        "|  Layer 12:          Historical Flood Freq.   [Weight: 0.05]      |",
        "|  =================================================================",
        "|                          |                                        |",
        "|                          v                                        |",
        "|          WEIGHTED OVERLAY (Sum of Wi x Li for all layers)        |",
        "|                          |                                        |",
        "|                          v                                        |",
        "|     FLOOD VULNERABILITY INDEX MAP (Continuous 0 to 1)            |",
        "|                          |                                        |",
        "|                          v                                        |",
        "|     RECLASSIFIED: Very High | High | Moderate | Low | Very Low   |",
        "+================================================================+",
    ])
    
    doc.add_page_break()



def add_methodology(doc):
    add_heading_styled(doc, "7. THE COMPLETE METHODOLOGY - Step-by-Step How Guide", level=1)
    add_para(doc, "In Simple Terms: This section explains EXACTLY how we will conduct this research, step by step, in plain language. The research spans 30 months divided into 6 phases. Each phase builds on the previous one, like building a house - you need the foundation before you can build walls.", bold=True, italic=True, font_size=11)
    
    # Overall Research Flow Flowchart
    add_flowchart(doc, "Overall Research Flow (6 Phases)", [
        "+====================================================================+",
        "|              OVERALL RESEARCH METHODOLOGY FLOWCHART                 |",
        "+====================================================================+",
        "|                                                                      |",
        "|  PHASE 1: DATA COLLECTION (Months 1-4)                              |",
        "|  [Satellite imagery + Field data + Historical records]               |",
        "|          |                                                           |",
        "|          v                                                           |",
        "|  PHASE 2: VULNERABILITY MAPPING (Months 4-8)                        |",
        "|  [AHP weights + GIS overlay = Flood Vulnerability Index]             |",
        "|          |                                                           |",
        "|          v                                                           |",
        "|  PHASE 3: HYDROLOGICAL MODELING (Months 8-16)                       |",
        "|  [SWAT (watershed) + HEC-RAS (river) = Flood simulation]            |",
        "|          |                                                           |",
        "|          v                                                           |",
        "|  PHASE 4: NbS SCENARIO TESTING (Months 16-22)                       |",
        "|  [Change land use in model --> measure flood reduction]              |",
        "|          |                                                           |",
        "|          v                                                           |",
        "|  PHASE 5: ECONOMIC ANALYSIS (Months 22-26)                          |",
        "|  [Calculate damage reduction --> Benefit-Cost Ratio]                 |",
        "|          |                                                           |",
        "|          v                                                           |",
        "|  PHASE 6: POLICY INTEGRATION (Months 26-30)                         |",
        "|  [Create DDMP templates --> Stakeholder validation]                  |",
        "+====================================================================+",
    ])
    
    # Phase 1
    add_heading_styled(doc, "Phase 1: Data Collection and Preprocessing (Months 1-4)", level=2)
    
    phase1_paras = [
        "What We Collect: In this first phase, we gather all the raw data needed for the entire research. This includes satellite images spanning 24 years (2000-2024) from multiple sensors, terrain elevation data, soil maps, rainfall records (50+ years of daily data), river discharge measurements (15+ years), census data, historical flood records, land revenue maps, and field survey data that we collect ourselves by visiting the study areas.",
        
        "Satellite Data Acquisition: We download Sentinel-2 optical images for at least 5 time periods (representing different seasons and years) for land-use classification. We access Sentinel-1 SAR images specifically from flood seasons (July-September) across multiple years to map historical flood extents. Landsat archives (1984-2024) provide the long-term change perspective. All satellite data is accessed through Google Earth Engine, which eliminates the need to download terabytes of data - we process it directly in the cloud.",
        
        "Field Data Collection: We conduct two field campaigns (one per study site) of 15-20 days each. Activities include: (1) Collecting GPS-referenced ground truth points for LULC validation (minimum 300 points per site); (2) Surveying river cross-sections at key locations for HEC-RAS model input; (3) Recording flood high-water marks from recent flood events (asking local residents, observing marks on buildings); (4) Photographing and documenting current NbS features (existing forests, wetlands, check dams); (5) Conducting household surveys on flood experience, damage, and willingness to participate in NbS programs; (6) Meeting local officials (District Magistrate, SDM, Block Development Officer) to collect DDMP documents and understand implementation constraints.",
        
        "Data Preprocessing - Making Raw Data Usable: Raw satellite images need several corrections before analysis: (a) Atmospheric correction - removing effects of haze and atmospheric scattering so surface reflectance values are accurate; (b) Cloud masking - identifying and excluding cloud-covered pixels; (c) Geometric correction - ensuring pixels align precisely with geographic coordinates; (d) Mosaicking - combining multiple image tiles to cover the full study area seamlessly. DEM preprocessing includes: filling artificial sinks (small depressions in data that would trap water flow unrealistically), projecting to local coordinate system (UTM Zone 44N for our study areas), and resampling to consistent resolution.",
        
        "Quality Checks: Every dataset undergoes quality verification: (1) Satellite image quality assessment (cloud cover percentage, data gaps, sensor anomalies); (2) DEM accuracy check using GPS ground control points; (3) Rainfall data completeness check and gap-filling using neighboring stations; (4) Discharge data quality check for rating curve accuracy and outlier identification; (5) Field data cross-verification with multiple sources (e.g., flood marks verified against satellite-observed flood extent dates).",
    ]
    for para in phase1_paras:
        add_para(doc, para)
    
    # Phase 2
    add_heading_styled(doc, "Phase 2: Vulnerability Mapping with AHP-GIS Integration (Months 4-8)", level=2)
    
    phase2_paras = [
        "The AHP Process Explained Simply: Analytic Hierarchy Process is a structured method for making complex decisions where many factors must be considered. Here is how it works in our research, step by step:",
        
        "Step 1 - Identify Factors: We identify 18 factors that influence flood vulnerability. These are divided into three categories: PHYSICAL factors (elevation, slope, drainage density, TWI, HAND, soil type, rainfall intensity, distance to river, geology, geomorphology), SOCIAL factors (population density, poverty level, female ratio, age dependency ratio), and RESILIENCE factors (road density, health facility access, EWS coverage, literacy rate).",
        
        "Step 2 - Pairwise Comparison: We ask 15-20 experts (professors, disaster management officials, field practitioners) to compare factors in pairs. For each pair, they rate which is more important for flood vulnerability on a scale of 1-9. For example: 'Is SLOPE more important than SOIL TYPE for determining flood vulnerability? If yes, how much more?' If slope is moderately more important, expert assigns 3. If strongly more important, assigns 5. We build a 18x18 matrix of these comparisons.",
        
        "Step 3 - Calculate Weights: The AHP algorithm (eigenvalue method) converts the pairwise comparison matrix into a set of weights (importance values) that sum to 1.0. For example: Elevation might get weight 0.12, Slope 0.11, HAND 0.09, Population density 0.04. Higher weight means the factor contributes more to the final vulnerability score.",
        
        "Step 4 - Consistency Check: We calculate the Consistency Ratio (CR). If CR > 0.10, the expert judgments contain logical contradictions and must be revised. This ensures our weights are scientifically defensible. If an expert says A > B and B > C but then says C > A, that is inconsistent and CR will be high.",
        
        "Step 5 - GIS Layer Preparation: Each of the 18 factors is prepared as a raster (grid) layer in GIS. Each layer is normalized to a 0-1 scale so they can be combined. Normalization methods depend on the factor: for elevation (lower = more vulnerable), we use Min-Max inversion. For drainage density (higher = more vulnerable), we use direct Min-Max scaling.",
        
        "Step 6 - Weighted Overlay in GIS: The normalized layers are multiplied by their AHP weights and summed: FVI = W1*L1 + W2*L2 + ... + W18*L18, where Wi is the weight and Li is the normalized layer value. This produces a continuous FVI map where every pixel has a vulnerability score between 0 and 1.",
        
        "Step 7 - Classification: The continuous FVI map is reclassified into 5 classes using natural breaks (Jenks method): Very High (0.8-1.0), High (0.6-0.8), Moderate (0.4-0.6), Low (0.2-0.4), Very Low (0-0.2). These classes are mapped with distinct colors and form the primary vulnerability product.",
        
        "Validation: We validate FVI maps against: (a) Historical flood damage records (do Very High zones correspond to actual damage hotspots?); (b) Community perception surveys (do residents in 'Very High' zones report frequent flooding?); (c) Satellite-observed flood extents (do historical SAR-derived flood maps overlap with high-FVI areas?). Target validation accuracy: > 75% correspondence.",
    ]
    for para in phase2_paras:
        add_para(doc, para)
    
    # AHP Flowchart
    add_flowchart(doc, "AHP Decision Tree for Weight Calculation", [
        "+================================================================+",
        "|           AHP DECISION TREE FOR FVI WEIGHT CALCULATION          |",
        "+================================================================+",
        "|                                                                  |",
        "|                    GOAL: Flood Vulnerability Index               |",
        "|                              |                                   |",
        "|            +-----------------+-----------------+                 |",
        "|            |                 |                 |                 |",
        "|            v                 v                 v                 |",
        "|     PHYSICAL (0.55)    SOCIAL (0.28)    RESILIENCE (0.17)       |",
        "|            |                 |                 |                 |",
        "|    +---+---+---+       +---+---+       +---+---+               |",
        "|    |   |   |   |       |   |   |       |   |   |               |",
        "|    v   v   v   v       v   v   v       v   v   v               |",
        "|  Elev Slp TWI HAND   Pop Pov Fem     Road Hlt EWS             |",
        "| .12  .11 .09 .09    .08 .07 .06     .05  .04 .04              |",
        "|  ... (+ 8 more)      (+ 1 more)     (+ 2 more)                |",
        "|                                                                  |",
        "|  Expert Pairwise Comparison (18 x 18 Matrix)                    |",
        "|            |                                                     |",
        "|            v                                                     |",
        "|  Eigenvalue Calculation --> Weight Vector                        |",
        "|            |                                                     |",
        "|            v                                                     |",
        "|  Consistency Ratio Check (CR < 0.10? If YES, proceed)           |",
        "|            |                                                     |",
        "|            v                                                     |",
        "|  Apply Weights to Normalized GIS Layers                         |",
        "|            |                                                     |",
        "|            v                                                     |",
        "|  FVI = Sum(Wi x Li) for i = 1 to 18                            |",
        "+================================================================+",
    ])
    
    # Phase 3
    add_heading_styled(doc, "Phase 3: Hydrological Modeling (Months 8-16)", level=2)
    
    phase3_paras = [
        "SWAT Model Explained Simply: The Soil and Water Assessment Tool (SWAT) is like a virtual watershed (river basin) that lives inside the computer. It divides the real watershed into hundreds of small pieces (HRUs - Hydrological Response Units) and for each piece, on each day, it calculates: How much rain fell? How much was intercepted by plant leaves? How much infiltrated into soil? How much became surface runoff? How much moved through the soil as lateral flow? How much reached groundwater? How much evaporated? By doing this calculation for every piece every day for years, it predicts how much water arrives at the river and when.",
        
        "SWAT Model Setup Process: (1) We import the DEM into SWAT (using QSWAT plugin) and the model automatically delineates the watershed and sub-basins. (2) We overlay land use map, soil map, and slope classes. SWAT creates HRUs at every unique combination of land use, soil, and slope. Typically 500-2000 HRUs per study watershed. (3) We input daily weather data (rainfall, temperature, solar radiation, humidity, wind speed). (4) We set parameter values for soil properties, groundwater, channel routing, and vegetation growth. (5) We run the model for a warm-up period (3 years, to initialize soil moisture and groundwater) and then for the simulation period (10+ years).",
        
        "HEC-RAS Model Explained Simply: While SWAT tells us how much water reaches the river, HEC-RAS tells us what happens to that water IN the river and on the floodplain. HEC-RAS solves the Saint-Venant equations (the mathematical equations that describe how water flows in open channels) to calculate water depth, velocity, and extent at every point along the river. When river flow exceeds the channel capacity, HEC-RAS simulates water spilling onto the floodplain, showing exactly which areas flood, to what depth, and for how long.",
        
        "HEC-RAS Model Setup: (1) We create river geometry from DEM and field survey data - the shape of the river channel and floodplain at multiple cross-sections spaced 100-500m apart. (2) We assign Manning's roughness values (n) to the channel and floodplain based on land cover. (3) For 2D modeling, we create a computational mesh (grid) covering the floodplain area. (4) We input the flow hydrograph (water volume over time) from SWAT output as the upstream boundary condition. (5) We run the model for specific flood events and generate output: water depth, velocity, flood extent over time.",
        
        "SWAT-HEC-RAS Coupling (How They Connect): SWAT and HEC-RAS are 'coupled' (connected) sequentially. First, SWAT simulates the watershed response to rainfall and produces a discharge hydrograph (a graph of river flow over time) at the point where our river reach of interest begins. This hydrograph becomes the INPUT to HEC-RAS, which then simulates the detailed flooding pattern along and across the river channel and floodplain. This coupling allows us to: (a) Simulate the effect of upstream NbS on downstream flooding (through SWAT), and (b) Map the precise spatial extent and depth of flooding in the area of interest (through HEC-RAS).",
    ]
    for para in phase3_paras:
        add_para(doc, para)
    
    # SWAT-HEC-RAS Coupling Flowchart
    add_flowchart(doc, "SWAT-HEC-RAS Coupling Process", [
        "+================================================================+",
        "|              SWAT - HEC-RAS COUPLING WORKFLOW                    |",
        "+================================================================+",
        "|                                                                  |",
        "|  RAINFALL DATA (Daily)                                          |",
        "|       |                                                          |",
        "|       v                                                          |",
        "|  +------------------+                                            |",
        "|  |   SWAT MODEL     |  (Simulates entire watershed)             |",
        "|  |                  |                                            |",
        "|  | DEM + Soil +     |                                            |",
        "|  | Land Use + LULC  |                                            |",
        "|  | = HRU-based      |                                            |",
        "|  | water balance    |                                            |",
        "|  +--------+---------+                                            |",
        "|           |                                                      |",
        "|           | OUTPUT: Daily/Hourly Discharge Hydrograph            |",
        "|           | (Flow in cumecs at sub-basin outlets)                |",
        "|           v                                                      |",
        "|  +------------------+                                            |",
        "|  |   HEC-RAS MODEL  |  (Simulates river channel + floodplain)   |",
        "|  |                  |                                            |",
        "|  | River Geometry + |                                            |",
        "|  | Manning's n +    |                                            |",
        "|  | 2D Mesh +        |                                            |",
        "|  | Boundary Conds.  |                                            |",
        "|  +--------+---------+                                            |",
        "|           |                                                      |",
        "|           | OUTPUT: Flood Maps                                   |",
        "|           v                                                      |",
        "|  +------------------------------------------+                    |",
        "|  | Flood Depth Map | Flood Extent | Velocity |                   |",
        "|  | (meters)        | (polygon)    | (m/s)    |                   |",
        "|  +------------------------------------------+                    |",
        "+================================================================+",
    ])
    
    phase3b_paras = [
        "Model Calibration with SUFI-2 (How We Make the Model Accurate): A model is only useful if it accurately represents reality. Calibration means adjusting model parameters until the model output closely matches observed real-world measurements. For SWAT, we compare model-predicted daily river discharge against 10+ years of observed discharge from CWC gauging stations.",
        
        "The SUFI-2 algorithm calibrates SWAT by: (1) Defining reasonable ranges for 26 key parameters (e.g., soil saturated hydraulic conductivity ranges from 0.01 to 100 mm/hr); (2) Using Latin Hypercube Sampling to generate 500 parameter sets that efficiently explore the 26-dimensional parameter space; (3) Running SWAT 500 times, once with each parameter set; (4) Calculating objective functions (NSE, R-squared, PBIAS) for each run by comparing model output to observed data; (5) Identifying the best-performing parameter sets and narrowing parameter ranges; (6) Repeating steps 2-5 for 3-5 iterations until convergence (NSE > 0.7).",
        
        "Performance Criteria Explained: Nash-Sutcliffe Efficiency (NSE) - measures how much better our model is compared to simply using the average observed value. NSE > 0.5 is satisfactory, > 0.65 is good, > 0.75 is very good. R-squared - measures correlation between predicted and observed values (how well the patterns match). Target: > 0.7. PBIAS (Percent Bias) - measures whether the model systematically over-predicts or under-predicts. Target: within plus or minus 25%. All three criteria must be simultaneously met for the calibration to be considered successful.",
        
        "Model Validation: After calibration, we test the model on a DIFFERENT time period (one that was NOT used for calibration). This verifies that the model truly learned the watershed physics, not just memorized the calibration period patterns. If validation performance is similar to calibration performance, we have confidence the model will accurately predict future scenarios including NbS interventions.",
    ]
    for para in phase3b_paras:
        add_para(doc, para)
    
    # Phase 4
    add_heading_styled(doc, "Phase 4: NbS Scenario Testing (Months 16-22)", level=2)
    
    phase4_paras = [
        "What Are Scenarios? A scenario is a 'what-if' experiment we run in the computer model. We change specific parameters (like land use) and observe how the output (flood characteristics) changes. By testing multiple scenarios, we can identify which NbS interventions provide the greatest flood reduction benefit.",
        
        "Scenario A - Baseline (Current Conditions): We run the model with current land use (as of 2024) under design storms of different magnitudes (10, 25, 50, 100-year return periods). This gives us the 'reference point' against which all NbS scenarios are compared. Results include: peak discharge, flood extent, flood depth, flood duration, and time to peak for each return period.",
        
        "Scenario B - Riparian Buffer Restoration: We modify the SWAT model by changing HRUs within 50m and 100m of river channels from their current land use (often degraded scrub, agriculture, or bare soil) to 'riparian forest.' This means changing: Curve Number (reducing CN from 75-85 to 55-65), Manning's n (increasing from 0.03-0.05 to 0.10-0.15), and root depth/LAI parameters. We run the modified model under the same design storms and compare results to Baseline.",
        
        "Scenario C - Wetland Restoration: We identify former wetland areas (using historical satellite imagery and geomorphological analysis) and model them as functional wetlands. In SWAT, this means creating pond/wetland features that store water during high flows. In HEC-RAS, we add storage areas connected to the main channel. Parameters changed: storage volume (based on wetland area and depth), outlet characteristics, initial water level.",
        
        "Scenario D - Combined NbS (Riparian + Wetland + Reforestation + Check Structures): This is the comprehensive scenario combining all NbS interventions simultaneously. It represents the maximum achievable flood reduction through nature-based approaches. We implement all changes from Scenarios B and C plus: upper catchment reforestation (converting degraded land to forest with appropriate CN, LAI, and root depth), and check structures in first-order streams (modeled as small reservoirs with specified storage and outlet).",
        
        "What Parameters We Change in Each Scenario and What We Measure: For each scenario, we record: (1) Peak discharge reduction (%) compared to baseline; (2) Flood extent reduction (sq km); (3) Maximum flood depth change (meters); (4) Time to peak increase (hours) - this is important because more time = more warning time; (5) Total flood volume change; (6) Flood duration change. All measured for 10, 25, 50, and 100-year return periods under both current climate and future climate (RCP 4.5, RCP 8.5) conditions.",
    ]
    for para in phase4_paras:
        add_para(doc, para)
    
    # NbS Scenario Flowchart
    add_flowchart(doc, "NbS Scenario Comparison Workflow", [
        "+================================================================+",
        "|               NbS SCENARIO COMPARISON WORKFLOW                   |",
        "+================================================================+",
        "|                                                                  |",
        "|  SAME DESIGN STORMS (10, 25, 50, 100-yr) applied to ALL:       |",
        "|                                                                  |",
        "|  +-----------+  +-----------+  +-----------+  +-----------+     |",
        "|  | SCENARIO A|  | SCENARIO B|  | SCENARIO C|  | SCENARIO D|     |",
        "|  | Baseline  |  | Riparian  |  | Wetland   |  | Combined  |     |",
        "|  | (Current) |  | Buffers   |  | Restore   |  | All NbS   |     |",
        "|  +-----------+  +-----------+  +-----------+  +-----------+     |",
        "|       |              |              |              |             |",
        "|       v              v              v              v             |",
        "|   SWAT+HEC-RAS  SWAT+HEC-RAS  SWAT+HEC-RAS  SWAT+HEC-RAS     |",
        "|   simulation    simulation    simulation    simulation          |",
        "|       |              |              |              |             |",
        "|       v              v              v              v             |",
        "|  Peak: 1200     Peak: 980      Peak: 1050    Peak: 750         |",
        "|  cumecs         cumecs         cumecs        cumecs             |",
        "|  (reference)    (-18%)         (-12%)        (-37%)             |",
        "|                                                                  |",
        "|  COMPARISON TABLE:                                              |",
        "|  Metric          A       B        C        D                    |",
        "|  Peak reduction  --      18%      12%      37%                  |",
        "|  Extent reductn  --      22%      15%      42%                  |",
        "|  Time to peak    --      +2hr     +1hr     +4hr                 |",
        "|  BCR             --      3.2      2.8      4.1                  |",
        "+================================================================+",
    ])
    
    # Phase 5
    add_heading_styled(doc, "Phase 5: Economic Analysis (Months 22-26)", level=2)
    
    phase5_paras = [
        "Stage-Damage Curves Explained Simply: A stage-damage curve tells us how much economic damage occurs at each flood depth. For example: at 0.5m depth, damage to a typical residential house might be Rs. 50,000 (furniture ruined, walls damaged); at 1.0m depth, Rs. 2,00,000 (electrical systems destroyed, structural damage); at 2.0m depth, Rs. 8,00,000 (complete contents loss, major structural damage). We develop these curves from historical damage survey data and building vulnerability assessments specific to our study areas.",
        
        "Expected Annual Damage (EAD) Calculation: EAD combines flood probability with damage. A 10-year flood (10% annual probability) causing Rs. 100 crore damage contributes 10 crore to EAD. A 100-year flood (1% annual probability) causing Rs. 1000 crore damage contributes 10 crore. By integrating across all return periods, we get the total expected damage per year. This is calculated by: (1) Running HEC-RAS for multiple return periods to get flood depth maps; (2) Overlaying depth maps on asset maps (buildings, crops, infrastructure) in GIS; (3) Applying stage-damage curves to calculate damage for each return period; (4) Integrating the probability-damage curve to get EAD.",
        
        "Benefit Calculation: The benefit of NbS is the REDUCTION in EAD. If current EAD is Rs. 50 crore/year and after NbS implementation EAD drops to Rs. 25 crore/year, the annual benefit is Rs. 25 crore. Over a 50-year project life, total benefit (discounted at 3% rate) might be Rs. 700+ crore. We also calculate non-market benefits using Total Economic Value framework: carbon sequestration value (at Rs. 1000/tonne CO2), biodiversity value, water quality improvement value, recreation/tourism value.",
        
        "Benefit-Cost Ratio (BCR) Explained Simply: BCR = Total Benefits divided by Total Costs. Costs include: NbS implementation cost (land preparation, planting, construction), maintenance cost (first 5 years before self-sustaining), monitoring cost, opportunity cost of land. Benefits include: flood damage reduction (EAD reduction), ecosystem service values, carbon sequestration, employment generated, health benefits from reduced flood-related disease. If BCR > 1, the investment pays for itself. We expect BCR of 2.5 to 4.8, meaning every rupee invested returns 2.5 to 4.8 rupees in benefits.",
        
        "Sensitivity Analysis: We test how our results change when key assumptions vary. What if NbS performs 20% worse than modeled? What if climate change is more severe? What if maintenance costs are higher? This shows policymakers that our conclusions are ROBUST - even under pessimistic assumptions, NbS remains economically justified.",
    ]
    for para in phase5_paras:
        add_para(doc, para)
    
    # Phase 6
    add_heading_styled(doc, "Phase 6: Policy Integration and DDMP Development (Months 26-30)", level=2)
    
    phase6_paras = [
        "What is a DDMP? The District Disaster Management Plan is a mandatory document under the Disaster Management Act 2005 that every district in India must prepare and update. It contains: hazard profile, vulnerability assessment, capacity analysis, risk reduction strategy, preparedness plan, response plan, and resource directory. Currently, most DDMPs lack specific, scientifically-backed NbS recommendations because the evidence base did not exist. Our research creates that evidence base.",
        
        "How Our Research Becomes Government Policy: We create modular 'NbS Chapters' ready for insertion into existing DDMP frameworks. Each chapter contains: (1) Scientific justification with local evidence (maps, numbers, statistics from our research specific to that district); (2) Prioritized list of NbS interventions ranked by BCR; (3) Implementation roadmap with clear timelines, responsible agencies, and budget estimates; (4) Maps showing exact locations for each intervention at village level; (5) Monitoring indicators and protocols; (6) Convergence opportunities with existing schemes (MGNREGA, PMKSY, AMRUT, CAMPA funds).",
        
        "Stakeholder Validation Process: We present our findings and DDMP modules to: (1) District officials (DM, SDM, BDOs) for administrative feasibility; (2) Technical experts (irrigation department, forest department) for implementation feasibility; (3) Community representatives (Gram Pradhans, Van Panchayat heads) for social acceptance; (4) Academic peers for scientific rigor. Feedback is incorporated iteratively until all stakeholders validate the final products.",
        
        "Knowledge Products Delivered: Beyond academic publications (3-4 journal papers in high-impact journals), we deliver practical products: DDMP modules (ready to adopt), policy briefs (2-page summaries for decision-makers), community awareness materials (in local language), training materials for field staff, and a web-based decision support tool where officials can explore maps and scenarios interactively.",
    ]
    for para in phase6_paras:
        add_para(doc, para)
    
    doc.add_page_break()



def add_study_areas(doc):
    add_heading_styled(doc, "8. STUDY AREAS - Detailed Profile", level=1)
    add_para(doc, "In Simple Terms: We study two very different locations to prove our framework works across India.", bold=True, italic=True, font_size=11)
    
    add_heading_styled(doc, "Site 1: Raipur Watershed, Dehradun, Uttarakhand", level=2)
    add_para(doc, "Location and Geography: The Raipur watershed is located in Dehradun district, Uttarakhand, in the Doon Valley between the Mussoorie Hills (Lesser Himalaya) to the north and the Siwalik Hills to the south. The watershed drains into the Song River, a tributary of the Ganga. Total watershed area is approximately 35-50 sq km with elevation ranging from 550m to 2200m above sea level. The terrain is characterized by steep slopes in the upper catchment (20-45 degrees), moderate slopes in the middle zone (5-20 degrees), and relatively flat areas in the lower Doon Valley floor (0-5 degrees).")
    add_para(doc, "Why Chosen: (1) Representative of Himalayan foothill flash flood dynamics affecting millions across the Himalayan belt; (2) Rapid urbanization of Dehradun is converting forest and agricultural land to impervious surfaces, increasing runoff; (3) Documented increase in flash flood frequency and intensity over the past two decades; (4) Presence of both forest (Van Panchayat managed) and degraded areas offering natural experimental contrast; (5) Availability of meteorological and hydrological data from IMD and state agencies; (6) Proximity to the researcher institution enabling frequent field visits; (7) Active community institutions (Van Panchayats) that could implement NbS recommendations.")
    add_para(doc, "Key Characteristics: The area receives 1,800-2,200 mm annual rainfall, concentrated in June-September monsoon (85% of annual rainfall in 4 months). Soil types include red loam in upper areas and alluvial deposits in valley floor. Forest cover has declined from 65% (1990) to approximately 45% (2024) due to urbanization and encroachment. Flash floods typically last 4-12 hours with very rapid rise (30-60 minutes from normal to peak). Primary flood hazard: sudden high-velocity flows carrying debris from steep, deforested slopes.")
    
    add_heading_styled(doc, "Site 2: Darbhanga District, Bihar", level=2)
    add_para(doc, "Location and Geography: Darbhanga district is located in the Mithilanchal region of north Bihar, bounded by the Kamla-Balan River to the east and influenced by the Kosi-Bagmati river system. The terrain is entirely flat alluvial plain with elevation ranging from only 45m to 55m above sea level (total relief of just 10 meters across the entire district). The extremely low gradient means water flows very slowly and spreads extensively during floods. District area is approximately 2,279 sq km.")
    add_para(doc, "Why Chosen: (1) One of India most chronically flood-affected districts with flooding occurring in 8 out of 10 years; (2) Representative of vast Gangetic plain flooding affecting over 100 million people annually across Bihar, UP, West Bengal, and Assam; (3) Extensive historical flood data available from CWC and state disaster management authority; (4) Presence of traditional water management systems (ahar-pyne irrigation) that represent indigenous NbS knowledge; (5) Clear failure of grey infrastructure with embankments; (6) Large wetland areas (chaurs) that have been gradually encroached but could be restored; (7) Strong MGNREGA implementation providing labor force for NbS activities.")
    add_para(doc, "Key Characteristics: Annual rainfall 1,200-1,400 mm, concentrated in monsoon. Alluvial soil (sandy loam to clay) with generally poor drainage. Extremely flat terrain means even 1-2m of water depth can inundate thousands of hectares. Flood duration is long: 15-45 days of continuous inundation. Primary hazard: extensive inundation from river overflow, waterlogging, and embankment breaches.")
    
    add_para(doc, "Comparison of Study Sites (20 Parameters):", bold=True)
    headers = ["Parameter", "Raipur-Dehradun (Uttarakhand)", "Darbhanga (Bihar)"]
    rows = [
        ("Physiography", "Himalayan foothills, steep terrain", "Gangetic alluvial plain, flat"),
        ("Elevation Range", "550 - 2200 m", "45 - 55 m"),
        ("Average Slope", "15-25 degrees (upper), 2-5 (lower)", "0.1 - 0.5 degrees"),
        ("Area", "35-50 sq km (watershed)", "2,279 sq km (district)"),
        ("Annual Rainfall", "1,800 - 2,200 mm", "1,200 - 1,400 mm"),
        ("Flood Type", "Flash floods (rapid onset, short)", "Riverine flooding (slow onset, long)"),
        ("Flood Duration", "4 - 12 hours", "15 - 45 days"),
        ("Primary Rivers", "Song River tributaries", "Kamla-Balan, Kosi influence"),
        ("Soil Type", "Red loam, alluvial (valley)", "Alluvial clay-loam, sandy loam"),
        ("Land Use Trend", "Forest to urban conversion", "Wetland to agriculture conversion"),
        ("Population Density", "Moderate-High (urban fringe)", "High (>1200/sq km rural)"),
        ("Poverty Level", "Moderate (15-20% BPL)", "High (35-40% BPL)"),
        ("Grey Infrastructure", "Limited embankments, check dams", "Extensive embankment network (1000+ km)"),
        ("NbS Potential", "Reforestation, riparian buffers", "Wetland restoration, floodplain reconnection"),
        ("Community Institutions", "Van Panchayats (forest councils)", "MGNREGA committees, Panchayati Raj"),
        ("Data Availability", "Good (IMD, state agencies)", "Good (CWC, WRD Bihar, long records)"),
        ("Key Challenge", "Rapid urbanization", "Embankments preventing natural flow"),
        ("Climate Risk", "Increasing extreme rainfall", "River discharge changes, monsoon shift"),
        ("Economic Activities", "Tourism, horticulture, urban", "Rice-wheat farming, fisheries"),
        ("Disaster History", "2010, 2013 flash floods", "Annual flooding, 2007, 2008, 2017 major"),
    ]
    add_table(doc, headers, rows)
    doc.add_page_break()



def add_timeline(doc):
    add_heading_styled(doc, "9. AI + GIS INTEGRATION TIMELINE", level=1)
    add_para(doc, "In Simple Terms: This table shows exactly WHEN during the 30-month research period AI and GIS tools are used, what they do in each month, and what outputs are produced.", bold=True, italic=True, font_size=11)
    
    headers = ["Month", "Primary Activity", "AI Component", "GIS Component", "Output Produced"]
    rows = [
        ("1-2", "Literature review + Data acquisition", "Setting up Python ML environment", "DEM download and preprocessing", "Complete data repository"),
        ("2-3", "Terrain analysis + Watershed delineation", "None (preprocessing)", "Slope, aspect, flow direction, TWI, HAND extraction", "Terrain derivative maps"),
        ("3-4", "Satellite image processing", "Random Forest classification in GEE", "Land use maps integration, change detection", "LULC maps for 5 periods"),
        ("4-5", "Field data collection", "GPS data processing for ML validation", "Field survey data into GIS database", "Ground truth dataset"),
        ("5-6", "AHP expert survey", "Eigenvalue optimization, CR computation", "Layer normalization (18 factors)", "AHP weight vector CR<0.10"),
        ("6-8", "FVI mapping", "AI classification for LULC input", "Weighted overlay, reclassification", "FVI maps for both sites"),
        ("8-10", "SWAT model setup", "SUFI-2 preparation", "Watershed subdivision, HRU definition", "SWAT model ready"),
        ("10-12", "SWAT calibration", "SUFI-2: 2500-5000 simulations", "Output visualization", "Calibrated SWAT (NSE>0.7)"),
        ("12-14", "HEC-RAS setup + SAR mapping", "ML flood extent from Sentinel-1", "River geometry, 2D mesh creation", "HEC-RAS + validation maps"),
        ("14-16", "HEC-RAS calibration", "CSI calculation", "Flood inundation maps", "Validated flood maps CSI>0.65"),
        ("16-18", "NbS site identification", "Suitability scoring with ML", "Multi-criteria suitability analysis", "NbS suitability maps"),
        ("18-20", "NbS Scenario B+C", "Parameter optimization", "Modified LULC layers", "Flood reduction results"),
        ("20-22", "Scenario D + climate", "Non-stationary frequency analysis", "Climate-adjusted flood maps", "Complete scenario comparison"),
        ("22-24", "Economic analysis", "ML-based damage estimation", "Spatial damage mapping, EAD", "BCR calculations"),
        ("24-26", "Sensitivity analysis", "Monte Carlo simulation", "Sensitivity maps", "Robust BCR ranges"),
        ("26-28", "DDMP module preparation", "None (policy writing)", "Cartographic production", "DDMP draft modules"),
        ("28-30", "Stakeholder validation", "Web decision support tool", "Interactive web maps", "Final products delivered"),
    ]
    add_table(doc, headers, rows)
    doc.add_page_break()



def add_expected_results(doc):
    add_heading_styled(doc, "10. EXPECTED RESULTS", level=1)
    add_para(doc, "In Simple Terms: Based on literature and preliminary analysis, here is what we expect to find.", bold=True, italic=True, font_size=11)
    
    add_para(doc, "Quantitative Results Expected from Hydrological Modeling:", bold=True)
    add_para(doc, "Peak Discharge Reduction: Scenario B (Riparian buffers alone): 15-22% reduction in peak flood discharge for 25-year return period. Scenario C (Wetland restoration alone): 10-18% reduction. Scenario D (Combined NbS): 30-45% reduction. These estimates are based on published literature from similar studies worldwide, adjusted for local conditions.")
    add_para(doc, "Flood Extent Reduction: Under Scenario D (Combined NbS), we expect flood inundation area to decrease by 25-40% for the 25-year flood in both study areas. This translates to thousands of hectares of land and thousands of households removed from the flood zone.")
    add_para(doc, "Time to Peak Increase: NbS interventions are expected to delay flood peak arrival by 2-6 hours depending on watershed size and NbS extent. This additional warning time is critically valuable for evacuation and emergency response.")
    add_para(doc, "Economic Results Expected:", bold=True)
    add_para(doc, "Benefit-Cost Ratios: We expect BCR ranging from 2.5 (for individual interventions in small areas) to 4.8 (for combined NbS at watershed scale over 50-year analysis period). These BCR values make NbS highly competitive with grey infrastructure alternatives that typically show BCR of 1.2-2.0 for embankments.")
    add_para(doc, "EAD Reduction: Expected reduction in Expected Annual Damage of 40-60% under combined NbS scenario. For Darbhanga district (with current EAD estimated at Rs. 500-800 crore/year), this could mean Rs. 200-480 crore annual savings.")
    add_para(doc, "Maps and Spatial Products:", bold=True)
    add_para(doc, "(1) Flood Vulnerability Index maps at 30m resolution for both sites; (2) Flood inundation maps for 4 return periods x 4 scenarios x 2 climate conditions = 32 unique flood maps per site; (3) NbS suitability maps showing optimal intervention locations; (4) Risk reduction maps showing how vulnerability changes under NbS scenarios; (5) DDMP-ready maps at appropriate administrative scales.")
    add_para(doc, "Policy Documents: (1) NbS-integrated DDMP modules for Dehradun and Darbhanga districts; (2) Policy brief for NDMA/SDMA on NbS for flood management; (3) Implementation guidelines for district-level NbS programs; (4) Monitoring protocol for NbS effectiveness assessment; (5) Replication guide for other districts to adapt the framework.")
    add_para(doc, "Academic Outputs: (1) 3-4 peer-reviewed journal papers in Natural Hazards, IJDRR, Journal of Hydrology, Environmental Science and Policy; (2) Conference presentations at national and international venues; (3) PhD dissertation; (4) Open-access data repository with all GIS layers and model files for replication.")
    doc.add_page_break()


def add_how_helps_india(doc):
    add_heading_styled(doc, "11. HOW THIS HELPS INDIA", level=1)
    add_para(doc, "In Simple Terms: This research is not just academic exercise - it produces practical tools and evidence that can save lives, protect livelihoods, and save government money.", bold=True, italic=True, font_size=11)
    
    add_para(doc, "For Flood-Affected Communities (Direct Beneficiaries): Our research provides scientific evidence that can redirect government investment toward NbS programs that directly protect communities. When implemented, NbS reduces flood depth and extent in vulnerable areas, potentially removing thousands of households from flood zones entirely. The time-to-peak increase from NbS gives communities 2-6 additional hours for evacuation. The IoT-based monitoring system concept provides real-time flood alerts. Most importantly, NbS implementation through MGNREGA creates local employment - communities get paid to protect themselves. Estimated direct beneficiary population: 50,000+ people in immediate study areas; millions when replicated across flood-prone districts.")
    add_para(doc, "For Government Agencies and Decision-Makers: District Collectors and DDMA chairpersons receive ready-to-implement DDMP modules requiring no additional technical expertise or consultant hiring. The BCR analysis provides the financial justification needed to allocate budget for NbS programs. Our maps and prioritization help target limited resources to locations with maximum impact. The framework can be integrated with existing schemes (MGNREGA, PMKSY, Namami Gange, CAMPA) for convergent funding. State and national authorities (SDMA, NDMA) get a replicable framework for 500+ flood-prone districts.")
    add_para(doc, "Economic Benefits to the Nation: Every Rs. 1 invested in flood prevention saves Rs. 7-10 in post-disaster relief and reconstruction. Our research provides the scientific basis for this preventive investment. If the combined NbS scenario reduces EAD by even 30% across India flood-prone areas, the national savings would be Rs. 15,000-25,000 crores annually. Additional economic benefits include: carbon sequestration value (contributing to India climate commitments), agricultural productivity improvement in formerly flood-damaged areas, reduced health costs from waterborne diseases, reduced infrastructure repair costs, and increased property values in risk-reduced areas.")
    add_para(doc, "Replication Potential: The AI-GIS framework developed in this research is designed to be replicable with minimal modification across any flood-prone district in India. The methodology uses freely available data (satellite imagery, global DEM) and open-source software (QGIS, Python, Google Earth Engine), meaning any university or government agency can apply it without expensive licenses. We will provide: (1) Step-by-step replication manual; (2) Open-source code repository; (3) Template GIS project files; (4) Training materials. Target: framework adopted by 10+ districts within 5 years of publication.")
    add_para(doc, "Alignment with National and International Frameworks: This research directly contributes to India commitments under the Sendai Framework for DRR, Paris Agreement (ecosystem-based adaptation), Sustainable Development Goals (SDG 11, SDG 13, SDG 15), National Action Plan on Climate Change (National Water Mission), and India Nationally Determined Contributions (NDCs) for climate adaptation. This multi-framework alignment maximizes policy relevance and funding opportunities.")
    doc.add_page_break()



def add_references(doc):
    add_heading_styled(doc, "12. REFERENCES", level=1)
    refs = [
        "1. IPCC (2021). Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press.",
        "2. IUCN (2020). Global Standard for Nature-Based Solutions. First Edition. IUCN, Gland, Switzerland.",
        "3. Debele, S.E., Kumar, P., Sahani, J. et al. (2019). Nature-based solutions for hydro-meteorological hazards. Environmental Research, 179, 108799.",
        "4. Neitsch, S.L., Arnold, J.G., Kiniry, J.R., Williams, J.R. (2011). SWAT Theoretical Documentation Version 2009. Texas Water Resources Institute.",
        "5. Brunner, G.W. (2020). HEC-RAS River Analysis System: Hydraulic Reference Manual. US Army Corps of Engineers.",
        "6. Saaty, T.L. (1980). The Analytic Hierarchy Process. McGraw-Hill, New York.",
        "7. Abbaspour, K.C. (2015). SWAT-CUP: SWAT Calibration and Uncertainty Programs. Eawag: Swiss Federal Institute.",
        "8. NDMA (2019). National Disaster Management Guidelines: Flood Risk Management. Government of India.",
        "9. CWC (2021). National Register of Large Dams. Central Water Commission, Ministry of Jal Shakti.",
        "10. Costanza, R. et al. (2014). Changes in the global value of ecosystem services. Global Environmental Change, 26, 152-158.",
        "11. Teng, J. et al. (2017). Flood inundation modelling: A review. Environmental Modelling and Software, 90, 201-216.",
        "12. Jha, A.K., Bloch, R., Lamond, J. (2012). Cities and Flooding. World Bank.",
        "13. MoEFCC (2019). India National Action Plan on Climate Change. Government of India.",
        "14. Mishra, V. et al. (2018). The Kerala flood of 2018. Hydrology and Earth System Sciences Discussions.",
        "15. Rawat, P.K. et al. (2011). Modelling of stream run-off for erosion hazard in Lesser Himalaya. J. Earth System Science, 120(1).",
        "16. Sanyal, J., Lu, X.X. (2004). Remote sensing in flood management. Natural Hazards, 33, 283-301.",
        "17. Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.",
        "18. Nash, J.E., Sutcliffe, J.V. (1970). River flow forecasting. Journal of Hydrology, 10(3), 282-290.",
        "19. UNDRR (2015). Sendai Framework for Disaster Risk Reduction 2015-2030.",
        "20. Disaster Management Act (2005). Parliament of India.",
        "21. Samela, C. et al. (2017). Geomorphic classifiers for flood-prone areas. Advances in Water Resources, 110.",
        "22. Wohl, E. et al. (2005). River restoration. Water Resources Research, 41(10).",
        "23. Kousky, C. (2010). Using natural capital to reduce disaster risk. J. Natural Resources Policy Research, 2(4).",
        "24. Green, C. et al. (2011). Guidance for assessing flood losses. CONHAZ Report.",
        "25. Merz, B. et al. (2010). Assessment of economic flood damage. NHESS, 10(8), 1697-1724.",
        "26. Opperman, J.J. et al. (2009). Sustainable floodplains through reconnection. Science, 326(5959).",
        "27. Palmer, M.A. et al. (2015). Manage water in a green way. Science, 349(6248), 584-585.",
        "28. Acreman, M., Holden, J. (2013). How wetlands affect floods. Wetlands, 33(5), 773-786.",
        "29. Dadson, S.J. et al. (2017). Natural flood management in the UK. Proceedings of the Royal Society A, 473.",
        "30. Kumar, P. et al. (2020). Towards operationalisation of NbS for natural hazards. Science of The Total Environment, 731.",
        "31. Vorogushyn, S. et al. (2010). Flood hazard assessment considering dike breaches. Water Resources Research, 46(8).",
        "32. Thieken, A.H. et al. (2005). Flood damage and influencing factors. Water Resources Research, 41(12).",
        "33. Ray, P.A., Brown, C.M. (2015). Confronting Climate Uncertainty in Water Resources Planning. World Bank.",
        "34. Cohen-Shacham, E. et al. (2016). Nature-Based Solutions to address global societal challenges. IUCN, Gland.",
        "35. Schanze, J. (2006). Flood risk management - a basic framework. Flood Risk Management, 1-20.",
    ]
    for ref in refs:
        add_para(doc, ref, font_size=10)
    doc.add_page_break()


def add_appendix(doc):
    add_heading_styled(doc, "13. APPENDIX: SOFTWARE AND TOOLS NEEDED", level=1)
    add_para(doc, "Complete list of software tools needed for this research:", bold=True)
    
    headers = ["Software/Tool", "Purpose in Research", "Cost", "Platform"]
    rows = [
        ("QGIS 3.x", "Primary GIS: mapping, spatial analysis, visualization", "FREE (Open Source)", "All platforms"),
        ("GRASS GIS 8.x", "Advanced raster hydrology: watershed, flow routing", "FREE (Open Source)", "All platforms"),
        ("Google Earth Engine", "Cloud satellite processing, ML classification", "FREE (for research)", "Web browser"),
        ("HEC-RAS 6.x", "River hydraulic modeling, flood inundation", "FREE (US Army Corps)", "Windows"),
        ("SWAT / QSWAT", "Watershed hydrological modeling, runoff simulation", "FREE (USDA-ARS)", "Windows/Linux"),
        ("SWAT-CUP (SUFI-2)", "Model calibration, uncertainty analysis", "FREE (Eawag)", "Windows"),
        ("Python 3.x + Libraries", "AI/ML, data processing, automation", "FREE (Open Source)", "All platforms"),
        ("scikit-learn", "Random Forest, SVM, clustering", "FREE (Open Source)", "Python library"),
        ("R Statistical Software", "Non-stationary frequency analysis, Bayesian", "FREE (Open Source)", "All platforms"),
        ("PostGIS + PostgreSQL", "Spatial database for large datasets", "FREE (Open Source)", "All platforms"),
        ("WhiteboxTools", "Advanced geomorphometric and DEM analysis", "FREE (Open Source)", "All platforms"),
        ("SAGA GIS", "Terrain analysis, climate interpolation", "FREE (Open Source)", "All platforms"),
        ("Jupyter Notebooks", "Interactive coding environment", "FREE (Open Source)", "All platforms"),
        ("Google Earth Pro", "Historical imagery, visual verification", "FREE", "Windows/Mac"),
        ("RStudio IDE", "IDE for R statistical programming", "FREE (Open Source)", "All platforms"),
        ("LibreOffice", "Report writing, DDMP document preparation", "FREE (Open Source)", "All platforms"),
    ]
    add_table(doc, headers, rows)
    
    add_para(doc, "Total Software Cost: Rs. 0 (all computational software is free and open-source). Hardware: Standard laptop with 16 GB RAM, 500 GB storage, internet connection. This makes the methodology highly accessible and replicable by any institution.", bold=True)
    add_para(doc, "")
    add_para(doc, "--- END OF RESEARCH REPORT ---", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "Prepared by: Raj Amritam, PhD Research Scholar", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "Supervisor: Dr. Nidhi Rawat, Assistant Professor", alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, "Department of Environmental Science, DBS Global University, Dehradun", alignment=WD_ALIGN_PARAGRAPH.CENTER)



if __name__ == "__main__":
    doc = create_document()
    # Will add sections in section functions
    add_executive_overview(doc)
    add_glossary(doc)
    add_problem_section(doc)
    add_solution_section(doc)
    add_ai_integration(doc)
    add_gis_integration(doc)
    add_methodology(doc)
    add_study_areas(doc)
    add_timeline(doc)
    add_expected_results(doc)
    add_how_helps_india(doc)
    add_references(doc)
    add_appendix(doc)

    output_path = "/projects/sandbox/mobile-printer-app/Research_Report_NbS_Flood_Mitigation_Raj_Amritam.docx"
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
