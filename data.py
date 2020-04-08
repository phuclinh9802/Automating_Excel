import xlrd
import openpyxl
import cython_runtime
from tkinter import *
import xlsxwriter

def new_file_calculated(list, cols):
    workbook = xlsxwriter.Workbook('calculated_data.xlsx')
    worksheet = workbook.add_worksheet()

    for x in range(cols):
        worksheet.write_column(0, x, list[x])

    workbook.close()

def readData(str):
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
    rows= ws.nrows
    cols = ws.ncols
    table = []
    # for y in range(cols):
    #     record.clear()
    #     for x in range(rows):
    #         if isinstance(ws.cell(x,y).value, float) and isinstance(ws.cell(x,16).value, float) and y != 16:
    #             record.append(ws.cell(x,y).value - ws.cell(x, 16).value)
    #     table.append(record)

    # for x in range(rows):
    #     if isinstance(ws.cell(x,0).value, float) and isinstance(ws.cell(x,16).value, float):
    #         record.append(ws.cell(x,0).value - ws.cell(x, 16).value)
    # print(record)
    for y in range(cols):
        if y != 16:
            record = []
            for x in range(rows):
                if isinstance(ws.cell(x,y).value, float) and isinstance(ws.cell(x,16).value, float):
                    record.append(ws.cell(x,y).value - ws.cell(x, 16).value)
            new_record = record
            table.append(new_record)

    # separating calculations to another xlsx file
    new_file_calculated(table, cols - 1)

readData('Raw_data_and_steps_Diabetes_data.xlsx')


