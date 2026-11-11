import openpyxl
from analyze_attendance import analyze_sheet, wb

batches_att = analyze_sheet("Attendence")
print(f"Total batches found in Attendence: {len(batches_att)}")
for b in batches_att:
    print(f"Batch: {b['name']} | Row {b['title_row']} | Header Row {b['header_row']} | Dates count: {len(b['date_cols'])} | Students: {len(b['students'])}")
