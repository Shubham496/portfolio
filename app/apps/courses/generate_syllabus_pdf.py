"""
MYTHOS Comprehensive Syllabus Brochure Generator
Builds a high-impact, styled 2-page curriculum brochure PDF using fpdf2.
"""

import os
from fpdf import FPDF
from app.core.config import settings


class MythosSyllabusPDF(FPDF):
    def header(self):
        # Top Dark Navy Banner
        self.set_fill_color(7, 11, 20)  # Dark Navy #070B14
        self.rect(0, 0, 210, 16, 'F')

        # Top Accent Split Line (Electric Blue on left, Vivid Orange on right)
        self.set_fill_color(37, 99, 235)  # Electric Blue
        self.rect(0, 16, 125, 1.2, 'F')
        self.set_fill_color(249, 115, 22)  # Vivid Orange
        self.rect(125, 16, 85, 1.2, 'F')

        # Header Title in Top Banner
        self.set_xy(10, 3.5)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(255, 255, 255)
        self.cell(95, 8, 'MYTHOS | ONLINE EDUCATIONAL INSTITUTE', align='L')

        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(148, 163, 184)
        self.cell(95, 8, 'WEEKEND COHORT | SAT & SUN 6:00 - 8:00 PM IST', align='R')
        self.ln(15)

    def footer(self):
        # Footer Baseline Bar
        self.set_y(-14)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())

        self.set_y(-12)
        self.set_font('Helvetica', 'B', 7.5)
        self.set_text_color(37, 99, 235)
        self.cell(45, 6, 'MYTHOS LEARNING ENGINE', align='L')

        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(71, 85, 105)
        self.cell(110, 6, f'Admissions: {settings.BUSINESS_EMAIL} | WhatsApp: +91 {settings.BUSINESS_WHATSAPP}', align='C')

        self.set_font('Helvetica', 'B', 7.5)
        self.set_text_color(100, 116, 139)
        self.cell(35, 6, f'Page {self.page_no()}', align='R')


