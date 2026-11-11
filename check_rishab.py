import openpyxl

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)
ws = wb["Sheet1"]

for r in [143, 144, 145, 153, 154, 155]:
    vals = [ws.cell(r, c).value for c in range(1, 10)]
    print(f"Row {r}: {vals}")
