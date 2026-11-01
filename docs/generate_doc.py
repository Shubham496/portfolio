"""Generate a clean, professional Word document project tracker."""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

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

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("FastAPI Portfolio & Multi-App Platform")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate-900

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Project Roadmap, Architecture Decisions & Action Item Tracker")
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(100, 116, 139) # Slate-500

    # Overview box
    p_ov = doc.add_paragraph()
    p_ov.paragraph_format.space_after = Pt(18)
    r_ov_label = p_ov.add_run("Project Objective: ")
    r_ov_label.bold = True
    r_ov_label.font.name = "Segoe UI"
    r_ov_label.font.color.rgb = RGBColor(30, 41, 59)
    r_ov_text = p_ov.add_run(
        "Build a high-performance, ultra-lightweight portfolio website and multi-application hub using "
        "FastAPI, SQLite, and Jinja2/Tailwind. The platform targets 100% free hosting tiers (Render, Fly.io, Koyeb) "
        "with < 100 MB baseline memory consumption, automated GitHub CI/CD, and custom domain routing."
    )
    r_ov_text.font.name = "Segoe UI"
    r_ov_text.font.color.rgb = RGBColor(51, 65, 85)

    # Section 1: Executive Summary & Project Specs
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Technical Architecture & Constraints")
    r_h1.font.name = "Segoe UI"
    r_h1.font.size = Pt(15)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(37, 99, 235) # Blue-600

    specs = [
        ("Framework", "FastAPI (Python 3.10+) with Uvicorn ASGI"),
        ("Memory Footprint Target", "< 100 MB RAM (free tier limit safely preserved at 512 MB)"),
        ("Frontend Engine", "Jinja2 Templates + Tailwind CSS + Responsive Mobile-first UX"),
        ("Database Layer", "SQLite locally (zero-overhead) / Cloud Turso or Neon Postgres for persistent state"),
        ("Deployment Target", "Render / Koyeb / Fly.io (Free Tier)"),
        ("CI/CD Pipeline", "GitHub Actions (main branch push -> test -> auto-deploy)"),
        ("Domain & Security", "Custom Domain via Cloudflare DNS + Free SSL/TLS")
    ]

    t_spec = doc.add_table(rows=len(specs) + 1, cols=2)
    t_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_spec.autofit = False

    # Header
    hdr = t_spec.rows[0].cells
    hdr[0].width = Inches(2.2)
    hdr[1].width = Inches(4.3)
    hdr[0].paragraphs[0].add_run("Component").bold = True
    hdr[1].paragraphs[0].add_run("Selected Architecture / Solution").bold = True
    for c in hdr:
        set_cell_shading(c, "E2E8F0") # Slate-200
        set_cell_margins(c, 100, 100, 150, 150)
        c.paragraphs[0].runs[0].font.name = "Segoe UI"
        c.paragraphs[0].runs[0].font.size = Pt(10)

    for i, (k, v) in enumerate(specs):
        row = t_spec.rows[i+1].cells
        row[0].width = Inches(2.2)
        row[1].width = Inches(4.3)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.bold = True
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)
        for c in row:
            set_cell_margins(c, 80, 80, 120, 120)
            if i % 2 == 1:
                set_cell_shading(c, "F8FAFC")

    # Section 2: Action Items Tracker
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(20)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Action Items & Milestone Tracker")
    r_h2.font.name = "Segoe UI"
    r_h2.font.size = Pt(15)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(37, 99, 235)

    tasks = [
        ("Task-01", "Initialize FastAPI structure, routers, static assets & Jinja2 templates", "Phase 1: Setup", "Completed", "Antigravity"),
        ("Task-02", "Design responsive Portfolio Homepage (Bio, Skills, Experience, Projects)", "Phase 1: Setup", "Completed", "Antigravity"),
        ("Task-03", "Build project documentation, README, and Word Tracker template", "Phase 1: Setup", "Completed", "Antigravity"),
        ("Task-04", "Develop Mini-App 1 (Interactive Utility, e.g., URL Shortener or JSON Toolkit)", "Phase 2: Apps", "Pending", "Pair"),
        ("Task-05", "Implement SQLite database session & model management", "Phase 2: Apps", "Pending", "Pair"),
        ("Task-06", "Develop Mini-App 2 (e.g., Markdown Note Stash or Prompt Manager)", "Phase 2: Apps", "Pending", "Pair"),
        ("Task-07", "Set up Git repository, commit history, and push to GitHub", "Phase 3: Deploy", "Pending", "User / Pair"),
        ("Task-08", "Configure Render / Koyeb Web Service connected to GitHub repository", "Phase 3: Deploy", "Pending", "User / Pair"),
        ("Task-09", "Configure Cloudflare DNS and attach custom domain with SSL", "Phase 3: Deploy", "Pending", "User")
    ]

    t_task = doc.add_table(rows=len(tasks) + 1, cols=5)
    t_task.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_task.autofit = False

    t_hdr = t_task.rows[0].cells
    widths = [Inches(0.9), Inches(2.6), Inches(1.1), Inches(1.0), Inches(0.9)]
    titles = ["ID", "Action Item Description", "Phase", "Status", "Owner"]

    for i, title in enumerate(titles):
        t_hdr[i].width = widths[i]
        run = t_hdr[i].paragraphs[0].add_run(title)
        run.bold = True
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        set_cell_shading(t_hdr[i], "1E293B") # Slate-800
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(t_hdr[i], 100, 100, 100, 100)

    for i, row_data in enumerate(tasks):
        row = t_task.rows[i+1].cells
        for col_idx, text in enumerate(row_data):
            row[col_idx].width = widths[col_idx]
            run = row[col_idx].paragraphs[0].add_run(text)
            run.font.name = "Segoe UI"
            run.font.size = Pt(9)
            set_cell_margins(row[col_idx], 80, 80, 100, 100)

            if col_idx == 3: # Status column styling
                run.bold = True
                if text == "Completed":
                    set_cell_shading(row[col_idx], "DCFCE7") # Green-100
                    run.font.color.rgb = RGBColor(22, 101, 52) # Green-800
                elif text == "In Progress":
                    set_cell_shading(row[col_idx], "FEF3C7") # Amber-100
                    run.font.color.rgb = RGBColor(146, 64, 14) # Amber-800
                else:
                    set_cell_shading(row[col_idx], "F1F5F9") # Slate-100
                    run.font.color.rgb = RGBColor(71, 85, 105) # Slate-600
            elif i % 2 == 1:
                set_cell_shading(row[col_idx], "F8FAFC")

    # Section 3: Mini-App Ideas Pipeline
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(20)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Mini-App Expansion Pipeline")
    r_h3.font.name = "Segoe UI"
    r_h3.font.size = Pt(15)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(37, 99, 235)

    p_apps = doc.add_paragraph()
    p_apps.paragraph_format.space_after = Pt(6)
    r_p_apps = p_apps.add_run("Each sub-app will be housed under app/apps/<app_name> with dedicated routes and zero impact on other modules:")
    r_p_apps.font.name = "Segoe UI"
    r_p_apps.font.size = Pt(10)

    app_list = [
        ("URL Shortener & Analytics", "Lightweight SQLite-backed link shortener with click counters and QR code generator."),
        ("JSON & API Schema Inspector", "Formatter, validator, and diff tool for developers directly in your portfolio."),
        ("Quick Notes / Pastebin", "Ephemeral or persistent markdown snippet repository with copy-to-clipboard functionality."),
        ("AI Utility / Summarizer", "Lightweight endpoint leveraging free Gemini API tier for quick text transformation.")
    ]

    for title, desc in app_list:
        p_item = doc.add_paragraph(style='List Bullet')
        p_item.paragraph_format.space_after = Pt(3)
        r_t = p_item.add_run(f"{title}: ")
        r_t.bold = True
        r_t.font.name = "Segoe UI"
        r_t.font.size = Pt(9.5)
        r_d = p_item.add_run(desc)
        r_d.font.name = "Segoe UI"
        r_d.font.size = Pt(9.5)

    doc.save("docs/Project_Action_Plan_and_Tracker.docx")
    print("Document created successfully at docs/Project_Action_Plan_and_Tracker.docx")

if __name__ == "__main__":
    build_tracker_doc()
