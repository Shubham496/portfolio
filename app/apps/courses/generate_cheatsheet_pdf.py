"""
MYTHOS 7 Primitives of Tabular Data Analysis Cheat Sheet Generator
Generates a publication-grade, 2-page A4 reference PDF using fpdf2.
"""

import os
from fpdf import FPDF
from app.core.config import settings


class MythosCheatSheetPDF(FPDF):
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
        self.cell(95, 8, 'DATA ANALYTICS COHORT | ARCHITECTURAL REFERENCE', align='R')
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
        self.cell(50, 6, 'MYTHOS DATA ANALYTICS', align='L')

        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(71, 85, 105)
        self.cell(105, 6, f'Admissions: {settings.BUSINESS_EMAIL} | WhatsApp: +91 {settings.BUSINESS_WHATSAPP}', align='C')

        self.set_font('Helvetica', 'B', 7.5)
        self.set_text_color(100, 116, 139)
        self.cell(35, 6, f'Page {self.page_no()}', align='R')


def _draw_primitive_card(pdf: FPDF, y_pos: float, num: int, title: str, subtitle: str, badge: str,
                         accent_rgb: tuple, sql_code: str, pandas_code: str, excel_code: str, bi_code: str,
                         card_h: float = 49.0):
    """Renders a structured 4-column comparison card for one tabular primitive."""
    # Outer box
    pdf.set_xy(10, y_pos)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_line_width(0.35)
    pdf.rect(10, y_pos, 190, card_h, 'DF')

    # Accent left border strip
    pdf.set_fill_color(*accent_rgb)
    pdf.rect(10, y_pos, 2.5, card_h, 'F')

    # Card Top Header
    pdf.set_xy(14, y_pos + 2.0)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(130, 4.5, f"{num}. {title.upper()}", align='L')

    # Pill Badge on Right
    badge_w = 40
    pdf.set_xy(156, y_pos + 2.0)
    pdf.set_fill_color(241, 245, 249)  # Slate 100
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.2)
    pdf.rect(156, y_pos + 2.0, badge_w, 4.5, 'DF')
    pdf.set_font('Helvetica', 'B', 6.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(badge_w, 4.5, badge, align='C')

    # Subtitle / Conceptual Action
    pdf.set_xy(14, y_pos + 6.8)
    pdf.set_font('Helvetica', 'I', 7.2)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(180, 3.5, subtitle, align='L')

    # 4-Column Syntax Comparison Box
    cols_y = y_pos + 11.0
    col_w = 46.0
    gap = 1.3
    start_x = 13.5
    col_h = card_h - 13.0

    columns_data = [
        ("SQL", (37, 99, 235), sql_code),           # Blue
        ("Pandas (Python)", (15, 118, 110), pandas_code), # Teal
        ("Excel", (22, 101, 52), excel_code),        # Green
        ("Power BI / M", (180, 83, 9), bi_code),     # Amber
    ]

    for i, (tool_name, header_rgb, code_text) in enumerate(columns_data):
        cx = start_x + (i * (col_w + gap))
        # Inner column box
        pdf.set_fill_color(248, 250, 252)  # Slate 50
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.25)
        pdf.rect(cx, cols_y, col_w, col_h, 'DF')

        # Tool Header Strip
        pdf.set_fill_color(*header_rgb)
        pdf.rect(cx, cols_y, col_w, 4.2, 'F')
        pdf.set_xy(cx, cols_y)
        pdf.set_font('Helvetica', 'B', 6.8)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_w, 4.2, tool_name, align='C')

        # Code Snippet inside
        pdf.set_xy(cx + 1.2, cols_y + 4.8)
        pdf.set_font('Courier', '', 6.0)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(col_w - 2.4, 3.0, code_text, align='L')


