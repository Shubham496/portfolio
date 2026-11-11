import openpyxl

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)
ws = wb["Sheet1"]

unique_notes = set()
for r in range(1, ws.max_row + 1):
    c3 = ws.cell(r, 3).value
    if c3 is not None:
        unique_notes.add(str(c3))

print("Unique col 3 values:", unique_notes)
