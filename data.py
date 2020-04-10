import xlrd
import openpyxl
import cython_runtime
from tkinter import *
from tkinter import messagebox
import timeit
import xlsxwriter



# file to be processed: Raw_data_and_steps_Diabetes_data.xlsx

# Replace 0 with empty cell
def replace_empty(list):
    table_len = len(list)
    element_len = len(list[0])
    for y in range(table_len):
        for x in range(element_len):
            if list[y][x] == 0:
                list[y][x] = None


def new_file_calculated(list, cols):
    workbook = xlsxwriter.Workbook('calculated_data_1.xlsx')
    worksheet = workbook.add_worksheet()

    for x in range(cols):
        worksheet.write_column(0, x, list[x])
    workbook.close()

# Read the data and calculate
def readData(str):
    # Load excel file to calculate
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
    rows= ws.nrows
    cols = ws.ncols
    table = []
    count = 0

    # calculate data - Blank
    for y in range(cols):
        if y > 0 and y < 16:
            count += 1
            record = []
            for x in range(rows):
                if isinstance(ws.cell(x,y).value, float) and isinstance(ws.cell(x,16).value, float):
                    record.append(ws.cell(x,y).value - ws.cell(x, 16).value)
            new_record = record
            table.append(new_record)

    # replace 0 with empty cell
    replace_empty(table)

    # separating calculations to another xlsx file
    new_file_calculated(table, count)

# Build a GUI to automatically calculate and generate a new separated file
def tkinter_window():

    window = Tk()
    frame = Frame(window)

    window.title("Calculating Metabolomic Data")

    window.geometry('600x100')

    lbl = Label(frame, text="Excel File Name")
    lbl.grid()

    txt = Entry(frame, width=40)
    txt.grid()

    def clicked():
        start = timeit.default_timer()
        res = "File has been entered."
        messagebox.showinfo('Success!', res)
        readData(txt.get())
        stop = timeit.default_timer()
        print("Time: ", stop - start)

    btn = Button(frame, text="Generate", command=clicked)

    btn.grid()

    frame.grid(row=0, column=0, sticky="NESW")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.mainloop()




tkinter_window()




