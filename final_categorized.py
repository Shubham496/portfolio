import openpyxl
from collections import defaultdict

file_path = r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)
ws = wb["Sheet1"]

def get_subject(bname):
    bname_lower = bname.lower()
    if "python" in bname_lower: return "Python"
    if "powerbi" in bname_lower or "power bi" in bname_lower: return "PowerBI"
    if "excel" in bname_lower: return "Excel"
    if "sql" in bname_lower: return "SQL"
    if "librar" in bname_lower: return "Libraries"
    if "statistic" in bname_lower: return "Statistics"
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

# Check all students:
# Let's collect every student entry
all_entries = []
for b_idx, b in enumerate(batches):
    for s in b["students"]:
        all_entries.append({
            "batch_idx": b_idx,
            "batch_name": b["name"],
            "subject": b["subject"],
            "row": s["row"],
            "sid": s["sid"],
            "name": s["name"],
            "p": s["p"], "a": s["a"], "o": s["o"],
            "attended": s["attended"],
            "total_days": s["total_days"],
            "att_str": "".join([x[1] for x in s["att_seq"]]),
            "start_date": str(s["att_seq"][0][0])[:10] if s["att_seq"] else ""
        })

# Pairwise check if two entries belong to the same student in the SAME subject
# Criteria:
# 1. Matching non-empty SID
# 2. Or matching full name (case insensitive, trimmed)
# 3. Or name is identical and one has SID and other doesn't

pairs = []
seen_pairs = set()

for i in range(len(all_entries)):
    for j in range(i + 1, len(all_entries)):
        e1 = all_entries[i]
        e2 = all_entries[j]
        
        if e1["subject"] != e2["subject"]:
            continue
            
        is_same = False
        match_reason = ""
        
        # SID match
        if e1["sid"] and e2["sid"] and e1["sid"] == e2["sid"]:
            is_same = True
            match_reason = f"Same SID ({e1['sid']})"
        elif e1["name"] and e2["name"]:
            n1 = e1["name"].lower().strip()
            n2 = e2["name"].lower().strip()
            if n1 == n2:
                is_same = True
                match_reason = f"Exact Name Match ('{e1['name']}')"
            # specific known full name match
            elif n1 in ["aditya agrawal", "aditya"] and n2 in ["aditya agrawal", "aditya"] and (e1["sid"] == "20251" or e2["sid"] == "20251" or e1["sid"] == e2["sid"]):
                is_same = True
                match_reason = "Aditya Agrawal match"
            elif n1 in ["yogesh thalor", "yogesh"] and n2 in ["yogesh thalor", "yogesh"] and (e1["sid"] == "20274" or e2["sid"] == "20274" or e1["sid"] == e2["sid"]):
                is_same = True
                match_reason = "Yogesh Thalor match"
            elif n1 in ["kuldeep singh", "kuldeep"] and n2 in ["kuldeep singh", "kuldeep"] and (e1["sid"] == "20263" or e2["sid"] == "20263"):
                is_same = True
                match_reason = "Kuldeep Singh match"
                
        if is_same:
            key = tuple(sorted([e1["row"], e2["row"]]))
            if key not in seen_pairs:
                seen_pairs.add(key)
                pairs.append((e1, e2, match_reason))

# Group connected components of entries
adj = defaultdict(set)
for e1, e2, r in pairs:
    adj[e1["row"]].add(e2["row"])
    adj[e2["row"]].add(e1["row"])

row_to_entry = {e["row"]: e for e in all_entries}

visited = set()
student_clusters = []
for r in adj:
    if r not in visited:
        cluster = []
        q = [r]
        visited.add(r)
        while q:
            curr = q.pop(0)
            cluster.append(row_to_entry[curr])
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)
        student_clusters.append(cluster)

print(f"Total verified students repeating batches in the same subject: {len(student_clusters)}\n")

# Now let's analyze who attended "few classes" (<= 4 classes attended) in their earlier batch!
few_classes_repeats = []
other_repeats = []

for cluster in student_clusters:
    # Sort cluster by batch_idx (chronological)
    sorted_cluster = sorted(cluster, key=lambda x: x["batch_idx"])
    # Check if the earlier batch had few classes attended (<= 4 classes attended, or <= 30% attendance)
    # Most batches have 7 to 28 classes. Attending 1-4 classes then dropping out is classic Ducat repeat behavior.
    b1 = sorted_cluster[0]
    b2 = sorted_cluster[1]
    
    if b1["attended"] <= 4:
        few_classes_repeats.append(sorted_cluster)
    else:
        other_repeats.append(sorted_cluster)

print("="*80)
print("CATEGORY 1: STUDENTS WHO ATTENDED FEW CLASSES (<= 4) IN FIRST BATCH AND REPEATED IN A LATER BATCH")
print("="*80)

for cluster in few_classes_repeats:
    name = next(c["name"] for c in cluster if c["name"])
    sid = next((c["sid"] for c in cluster if c["sid"]), "N/A")
    subj = cluster[0]["subject"]
    print(f"\nStudent: {name} (SID: {sid}) | Subject: {subj}")
    for idx, b in enumerate(cluster):
        print(f"  Batch {idx+1}: {b['batch_name']} (Row {b['row']})")
        print(f"    Start: {b['start_date']} | Attended: {b['attended']}/{b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Seq: {b['att_str']}")

print("\n" + "="*80)
print("CATEGORY 2: STUDENTS WHO ATTENDED MORE CLASSES IN FIRST BATCH BUT REPEATED / RE-ATTENDED")
print("="*80)

for cluster in other_repeats:
    name = next(c["name"] for c in cluster if c["name"])
    sid = next((c["sid"] for c in cluster if c["sid"]), "N/A")
    subj = cluster[0]["subject"]
    print(f"\nStudent: {name} (SID: {sid}) | Subject: {subj}")
    for idx, b in enumerate(cluster):
        print(f"  Batch {idx+1}: {b['batch_name']} (Row {b['row']})")
        print(f"    Start: {b['start_date']} | Attended: {b['attended']}/{b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Seq: {b['att_str']}")
