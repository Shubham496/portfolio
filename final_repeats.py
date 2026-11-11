import openpyxl
from collections import defaultdict
import datetime

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)
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
            "dates": [],
            "students": []
        }
        continue
        
    if current_batch:
        if not current_batch["dates"]:
            if any(x in c1_str.lower() for x in ["student", "sid", "id"]) or any(x in c2_str.lower() for x in ["name"]):
                for c in range(3, ws.max_column + 1):
                    val = ws.cell(r, c).value
                    if val is not None:
                        val_str = str(val).strip()
                        if "note" in val_str.lower():
                            continue
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
            
        att_seq = []
        p, a, o = 0, 0, 0
        for col_idx, dval in current_batch["dates"]:
            cell_v = ws.cell(r, col_idx).value
            status = str(cell_v).strip().upper() if cell_v is not None else "-"
            att_seq.append((dval, status))
            if status == "P": p += 1
            elif status == "A": a += 1
            elif status == "O": o += 1
            
        current_batch["students"].append({
            "sid": str(sid).strip() if sid is not None else "",
            "name": str(name).strip() if name is not None else "",
            "p": p, "a": a, "o": o, "attended": p + o,
            "total_days": len(current_batch["dates"]),
            "att_seq": att_seq
        })

if current_batch:
    batches.append(current_batch)

# Group by student
students_map = defaultdict(lambda: defaultdict(list))
student_names = {}

for b_idx, b in enumerate(batches):
    for s in b["students"]:
        key = s["sid"] if s["sid"] else s["name"].lower()
        students_map[key][b["subject"]].append({
            "batch_idx": b_idx,
            "batch_name": b["name"],
            "subject": b["subject"],
            "p": s["p"], "a": s["a"], "o": s["o"],
            "attended": s["attended"],
            "total_days": s["total_days"],
            "att_seq": "".join([x[1] for x in s["att_seq"]]),
            "start_date": str(s["att_seq"][0][0])[:10] if s["att_seq"] else ""
        })
        student_names[key] = (s["sid"], s["name"])

# Also merge by student name if different SID or missing SID
name_to_keys = defaultdict(set)
for k, (sid, name) in student_names.items():
    if name:
        name_to_keys[name.lower()].add(k)

print("TOTAL UNIQUE STUDENT KEYS:", len(students_map))

# Find students repeating the same subject
repeating_cases = []

for key, subj_dict in students_map.items():
    for subj, blist in subj_dict.items():
        if len(blist) > 1:
            sid, name = student_names[key]
            repeating_cases.append({
                "key": key,
                "sid": sid,
                "name": name,
                "subject": subj,
                "batches": blist
            })

print(f"Total repeating cases found: {len(repeating_cases)}")

# Categorize:
# Case 1: Attended few classes (<= 4 classes) in earlier batch, then enrolled in another batch of same subject
# Case 2: Attended regular classes in both batches (e.g., project class or regular refresher)
print("\n" + "="*80)
print("CASE 1: ATTENDED FEW CLASSES (<= 4) IN AN EARLIER BATCH & REPEATING IN A LATER BATCH")
print("="*80)

for c in repeating_cases:
    # Sort batches by batch_idx (chronological)
    sorted_batches = sorted(c["batches"], key=lambda x: x["batch_idx"])
    # check if any earlier batch had <= 4 attended
    earlier_had_few = any(b["attended"] <= 4 for b in sorted_batches[:-1])
    # or all had few
    if earlier_had_few:
        print(f"\nStudent: {c['name']} (SID: {c['sid']}) | Subject: {c['subject']}")
        for idx, b in enumerate(sorted_batches):
            print(f"  Batch {idx+1}: {b['batch_name']}")
            print(f"    StartDate: {b['start_date']} | Attended: {b['attended']}/{b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Pattern: {b['att_seq']}")

print("\n" + "="*80)
print("CASE 2: OTHER STUDENTS IN MULTIPLE BATCHES OF THE SAME SUBJECT")
print("="*80)
for c in repeating_cases:
    sorted_batches = sorted(c["batches"], key=lambda x: x["batch_idx"])
    earlier_had_few = any(b["attended"] <= 4 for b in sorted_batches[:-1])
    if not earlier_had_few:
        print(f"\nStudent: {c['name']} (SID: {c['sid']}) | Subject: {c['subject']}")
        for idx, b in enumerate(sorted_batches):
            print(f"  Batch {idx+1}: {b['batch_name']}")
            print(f"    StartDate: {b['start_date']} | Attended: {b['attended']}/{b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Pattern: {b['att_seq']}")
