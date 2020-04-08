import openpyxl
cpdef test(string data_name):
    wb = openpyxl.load_workbook(data_name)
    print(wb.sheetnames[0])

