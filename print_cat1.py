from final_categorized import few_classes_repeats

print(f"Total students in Category 1: {len(few_classes_repeats)}")
for idx, cluster in enumerate(few_classes_repeats, 1):
    name = next(c["name"] for c in cluster if c["name"])
    sid = next((c["sid"] for c in cluster if c["sid"]), "N/A")
    subj = cluster[0]["subject"]
    print(f"\n{idx}. Student: {name} (SID: {sid}) | Subject: {subj}")
    for b_idx, b in enumerate(cluster):
        print(f"   Batch {b_idx+1}: {b['batch_name']} (Row {b['row']})")
        print(f"     Start: {b['start_date']} | Attended: {b['attended']}/{b['total_days']} (P={b['p']}, O={b['o']}, A={b['a']}) | Pattern: {b['att_str']}")
