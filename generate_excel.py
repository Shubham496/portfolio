import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Let's import our existing extraction logic to get exact clean data
from final_categorized import few_classes_repeats, other_repeats

wb_new = openpyxl.Workbook()

# Setup styles
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill_blue = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
header_fill_navy = PatternFill(start_color="203764", end_color="203764", fill_type="solid")
header_fill_green = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")

title_font = Font(name="Calibri", size=16, bold=True, color="1F4E79")
subtitle_font = Font(name="Calibri", size=11, italic=True, color="595959")
section_font = Font(name="Calibri", size=13, bold=True, color="203764")

bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)
italic_font = Font(name="Calibri", size=9, italic=True)

thin_border_side = Side(border_style="thin", color="D9D9D9")
thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

double_bottom_border = Border(
    left=thin_border_side, right=thin_border_side, top=thin_border_side,
    bottom=Side(border_style="double", color="1F4E79")
)

# Striping fills
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
highlight_green = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # Success
highlight_yellow = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # Moderate
highlight_red = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # Chronic dropout

# Alignments
align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")
align_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)

# -------------------------------------------------------------
# SHEET 1: Few Classes & Repeated (Primary focus)
# -------------------------------------------------------------
ws1 = wb_new.active
ws1.title = "Early Dropouts & Repeaters"
ws1.views.sheetView[0].showGridLines = True

# Title block
ws1.cell(1, 1, "DUCAT ATTENDANCE ANALYSIS: STUDENTS REPEATING BATCHES AFTER FEW CLASSES").font = title_font
ws1.cell(2, 1, "Students who attended <= 4 classes in their initial batch, dropped out, and re-enrolled in another batch of the same subject").font = subtitle_font

headers_sheet1 = [
    "S.No", "Student Name", "Student ID", "Subject",
    "Batch 1 Name", "Batch 1 Start", "Attended (B1)", "Total Days (B1)", "Attendance % (B1)", "Attendance Sequence (B1)",
    "Batch 2 Name (Repeat)", "Batch 2 Start", "Attended (B2)", "Total Days (B2)", "Attendance % (B2)", "Attendance Sequence (B2)",
    "Repeat Outcome & Remarks"
]

header_row_idx = 4
for col_idx, header in enumerate(headers_sheet1, 1):
    cell = ws1.cell(header_row_idx, col_idx, header)
    cell.font = header_font
    cell.fill = header_fill_blue
    cell.alignment = align_center
    cell.border = thin_border
ws1.row_dimensions[header_row_idx].height = 28

row_num = header_row_idx + 1

def determine_outcome(b1_att, b2_att, b2_days, subj, name):
    pct2 = (b2_att / b2_days * 100) if b2_days > 0 else 0
    if pct2 >= 70 or b2_att >= 15:
        return "Success: Successfully completed the course on second attempt", highlight_green
    elif b2_att <= 2:
        return "Chronic Dropout: Attended <= 2 classes again in repeat batch", highlight_red
    elif b2_att <= 4:
        return "Partial Repeat: Dropped out again after few classes in repeat batch", highlight_yellow
    else:
        return "Improved: Significant improvement in repeat attendance", highlight_green

for s_idx, cluster in enumerate(few_classes_repeats, 1):
    name = next(c["name"] for c in cluster if c["name"])
    sid = next((c["sid"] for c in cluster if c["sid"]), "N/A")
    subj = cluster[0]["subject"]
    
    b1 = cluster[0]
    b2 = cluster[1] if len(cluster) > 1 else cluster[0]
    
    pct1 = round((b1["attended"] / b1["total_days"]) * 100, 1) if b1["total_days"] > 0 else 0
    pct2 = round((b2["attended"] / b2["total_days"]) * 100, 1) if b2["total_days"] > 0 else 0
    
    # Custom remarks
    if b1["row"] == 129 and b2["row"] == 137:
        outcome, outcome_fill = "Repeated in same batch: re-entered from absent to present", highlight_yellow
    else:
        outcome, outcome_fill = determine_outcome(b1["attended"], b2["attended"], b2["total_days"], subj, name)
    
    fill = zebra_fill if s_idx % 2 == 0 else white_fill
    
    vals = [
        (s_idx, align_center),
        (name, align_left),
        (sid, align_center),
        (subj, align_center),
        (b1["batch_name"], align_left),
        (b1["start_date"], align_center),
        (b1["attended"], align_center),
        (b1["total_days"], align_center),
        (f"{pct1}%", align_right),
        (b1["att_str"], align_left),
        (b2["batch_name"], align_left),
        (b2["start_date"], align_center),
        (b2["attended"], align_center),
        (b2["total_days"], align_center),
        (f"{pct2}%", align_right),
        (b2["att_str"], align_left),
        (outcome, align_left)
    ]
    
    for c_idx, (v, al) in enumerate(vals, 1):
        cell = ws1.cell(row_num, c_idx, v)
        cell.font = regular_font
        cell.alignment = al
        cell.border = thin_border
        if c_idx == 17:
            cell.fill = outcome_fill
        else:
            cell.fill = fill
            
    ws1.row_dimensions[row_num].height = 20
    row_num += 1

