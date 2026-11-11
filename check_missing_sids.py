import openpyxl

wb = openpyxl.load_workbook(r"C:\Users\Hp\Desktop\Attendence Ducat.xlsx", data_only=True)
ws = wb["Sheet1"]

for r in range(1, ws.max_row + 1):
    c1 = ws.cell(r, 1).value
    c2 = ws.cell(r, 2).value
    c2_str = str(c2).lower() if c2 else ""
    for name in ["hani", "shubham", "somya", "ritik", "arshad", "darshil", "kuldeep", "aditya"]:
        if name in c2_str:
            print(f"Row {r:3d}: SID={c1!r}, Name={c2!r}, Date3={ws.cell(r,3).value!r}, Date4={ws.cell(r,4).value!r}")
