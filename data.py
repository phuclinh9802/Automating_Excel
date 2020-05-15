import xlrd
import openpyxl
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import timeit
import xlsxwriter
import csv
from itertools import zip_longest
import random
import string
import numpy as np
import scipy


# file to be processed: Raw_data_and_steps_Diabetes_data.xlsx
# Replace 0 with empty cell
from scipy.stats import sem, t


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


# Read group data only: 1. Control 2. Diabetes 3. Diabetes+Insulin
def read_group_data(str):
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
    rows = ws.nrows
    cols = ws.ncols
    table = []
    count = 0
    average_column = calculate_average(str)

    for y in range(cols):
        record = []
        if y < cols - 1:
            for x in range(rows):
                record.append(ws.cell(x,y).value)
            new_record = record
            table.append(new_record)

    # calculate average of group data in each row using openpyxl
    table.append(average_column)

    return table


# Read the data and calculate
def read_data(str):
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
                    if ws.cell(x, y).value - ws.cell(x, 16).value >=0:
                        record.append(ws.cell(x, y).value - ws.cell(x, 16).value)
                    else:
                        record.append(None)
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


# produce table only with new count (not generating new xlsx file)
def produce_table_only(string):
    original_table = read_data("Raw_data_and_steps_Diabetes_data.xlsx")
    separated_table = separating_group(original_table, string)
    return


# produce a new data with count
def produce_count_data(string):
    original_table = read_data("Raw_data_and_steps_Diabetes_data.xlsx")
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

    window.geometry('700x200')

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Calculate Step 1")
    tab_control.pack(expand=YES, fill="both")

    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Separate Group")

    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Check Percentage")

    tab4 = ttk.Frame(tab_control)
    tab_control.add(tab4, text="Final Data")

    # tab 1
    lbl = Label(tab1, text="Excel File Name")
    lbl.pack(padx=2, pady=2)

    txt = Entry(tab1, width=40)
    txt.pack(padx=2, pady=2)

    # generate a new xlsx file
    def clicked():
        res = "File has been entered."
        read_data(txt.get())
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
    #
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

    # tab 4 - save to csv
    lbl_4 = Label(tab4, text="Generate Final Data")
    lbl_4.pack(padx=2, pady=2)

    def final():
        start = timeit.default_timer()
        final_table = []
        # produce data after checking percentage in tables
        control_table = read_group_data("Control_Group.xlsx")
        diabetes_table = read_group_data("Diabetes_Group.xlsx")
        diabetes_insulin_table = read_group_data("Diabetes_Insulin_Group.xlsx")

        # append to a big table
        for x in range(len(control_table)):
            final_table.append(control_table[x])
        for x in range(len(diabetes_table)):
            final_table.append(diabetes_table[x])
        for x in range(len(diabetes_insulin_table)):
            final_table.append(diabetes_insulin_table[x])

        save_csv(final_table)
        stop = timeit.default_timer()
        print('Time: ', stop - start)

    btn_4 = Button(tab4, text="Generate", command=final)
    btn_4.pack(padx=5, pady=5)
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

    # appending the count table to count the appearance of data each row
    tab.append(count_table)

    return tab

def final_separated_table(table):
    for x in range(len(table[0])):
        if table[5][x]/5.0 < 0.65:
            table[5][x] = 0
            for y in range(0, len(table) - 1):
                table[y][x] = None

    return table


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

# save to csv file
def save_csv(table):
    export_data = zip_longest(*table, fillvalue='')
    with open('final_data.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(("C", "C", "C", "C", "C", "Avg", "D", "D", "D", "D", "D", "Avg", "D+I", "D+I", "D+I", "D+I", "D+I", "Avg"))
        writer.writerows(export_data)
    file.close()


# average of group data
def calculate_average(string):
    wb = openpyxl.load_workbook(filename=string)
    sheet = wb['Sheet1']
    row = sheet.max_row
    column = sheet.max_column
    col = []
    for x in range(1, row + 1):
        average = 0.0
        for y in range(1, column):
            if sheet.cell(row=x, column=y).value is not None:
                average = average + sheet.cell(row=x, column=y).value
        average = average / 5.0
        col.append(average)

    wb.save(string)

    return col


# change back empty cells to 0
def change_to_zero(table):
    for x in range(table):
        for y in range(table[0]):
            if (table[x][y] is None):
                table[x][y] = 0;
# p value to compare 2 groups
def get_p_value(str1, str2):
    # read data from specific groups
    table_1 = read_group_data(str1);
    table_2 = read_group_data(str2);

    # change None to 0 cell
    change_to_zero(table_1);
    change_to_zero(table_2);

    # p value calculation
    p_col = []

    # get each row
    data_1 = get_row(table_1)
    data_2 = get_row(table_2)

    for x in range(len(data_1)):
        # get mean
        mean1, mean2 = np.mean(data_1[x]), np.mean(data_2[x])
        # get std error
        se1, se2 = sem(data_1[x]), sem(data_2[x])
        # standard error on the difference between the samples
        sed = np.sqrt(se1 ** 2.0 + se2 ** 2.0)
        # calculate T Statistic
        t_stat = (mean1 - mean2) / sed
        # degrees of freedom
        df = len(data_1[x]) + len(data_2[x]) - 2
        # calculate the p-value
        p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0
        p_col.append(p)

    return p_col


#get std
def get_row(table):
    tab = []
    for x in range(len(table[0])):
        rec = []
        for y in range(len(table)):
            rec.append(table[y][x])
        new_rec = rec
        tab.append(new_rec)

    return tab







tkinter_window()

# print(read_group_data("Control_Group.xlsx")[5])

# table = [[1,2,3], [None,4,5], [None, 3,6], [3,5,6], [5,6,7], [3,5,5]]
#




# defining function for random
# string id with parameter
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


# function call for random string
# generation with size 8 and string

for x in range(5):
    print(ran_gen(1, "CD") + ran_gen(5, "0123456789"))


# test p value calculation
