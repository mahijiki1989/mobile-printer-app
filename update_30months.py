#!/usr/bin/env python3
"""Patch both Advanced docs to 30-month fast-track timeline"""
from docx import Document
from docx.shared import Pt, Inches
import os

print("=" * 60)
print("PATCHING PhD DISSERTATION PROPOSAL -> 30 MONTHS")
print("=" * 60)
phd_path = '/projects/sandbox/mobile-printer-app/PhD_Dissertation_Proposal_Advanced_Raj_Amritam.docx'
doc = Document(phd_path)

def replace_para_text(para, new_text, courier=False):
    for run in para.runs:
        run.text = ''
    if para.runs:
        run = para.runs[0]
    else:
        run = para.add_run('')
    run.text = new_text
    if courier:
        run.font.name = 'Courier New'
        run.font.size = Pt(8)
    else:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

new_phd_gantt = """ACTIVITY                      Y1Q1 Y1Q2 Y1Q3 Y1Q4 Y2Q1 Y2Q2 Y2Q3 Y2Q4 Y3Q1 Y3Q2
=====================================================================================
 [30-MONTH FAST-TRACK PHD PIPELINE]

1. Literature Review         ###  ###
2. Field Reconnaissance      ###  ###
3. Data Acquisition          ###  ###  ###
4. Field Ground-truthing          ###  ###  ###
5. AHP Expert Panel               ###  ###
6. FVI Development                     ###  ###
7. FVI Validation                           ###
8. SWAT Setup                          ###  ###  ###
9. SWAT Calibration (SUFI-2)                     ###  ###
10. SWAT Validation                                   ###
11. HEC-RAS 2D Setup                             ###  ###
12. HEC-RAS Calibration                               ###  ###
13. NbS Scenarios A,B,C                               ###  ###  ###
14. NbS Scenario D + Sensitivity                           ###  ###
15. Economic Valuation                                          ###  ###
16. Stakeholder Workshops                                            ###  ###
17. DDMP Annexure Templates                                          ###
18. Paper 1 (Review)              ...  ###  ###  *Submit P1 (M9)
19. Paper 2 (FVI)                                ...  ###  ###  *Submit P2 (M15)
20. Paper 3 (SWAT/HEC-RAS)                                 ...  ###  *Submit P3 (M22)
21. Paper 4 (Economic)                                          ...  *Submit P4 (M27)
22. Dissertation Writing                                                  ###  ###
23. Pre-submission Seminar                                                     ###
24. Final Submission                                                              *(M30)

  Legend: ### = Active execution    ... = Continuous/Background    * = Milestone
  TOTAL DURATION: 30 MONTHS (Accelerated Fast-Track)"""

phd_gantt_replaced = False
for i, para in enumerate(doc.paragraphs):
    if 'Y1Q1 Y1Q2 Y1Q3 Y1Q4' in para.text and 'ACTIVITY' in para.text:
        replace_para_text(para, new_phd_gantt, courier=True)
        phd_gantt_replaced = True
        print(f"  PhD Gantt chart replaced (paragraph {i})")
        break

phd_milestones_new = [
    ['Y1Q1','M1-3','Literature review + Field plan + Initial data','200+ refs annotated'],
    ['Y1Q2','M4-6','AHP panel convened + FVI weights derived','CR < 0.10 achieved'],
    ['Y1Q3','M7-9','FVI maps validated + Paper 1 submitted','Submission ID + AUC>0.75'],
    ['Y1Q4','M10-12','SWAT setup + initial calibration','Working models both sites'],
    ['Y2Q1','M13-15','SWAT calibration complete + Paper 2 submitted','NSE>0.6 + submission'],
    ['Y2Q2','M16-18','HEC-RAS 2D setup + Scenarios A, B, C','Validated flood maps'],
    ['Y2Q3','M19-21','Scenario D + Sensitivity analysis','BCR & uncertainty quantified'],
    ['Y2Q4','M22-24','Economic valuation + Paper 3 submitted','TEV + submission'],
    ['Y3Q1','M25-27','DDMP templates + Paper 4 submitted + Workshops','Templates adopted'],
    ['Y3Q2','M28-30','Dissertation submission + Defense','Final submission'],
]
for table in doc.tables:
    if len(table.rows) >= 1:
        hdr = ' '.join([c.text.strip() for c in table.rows[0].cells])
        if 'Quarter' in hdr and 'Key Deliverable' in hdr and 'Months' in hdr:
            for ri, new_row in enumerate(phd_milestones_new, 1):
                if ri < len(table.rows):
                    for ci, val in enumerate(new_row):
                        if ci < len(table.rows[ri].cells):
                            cell = table.rows[ri].cells[ci]
                            cell.text = val
                            for p in cell.paragraphs:
                                for r in p.runs:
                                    r.font.size = Pt(10)
            rows_to_remove = list(table.rows[11:])
            for row in rows_to_remove:
                row._element.getparent().remove(row._element)
            print(f"  PhD Quarterly Milestones updated (10 quarters)")
            break

