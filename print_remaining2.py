import detailed_analysis

keys = list(detailed_analysis.all_students.keys())
idx_568 = keys.index('20568')
print("Keys total:", len(keys), "Keys after 20568:", len(keys) - idx_568 - 1)

for key in keys[idx_568+1:]:
    entries = detailed_analysis.all_students[key]
    by_subj = detailed_analysis.defaultdict(list)
    for e in entries:
        by_subj[e["subject"]].append(e)
    for subj, subj_entries in by_subj.items():
        if len(subj_entries) > 1:
            print(f"\nStudent: '{subj_entries[0]['name']}' (Key: {key}) | Subject: {subj} | Total Batches in Subject: {len(subj_entries)}")
            for idx, e in enumerate(subj_entries):
                att_str = "".join([s[1] for s in e["day_by_day"]])
                first_date = str(e["day_by_day"][0][0])[:10] if e["day_by_day"] else "?"
                print(f"  Batch {idx+1}: {e['batch_name']}")
                print(f"    StartDate: {first_date} | Attended: {e['attended']} / {e['total_days']} (P={e['p']}, O={e['o']}, A={e['a']})")
                print(f"    Attendance sequence: {att_str}")
