import os
from fpdf import FPDF


class SyllabusPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)  # Slate 900
        self.rect(0, 0, 210, 16, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 4)
        self.cell(0, 8, 'DATA ANALYSIS MASTERCLASS | WEEKEND BATCH (SAT & SUN 6-8 PM IST)', 0, 0, 'C')
        self.ln(16)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f'Instructor: Shubham Singh  |  Phone: +91 9520132466  |  Page {self.page_no()}', 0, 0, 'C')


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
    pdf.multi_cell(0, 5, 'Instructor: Shubham Singh - Lead Python & Data Architecture Consultant\nIndustry Background: Ducat, Netmax Technologies, LNP Infotech | 120+ Senior Developers & Students Mentored')
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
        'Excel Advanced Modeling & Cleansing',
        [
            'Advanced Lookup & Formulas: XLOOKUP, INDEX/MATCH, VLOOKUP, Nested IFs, SUMIFS',
            'Data Cleaning, Text Functions (TRIM, SUBSTITUTE, TEXTSPLIT), and Flash Fill',
            'Interactive Pivot Tables, Calculated Fields, Grouping & Executive Pivot Charts',
            'Data Validation, Conditional Formatting & What-If Financial Analysis'
        ]
    )

    # Module 2
    render_module(
        2,
        'SQL for Data Analysis & Relational Databases',
        [
            'Relational Database Architecture, Schema Design, Normalization, Primary/Foreign Keys',
            'Complex Querying: Multi-Table INNER/LEFT/RIGHT/FULL JOINs, Subqueries, and CTEs',
            'Analytical Window Functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE, LEAD/LAG',
            'Aggregations, Grouping Sets, HAVING clauses, and Real-world Query Optimization'
        ]
    )

    # Module 3
    render_module(
        3,
        'Python Programming for Data Analytics',
        [
            'Python Foundations: Data structures (Lists, Tuples, Dictionaries), Control Flow, Functions',
            'NumPy Computing: Vectorized array operations, matrix mathematics, indexing & slicing',
            'Pandas DataFrames: Reading CSV/Excel/SQL, Filtering, Handling Missing/Duplicate records',
            'Automated Data Transformation, Aggregations, GroupBy pipelines, and Scripted Reporting'
        ]
    )

    # Module 4
    render_module(
        4,
        'Power BI Business Intelligence & Interactive Dashboards',
        [
            'End-to-End ETL with Power Query: Cleansing, Unpivoting, Merging & Appending Queries',
            'Relational Data Modeling: Star Schema, Snowflake Schema, 1-to-Many Relationships',
            'DAX Measures: CALCULATE, FILTER, ALL, RELATED, Date-Time Intelligence (YTD, MTD, YoY)',
            'Executive Visualization: Drill-through reports, interactive slicers, KPI visual cards'
        ]
    )

    # Module 5
    render_module(
        5,
        'Tableau Visual Storytelling & Dashboards',
        [
            'Connecting to Varied Sources (Files, Relational Databases, Cloud Warehouses)',
            'Visual Dimensions vs Measures, Discrete vs Continuous data attributes',
            'Calculated Fields, Table Calculations, User Parameters, and Custom Sets',
            'Multi-layer Interactive Dashboards, Action Filters, and Executive Storyboards'
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
