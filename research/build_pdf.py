"""Render the research brief Markdown into a clean, multi-page PDF.

Uses reportlab only (no system dependencies). Handles:
  - Headings (H1-H4)
  - Paragraphs with bold/italic inline
  - Bulleted and numbered lists
  - Horizontal rules (--- => page break / section divider)
  - GitHub-flavoured tables (| col | col |)
  - A cover page

Run: python3 build_pdf.py
Output: research_brief.pdf in the same directory.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT_MD = os.path.join(HERE, "flood_ews_nbs_research_brief.md")
OUTPUT_PDF = os.path.join(HERE, "research_brief.pdf")

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

base = getSampleStyleSheet()

STYLES = {
    "Body": ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        textColor=colors.HexColor("#111827"),
    ),
    "BodyLeft": ParagraphStyle(
        "BodyLeft",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=6,
        textColor=colors.HexColor("#111827"),
    ),
    "Bullet": ParagraphStyle(
        "Bullet",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        leftIndent=14,
        bulletIndent=2,
        spaceAfter=3,
        textColor=colors.HexColor("#111827"),
    ),
    "H1": ParagraphStyle(
        "H1",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceBefore=14,
        spaceAfter=10,
        textColor=colors.HexColor("#0F172A"),
    ),
    "H2": ParagraphStyle(
        "H2",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#1E3A8A"),
    ),
    "H3": ParagraphStyle(
        "H3",
        parent=base["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor("#1E40AF"),
    ),
    "H4": ParagraphStyle(
        "H4",
        parent=base["Heading4"],
        fontName="Helvetica-BoldOblique",
        fontSize=10.5,
        leading=14,
        spaceBefore=6,
        spaceAfter=3,
        textColor=colors.HexColor("#374151"),
    ),
    "CoverTitle": ParagraphStyle(
        "CoverTitle",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=18,
    ),
    "CoverSubtitle": ParagraphStyle(
        "CoverSubtitle",
        parent=base["Title"],
        fontName="Helvetica",
        fontSize=14,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=10,
    ),
    "CoverMeta": ParagraphStyle(
        "CoverMeta",
        parent=base["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=10.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#374151"),
    ),
    "TableCell": ParagraphStyle(
        "TableCell",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#111827"),
    ),
    "TableHeader": ParagraphStyle(
        "TableHeader",
        parent=base["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.white,
    ),
}

# ---------------------------------------------------------------------------
# Inline markdown -> reportlab markup
# ---------------------------------------------------------------------------

def inline(text: str) -> str:
    """Convert inline markdown (**bold**, *italic*, `code`) to reportlab tags."""
    # Escape XML special chars first
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    # Bold-italic ***x***  (rare)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)
    # Bold **x**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic *x*
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    # Inline code `x`
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    return text


# ---------------------------------------------------------------------------
# Markdown parser -> flowables
# ---------------------------------------------------------------------------

def parse_table(table_lines: list[str]):
    """Parse a GitHub-flavoured markdown table.

    table_lines: includes header row, separator row, body rows.
    Returns a Table flowable.
    """
    rows = []
    for line in table_lines:
        # split on |, drop empty leading/trailing cells
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return None
    header = rows[0]
    body = rows[2:]  # skip the |---|---| separator
    n_cols = len(header)

    # Build flowables for each cell (so they wrap)
    table_data = []
    table_data.append([Paragraph(inline(c), STYLES["TableHeader"]) for c in header])
    for row in body:
        # pad / truncate to n_cols
        row = (row + [""] * n_cols)[:n_cols]
        table_data.append([Paragraph(inline(c), STYLES["TableCell"]) for c in row])

    # Column widths: divide page width proportionally; first column slightly narrower.
    page_width = A4[0] - 2.5 * cm - 2.5 * cm  # match doc margins below
    if n_cols == 4:
        widths = [page_width * w for w in (0.18, 0.30, 0.27, 0.25)]
    elif n_cols == 5:
        widths = [page_width * w for w in (0.17, 0.25, 0.22, 0.20, 0.16)]
    else:
        widths = [page_width / n_cols] * n_cols

    tbl = Table(table_data, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94A3B8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#475569")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def md_to_flowables(md_text: str):
    flow = []
    lines = md_text.splitlines()
    i = 0
    in_code = False
    code_buf: list[str] = []
    bullet_buf: list[tuple[str, str]] = []  # (marker, text)

    def flush_bullets():
        if not bullet_buf:
            return
        for marker, text in bullet_buf:
            bullet_text = inline(text)
            p = Paragraph(bullet_text, STYLES["Bullet"], bulletText=marker)
            flow.append(p)
        bullet_buf.clear()
        flow.append(Spacer(1, 4))

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        # Code block fences
        if line.startswith("```"):
            if in_code:
                # close
                flush_bullets()
                code_str = "\n".join(code_buf)
                flow.append(Paragraph(
                    f'<font face="Courier" size="9">{code_str.replace(chr(10), "<br/>")}</font>',
                    STYLES["BodyLeft"],
                ))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Horizontal rule -> page break for major section separators
        if line.strip() == "---":
            flush_bullets()
            flow.append(PageBreak())
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_bullets()
            level = len(m.group(1))
            text = inline(m.group(2).strip())
            style = STYLES[f"H{level}"]
            flow.append(Paragraph(text, style))
            i += 1
            continue

        # Tables (GitHub flavoured)
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-: |]+\|$", lines[i + 1].strip()):
            flush_bullets()
            tbl_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                tbl_lines.append(lines[j].strip())
                j += 1
            tbl = parse_table(tbl_lines)
            if tbl is not None:
                flow.append(Spacer(1, 4))
                flow.append(tbl)
                flow.append(Spacer(1, 8))
            i = j
            continue

        # Bulleted list
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if m:
            bullet_buf.append(("\u2022", m.group(2)))
            i += 1
            continue

        # Numbered list
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m:
            bullet_buf.append((f"{m.group(2)}.", m.group(3)))
            i += 1
            continue

        # Blank line
        if line.strip() == "":
            flush_bullets()
            i += 1
            continue

        # Paragraph: gather contiguous non-blank, non-special lines
        flush_bullets()
        para_lines = [line]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].rstrip()
            if (
                nxt.strip() == ""
                or nxt.startswith("#")
                or nxt.startswith("```")
                or nxt.startswith("|")
                or nxt.strip() == "---"
                or re.match(r"^(\s*)[-*]\s+", nxt)
                or re.match(r"^(\s*)\d+\.\s+", nxt)
            ):
                break
            para_lines.append(nxt)
            j += 1
        para = " ".join(s.strip() for s in para_lines)
        flow.append(Paragraph(inline(para), STYLES["Body"]))
        i = j

    flush_bullets()
    return flow


# ---------------------------------------------------------------------------
# Cover page
# ---------------------------------------------------------------------------

def cover_flowables():
    flow = []
    flow.append(Spacer(1, 4 * cm))
    flow.append(Paragraph("Climate Resilience for Vulnerable Districts", STYLES["CoverTitle"]))
    flow.append(Paragraph(
        "Designing Community Flood Early Warning Systems and Nature-Based Flood Protection "
        "that Deliver Measurable Risk Reduction and Can Be Scaled Across Multiple Districts",
        STYLES["CoverSubtitle"],
    ))
    flow.append(Spacer(1, 1.2 * cm))
    flow.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#1E3A8A"),
                           spaceBefore=0, spaceAfter=10, hAlign="CENTER"))
    flow.append(Paragraph(
        "A PhD-level research brief and implementation framework",
        STYLES["CoverMeta"],
    ))
    flow.append(Paragraph(
        "for an India-focused, practitioner-scholar inquiry",
        STYLES["CoverMeta"],
    ))
    flow.append(Spacer(1, 6 * cm))
    flow.append(Paragraph(
        f"Prepared: {datetime.now().strftime('%B %Y')}",
        STYLES["CoverMeta"],
    ))
    flow.append(Paragraph(
        "Anchored in IPCC AR6, UNDRR Sendai Framework, "
        "WMO Multi-Hazard EWS guidelines, and the UN Early Warnings for All initiative",
        STYLES["CoverMeta"],
    ))
    flow.append(PageBreak())
    return flow


# ---------------------------------------------------------------------------
# Page templates with header / footer
# ---------------------------------------------------------------------------

def on_page(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(
        2.5 * cm, 1.2 * cm,
        "Climate Resilience for Vulnerable Districts \u2014 PhD Research Brief",
    )
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.setLineWidth(0.4)
    canvas.line(2.5 * cm, 1.6 * cm, A4[0] - 2.5 * cm, 1.6 * cm)
    canvas.restoreState()


def on_cover_page(canvas, doc):
    # No footer on cover
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#F8FAFC"))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#1E3A8A"))
    canvas.setLineWidth(2)
    canvas.line(2.5 * cm, A4[1] - 2 * cm, A4[0] - 2.5 * cm, A4[1] - 2 * cm)
    canvas.line(2.5 * cm, 2 * cm, A4[0] - 2.5 * cm, 2 * cm)
    canvas.restoreState()


def build():
    if not os.path.exists(INPUT_MD):
        sys.exit(f"Input markdown not found: {INPUT_MD}")
    with open(INPUT_MD, encoding="utf-8") as f:
        md = f.read()

    doc = BaseDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2 * cm,
        title="Climate Resilience for Vulnerable Districts",
        author="PhD research brief",
        subject="Community Flood EWS + Nature-Based Solutions for Vulnerable Indian Districts",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="content",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    cover_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="cover",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=cover_frame, onPage=on_cover_page),
        PageTemplate(id="content", frames=frame, onPage=on_page),
    ])

    story = []
    story.extend(cover_flowables())
    # Switch to content template after cover by inserting a NextPageTemplate
    from reportlab.platypus import NextPageTemplate
    # Insert NextPageTemplate immediately before cover_flowables' final PageBreak
    # Simpler: prepend it now.
    story.insert(0, NextPageTemplate("content"))

    story.extend(md_to_flowables(md))
    doc.build(story)
    size = os.path.getsize(OUTPUT_PDF)
    print(f"Wrote {OUTPUT_PDF} ({size/1024:.1f} KB)")


if __name__ == "__main__":
    build()