def generate_syllabus_pdf(output_path: str = "app/static/pdf/Data_Analysis_Syllabus.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = MythosSyllabusPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # ═════════════════════════════════════════════════════════════
    # PAGE 1: Intro, Schedule & Modules 1 - 3
    # ═════════════════════════════════════════════════════════════
    pdf.add_page()

    # Document Headline
    pdf.set_y(21)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(15, 23, 42)  # Slate 900
    pdf.cell(0, 8, 'Complete Data Analysis Masterclass', align='L', new_x="LMARGIN", new_y="NEXT")

    # Subtitle / Pillar Spectrum
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(37, 99, 235)  # Electric Blue
    pdf.cell(0, 5, 'Production-Grade Mentorship: Python | SQL | Power BI | Excel | Tableau', align='L', new_x="LMARGIN", new_y="NEXT")

    # Value proposition
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 4.5, f'{settings.TRUST_CLAIM} | 100% Weekend Live Interactive Coding | Real Capstones', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # ── Fixed Schedule & Format Strip ──
    sched_y = pdf.get_y()
    pdf.set_fill_color(248, 250, 252)  # Slate 50
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.4)
    pdf.rect(10, sched_y, 190, 16, 'DF')

    # Accent left border for schedule
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(10, sched_y, 2.5, 16, 'F')

    # Schedule Column 1
    pdf.set_xy(15, sched_y + 2)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(45, 3.5, 'BATCH SCHEDULE', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(45, 5, 'Saturday & Sunday Only', align='L')

    # Schedule Column 2
    pdf.set_xy(68, sched_y + 2)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(45, 3.5, 'LIVE TIMINGS', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(68)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(45, 5, '6:00 PM - 8:00 PM IST', align='L')

    # Schedule Column 3
    pdf.set_xy(125, sched_y + 2)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(40, 3.5, 'DURATION & COHORT', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(125)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(40, 5, '8-10 Wks | 25 Max Seats', align='L')

    # Schedule Column 4
    pdf.set_xy(172, sched_y + 2)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(26, 3.5, 'ADMISSION', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(172)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(16, 185, 129)  # Emerald
    pdf.cell(26, 5, 'Selection-Based', align='L')

    pdf.set_y(sched_y + 19)

    # Helper function for rendering styled module cards
    def draw_module_card(num, title, badge, accent_rgb, topics, deep_dives, card_h=67):
        cur_y = pdf.get_y()

        # Background card
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.35)
        pdf.rect(10, cur_y, 190, card_h, 'DF')

        # Color Accent Bar on Left
        pdf.set_fill_color(*accent_rgb)
        pdf.rect(10, cur_y, 3, card_h, 'F')

        # Number Badge
        pdf.set_fill_color(*accent_rgb)
        pdf.rect(16, cur_y + 3.5, 7, 7, 'F')
        pdf.set_xy(16, cur_y + 3.5)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(7, 7, str(num), align='C')

        # Module Title
        pdf.set_xy(26, cur_y + 3.5)
        pdf.set_font('Helvetica', 'B', 10.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(115, 7, title, align='L')

        # Category Pill Badge
        badge_w = 42
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(153, cur_y + 4.5, badge_w, 5, 'DF')
        pdf.set_xy(153, cur_y + 4.5)
        pdf.set_font('Helvetica', 'B', 6.5)
        pdf.set_text_color(*accent_rgb)
        pdf.cell(badge_w, 5, badge.upper(), align='C')

        # Core Topics Heading
        pdf.set_xy(16, cur_y + 12)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(85, 3.5, 'CORE COMPETENCIES & TECHNIQUES:', align='L')

        # Deep Dives Heading
        pdf.set_xy(105, cur_y + 12)
        pdf.cell(90, 3.5, 'HANDS-ON PRODUCTION LABS & AUTOMATION:', align='L')

        # Two-Column Content: Left = Topics, Right = Deep Dives
        col_y = cur_y + 16.5

        # Left Column (Core Topics)
        pdf.set_xy(16, col_y)
        pdf.set_font('Helvetica', '', 7.5)
        pdf.set_text_color(51, 65, 85)
        for t in topics:
            pdf.set_x(16)
            pdf.set_font('Helvetica', 'B', 7.5)
            pdf.set_text_color(*accent_rgb)
            pdf.cell(3, 4.2, '>', align='L')
            pdf.set_font('Helvetica', '', 7.5)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(82, 4.2, t[:56], align='L', new_x="LMARGIN", new_y="NEXT")

        # Right Column (Deep Dives)
        pdf.set_xy(105, col_y)
        for d in deep_dives:
            pdf.set_x(105)
            pdf.set_font('Helvetica', 'B', 7.5)
            pdf.set_text_color(16, 185, 129)
            pdf.cell(3, 4.2, '*', align='L')
            pdf.set_font('Helvetica', '', 7.5)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(90, 4.2, d[:62], align='L', new_x="LMARGIN", new_y="NEXT")

        pdf.set_y(cur_y + card_h + 3.5)

    # ── Module 1: Excel ──
    draw_module_card(
        num=1,
        title="Excel Advanced Modeling, Power Query & VBA",
        badge="Spreadsheets & Automation",
        accent_rgb=(33, 115, 70),  # Excel Forest Green
        topics=[
            "Power Query Editor: Multi-file ingestion, ETL shaping & unpivoting",
            "Advanced Formulas: Dynamic Arrays, XLOOKUP, INDEX/MATCH, FILTER",
            "Modern Functions: LET (variables) & LAMBDA custom reusable logic",
            "Financial Modeling: What-If Analysis, Goal Seek & Scenarios"
        ],
        deep_dives=[
            "VBA & Macros: Subroutines, loops, custom UDFs & one-click reports",
            "Multi-table linked data models with automated refresh pipelines",
            "Executive dashboards: Multi-slicer linkage, dynamic sparklines & KPIs",
            "Automated folder ingestion eliminating manual monthly copy-pasting"
        ],
        card_h=37
    )

    # ── Module 2: SQL ──
    draw_module_card(
        num=2,
        title="SQL for Data Analysis & Relational Databases",
        badge="Database Architecture",
        accent_rgb=(37, 99, 235),  # Electric Blue
        topics=[
            "Relational Architecture: Schema design, 3NF normalization, PK/FK",
            "Complex Joins: Multi-table INNER, LEFT, RIGHT, FULL OUTER joins",
            "Analytical Window Functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE",
            "Lead & Lag Analysis: Period-over-period sales without self-joins"
        ],
        deep_dives=[
            "CTEs (Common Table Expressions) & Recursive hierarchical queries",
            "Query Optimization: B-Tree indexing strategies & EXPLAIN ANALYZE",
            "Business Metrics: Cohort retention, churn velocity & active users",
            "PostgreSQL & MySQL enterprise transactional dataset manipulation"
        ],
        card_h=37
    )

    # ── Module 3: Python ──
    draw_module_card(
        num=3,
        title="Python for Data Analysis & Automation",
        badge="Core Programming & ETL",
        accent_rgb=(217, 119, 6),  # Amber / Python Gold
        topics=[
            "Python Foundations: Data structures, control flow & modular scripts",
            "NumPy Computing: Vectorized ndarrays, broadcasting & matrix math",
            "Pandas Wrangling: Multi-index GroupBy, pivot_table(), melt()",
            "Data Cleansing: Missing value imputation, .str methods, Regex extraction"
        ],
        deep_dives=[
            "SQLAlchemy Ingestion: Connecting Python to relational warehouses",
            "Automated ETL pipelines: Parsing heterogeneous CSVs & Excel sheets",
            "Statistical Distributions: Outlier detection with Matplotlib & Seaborn",
            "Production scripting: Automated email alerting & cron-scheduled jobs"
        ],
        card_h=37
    )

    # Bottom Trust Note on Page 1
    pdf.set_y(268)
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 11, 'DF')
    pdf.set_xy(13, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(40, 3.5, 'PRACTICAL CODE RIGOR:', align='L')
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(145, 3.5, 'Every session involves live hands-on execution. You write code and solve queries in real-time.', align='L')
    pdf.set_xy(13, pdf.get_y() + 4)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(180, 3, 'Zero prerequisite barriers: Program covers zero to advanced production execution over 8-10 weeks.', align='L')

    # ═════════════════════════════════════════════════════════════
    # PAGE 2: Modules 4 - 6, Capstone Projects & Admissions Desk
    # ═════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_y(21)

    # ── Module 4: Power BI ──
    draw_module_card(
        num=4,
        title="Power BI Interactive Business Intelligence",
        badge="Enterprise BI & Modeling",
        accent_rgb=(234, 88, 12),  # Orange / Power BI
        topics=[
            "Power Query ETL: Shaping, unpivoting, merging queries, column profiles",
            "Relational Data Modeling: Star Schema vs Snowflake, Fact/Dim tables",
            "Advanced DAX: Row/Filter context, CALCULATE, FILTER, ALL, VALUES",
            "Time Intelligence: YTD, QTD, MTD, SAMEPERIODLASTYEAR, moving averages"
        ],
        deep_dives=[
            "Executive Dashboards: Drill-through reports, bookmarks & custom tooltips",
            "Virtual Tables: SUMMARIZE, ADDCOLUMNS, safe numerical division",
            "Managing relationships: Active vs inactive (USERELATIONSHIP logic)",
            "Power BI Service deployment: Scheduled refreshes & workspace governance"
        ],
        card_h=37
    )

    # ── Module 5: Tableau ──
    draw_module_card(
        num=5,
        title="Tableau Visual Storytelling & Analytics",
        badge="Visual Storyboards",
        accent_rgb=(124, 58, 237),  # Violet / Tableau
        topics=[
            "Enterprise Connections: Databases, CSVs, cloud warehouses & blending",
            "Level of Detail (LOD): FIXED, INCLUDE, EXCLUDE calculations",
            "Table Calculations: Running totals, percent of total, rank, window stats",
            "Interactive Dashboards: Filter actions, highlight actions & set actions"
        ],
        deep_dives=[
            "Dynamic Parameters: User-driven metric switching & what-if controls",
            "Multi-chapter storyboards for C-suite executive decision-making",
            "Extract performance tuning & dashboard latency optimization",
            "Tableau Public portfolio publishing with live interactive web embeds"
        ],
        card_h=37
    )

    # ── Module 6: Career Prep ──
    draw_module_card(
        num=6,
        title="Career Acceleration: GitHub, Resume & LinkedIn",
        badge="Job Readiness & Portfolio",
        accent_rgb=(14, 165, 233),  # Cyan / Career
        topics=[
            "GitHub Architecture: Open-source repositories with production READMEs",
            "ATS Resume Engineering: Action + Tool + Metric formula for Data roles",
            "LinkedIn Optimization: High-converting headline, demos & inbound magnet",
            "Live Technical Mocks: Timed SQL screenings on CoderPad & HackerRank"
        ],
        deep_dives=[
            "Data dictionaries & architecture schemas for 3+ portfolio capstones",
            "Passing automated recruiter screeners with keyword-dense formatting",
            "Direct outreach frameworks for hiring managers & senior data leads",
            "Dashboard defense: Justifying DAX measures & schema design under pressure"
        ],
        card_h=37
    )

    # ── Hands-On Production Capstones Box ──
    cap_y = pdf.get_y()
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.35)
    pdf.rect(10, cap_y, 190, 39, 'DF')

    # Top Capstone Accent Header
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(10, cap_y, 190, 7.5, 'F')
    pdf.set_xy(14, cap_y + 1)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(120, 5.5, '3 PRODUCTION PORTFOLIO CAPSTONES (BUILT LIVE DURING COHORT):', align='L')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(251, 146, 60)
    pdf.cell(60, 5.5, 'PORTFOLIO ASSETS FOR GITHUB', align='R')

    # Capstone 1
    pdf.set_xy(14, cap_y + 9.5)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(5, 4, '1.', align='L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(75, 4, 'Adidas Retail Intelligence & Forecasting:', align='L')
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(100, 4, 'Multi-region revenue tracking, inventory turnover velocity, and DAX KPI models.', align='L')

    # Capstone 2
    pdf.set_xy(14, cap_y + 16.5)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(5, 4, '2.', align='L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(75, 4, 'Automated Multi-Source Data Warehouse:', align='L')
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(100, 4, 'Python ETL pipelines consolidating raw APIs/CSVs into 3NF PostgreSQL database.', align='L')

    # Capstone 3
    pdf.set_xy(14, cap_y + 23.5)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(5, 4, '3.', align='L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(75, 4, 'Event Intelligence & Attendance Analytics:', align='L')
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(100, 4, 'Interactive ticketing analytics, cohort attrition curves, and executive storyboards.', align='L')

    # Capstone Outcome Footer
    pdf.set_xy(14, cap_y + 31)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(180, 4, 'GRADUATION OUTCOME: You complete the cohort with 3 production-grade repositories ready for interviews.', align='L')

    # ── Admissions & Counseling Desk Strip ──
    desk_y = cap_y + 42.5
    pdf.set_fill_color(7, 11, 20)  # Dark Navy
    pdf.rect(10, desk_y, 190, 21, 'F')

    pdf.set_xy(15, desk_y + 2.5)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(120, 4.5, 'ADMISSIONS & TECHNICAL COUNSELING DESK', align='L')

    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(249, 115, 22)
    pdf.cell(60, 4.5, 'OFFICIAL ACADEMIC ADMISSIONS', align='R')

    pdf.set_xy(15, desk_y + 8.5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(90, 4, f'Email: {settings.BUSINESS_EMAIL}', align='L')
    pdf.cell(90, 4, f'WhatsApp / Direct Call: +91 {settings.BUSINESS_WHATSAPP}', align='R')

    pdf.set_xy(15, desk_y + 13.5)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(180, 4, 'Direct 1-on-1 cohort orientation and onboarding guidelines are communicated to each admitted student.', align='L')

    pdf.output(output_path)
    print(f"Successfully generated styled syllabus brochure: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_syllabus_pdf()
