import openpyxl
from collections import defaultdict
import datetime
import re

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
            "att_seq": att_seq,
            "row": r
        })

if current_batch:
    batches.append(current_batch)

# Build a unified student directory connecting by SID and Name
# If a name has a known SID, map that name to the SID
name_to_sid = {}
for b in batches:
    for s in b["students"]:
        if s["sid"] and s["name"]:
            norm_name = s["name"].lower().strip()
            name_to_sid[norm_name] = s["sid"]

# Also map first names if unique
first_name_to_sid = {}
first_name_counts = defaultdict(set)
for norm_name, sid in name_to_sid.items():
    fn = norm_name.split()[0]
    first_name_counts[fn].add(sid)
for fn, sids in first_name_counts.items():
    if len(sids) == 1:
        first_name_to_sid[fn] = list(sids)[0]

def resolve_student_id(sid, name):
    if sid:
        return sid
    norm = name.lower().strip()
    if norm in name_to_sid:
        return name_to_sid[norm]
    fn = norm.split()[0] if norm else ""
    if fn in first_name_to_sid:
        return first_name_to_sid[fn]
    return f"NAME:{norm}"

# Group student records
student_records = defaultdict(list)
for b_idx, b in enumerate(batches):
    for s in b["students"]:
        st_id = resolve_student_id(s["sid"], s["name"])
        student_records[st_id].append({
            "batch_idx": b_idx,
            "batch_name": b["name"],
            "subject": b["subject"],
            "row": s["row"],
            "sid": s["sid"] or st_id,
            "name": s["name"],
            "p": s["p"], "a": s["a"], "o": s["o"],
            "attended": s["attended"],
            "total_days": s["total_days"],
            "att_seq": "".join([x[1] for x in s["att_seq"]]),
            "start_date": str(s["att_seq"][0][0])[:10] if s["att_seq"] else ""
        })

print("="*100)
print(f"ANALYSIS OF STUDENTS REPEATING THE SAME SUBJECT/BATCH")
print("="*100)

results = []

for st_id, records in student_records.items():
    # group by subject
    by_subj = defaultdict(list)
    for r in records:
        by_subj[r["subject"]].append(r)
        
    for subj, subj_recs in by_subj.items():
        if len(subj_recs) > 1:
            subj_recs = sorted(subj_recs, key=lambda x: x["batch_idx"])
            # check attendance in the earlier batch(es)
            # We want students who attended "few classes" in their earlier batch(es)
            results.append({
                "st_id": st_id,
                "name": subj_recs[0]["name"],
                "subject": subj,
                "batches": subj_recs
            })

print(f"Total students enrolled in multiple batches of same subject: {len(results)}\n")

# Sort into:
# Group A: Attended few classes (<= 4 classes) in batch 1 and then repeating in batch 2
# Group B: Attended few classes in batch 2 (dropped out in repeat)
# Group C: Attended substantial classes in both (e.g. revision / project class / regular dual attendance)

for r in results:
    b1 = r["batches"][0]
    b2 = r["batches"][1]
    extra = r["batches"][2:] if len(r["batches"]) > 2 else []
    
    # Classify
    print(f"Student: {r['name']} (ID: {r['st_id']}) — Subject: {r['subject']}")
    for i, b in enumerate(r["batches"]):
        print(f"   Batch {i+1}: {b['batch_name']} (Row {b['row']})")
        print(f"     Start: {b['start_date']} | Attended: {b['attended']} / {b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Sequence: {b['att_seq']}")
    print("-" * 80)