new_paper_months = {'Paper 1':'Month 9','Paper 2':'Month 15','Paper 3':'Month 22','Paper 4':'Month 27'}
for table in doc.tables:
    if len(table.rows) >= 1:
        hdr = ' '.join([c.text.strip() for c in table.rows[0].cells])
        if 'Paper' in hdr and 'Target Journal' in hdr and 'Submission' in hdr:
            for row in table.rows[1:]:
                paper_label = row.cells[0].text.strip()
                if paper_label in new_paper_months and len(row.cells) >= 6:
                    cell = row.cells[5]
                    cell.text = new_paper_months[paper_label]
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(10)
            print(f"  PhD Publication submission months updated")
            break

doc.save(phd_path)
print(f"  PhD doc saved: {os.path.getsize(phd_path):,} bytes\n")

print("=" * 60)
print("PATCHING GRANT PROJECT PROPOSAL -> 30 MONTHS")
print("=" * 60)
grant_path = '/projects/sandbox/mobile-printer-app/Grant_Project_Proposal_Advanced_Raj_Amritam.docx'
doc = Document(grant_path)

text_replacements = {
    '36 Months (3-Year Fast-Track Strategy)': '30 Months (2.5-Year Fast-Track Strategy)',
    '36 Months': '30 Months',
    '3-Year Fast-Track': '2.5-Year Fast-Track',
    '36-month execution window': '30-month execution window',
    'over 36 months': 'over 30 months',
    'within a 36-month': 'within a 30-month',
    'within a single 36-month': 'within a single 30-month',
    '36-month project': '30-month project',
}

para_changes = 0
for para in doc.paragraphs:
    full_text = para.text
    for old, new in text_replacements.items():
        if old in full_text:
            for run in para.runs:
                if old in run.text:
                    run.text = run.text.replace(old, new)
                    para_changes += 1

table_changes = 0
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for old, new in text_replacements.items():
                    if old in para.text:
                        for run in para.runs:
                            if old in run.text:
                                run.text = run.text.replace(old, new)
                                table_changes += 1

print(f"  Text replacements: {para_changes} in paragraphs, {table_changes} in tables")

new_grant_gantt = """TASK / ACTIVITY               Y1Q1 Y1Q2 Y1Q3 Y1Q4 Y2Q1 Y2Q2 Y2Q3 Y2Q4 Y3Q1 Y3Q2
=====================================================================================
 [30-MONTH FAST-TRACK PROJECT IMPLEMENTATION]

A. PROJECT INCEPTION
  A1. Site selection         ###
  A2. SDMA MoU               ###
  A3. Inception workshop     ###

B. TASK 1: FVI ATLAS
  B1. Data acquisition       ###  ###
  B2. AHP expert panel            ###  ###
  B3. FVI computation                  ###  ###
  B4. Validation                            ###
  B5. Web portal launch                          ###

C. TASK 2: NbS PILOT
  C1. Site MoU+VanPanchayat       ###
  C2. MGNREGA mobilization              ###
  C3. Plant nursery raising             ###  ###
  C4. Civil works (bunding)                  ###  ###
  C5. Plantation                                  ###
  C6. Monitoring (continuous)                     ###  ###  ###  ###  ###

D. TASK 3: IoT EWS
  D1. Equipment procurement        ###
  D2. Sensor installation               ###
  D3. Server+threshold setup                 ###
  D4. Community sensitization                ###  ###
  D5. Drill 1 (May 2026)                            ###
  D6. Drill 2 (Aug 2026)                                 ###
  D7. Drill 3 (May 2027)                                            ###

E. SHG TASK FORCE
  E1. Identification + training              ###  ###
  E2. Refresher training                                    ###

F. DDMP INTEGRATION
  F1. Annexure drafting                                ###  ###
  F2. Stakeholder workshops                                 ###  ###
  F3. Administrative order pursuit                                    ###

G. M&E
  G1. Quarterly progress reviews ...  ...  ...  ...  ...  ...  ...  ...  ...  ...
  G2. Mid-term evaluation                                  *(M15)
  G3. End-term evaluation                                                   *(M30)

H. PUBLICATIONS
  H1. Paper 1 (Review)           ###  ###  *Submit M9
  H2. Paper 2 (FVI)                          ...  ###  *Submit M15
  H3. Paper 3 (Hydrology)                                  ...  *Submit M22
  H4. Paper 4 (Economics)                                            *Submit M27

  Legend: ### Active   ... Background   * Milestone
  TOTAL DURATION: 30 MONTHS (Accelerated Fast-Track)"""

