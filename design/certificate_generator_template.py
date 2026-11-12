"""
MYTHOS Certificate of Completion Generator
Generates official A4 landscape graduation certificates using design tokens and FPDF2.
"""

import os
import json
import argparse
from fpdf import FPDF


def generate_certificate(
    candidate_name: str = "Priya Verma",
    cert_id: str = "MYTHOS-DA-2026-B1001",
    issue_date: str = "November 12, 2026",
    output_path: str = "app/static/certificates/Sample_Certificate.pdf"
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load design tokens if available
    tokens_path = os.path.join(os.path.dirname(__file__), "tokens.json")
    if os.path.exists(tokens_path):
        with open(tokens_path, "r", encoding="utf-8") as f:
            tokens = json.load(f)
    else:
        tokens = {}

    # Initialize A4 Landscape PDF (297mm x 210mm)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # --- Background Canvas ---
    pdf.set_fill_color(252, 253, 254)  # Parchment Light Slate
    pdf.rect(0, 0, 297, 210, 'F')

    # --- Outer Double Border with Mythos Royal Blue & Electric Blue ---
    pdf.set_draw_color(30, 58, 138)  # Royal Blue (#1E3A8A)
    pdf.set_line_width(2.0)
    pdf.rect(12, 12, 273, 186, 'D')

    pdf.set_draw_color(37, 99, 235)  # Electric Blue (#2563EB)
    pdf.set_line_width(0.7)
    pdf.rect(15.5, 15.5, 266, 179, 'D')

    # --- Four Corner Cornerstones (Vivid Orange Accents #F97316) ---
    pdf.set_fill_color(249, 115, 22)
    corners = [
        (12, 12), (281, 12), (12, 194), (281, 194)
    ]
    for cx, cy in corners:
        pdf.rect(cx, cy, 4, 4, 'F')

    # --- Header: Institution Brand ---
    pdf.set_y(24)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(7, 11, 20)  # Dark Navy
    pdf.cell(0, 8, 'M Y T H O S', align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(100, 116, 139)  # Slate 500
    pdf.cell(0, 5, 'ACADEMY OF DATA SYSTEMS & ARCHITECTURE', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # --- Certificate Award Title ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(37, 99, 235)  # Electric Blue
    pdf.cell(0, 6, 'CERTIFICATE OF EXCELLENCE & COMPLETION', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # --- Presentation Line ---
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, 'THIS IS PROUDLY PRESENTED TO', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # --- Candidate Name (Prominent & Bold) ---
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(15, 23, 42)  # Slate 900
    pdf.cell(0, 12, candidate_name.upper(), align='C', new_x="LMARGIN", new_y="NEXT")

    # Decorative Gradient Underline Bar
    line_w = 120
    line_x = (297 - line_w) / 2
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(line_x, pdf.get_y() + 1, line_w / 2, 1.2, 'F')
    pdf.set_fill_color(249, 115, 22)
    pdf.rect(line_x + line_w / 2, pdf.get_y() + 1, line_w / 2, 1.2, 'F')
    pdf.ln(6)

    # --- Certification Body Copy ---
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(51, 65, 85)
    pdf.set_x(36)
    citation = (
        "For successfully completing the intensive 10-week Weekend Data Analysis Masterclass, "
        "demonstrating exceptional hands-on capability in architecting end-to-end production data pipelines, "
        "advanced relational SQL modeling, and executive business intelligence solutions."
    )
    pdf.multi_cell(225, 5.5, citation, 0, 'C')
    pdf.ln(4)

    # --- 5 Accredited Technology Pillars ---
    pdf.set_y(pdf.get_y() + 2)
    pillars = [
        "Python ETL",
        "Relational SQL",
        "Power BI Dashboards",
        "Excel Modeling & VBA",
        "Tableau Storytelling"
    ]
    total_pill_width = len(pillars) * 44 + (len(pillars) - 1) * 4
    start_x = (297 - total_pill_width) / 2
    y_pos = pdf.get_y()

    for idx, p in enumerate(pillars):
        px = start_x + idx * (44 + 4)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.set_line_width(0.3)
        pdf.rect(px, y_pos, 44, 7, 'DF')
        pdf.set_xy(px, y_pos + 1)
        pdf.set_font('Helvetica', 'B', 7.5)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(44, 5, p, 0, 0, 'C')

    pdf.ln(18)

    # --- Security & Signatory Footer ---
    footer_y = 158

    # Left: Date & Batch
    pdf.set_xy(25, footer_y)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(55, 4, f"Issued: {issue_date}", 0, 1, 'L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, "Batch: DA-WKND-2026-B1", 0, 0, 'L')

    # Center: Embossed Digital Seal
    seal_x = (297 - 40) / 2
    pdf.set_fill_color(249, 115, 22)
    pdf.ellipse(seal_x, footer_y - 8, 40, 20, 'F')
    pdf.set_fill_color(15, 23, 42)
    pdf.ellipse(seal_x + 1.5, footer_y - 6.5, 37, 17, 'F')
    pdf.set_xy(seal_x, footer_y - 2)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 4, "VERIFIED MENTORSHIP", 0, 1, 'C')
    pdf.set_xy(seal_x, footer_y + 1.5)
    pdf.set_font('Helvetica', '', 6)
    pdf.set_text_color(251, 146, 60)
    pdf.cell(40, 3, "OFFICIAL ACCREDITATION", 0, 0, 'C')

    # Right: Verification Serial & Link
    pdf.set_xy(217, footer_y)
    pdf.set_font('Courier', 'B', 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(55, 4, cert_id, 0, 1, 'R')
    pdf.set_x(217)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(55, 4, "mythostech.in/verify", 0, 0, 'R')

    # Signatures
    sig_y = footer_y + 12
    pdf.set_line_width(0.4)
    pdf.set_draw_color(148, 163, 184)
    
    # Sig 1
    pdf.line(25, sig_y + 8, 85, sig_y + 8)
    pdf.set_xy(25, sig_y + 9)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 4, "Lead Technical Mentor", 0, 1, 'L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(60, 3, "Data Architecture & Analytics", 0, 0, 'L')

    # Sig 2
    pdf.line(212, sig_y + 8, 272, sig_y + 8)
    pdf.set_xy(212, sig_y + 9)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 4, "Program Director", 0, 1, 'R')
    pdf.set_x(212)
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(60, 3, "Cohort Admissions & Operations", 0, 0, 'R')

    pdf.output(output_path)
    print(f"Generated official certificate: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Mythos Student Certificate")
    parser.add_argument("--name", default="Priya Verma", help="Student full name")
    parser.add_argument("--id", default="MYTHOS-DA-2026-B1001", help="Certificate ID")
    parser.add_argument("--date", default="November 12, 2026", help="Issue date")
    parser.add_argument("--out", default="app/static/certificates/Sample_Certificate.pdf", help="Output path")
    args = parser.parse_args()

    generate_certificate(args.name, args.id, args.date, args.out)
