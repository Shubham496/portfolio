import openpyxl
from collections import defaultdict
import datetime

file_path = r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)

def analyze_sheet(ws_name):
    ws = wb[ws_name]
    print(f"\n========================================================")
    print(f"ANALYZING SHEET: {ws_name}")
    print(f"========================================================")
    
    batches = []
    current_batch = None
    
    for r in range(1, ws.max_row + 1):
        c1 = ws.cell(r, 1).value
        c2 = ws.cell(r, 2).value
        
        # Check if batch title
        c1_str = str(c1).strip() if c1 is not None else ""
        c2_str = str(c2).strip() if c2 is not None else ""
        
        # Check if line is batch title
        is_title = False
        bname = None
        for kw in ["batch", "powerbi", "python", "excel", "sql", "project", "statistics", "librar"]:
            if kw in c1_str.lower() and not any(x in c1_str.lower() for x in ["student", "sid"]):
                is_title = True
                bname = c1_str + (f" - {c2_str}" if c2_str else "")
                break
            elif kw in c2_str.lower() and not any(x in c2_str.lower() for x in ["student", "sid", "name"]):
                is_title = True
                bname = (f"{c1_str} - " if c1_str else "") + c2_str
                break
                
        if is_title:
            if current_batch:
                batches.append(current_batch)
            current_batch = {
                "name": bname,
                "title_row": r,
                "header_row": None,
                "date_cols": {}, # col_idx -> date_val
                "notes_col": None,
                "students": []
            }
            continue
            
        if current_batch:
            # Check if this row is header row (contains SID / Student ID / Name / Dates)
            if current_batch["header_row"] is None:
                if any(x in c1_str.lower() for x in ["student", "sid", "id"]) or any(x in c2_str.lower() for x in ["name"]):
                    current_batch["header_row"] = r
                    # find date cols
                    for c in range(1, ws.max_column + 1):
                        val = ws.cell(r, c).value
                        if val is not None:
                            val_str = str(val).strip()
                            if "note" in val_str.lower():
                                current_batch["notes_col"] = c
                            elif c >= 3 and not any(x in val_str.lower() for x in ["student", "sid", "name", "id", "column1"]):
                                current_batch["date_cols"][c] = val
                            elif "column1" in val_str.lower() and c > 3:
                                # sometimes a blank or date column
                                current_batch["date_cols"][c] = val
                    continue
            
            # If header is found, check if this is a student row
            # If row is empty, skip
            row_has_val = any(ws.cell(r, c).value is not None for c in range(1, ws.max_column + 1))
            if not row_has_val:
                continue
                
            sid = ws.cell(r, 1).value
            name = ws.cell(r, 2).value
            
            # If name is None and sid is None, skip
            if sid is None and name is None:
                continue
                
            # If name is None but sid is a string that looks like a title, break/continue
            if isinstance(sid, str) and any(kw in sid.lower() for kw in ["batch", "powerbi", "python", "excel", "sql"]):
                continue
                
            notes_val = ws.cell(r, current_batch["notes_col"]).value if current_batch["notes_col"] else None
            
            # Read attendance
            att_records = {}
            for col_idx, dval in current_batch["date_cols"].items():
                cell_v = ws.cell(r, col_idx).value
                if cell_v is not None:
                    att_records[col_idx] = str(cell_v).strip().upper()
                else:
                    att_records[col_idx] = None
                    
            current_batch["students"].append({
                "row": r,
                "sid": sid,
                "name": str(name).strip() if name is not None else "",
                "notes": notes_val,
                "att": att_records
            })
            
    if current_batch:
        batches.append(current_batch)
        
    return batches

batches_sheet1 = analyze_sheet("Sheet1")
print(f"Total batches found in Sheet1: {len(batches_sheet1)}")
for b in batches_sheet1:
    print(f"Batch: {b['name']} | Row {b['title_row']} | Header Row {b['header_row']} | Dates count: {len(b['date_cols'])} | Students: {len(b['students'])}")