# -------------------------------------------------------------
# SHEET 2: All Same-Subject Repeats (Comprehensive)
# -------------------------------------------------------------
ws2 = wb_new.create_sheet(title="All Same-Subject Repeats")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(1, 1, "ALL STUDENTS ENROLLED IN MULTIPLE BATCHES OF THE SAME SUBJECT").font = title_font
ws2.cell(2, 1, "Complete log of every student appearing in 2 or more batches of the same course (including dropouts, refresher attendees, and project classes)").font = subtitle_font

headers_sheet2 = [
    "S.No", "Student Name", "Student ID", "Subject", "Batch Number",
    "Batch Name", "Start Date", "Present (P)", "Online (O)", "Absent (A)", "Attended Days", "Total Classes", "Attendance %", "Attendance Pattern"
]

header_row_idx2 = 4
for col_idx, header in enumerate(headers_sheet2, 1):
    cell = ws2.cell(header_row_idx2, col_idx, header)
    cell.font = header_font
    cell.fill = header_fill_navy
    cell.alignment = align_center
    cell.border = thin_border
ws2.row_dimensions[header_row_idx2].height = 28

row_num2 = header_row_idx2 + 1
global_idx = 1

all_clusters = few_classes_repeats + other_repeats
# Sort by student name
all_clusters = sorted(all_clusters, key=lambda c: next(x["name"] for x in c if x["name"]).lower())

for cluster in all_clusters:
    name = next(c["name"] for c in cluster if c["name"])
    sid = next((c["sid"] for c in cluster if c["sid"]), "N/A")
    subj = cluster[0]["subject"]
    
    cluster_fill = zebra_fill if global_idx % 2 == 0 else white_fill
    
    for b_num, b in enumerate(cluster, 1):
        pct = round((b["attended"] / b["total_days"]) * 100, 1) if b["total_days"] > 0 else 0
        vals = [
            (global_idx if b_num == 1 else "", align_center),
            (name if b_num == 1 else f'"{name}" (cont.)', align_left),
            (sid if b_num == 1 else "", align_center),
            (subj if b_num == 1 else "", align_center),
            (f"Batch {b_num}", align_center),
            (b["batch_name"], align_left),
            (b["start_date"], align_center),
            (b["p"], align_center),
            (b["o"], align_center),
            (b["a"], align_center),
            (b["attended"], align_center),
            (b["total_days"], align_center),
            (f"{pct}%", align_right),
            (b["att_str"], align_left)
        ]
        
        for c_idx, (v, al) in enumerate(vals, 1):
            cell = ws2.cell(row_num2, c_idx, v)
            cell.font = regular_font
            cell.alignment = al
            cell.border = thin_border
            cell.fill = cluster_fill
            
        ws2.row_dimensions[row_num2].height = 20
        row_num2 += 1
    global_idx += 1

# -------------------------------------------------------------
# SHEET 3: Subject & Pattern Summary
# -------------------------------------------------------------
ws3 = wb_new.create_sheet(title="Subject Summary & KPI")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(1, 1, "EXECUTIVE SUMMARY: REPEAT PATTERNS BY SUBJECT").font = title_font
ws3.cell(2, 1, "Aggregated analysis of student retention, dropouts, and repeat behavior across subjects").font = subtitle_font

