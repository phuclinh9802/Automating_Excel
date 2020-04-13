import xlrd
import openpyxl
import cython_runtime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
    workbook = xlsxwriter.Workbook('calculated_data_2.xlsx')
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
        record = []
        count += 1
        for x in range(rows):
            if y > 0 and y < 16:
                if isinstance(ws.cell(x,y).value, float) and isinstance(ws.cell(x,16).value, float):
                    record.append(ws.cell(x,y).value - ws.cell(x, 16).value)
                else:
                    record.append(ws.cell(x,y).value)
            else:
                record.append(ws.cell(x,y).value)
        new_record = record
        table.append(new_record)

    # replace 0 with empty cell
    replace_empty(table)

    # separating calculations to another xlsx file
    new_file_calculated(table, count)

    return table

# procuce a new data with count
def produce_count_data(str):
    original_table = readData("Raw_data_and_steps_Diabetes_data.xlsx")
    separated_table = separating_group(original_table, str)

    if str == "Control":
        workbook = xlsxwriter.Workbook('Control_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(separated_table):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()
    elif str == "Diabetes":
        workbook = xlsxwriter.Workbook('Diabetes_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(separated_table):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()
    elif str == "Diabetes+Insulin":
        workbook = xlsxwriter.Workbook('Diabetes_Insulin_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(separated_table):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()



# Build a GUI to automatically calculate and generate a new separated file
def tkinter_window():

    window = Tk()
    # frame = Frame(window)
    window.title("Calculating Metabolomic Data")

    window.geometry('500x200')

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Calculate Step 1")
    tab_control.pack(expand=1, fill="both")

    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Separate Group")

    # tab 1
    lbl = Label(tab1, text="Excel File Name")
    lbl.pack()

    txt = Entry(tab1, width=40)
    txt.pack()

    # generate a new xlsx file
    def clicked():
        start = timeit.default_timer()
        res = "File has been entered."
        messagebox.showinfo('Success!', res)
        readData(txt.get())
        stop = timeit.default_timer()
        print("Time: ", stop - start)

    btn = Button(tab1, text="Generate", command=clicked)
    btn.pack()

    # tab 2
    lbl_2 = Label(tab2, text="Group Name")
    lbl_2.pack()

    txt_2 = Entry(tab2, width=40)
    txt_2.pack()

    def separate():
        res = "Group name has been entered"
        failed_msg = 'There is no such group. Please try again'
        if txt_2.get() != 'Control' or txt_2.get() != 'Diabetes' or txt_2.get() != 'Diabetes+Insulin':
            messagebox.showInfo('Failed!', failed_msg)
        else:
            messagebox.showinfo('Success!', res)
            produce_count_data(txt_2.get())

    btn_2 = Button(tab2, text="Generate", command=separate)
    btn_2.pack()

    window.mainloop()


# separate group
def separating_group(table, str):
    count = 0
    tab = []
    for y in range(table):
        record = []
        if table[y][0] == str:
            for x in range(table[0]):
                if isinstance(table[x][y], float):
                    record.append(table[x][y])
            new_record = record
            tab.append(new_record)

    count_table = []
    for x in range(tab[0]):
        count = 0
        for y in range(tab):
            if tab[x][y] is not None:
                count += 1
        count_table.append(count)

    tab.append(count_table)

    return tab


tkinter_window()



