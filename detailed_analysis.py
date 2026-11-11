import openpyxl
from collections import defaultdict
import datetime

file_path = r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)
ws = wb["Sheet1"]

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
                            pass
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
            
        att_day_by_day = []
        p_cnt, a_cnt, o_cnt = 0, 0, 0
        for col_idx, dval in current_batch["dates"]:
            cell_v = ws.cell(r, col_idx).value
            status = str(cell_v).strip().upper() if cell_v is not None else "-"
            att_day_by_day.append((dval, status))
            if status == "P": p_cnt += 1
            elif status == "A": a_cnt += 1
            elif status == "O": o_cnt += 1
            
        current_batch["students"].append({
            "sid": str(sid).strip() if sid is not None else "",
            "name": str(name).strip() if name is not None else "",
            "row": r,
            "p": p_cnt,
            "a": a_cnt,
            "o": o_cnt,
            "attended": p_cnt + o_cnt,
            "total_days": len(current_batch["dates"]),
            "day_by_day": att_day_by_day
        })

if current_batch:
    batches.append(current_batch)

# Now link students by ID or clean name
# Create student directory
all_students = defaultdict(list)
for b_idx, b in enumerate(batches):
    for s in b["students"]:
        key = s["sid"] if s["sid"] else s["name"].lower()
        all_students[key].append({
            "batch_idx": b_idx,
            "batch_name": b["name"],
            "subject": b["subject"],
            "sid": s["sid"],
            "name": s["name"],
            "p": s["p"],
            "a": s["a"],
            "o": s["o"],
            "attended": s["attended"],
            "total_days": s["total_days"],
            "day_by_day": s["day_by_day"],
            "row": s["row"]
        })

# Let's inspect all candidates where a student appears in multiple batches of the same subject
print("\n" + "="*80)
print("CANDIDATES: STUDENTS REPEATING SAME SUBJECT/BATCH")
print("="*80)

for key, entries in all_students.items():
    # group by subject
    by_subj = defaultdict(list)
    for e in entries:
        by_subj[e["subject"]].append(e)
    for subj, subj_entries in by_subj.items():
        if len(subj_entries) > 1:
            # Check if any entry had few classes attended (e.g. <= 4 attended)
            has_few = any(e["attended"] <= 4 for e in subj_entries)
            print(f"\nStudent: '{subj_entries[0]['name']}' (Key: {key}) | Subject: {subj} | Total Batches in Subject: {len(subj_entries)}")
            for idx, e in enumerate(subj_entries):
                att_str = "".join([s[1] for s in e["day_by_day"]])
                first_date = str(e["day_by_day"][0][0])[:10] if e["day_by_day"] else "?"
                print(f"  Batch {idx+1}: {e['batch_name']}")
                print(f"    StartDate: {first_date} | Attended: {e['attended']} / {e['total_days']} (P={e['p']}, O={e['o']}, A={e['a']})")
                print(f"    Attendance sequence: {att_str}")