headers_sheet3 = [
    "Subject / Course", "Total Unique Repeaters", "Early Dropouts (<=4 Classes in Batch 1)",
    "Chronic Dropouts (<=2 in Batch 2)", "Successful Course Completers", "Refresher / Project Class Attendees"
]

header_row_idx3 = 4
for col_idx, header in enumerate(headers_sheet3, 1):
    cell = ws3.cell(header_row_idx3, col_idx, header)
    cell.font = header_font
    cell.fill = header_fill_green
    cell.alignment = align_center
    cell.border = thin_border
ws3.row_dimensions[header_row_idx3].height = 28

# Compile stats
subj_stats = {
    "PowerBI": {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0},
    "Python": {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0},
    "Excel": {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0},
    "SQL": {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0},
    "Libraries": {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0},
}

for cluster in all_clusters:
    subj = cluster[0]["subject"]
    if subj not in subj_stats:
        subj_stats[subj] = {"total": 0, "early_dropout": 0, "chronic": 0, "completed": 0, "refresher": 0}
    subj_stats[subj]["total"] += 1
    
    b1 = cluster[0]
    b2 = cluster[1] if len(cluster) > 1 else cluster[0]
    
    if b1["attended"] <= 4:
        subj_stats[subj]["early_dropout"] += 1
        if b2["attended"] <= 2:
            subj_stats[subj]["chronic"] += 1
        elif b2["attended"] >= 15 or (b2["total_days"] > 0 and b2["attended"] / b2["total_days"] >= 0.7):
            subj_stats[subj]["completed"] += 1
    else:
        subj_stats[subj]["refresher"] += 1

row_num3 = header_row_idx3 + 1
for subj, st in subj_stats.items():
    vals = [
        (subj, align_left, bold_font),
        (st["total"], align_center, regular_font),
        (st["early_dropout"], align_center, regular_font),
        (st["chronic"], align_center, regular_font),
        (st["completed"], align_center, regular_font),
        (st["refresher"], align_center, regular_font)
    ]
    fill = zebra_fill if (row_num3 % 2 == 0) else white_fill
    for c_idx, (v, al, f) in enumerate(vals, 1):
        cell = ws3.cell(row_num3, c_idx, v)
        cell.font = f
        cell.alignment = al
        cell.border = thin_border
        cell.fill = fill
    ws3.row_dimensions[row_num3].height = 22
    row_num3 += 1

# Total row
total_vals = [
    ("Total", align_left, bold_font),
    (sum(s["total"] for s in subj_stats.values()), align_center, bold_font),
    (sum(s["early_dropout"] for s in subj_stats.values()), align_center, bold_font),
    (sum(s["chronic"] for s in subj_stats.values()), align_center, bold_font),
    (sum(s["completed"] for s in subj_stats.values()), align_center, bold_font),
    (sum(s["refresher"] for s in subj_stats.values()), align_center, bold_font)
]
for c_idx, (v, al, f) in enumerate(total_vals, 1):
    cell = ws3.cell(row_num3, c_idx, v)
    cell.font = f
    cell.alignment = al
    cell.border = double_bottom_border
    cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
ws3.row_dimensions[row_num3].height = 24

# Auto-adjust column widths across all sheets
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            # ignore title rows for width calculation
            if cell.row in [1, 2]:
                continue
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

# Specific column tuning for Sheet 1
ws1.column_dimensions["A"].width = 7
ws1.column_dimensions["B"].width = 20
ws1.column_dimensions["C"].width = 13
ws1.column_dimensions["D"].width = 12
ws1.column_dimensions["E"].width = 26
ws1.column_dimensions["J"].width = 24
ws1.column_dimensions["K"].width = 24
ws1.column_dimensions["P"].width = 24
ws1.column_dimensions["Q"].width = 50

# Save files
desktop_path = r"C:\Users\Hp\Desktop\Repeated_Batches_Analysis.xlsx"
workspace_path = r"f:\Projects\coding\Repeated_Batches_Analysis.xlsx"

wb_new.save(desktop_path)
wb_new.save(workspace_path)

print(f"Successfully saved Excel file to:\n1. {desktop_path}\n2. {workspace_path}")