def generate_cheatsheet_pdf(output_path: str = "app/static/pdf/Data_Analysis_7_Primitives_CheatSheet.pdf"):
    """Builds the 2-page publication-grade reference PDF for the 7 Data Analysis Primitives."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = MythosCheatSheetPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)

    # ═════════════════════════════════════════════════════════════
    # PAGE 1: Intro Banner & Primitives 1 to 4
    # ═════════════════════════════════════════════════════════════
    pdf.add_page()

    # Document Headline
    pdf.set_y(19.5)
    pdf.set_font('Helvetica', 'B', 17)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7.5, 'The 7 Primitives of Tabular Data Analysis', align='L', new_x="LMARGIN", new_y="NEXT")

    # Subtitle
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 4.5, 'A Universal Rosetta Stone for SQL, Python (Pandas), Microsoft Excel & Power BI', align='L', new_x="LMARGIN", new_y="NEXT")

    # Tabular Invariant Strip
    inv_y = pdf.get_y() + 1.5
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    pdf.rect(10, inv_y, 190, 8.5, 'DF')
    pdf.set_fill_color(249, 115, 22)
    pdf.rect(10, inv_y, 2.0, 8.5, 'F')
    pdf.set_xy(13, inv_y + 1.2)
    pdf.set_font('Helvetica', 'B', 7.0)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(185, 3.2, 'THE TABULAR INVARIANT: Tabular data consists strictly of rows (observations) and columns (attributes).', align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(13)
    pdf.set_font('Helvetica', '', 6.8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(185, 3.0, '95% of data transformations in any tool reduce to these 7 operations. Stop memorizing endless syntax.', align='L')

    # Card 1: Add or Filter Columns
    _draw_primitive_card(
        pdf=pdf,
        y_pos=inv_y + 11.0,
        num=1,
        title="Add or Filter Columns",
        subtitle="Vertical Slicing & Feature Engineering: Keep, discard, or compute new attributes row-by-row.",
        badge="Single-Table Slice",
        accent_rgb=(37, 99, 235),
        sql_code="SELECT id, name,\n  price * qty AS total\nFROM orders;",
        pandas_code="df[['id', 'name']]\ndf['total'] = (\n  df['price'] * df['qty']\n)",
        excel_code="=[@Price]*[@Qty]\n=CHOOSECOLS(\n  Orders, 1, 3\n)",
        bi_code="Power Query:\n* Choose Columns\n* Add Custom Column\nDAX: Total = P * Q",
        card_h=46.0
    )

    # Card 2: Add or Filter Rows
    _draw_primitive_card(
        pdf=pdf,
        y_pos=inv_y + 59.0,
        num=2,
        title="Add or Filter Rows",
        subtitle="Horizontal Slicing & Sampling: Restrict observations via boolean conditions, Top N, or deduplication.",
        badge="Single-Table Slice",
        accent_rgb=(16, 185, 129),
        sql_code="SELECT * FROM orders\nWHERE status='Active'\nLIMIT 50;",
        pandas_code="df[df['status']=='Act']\ndf.query(\"status=='A'\")\ndf.head(50)",
        excel_code="=FILTER(Orders,\n  Orders[Status]=\"Act\")\nCtrl+Shift+L",
        bi_code="Power Query:\n* Filter Rows\n* Keep Top Rows (50)\nDAX: FILTER(T, cond)",
        card_h=46.0
    )

    # Card 3: Order by Columns
    _draw_primitive_card(
        pdf=pdf,
        y_pos=inv_y + 107.0,
        num=3,
        title="Order by Columns",
        subtitle="Positional Sorting: Arrange observations ascending or descending across one or multiple columns.",
        badge="Single-Table Sort",
        accent_rgb=(147, 51, 234),
        sql_code="SELECT * FROM orders\nORDER BY status ASC,\n  order_date DESC;",
        pandas_code="df.sort_values(\n  by=['status','date'],\n  ascending=[True,False]\n)",
        excel_code="=SORTBY(Orders,\n  Orders[Status], 1,\n  Orders[Date], -1)",
        bi_code="Power Query:\n* Sort Ascending\n* Sort Descending\nModel: Sort By Column",
        card_h=46.0
    )

    # Card 4: Group & Aggregate
    _draw_primitive_card(
        pdf=pdf,
        y_pos=inv_y + 155.0,
        num=4,
        title="Group & Aggregate",
        subtitle="Dimensional Collapse: Bucket rows by dimensions & compute scalar aggregates (SUM, COUNT, AVG, MIN, MAX).",
        badge="Multi-Row Collapse",
        accent_rgb=(234, 88, 12),
        sql_code="SELECT category,\n  COUNT(*) AS cnt,\n  SUM(amt) AS rev\nGROUP BY category;",
        pandas_code="df.groupby('cat').agg(\n  cnt=('id','count'),\n  rev=('amt','sum')\n).reset_index()",
        excel_code="Pivot Table Rows/Vals\n=SUMIFS(C:C, A:A, \"X\")\n=COUNTIFS(...)",
        bi_code="Power Query:\n* Transform > Group By\nDAX Measures:\nRev = SUM(Sales[Amt])",
        card_h=46.0
    )

    # ═════════════════════════════════════════════════════════════
    # PAGE 2: Primitives 5 to 7 & Production Truth & Diagnostic
    # ═════════════════════════════════════════════════════════════
    pdf.add_page()

    # Page 2 Sub-banner
    pdf.set_y(19.5)
    pdf.set_font('Helvetica', 'B', 13.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6.0, 'Multi-Table Combinations, Reshaping & Production Truth', align='L', new_x="LMARGIN", new_y="NEXT")

    p2_y = 27.0

    # Card 5: Attach Table Below Another
    _draw_primitive_card(
        pdf=pdf,
        y_pos=p2_y,
        num=5,
        title="Attach Table Below Another (Stack / Append)",
        subtitle="Vertical Union: Schema alignment to stack more observations. Requires identical column names/types.",
        badge="Multi-Table Append",
        accent_rgb=(13, 148, 136),
        sql_code="SELECT * FROM q1\nUNION ALL\nSELECT * FROM q2;",
        pandas_code="pd.concat(\n  [df_q1, df_q2],\n  axis=0,\n  ignore_index=True\n)",
        excel_code="=VSTACK(Q1_Tbl, Q2_Tbl)\nCopy-paste stack",
        bi_code="Power Query:\n* Home > Append\n  Queries as New\n*(Vertical schema bind)",
        card_h=44.0
    )

    # Card 6: Attach Table Side by Side
    _draw_primitive_card(
        pdf=pdf,
        y_pos=p2_y + 46.0,
        num=6,
        title="Attach Table Side by Side (Merge / Join)",
        subtitle="Horizontal Enrichment: Match records between Primary Key & Foreign Key (Inner, Left, Right, Full Outer).",
        badge="Multi-Table Join",
        accent_rgb=(79, 70, 229),
        sql_code="SELECT o.*, c.name\nFROM orders o\nLEFT JOIN cust c\n  ON o.c_id = c.id;",
        pandas_code="pd.merge(\n  orders, cust,\n  on='c_id',\n  how='left'\n)",
        excel_code="=XLOOKUP([@c_id],\n  Cust[id], Cust[name])\n=HSTACK(T1, T2)",
        bi_code="Power Query:\n* Merge Queries (Left)\nData Model: 1-to-Many\nrelationship drag line",
        card_h=44.0
    )

    # Card 7: Pivot and Unpivot
    _draw_primitive_card(
        pdf=pdf,
        y_pos=p2_y + 92.0,
        num=7,
        title="Pivot and Unpivot (Dimensional Reshaping)",
        subtitle="Reshaping: Pivot (Tall -> Wide for human reports) vs Unpivot (Wide -> Tall for BI columnar engines).",
        badge="Reshaping",
        accent_rgb=(217, 70, 239),
        sql_code="SELECT rep,\n  SUM(CASE WHEN q='Q1'\n    THEN val END) AS Q1\nGROUP BY rep;",
        pandas_code="# Pivot: df.pivot_table()\n# Unpivot (Melt):\ndf.melt(id_vars=['rep'],\n  var_name='qtr')",
        excel_code="Pivot Table Columns\nPower Query:\n* Transform > Unpivot\n  Other Columns",
        bi_code="Power Query:\n* Unpivot Columns\n*(Critical for Star\nSchema optimization)",
        card_h=44.0
    )

    # Production Truth Section
    prod_y = p2_y + 138.5
    pdf.set_xy(10, prod_y)
    pdf.set_fill_color(254, 242, 242)  # Red 50
    pdf.set_draw_color(252, 165, 165)
    pdf.set_line_width(0.35)
    pdf.rect(10, prod_y, 190, 48.0, 'DF')
    pdf.set_fill_color(220, 38, 38)
    pdf.rect(10, prod_y, 2.5, 48.0, 'F')

    pdf.set_xy(14, prod_y + 2.0)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(180, 4.0, 'SKIPPED FOUNDATIONS & PRODUCTION TRUTH (WHAT INTERNET TUTORIALS OMIT)', align='L')

    truths = [
        ("UNION ALL vs UNION (Primitive 5):", "UNION performs an implicit DISTINCT across all columns, triggering an expensive disk sort and hash deduplication pass. In production pipelines, always default to UNION ALL unless duplicate removal is required."),
        ("Cartesian Explosion & Non-Unique Join Keys (Primitive 6):", "If the right lookup table contains duplicate keys, a LEFT JOIN silently duplicates left-hand rows, corrupting financial metrics (SUM/COUNT). Always verify key uniqueness before joining."),
        ("Wide vs Tall Data (Primitive 7):", "Human spreadsheets prefer Wide formats (12 monthly columns), but columnar engines (Power BI VertiPaq, DuckDB, Pandas) compress tall, unpivoted columns up to 10x better. Never load wide reports into Power BI - always unpivot first.")
    ]

    ty = prod_y + 7.5
    for title_txt, body_txt in truths:
        pdf.set_xy(14, ty)
        pdf.set_font('Helvetica', 'B', 7.2)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(180, 3.2, title_txt, align='L', new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(14)
        pdf.set_font('Helvetica', '', 6.7)
        pdf.set_text_color(71, 85, 105)
        pdf.multi_cell(182, 3.0, body_txt, align='L')
        ty += 13.0

    # 3-Step Decision Heuristic Box
    heur_y = prod_y + 50.0
    pdf.set_xy(10, heur_y)
    pdf.set_fill_color(240, 253, 250)  # Teal 50
    pdf.set_draw_color(153, 246, 228)
    pdf.set_line_width(0.3)
    pdf.rect(10, heur_y, 190, 24.0, 'DF')
    pdf.set_fill_color(13, 148, 136)
    pdf.rect(10, heur_y, 2.5, 24.0, 'F')

    pdf.set_xy(14, heur_y + 1.8)
    pdf.set_font('Helvetica', 'B', 8.0)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(180, 3.8, 'THE 3-STEP PROBLEM-SOLVING DIAGNOSTIC', align='L')

    steps = [
        ("Step 1 (Source Tables):", "Does answer exist in 1 table? If NO -> Adding rows? Use Primitive 5 (UNION ALL). Adding attributes? Use Primitive 6 (JOIN)."),
        ("Step 2 (Aggregation):", "Need atomic records? Use Primitives 1, 2, 3 (SELECT, WHERE, ORDER BY). Need summary metrics? Use Primitive 4 (GROUP BY)."),
        ("Step 3 (Reshaping):", "Need a human-readable summary matrix? Use Primitive 7 (PIVOT). Feeding a dashboard or data model? Use Primitive 7 (UNPIVOT).")
    ]

    sy = heur_y + 6.0
    for s_title, s_desc in steps:
        pdf.set_xy(14, sy)
        pdf.set_font('Helvetica', 'B', 6.8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(32, 3.2, s_title, align='L')
        pdf.set_font('Helvetica', '', 6.8)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(150, 3.2, s_desc, align='L')
        sy += 5.5

    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    generate_cheatsheet_pdf()
