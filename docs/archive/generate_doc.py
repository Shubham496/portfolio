"""Generate a clean, professional Word document project tracker reflecting current milestones."""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def build_tracker_doc():
    doc = Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("FastAPI Multi-App Portfolio & Microservices Hub")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Live Deployment, Production Tracker & Sprint Roadmap")
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Live Status Callout Box
    p_status = doc.add_paragraph()
    p_status.paragraph_format.space_after = Pt(16)
    r_s1 = p_status.add_run("Live Deployment Status: ")
    r_s1.bold = True
    r_s1.font.name = "Segoe UI"
    r_s1.font.color.rgb = RGBColor(22, 101, 52)
    r_s2 = p_status.add_run(
        "Deployed to Render (portfolio-ccy5.onrender.com) connected to GitHub repo (Shubham496/portfolio). "
        "Custom domain mythostech.in DNS verified via BigRock nameservers with automated SSL generation active."
    )
    r_s2.font.name = "Segoe UI"
    r_s2.font.color.rgb = RGBColor(51, 65, 85)

    # Section 1: Architecture Specifications
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(10)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Technical Architecture & Environment Configuration")
    r_h1.font.name = "Segoe UI"
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(37, 99, 235)

    specs = [
        ("Framework & Engine", "FastAPI (Python 3.10+) with Uvicorn ASGI (< 50 MB memory footprint)"),
        ("Configuration Structure", "Modular Two-Tier: app/core/local.py (dev) & app/core/deployment.py (prod)"),
        ("Live Domain", "https://mythostech.in and https://www.mythostech.in"),
        ("Source Control", "GitHub (https://github.com/Shubham496/portfolio.git) on branch main"),
        ("Hosting Platform", "Render Web Service (Auto-deploy on git push, Free Tier 512 MB)"),
        ("DNS Provider", "BigRock (A record -> 216.24.57.1, CNAME -> portfolio-ccy5.onrender.com)"),
        ("Database Strategy", "Local SQLite (zero-config); Ready for Turso / Neon Serverless in cloud")
    ]

    t_spec = doc.add_table(rows=len(specs) + 1, cols=2)
    t_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_spec.autofit = False

    hdr = t_spec.rows[0].cells
    hdr[0].width = Inches(2.3)
    hdr[1].width = Inches(4.2)
    hdr[0].paragraphs[0].add_run("Component").bold = True
    hdr[1].paragraphs[0].add_run("Active Solution / Status").bold = True
    for c in hdr:
        set_cell_shading(c, "E2E8F0")
        set_cell_margins(c, 100, 100, 140, 140)
        c.paragraphs[0].runs[0].font.name = "Segoe UI"
        c.paragraphs[0].runs[0].font.size = Pt(9.5)

    for i, (k, v) in enumerate(specs):
        row = t_spec.rows[i+1].cells
        row[0].width = Inches(2.3)
        row[1].width = Inches(4.2)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9)
        r0.bold = True
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9)
        for c in row:
            set_cell_margins(c, 70, 70, 120, 120)
            if i % 2 == 1:
                set_cell_shading(c, "F8FAFC")

    # Section 2: Milestone Tracker
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Milestone & Action Item Tracker")
    r_h2.font.name = "Segoe UI"
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(37, 99, 235)

    tasks = [
        ("Task-01", "Initialize FastAPI skeleton, templates, static routes & health check", "Phase 1: Setup", "Completed", "Pair"),
        ("Task-02", "Design developer portfolio homepage with resume data & custom photo", "Phase 1: Setup", "Completed", "Pair"),
        ("Task-03", "Split config into local.py & deployment.py with environment detection", "Phase 1: Setup", "Completed", "Pair"),
        ("Task-04", "Initialize Git repository, push to Shubham496/portfolio on GitHub", "Phase 1: Setup", "Completed", "Pair"),
        ("Task-05", "Deploy Web Service on Render with automatic build hooks", "Phase 1: Deploy", "Completed", "Pair"),
        ("Task-06", "Configure BigRock DNS (A & CNAME records) for mythostech.in", "Phase 1: Deploy", "Completed", "Pair"),
        ("Task-07", "SSL certificate handshake resolution on custom domain", "Phase 1: Deploy", "In Progress", "Render / DNS"),
        ("Task-08", "Build Mini-App 1: High-Performance URL Shortener & Analytics", "Phase 2: Apps", "Next Up", "Pair"),
        ("Task-09", "Implement SQLite database models & URL hash generator", "Phase 2: Apps", "Pending", "Pair"),
        ("Task-10", "Build Mini-App 2: JSON Formatter, Validator & Tree Inspector", "Phase 2: Apps", "Pending", "Pair"),
        ("Task-11", "Build Mini-App 3: Markdown Scratchpad with Live Preview & Export", "Phase 2: Apps", "Pending", "Pair")
    ]

    t_task = doc.add_table(rows=len(tasks) + 1, cols=5)
    t_task.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_task.autofit = False

    t_hdr = t_task.rows[0].cells
    widths = [Inches(0.8), Inches(2.7), Inches(1.1), Inches(1.0), Inches(0.9)]
    titles = ["ID", "Action Item Description", "Phase", "Status", "Owner"]

    for i, title in enumerate(titles):
        t_hdr[i].width = widths[i]
        run = t_hdr[i].paragraphs[0].add_run(title)
        run.bold = True
        run.font.name = "Segoe UI"
        run.font.size = Pt(9)
        set_cell_shading(t_hdr[i], "1E293B")
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(t_hdr[i], 90, 90, 90, 90)

    for i, row_data in enumerate(tasks):
        row = t_task.rows[i+1].cells
        for col_idx, text in enumerate(row_data):
            row[col_idx].width = widths[col_idx]
            run = row[col_idx].paragraphs[0].add_run(text)
            run.font.name = "Segoe UI"
            run.font.size = Pt(8.5)
            set_cell_margins(row[col_idx], 70, 70, 90, 90)

            if col_idx == 3:
                run.bold = True
                if text == "Completed":
                    set_cell_shading(row[col_idx], "DCFCE7")
                    run.font.color.rgb = RGBColor(22, 101, 52)
                elif text == "In Progress":
                    set_cell_shading(row[col_idx], "FEF3C7")
                    run.font.color.rgb = RGBColor(146, 64, 14)
                elif text == "Next Up":
                    set_cell_shading(row[col_idx], "DBEAFE")
                    run.font.color.rgb = RGBColor(29, 78, 216)
                else:
                    set_cell_shading(row[col_idx], "F1F5F9")
                    run.font.color.rgb = RGBColor(71, 85, 105)
            elif i % 2 == 1:
                set_cell_shading(row[col_idx], "F8FAFC")

    # Section 3: Next Sprints
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(18)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Next Sprint: URL Shortener & Analytics Micro-App Architecture")
    r_h3.font.name = "Segoe UI"
    r_h3.font.size = Pt(14)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(37, 99, 235)

    p_sprint = doc.add_paragraph()
    p_sprint.paragraph_format.space_after = Pt(6)
    r_sp = p_sprint.add_run(
        "Now that the foundation, repository, and live hosting are connected, we start implementing "
        "the micro-app suite directly inside the app/apps/ directory:"
    )
    r_sp.font.name = "Segoe UI"
    r_sp.font.size = Pt(9.5)

    steps = [
        ("Directory Isolation", "app/apps/url_shortener/ with router.py, models.py, and templates/"),
        ("Database Layer", "SQLite table tracking id, original_url, short_code, created_at, clicks, and last_accessed"),
        ("Core Functionality", "Input URL -> generate Base62 or custom short slug -> redirect /s/{code} -> increment analytics"),
        ("Analytics View", "Clean live table and stats card showing most visited links and real-time click counts")
    ]

    for title, desc in steps:
        p_item = doc.add_paragraph(style='List Bullet')
        p_item.paragraph_format.space_after = Pt(2)
        r_t = p_item.add_run(f"{title}: ")
        r_t.bold = True
        r_t.font.name = "Segoe UI"
        r_t.font.size = Pt(9)
        r_d = p_item.add_run(desc)
        r_d.font.name = "Segoe UI"
        r_d.font.size = Pt(9)

    doc.save("docs/Project_Action_Plan_and_Tracker.docx")
    print("Action Plan & Tracker updated successfully at docs/Project_Action_Plan_and_Tracker.docx")

if __name__ == "__main__":
    build_tracker_doc()
