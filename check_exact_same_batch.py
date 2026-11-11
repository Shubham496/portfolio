import openpyxl
from collections import defaultdict

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)
ws = wb["Sheet1"]

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
            "att_seq": "".join([x[1] for x in att_seq]),
            "row": r
        })

if current_batch:
    batches.append(current_batch)

print("="*80)
print("DUPLICATE / REPEATED STUDENTS WITHIN THE EXACT SAME BATCH")
print("="*80)

same_batch_duplicates = []
for b in batches:
    seen = defaultdict(list)
    for s in b["students"]:
        key = s["sid"] if s["sid"] else s["name"].lower()
        seen[key].append(s)
    for key, entries in seen.items():
        if len(entries) > 1:
            same_batch_duplicates.append((b["name"], entries))

for bname, entries in same_batch_duplicates:
    print(f"\nBatch: {bname}")
    for e in entries:
        print(f"  Row {e['row']}: SID={e['sid']}, Name='{e['name']}', Attended={e['attended']}/{e['total_days']} (P={e['p']}, O={e['o']}, A={e['a']}) | Seq: {e['att_seq']}")
