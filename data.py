import xlrd
import openpyxl
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import timeit
import xlsxwriter

# file to be processed: Raw_data_and_steps_Diabetes_data.xlsx
# Replace 0 with empty cell


def replace_empty(lists):
    table_len = len(lists)
    element_len = len(lists[0])
    for y in range(table_len):
        for x in range(element_len):
            if lists[y][x] == 0:
                lists[y][x] = None


# create a new empty xlsx file
# def new_file():
#     workbook = xlsxwriter.Workbook('new_file.xlsx')
#     worksheet = workbook.add_worksheet()
#     for x in range()
#         worksheet.write(0,0)
#     workbook.close()

# create calculated data from original table
def new_file_calculated(lists, cols):
    workbook = xlsxwriter.Workbook('calculated_data_2.xlsx')
    worksheet = workbook.add_worksheet()

    for x in range(cols):
        worksheet.write_column(0, x, lists[x])
    workbook.close()

# Read the data and calculate
def readData(str):
    # Load excel file to calculate
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
    rows = ws.nrows
    cols = ws.ncols
    table = []
    count = 0

    # calculate data - Blank
    for y in range(cols):
        record = []
        count += 1
        for x in range(rows):
            if 0 < y < 16:
                if isinstance(ws.cell(x, y).value, float) and isinstance(ws.cell(x, 16).value, float):
                    record.append(ws.cell(x, y).value - ws.cell(x, 16).value)
                else:
                    record.append(ws.cell(x, y).value)
            else:
                record.append(ws.cell(x, y).value)
        new_record = record
        table.append(new_record)

    # replace 0 with empty cell
    replace_empty(table)

    # separating calculations to another xlsx file
    new_file_calculated(table, count)

    return table


# produce a new data with count
def produce_count_data(string):
    original_table = readData("Raw_data_and_steps_Diabetes_data.xlsx")
    separated_table = separating_group(original_table, string)

    if string == "Control":
        workbook = xlsxwriter.Workbook('Control_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(len(separated_table)):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()
    elif string == "Diabetes":
        workbook = xlsxwriter.Workbook('Diabetes_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(len(separated_table)):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()
    elif string == "Diabetes+Insulin":
        workbook = xlsxwriter.Workbook('Diabetes_Insulin_Group.xlsx')
        worksheet = workbook.add_worksheet()
        for x in range(len(separated_table)):
            worksheet.write_column(0, x, separated_table[x])
        workbook.close()
    else:
        print("Please Try Again!")


# Build a GUI to automatically calculate and generate a new separated file
def tkinter_window():

    window = Tk()
    # frame = Frame(window)
    window.title("Calculating Metabolomic Data")

    window.geometry('500x200')

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Calculate Step 1")
    tab_control.pack(expand=YES, fill="both")

    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Separate Group")

    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Check Percentage")

    # tab 1
    lbl = Label(tab1, text="Excel File Name")
    lbl.pack(padx=2, pady=2)

    txt = Entry(tab1, width=40)
    txt.pack(padx=2, pady=2)

    # generate a new xlsx file
    def clicked():
        res = "File has been entered."
        readData(txt.get())
        messagebox.showinfo('Success!', res)

    btn = Button(tab1, text="Generate", command=clicked)
    btn.pack(padx=5, pady=5)

    # tab 2
    lbl_2 = Label(tab2, text="Group Name")
    lbl_2.pack(padx=2, pady=2)

    txt_2 = Entry(tab2, width=40)
    txt_2.pack(padx=2, pady=2)

    def separate():
        res = "Group name has been entered"
        failed_msg = 'There is no such group. Please try again'
        text = txt_2.get()
        # if text != 'Control' or text != 'Diabetes' or text != 'Diabetes+Insulin':
        #     messagebox.showinfo('Failed!', failed_msg)
        if text == "Control" or text == "Diabetes" or text == "Diabetes+Insulin":
            produce_count_data(text)
            messagebox.showinfo('Success!', res)

    btn_2 = Button(tab2, text="Generate", command=separate)
    btn_2.pack(padx=5, pady=5)

    # tab 3 - check percentage
    lbl_3 = Label(tab3, text="Group Name")
    lbl_3.pack(padx=2, pady=2)

    txt_3 = Entry(tab3, width=40)
    txt_3.pack(padx=2,pady=2)

    def check():
        text = txt_3.get()
        res = "Perfect! The file is being processed."
        failed = "Either the group does not exist or the file have not been created. Please try again."
        if text == "Control":
            check_percentage("Control_Group.xlsx")
            messagebox.showinfo('Success!', res)
        elif text == "Diabetes":
            check_percentage("Diabetes_Group.xlsx")
            messagebox.showinfo('Success!', res)
        elif text == "Diabetes+Insulin":
            check_percentage("Diabetes_Insulin_Group.xlsx")
            messagebox.showinfo('Success!', res)
        else:
            messagebox.showinfo('Failed!', failed)

    btn_3 = Button(tab3, text="Generate", command=check)
    btn_3.pack(padx=5, pady=5)

    window.mainloop()


# separate group
def separating_group(table, string):
    count = 0
    tab = []

    for y in range(len(table)):
        record = []
        if table[y][0] == string:
            for x in range(len(table[1])):
                if isinstance(table[y][x], float) or table[y][x] is None:
                    record.append(table[y][x])
            new_record = record
            tab.append(new_record)

    count_table = []
    for x in range(len(tab[0])):
        count = 0
        for y in range(len(tab)):
            if tab[y][x] is not None:
                count += 1
        count_table.append(count)

    tab.append(count_table)
    return tab


# check if over 65%, if yes -> keep. If not, empty cells in row
def check_percentage(string):
    wb = openpyxl.load_workbook(filename=string)
    sheet = wb['Sheet1']
    row = sheet.max_row
    column = sheet.max_column
    for x in range(1, row + 1):
        if sheet.cell(row=x, column=6).value/5.0 < 0.65:
            sheet.cell(row=x, column=6).value = 0
            for y in range(1, column):
                sheet.cell(row=x, column=y).value = None

    wb.save(string)


tkinter_window()
