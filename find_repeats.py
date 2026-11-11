import openpyxl
from collections import defaultdict
import re

file_path = r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)
ws = wb["Sheet1"]

# Let's map batch name to course/subject category
def get_subject(bname):
    bname_lower = bname.lower()
    if "python" in bname_lower:
        return "Python"
    if "powerbi" in bname_lower or "power bi" in bname_lower:
        return "PowerBI"
    if "excel" in bname_lower:
        return "Excel"
    if "sql" in bname_lower:
        return "SQL"
    if "librar" in bname_lower:
        return "Libraries"
    if "statistic" in bname_lower:
        return "Statistics"
    return "Other"

# Re-parse Sheet1 accurately
batches = []
current_batch = None

for r in range(1, ws.max_row + 1):
    c1 = ws.cell(r, 1).value
    c2 = ws.cell(r, 2).value
    c1_str = str(c1).strip() if c1 is not None else ""
    c2_str = str(c2).strip() if c2 is not None else ""
    
    is_title = False
    bname = None
    for kw in ["batch", "powerbi", "python", "excel", "sql", "project", "statistics", "librar"]:
        if kw in c1_str.lower() and not any(x in c1_str.lower() for x in ["student", "sid", "id"]):
            is_title = True
            bname = c1_str + (f" - {c2_str}" if c2_str else "")
            break
        elif kw in c2_str.lower() and not any(x in c2_str.lower() for x in ["student", "sid", "name", "id"]):
            is_title = True
            bname = (f"{c1_str} - " if c1_str else "") + c2_str
            break
            
    if is_title:
        if current_batch:
            batches.append(current_batch)
        current_batch = {
            "name": bname,
            "subject": get_subject(bname),
            "title_row": r,
            "header_row": None,
            "dates": [],
            "notes_col": None,
            "students": []
        }
        continue
        
    if current_batch:
        if current_batch["header_row"] is None:
            if any(x in c1_str.lower() for x in ["student", "sid", "id"]) or any(x in c2_str.lower() for x in ["name"]):
                current_batch["header_row"] = r
                for c in range(1, ws.max_column + 1):
                    val = ws.cell(r, c).value
                    if val is not None:
                        val_str = str(val).strip()
                        if "note" in val_str.lower():
                            current_batch["notes_col"] = c
                        elif c >= 3 and not any(x in val_str.lower() for x in ["student", "sid", "name", "id", "column1"]):
                            current_batch["dates"].append((c, val))
                        elif "column1" in val_str.lower() and c > 3:
                            current_batch["dates"].append((c, val))
                continue
                
        row_has_val = any(ws.cell(r, c).value is not None for c in range(1, ws.max_column + 1))
        if not row_has_val:
            continue
            
        sid = ws.cell(r, 1).value
        name = ws.cell(r, 2).value
        
        if sid is None and name is None:
            continue
        if isinstance(sid, str) and any(kw in sid.lower() for kw in ["batch", "powerbi", "python", "excel", "sql"]):
            continue
            
        notes_val = ws.cell(r, current_batch["notes_col"]).value if current_batch["notes_col"] else None
        
        att_list = []
        p_count = 0
        a_count = 0
        o_count = 0
        total_classes = 0
        
        for col_idx, dval in current_batch["dates"]:
            cell_v = ws.cell(r, col_idx).value
            if cell_v is not None:
                v = str(cell_v).strip().upper()
                att_list.append((dval, v))
                if v == "P":
                    p_count += 1
                elif v == "A":
                    a_count += 1
                elif v == "O":
                    o_count += 1
                total_classes += 1
            else:
                att_list.append((dval, None))
                
        current_batch["students"].append({
            "row": r,
            "sid": str(sid).strip() if sid is not None else None,
            "name": str(name).strip() if name is not None else "",
            "notes": str(notes_val).strip() if notes_val is not None else None,
            "p": p_count,
            "a": a_count,
            "o": o_count,
            "attended": p_count + o_count,
            "total_marked": total_classes,
            "att_list": att_list
        })

if current_batch:
    batches.append(current_batch)

# Check all students and group by student (ID and Name)
students_by_id = defaultdict(list)
students_by_name = defaultdict(list)

for b in batches:
    for s in b["students"]:
        entry = {
            "batch": b["name"],
            "subject": b["subject"],
            "title_row": b["title_row"],
            "row": s["row"],
            "sid": s["sid"],
            "name": s["name"],
            "notes": s["notes"],
            "p": s["p"],
            "a": s["a"],
            "o": s["o"],
            "attended": s["attended"],
            "total_marked": s["total_marked"],
            "att_list": s["att_list"]
        }
        if s["sid"]:
            students_by_id[s["sid"]].append(entry)
        if s["name"]:
            students_by_name[s["name"].lower()].append(entry)

print("\n========================================================")
print("1. STUDENTS APPEARING IN MULTIPLE BATCHES OF THE SAME SUBJECT")
print("========================================================")

same_subject_repeats = []
for sid, records in students_by_id.items():
    # Group records by subject
    by_subj = defaultdict(list)
    for rec in records:
        by_subj[rec["subject"]].append(rec)
    for subj, subj_recs in by_subj.items():
        if len(subj_recs) > 1:
            same_subject_repeats.append((sid, subj_recs[0]["name"], subj, subj_recs))

# Also check by name (in case SID was missing in one batch)
for name, records in students_by_name.items():
    # If already covered by SID, don't duplicate
    by_subj = defaultdict(list)
    for rec in records:
        by_subj[rec["subject"]].append(rec)
    for subj, subj_recs in by_subj.items():
        if len(subj_recs) > 1:
            # check if any SID already found
            sids = {r["sid"] for r in subj_recs if r["sid"]}
            if not any(s in [x[0] for x in same_subject_repeats] for s in sids):
                same_subject_repeats.append((str(sids), name, subj, subj_recs))

print(f"Total students appearing in multiple batches of same subject: {len(same_subject_repeats)}\n")
for sid, name, subj, recs in same_subject_repeats:
    print(f"--- Student: {name} (SID: {sid}) in Subject: {subj} (Count: {len(recs)}) ---")
    for r in recs:
        print(f"    Batch: '{r['batch']}' (Row {r['row']}) | Attended: {r['attended']} (P={r['p']}, O={r['o']}, A={r['a']}, Total marked={r['total_marked']}) | Notes: {r['notes']}")