for para in doc.paragraphs:
    if 'TASK / ACTIVITY' in para.text and 'Y1Q1' in para.text:
        replace_para_text(para, new_grant_gantt, courier=True)
        print(f"  Grant Gantt chart replaced")
        break

for table in doc.tables:
    if len(table.rows) >= 1:
        hdr = ' '.join([c.text.strip() for c in table.rows[0].cells])
        if 'Year 1' in hdr and 'Year 2' in hdr and 'Year 3' in hdr and 'Justification' in hdr:
            new_budget = [
                ['A','CAPITAL & ANALYTICAL EQUIPMENT','4,50,000','4,50,000','-','-','Front-loaded'],
                ['A1','IoT River-Level Sensors (3 x 75K)','2,25,000','2,25,000','-','-','One-time'],
                ['A2','Micro-Automatic Weather Station','1,25,000','1,25,000','-','-','Single AWS'],
                ['A3','GIS Workstation (64GB RAM, RTX GPU)','1,00,000','1,00,000','-','-','Hydro modeling'],
                ['B','OPERATIONAL & MATERIAL ASSETS','8,50,000','2,50,000','5,00,000','1,00,000','Year 2 heavy'],
                ['B1','Vegetative/Bamboo materials','2,50,000','-','2,50,000','-','NbS Year 2'],
                ['B2','Community workshops & SHG training','1,50,000','60,000','60,000','30,000','Continuous'],
                ['B3','API server + IVR (30 months)','1,80,000','72,000','72,000','36,000','Ongoing'],
                ['B4','Satellite processing credits','70,000','40,000','30,000','-','GEE/AWS'],
                ['B5','Field instrumentation','1,00,000','60,000','40,000','-','Infiltrometers'],
                ['B6','Civil works & tools','1,00,000','18,000','48,000','34,000','Structures'],
                ['C','MANPOWER & FELLOWSHIP','13,00,000','5,16,000','5,16,000','2,68,000','Largest (30mo)'],
                ['C1','JRF/SRF Fellowship (Rs.35K x 30mo)','10,50,000','4,20,000','4,20,000','2,10,000','Full-time scholar'],
                ['C2','Field Surveyors (seasonal)','40,000','12,000','12,000','16,000','Monsoon'],
                ['D','TRAVEL & CONTINGENCY','2,50,000','1,00,000','1,00,000','50,000','Distributed'],
                ['D1','In-state field travel','1,20,000','48,000','48,000','24,000','Site visits'],
                ['D2','Conference participation','80,000','-','40,000','40,000','Y2-Y3'],
                ['D3','Overheads + 10% contingency','50,000','17,000','17,000','16,000','Buffer'],
                ['','GRAND TOTAL','28,50,000','13,16,000','11,16,000','4,18,000','Target'],
            ]
            num_rows = len(table.rows)
            for ri, new_row in enumerate(new_budget, 1):
                if ri < num_rows:
                    for ci, val in enumerate(new_row):
                        if ci < len(table.rows[ri].cells):
                            cell = table.rows[ri].cells[ci]
                            cell.text = val
                            for p in cell.paragraphs:
                                for r in p.runs:
                                    r.font.size = Pt(10)
            print(f"  Grant budget updated for 30-month timeline")
            break

for table in doc.tables:
    if len(table.rows) >= 1:
        hdr = ' '.join([c.text.strip() for c in table.rows[0].cells])
        if 'Activity' in hdr and 'Months' in hdr and 'Deliverable' in hdr:
            for row in table.rows[1:]:
                if 'Paper 2' in row.cells[0].text:
                    row.cells[1].text = 'M15'
                    for p in row.cells[1].paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(10)
                    print(f"  Paper 2 submission updated to M15")
                    break
            break

doc.save(grant_path)
print(f"  Grant doc saved: {os.path.getsize(grant_path):,} bytes\n")

print("=" * 60)
print("FINAL WORD COUNTS")
print("=" * 60)
for fname, label in [(phd_path, 'PhD Advanced (30-month)'), (grant_path, 'Grant Advanced (30-month)')]:
    d = Document(fname)
    text = ' '.join([p.text for p in d.paragraphs])
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                text += ' ' + c.text
    print(f"  {label}: {len(text.split())} words")
