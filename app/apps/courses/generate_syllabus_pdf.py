import os
from fpdf import FPDF


class SyllabusPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)  # Slate 900
        self.rect(0, 0, 210, 16, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 4)
        self.cell(0, 8, 'MYTHOS | DATA ANALYSIS MASTERCLASS | WEEKEND BATCH (SAT & SUN 6-8 PM IST)', 0, 0, 'C')
        self.ln(16)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f'Instructor: Shubham Singh  |  WhatsApp: +91 8727864157  |  Page {self.page_no()}', 0, 0, 'C')


def generate_syllabus_pdf():
    os.makedirs("app/static/pdf", exist_ok=True)
    pdf_path = "app/static/pdf/Data_Analysis_Syllabus.pdf"

    pdf = SyllabusPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Document Header Title
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, 'Complete Data Analysis Masterclass', 0, 1, 'L')

    # Subtitle
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(37, 99, 235)  # Blue 600
    pdf.cell(0, 6, 'Hands-On Mentorship: Python, SQL, Power BI, Excel & Tableau', 0, 1, 'L')
    pdf.ln(2)

    # Instructor & Credentials
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 5, 'Instructor: Shubham Singh - Lead Python & Data Architecture Consultant\nIndustry Background: Ducat, Netmax Technologies, LNP Infotech | 550+ Students & Senior Developers Trained')
    pdf.ln(4)

    # Schedule Box
    pdf.set_fill_color(241, 245, 249)  # Slate 100
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 22, 'DF')
    
    current_y = pdf.get_y() + 3
    pdf.set_xy(14, current_y)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 5, 'BATCH SCHEDULE:', 0, 0)
    pdf.cell(60, 5, 'TIMINGS:', 0, 0)
    pdf.cell(60, 5, 'FORMAT & DURATION:', 0, 1)

    pdf.set_xy(14, current_y + 6)
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(60, 6, 'Saturday & Sunday Only', 0, 0)
    pdf.cell(60, 6, '6:00 PM - 8:00 PM IST', 0, 0)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(60, 6, '8-10 Weeks (Live Online Hands-On)', 0, 1)
    pdf.ln(12)

    # Section: Course Pillars
    def render_module(num, title, topics):
        pdf.set_fill_color(37, 99, 235)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(8, 7, f' {num} ', 0, 0, 'C', True)
        
        pdf.set_fill_color(248, 250, 252)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 7, f'  {title}', 0, 1, 'L', True)
        pdf.ln(1)

        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(51, 65, 85)
        for t in topics:
            pdf.cell(6, 4.5, '-', 0, 0, 'R')
            pdf.cell(0, 4.5, f'  {t}', 0, 1, 'L')
        pdf.ln(3)

    # Module 1
    render_module(
        1,
        'Excel Advanced Modeling, Power Query & VBA',
        [
            'Power Query Editor: Multi-file ingestion, unpivoting, merging/appending datasets & ETL cleanses',
            'VBA & Automation: Recording macros, writing subroutines, automating recurring weekly reports',
            'Advanced Lookup & Dynamic Arrays: XLOOKUP, INDEX/MATCH, FILTER, UNIQUE, Nested IFS',
            'Data Validation, Conditional Formatting & What-If Financial Analysis (Goal Seek, Scenarios)'
        ]
    )

    # Module 2
    render_module(
        2,
        'SQL for Data Analysis & Relational Databases',
        [
            'Relational Database Architecture, Schema Design, 3NF Normalization, Primary/Foreign Keys',
            'Complex Querying: Multi-Table INNER/LEFT/RIGHT/FULL JOINs, Subqueries, and Nested CTEs',
            'Analytical Window Functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE, LEAD/LAG, Running Totals',
            'Performance Tuning: B-tree indexing, EXPLAIN ANALYZE, and real-world business analytics queries'
        ]
    )

    # Module 3
    render_module(
        3,
        'Python Programming for Data Analytics & ETL',
        [
            'Python Foundations: Data structures (Lists, Tuples, Dictionaries), Control Flow, Functions',
            'NumPy Computing: Vectorized array operations, matrix mathematics, indexing & slicing',
            'Pandas DataFrames: High-speed wrangling, missing data imputation, regex extraction, GroupBy pipelines',
            'Automated Data Transformation, SQLAlchemy database ingestion, and scheduled reporting scripts'
        ]
    )

    # Module 4
    render_module(
        4,
        'Power BI Business Intelligence & Interactive Dashboards',
        [
            'End-to-End ETL with Power Query: Cleansing, unpivoting, merging & data modeling',
            'Relational Data Modeling: Star Schema, Snowflake Schema, 1-to-Many Relationships',
            'Advanced DAX: CALCULATE, FILTER, ALL, RELATED, Time Intelligence (YTD, MTD, YoY, moving averages)',
            'Executive Visualization: Drill-through reports, interactive slicers, custom tooltips, KPI cards'
        ]
    )

    # Module 5
    render_module(
        5,
        'Tableau Visual Storytelling & Dashboards',
        [
            'Connecting to Varied Sources (Files, Relational Databases, Cloud Warehouses)',
            'Level of Detail (LOD) Calculations: FIXED, INCLUDE, EXCLUDE expressions & Table calculations',
            'Interactive Dashboards: Filter actions, highlight actions, set actions, and dynamic parameters',
            'Storyboarding & Cloud Publishing: Multi-chapter executive presentations on Tableau Public'
        ]
    )

    # Module 6
    render_module(
        6,
        'Career Acceleration: GitHub, Resume & LinkedIn Setup',
        [
            'GitHub Portfolio: Open-source repositories with production READMEs, architecture schemas & demos',
            'ATS-Optimized Resume: Quantified impact bullet points (Action + Tool + Metric) tailored for Data roles',
            'LinkedIn Setup: High-converting headline, featured projects, and recruiter direct outreach framework',
            'Interview Preparation: 1-on-1 mock technical interviews, live SQL problem solving on CoderPad'
        ]
    )

    # Capstone & Projects Strip
    pdf.ln(2)
    pdf.set_fill_color(236, 253, 245)  # Emerald 50
    pdf.set_draw_color(167, 243, 208)
    pdf.rect(10, pdf.get_y(), 190, 24, 'DF')
    
    box_y = pdf.get_y() + 2
    pdf.set_xy(14, box_y)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(6, 95, 70)  # Emerald 800
    pdf.cell(0, 5, 'HANDS-ON PRODUCTION CAPSTONE PROJECTS:', 0, 1)

    pdf.set_xy(14, box_y + 5.5)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 4.2, '1. Retail & E-Commerce Sales Performance Suite (Python ETL + SQL + Power BI Dashboard)\n2. Financial Transactions & Compliance Auditing Analysis (SQL + Tableau Visual Storyboard)\nAll students complete live portfolio assets ready to showcase on GitHub and LinkedIn.')

    pdf.output(pdf_path)
    print(f"Successfully generated {pdf_path}")


if __name__ == "__main__":
    generate_syllabus_pdf()
