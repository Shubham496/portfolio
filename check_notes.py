import openpyxl

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    notes_found = []
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            val = ws.cell(r, c).value
            if val is not None and isinstance(val, str):
                v_lower = val.lower().strip()
                if any(w in v_lower for w in ["repeat", "left", "drop", "change", "rejoin", "again"]):
                    notes_found.append((r, c, val))
    print(f"Sheet {sheet_name}: matching keywords count: {len(notes_found)}")
    for item in notes_found[:20]:
        print(f"  Row {item[0]}, Col {item[1]}: {item[2]}")
