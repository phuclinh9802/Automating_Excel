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
import math


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


# Read group data only
def read_group_data(str):
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
    rows = ws.nrows
    cols = ws.ncols
    table = []
    count = 0

    for y in range(cols):
        record = []
        if y < cols - 1:
            for x in range(rows):
                record.append(ws.cell(x, y).value)
            new_record = record
            table.append(new_record)


    return table

# Read group data with average: 1. Control 2. Diabetes 3. Diabetes+Insulin
def read_group_data_with_average(str):
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

    tab5 = ttk.Frame(tab_control)
    tab_control.add(tab5, text="Get p value")

    tab6 = ttk.Frame(tab_control)
    tab_control.add(tab6, text="Up/Down-regulated")


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
    lbl_2 = Label(tab2, text="Group Name: Control, Diabetes, Diabetes+Insulin")
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
    lbl_3 = Label(tab3, text="Group Name: Control, Diabetes, Diabetes+Insulin")
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
        res = "Perfect! The file is being processed."
        final_table = []
        # produce data after checking percentage in tables
        control_table = read_group_data_with_average("Control_Group.xlsx")
        diabetes_table = read_group_data_with_average("Diabetes_Group.xlsx")
        diabetes_insulin_table = read_group_data_with_average("Diabetes_Insulin_Group.xlsx")


        # append to a big table
        for x in range(len(control_table)):
            final_table.append(control_table[x])
        for x in range(1, len(diabetes_table)):
            final_table.append(diabetes_table[x])
        for x in range(1, len(diabetes_insulin_table)):
            final_table.append(diabetes_insulin_table[x])

        save_csv(final_table)
        messagebox.showinfo('Success!', res)
        stop = timeit.default_timer()
        print('Time: ', stop - start)

    btn_4 = Button(tab4, text="Generate", command=final)
    btn_4.pack(padx=5, pady=5)

    # tab 5 - get p value
    lbl_5 = Label(tab5, text="Get p value - C: Control, D: Diabetes; DI: Diabetes+Insulin")
    lbl_5.pack(padx=2, pady=2)

    txt_5 = Entry(tab5, width=20)
    txt_5.pack(padx=2, pady=2)

    txt_5_2 = Entry(tab5, width=20)
    txt_5_2.pack(padx=2, pady=2)

    v = IntVar()
    radio_1 = Radiobutton(tab5, text="p value only", variable=v, value=0)
    radio_1.pack(anchor=W)
    radio_2 = Radiobutton(tab5, text="p and log2", variable=v, value=1)
    radio_2.pack(anchor=W)

    # generate file based on entry
    def pval():
        res = "File has been generated"
        failed = "Please enter the correct group"
        if v.get() == 0:
            if (txt_5.get() == "C" and txt_5_2.get() == "D") or (txt_5.get() == "D" and txt_5_2.get() == "C"):
                produce_combine_p("Control_Group.xlsx", "Diabetes_Group.xlsx", 0)
                messagebox.showinfo('Success!', res)
            elif (txt_5.get() == "C" and txt_5_2.get() == "DI") or (txt_5.get() == "DI" and txt_5_2.get() == "C"):
                produce_combine_p("Control_Group.xlsx", "Diabetes_Insulin_Group.xlsx", 0)
                messagebox.showinfo('Success!', res)
            elif (txt_5.get() == "D" and txt_5_2.get() == "DI") or (txt_5.get() == "DI" and txt_5_2.get() == "D"):
                produce_combine_p("Diabetes_Group.xlsx", "Diabetes_Insulin_Group.xlsx", 0)
                messagebox.showinfo('Success!', res)
            else:
                messagebox.showerror("Error", failed)
        if v.get() == 1:
            if (txt_5.get() == "C" and txt_5_2.get() == "D") or (txt_5.get() == "D" and txt_5_2.get() == "C"):
                produce_combine_p("Control_Group.xlsx", "Diabetes_Group.xlsx", 1)
                messagebox.showinfo('Success!', res)
            elif (txt_5.get() == "C" and txt_5_2.get() == "DI") or (txt_5.get() == "DI" and txt_5_2.get() == "C"):
                produce_combine_p("Control_Group.xlsx", "Diabetes_Insulin_Group.xlsx", 1)
                messagebox.showinfo('Success!', res)
            elif (txt_5.get() == "D" and txt_5_2.get() == "DI") or (txt_5.get() == "DI" and txt_5_2.get() == "D"):
                produce_combine_p("Diabetes_Group.xlsx", "Diabetes_Insulin_Group.xlsx", 1)
                messagebox.showinfo('Success!', res)
            else:
                messagebox.showerror("Error", failed)

    btn_5 = Button(tab5, text="Generate", command=pval)
    btn_5.pack(padx=5, pady=5)

    # tab 6
    lbl_6 = Label(tab6, text="Group Name: Control, Diabetes, Diabetes+Insulin")
    lbl_6.pack(padx=2, pady=2)

    b = IntVar()
    radio_cd = Radiobutton(tab6, text="Control - Diabetes", variable=b, value=0)
    radio_cd.pack(anchor=W)
    radio_cdi = Radiobutton(tab6, text="Control - Diabetes+Insulin", variable=b, value=1)
    radio_cdi.pack(anchor=W)
    radio_ddi = Radiobutton(tab6, text="Diabetes - Diabetes+Insulin", variable=b, value=2)
    radio_ddi.pack(anchor=W)

    a = IntVar()
    radio_up = Radiobutton(tab6, text="Up-regulated", variable=a, value=0)
    radio_up.pack(anchor=W)
    radio_down = Radiobutton(tab6, text="Down-regulated", variable=a, value=1)
    radio_down.pack(anchor=W)

    # generate up-regulated / down-regulated file based on radio choice
    def up_down():
        table = []
        res = "Yes! You have successfully generated the file"
        failed = "Please try again"
        if a.get() == 0:
            if b.get() == 0:
                table = up_down_regulated("C_DM1_p_value_log2.xlsx", 0)
                workbook = xlsxwriter.Workbook('Up (C x DM1).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            elif b.get() == 1:
                table = up_down_regulated("C_DM1+I_p_value_log2.xlsx", 0)
                workbook = xlsxwriter.Workbook('Up (C x DM1+I).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            elif b.get() == 2:
                table = up_down_regulated("D_DM1+I_p_value_log2.xlsx", 0)
                workbook = xlsxwriter.Workbook('Up (D x DM1+I).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            else:
                messagebox.showerror("Failed!", failed)
        elif a.get() == 1:
            if b.get() == 0:
                table = up_down_regulated("C_DM1_p_value_log2.xlsx", 1)
                workbook = xlsxwriter.Workbook('Down (C x DM1).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            elif b.get() == 1:
                table = up_down_regulated("C_DM1+I_p_value_log2.xlsx", 1)
                workbook = xlsxwriter.Workbook('Down (C x DM1+I).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            elif b.get() == 2:
                table = up_down_regulated("D_DM1+I_p_value_log2.xlsx", 1)
                workbook = xlsxwriter.Workbook('Down (D x DM1+I).xlsx')
                worksheet = workbook.add_worksheet()
                for x in range(len(table)):
                    worksheet.write_column(0, x, table[x])
                workbook.close()
                messagebox.showinfo("Success!", res)
            else:
                messagebox.showerror("Failed!", failed)
        else:
            messagebox.showerror("Failed!", failed)

    btn_6 = Button(tab6, text="Generate", command=up_down)
    btn_6.pack(padx=5, pady=5)
    window.mainloop()

# abbreviation
def abbreviation(table, string):
    if string == "Control":
       table.append("C")
    elif string == "Diabetes":
        table.append("DM1")
    elif string == "Diabetes+Insulin":
        table.append("DM1+I")

# separate group
def separating_group(table, string):
    count = 0
    tab = []
    original_table = read_data("Raw_data_and_steps_Diabetes_data.xlsx")[0]
    slicing = slice(1, len(original_table))
    tab.append(original_table[slicing])

    for y in range(len(table)):
        record = []
        if table[y][0] == string:
            abbreviation(record, string)
            for x in range(len(table[1])):
                if isinstance(table[y][x], float) or table[y][x] is None:
                    record.append(table[y][x])
            new_record = record
            tab.append(new_record)

    count_table = ["Count"]
    for x in range(1, len(tab[0])): # not counting first row - title row
        count = 0
        for y in range(1, len(tab)): # not counting first column - m/z column
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
    for x in range(2, row + 1):
        if sheet.cell(row=x, column=7).value/5.0 < 0.65:
            sheet.cell(row=x, column=7).value = 0
            for y in range(2, column):
                sheet.cell(row=x, column=y).value = None

    wb.save(string)


# save to csv file
def save_csv(table):
    export_data = zip_longest(*table, fillvalue='')
    with open('final_data.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        # writer.writerow(("m/z","C", "C", "C", "C", "C", "Avg", "D", "D", "D", "D", "D", "Avg", "D+I", "D+I", "D+I", "D+I", "D+I", "Avg"))
        writer.writerows(export_data)
    file.close()


# average of group data : Control_Group.xlsx, Diabetes_Group.xlsx, Diabetes_Insulin_Group.xlsx
def calculate_average(string):
    wb = openpyxl.load_workbook(filename=string)
    sheet = wb['Sheet1']
    row = sheet.max_row
    column = sheet.max_column
    col = []
    col.append("AVG")
    for x in range(2, row + 1):
        average = 0.0
        for y in range(2, column):
            if sheet.cell(row=x, column=y).value is not None:
                average = average + sheet.cell(row=x, column=y).value
        average = average / 5.0
        col.append(average)

    change_to_1(col)
    wb.save(string)

    return col


# change avg column to 1 if avg element = 0
def change_to_1(table):
    for x in range(len(table)):
        if table[x] == 0:
            table[x] = 1

    return table


# calculate log_2 of average of 2 group data
def calculate_log(str1, str2):
    avg_1 = calculate_average(str1)
    avg_2 = calculate_average(str2)

    log_col = []

    for x in range(len(avg_1)):
        log = get_log(avg_1[x], avg_2[x])
        log_col.append(log)

    return log_col


# change back empty cells to 0
def change_to_zero(table):
    # print(len(table))
    # print(len(table[0]))
    for x in range(len(table)):
        for y in range(len(table[0])):
            if table[x][y] == "":
                table[x][y] = 0


# test p value calculation
def test_p(data_1, data_2):
    mean1 = np.mean(data_1)
    mean2 = np.mean(data_2)
    # get std error
    se1 = sem(data_1)
    se2 = sem(data_2)
    # standard error on the difference between the samples
    sed = np.sqrt(se1 ** 2.0 + se2 ** 2.0)
    if sed == 0:
        return None
    # calculate T Statistic
    t_stat = (mean1 - mean2) / sed
    # degrees of freedom
    df = len(data_1) + len(data_2) - 2
    # calculate the p-value
    p = (1.0 - t.cdf(abs(t_stat), df))
    return p


# get m/z column
def get_mz_col():
    return read_group_data("Control_Group.xlsx")[0]


# p value to compare 2 groups
def get_p_value(str1, str2):
    # read data from specific groups
    table_1 = read_group_data(str1)
    slicing1 = slice(1, len(table_1))
    table_1 = table_1[slicing1]

    table_2 = read_group_data(str2)
    slicing2 = slice(1, len(read_group_data(str2)))
    table_2 = table_2[slicing2]

    # change None to 0 cell
    change_to_zero(table_1)
    change_to_zero(table_2)

    # p value calculation
    p_col = []

    # get each row
    data_1 = get_row(table_1)
    data_2 = get_row(table_2)
    # print(test_p(data_1[0], data_2[0]))
    for x in range(len(data_1)):
        p = test_p(data_1[x], data_2[x])
        p_col.append(p)

    return p_col


# test get log2
def get_log(a1, a2):
    return np.log2(a1) - np.log2(a2)


# combine p value with 2 group data
def produce_combine_p(str1, str2, type):
    # initialize table to combine data
    group_1 = ""
    group_2 = ""
    if str1 == "Control_Group.xlsx":
        group_1 = "C"
    elif str2 == "Control_Group.xlsx":
        group_2 = "C"
    if str1 == "Diabetes_Group.xlsx":
        group_1 = "DM1"
    elif str2 == "Diabetes_Group.xlsx":
        group_2 = "DM1"
    if str1 == "Diabetes_Insulin_Group.xlsx":
        group_1 = "DM1+I"
    elif str2 == "Diabetes_Insulin_Group.xlsx":
        group_2 = "DM1+I"

    table = []

    table.append(get_mz_col())
    # read data from specific groups
    table_1 = read_group_data(str1)
    table_2 = read_group_data(str2)

    # append each column into the table
    # str1 data
    for x in range(1, len(table_1)):
        # insert name of group at the first row
        table_1[x].insert(0, group_1)
        table.append(table_1[x])

    # str1 average data
    avg_1 = calculate_average(str1)
    change_to_1(avg_1)
    avg_1.insert(0, "AVG")
    table.append(avg_1)

    # str2 data
    for x in range(1, len(table_2)):
        table_2[x].insert(0, group_2)
        table.append(table_2[x])

    # str2 average data
    avg_2 = calculate_average(str2)
    change_to_1(avg_2)
    avg_2.insert(0, "AVG")
    table.append(avg_2)

    # change None to 0 cell
    change_to_zero(table_1)
    change_to_zero(table_2)

    # append p_value column
    p_col = get_p_value(str1, str2)
    p_col.insert(0, "p_value")
    table.append(p_col)

    # New workbook xlsx file
    # p value only
    if type == 0:
        produce_file_p_log(table, str1, str2, type)

    # both p value and log
    elif type == 1:
        log_col = calculate_log(str1, str2)
        str_log = "LOG2FC " + group_1 + "/" + group_2
        log_col.insert(0, str_log)
        table.append(log_col)
        produce_file_p_log(table, str1, str2, type)


# decide if up-regulated or down-regulated
def up_down_regulated(file, up_or_down):
    table = read_all_data(file)
    change_to_zero(table)

    # keep track of index
    i = 1
    # if up-regulated
    if up_or_down == 0:
        # loop to put data to the correct list
        # for y in range(len(table[0]) - 1):

        while i < len(table[0]):
            if table[len(table) - 2][i] == 0 and table[len(table) - 1][i] == 0:
                for x in table:
                    del x[i]
            elif table[len(table) - 2][i] >= 0.05 or table[len(table) - 1][i] <= 0.5849:
                for x in table:
                    del x[i]
            else:
                i += 1

    # [[2,3,4,5], [3,4,5,6], [2,4,5,6]]
    # [[3,4,5], [4,5,6], [4,5,6]] - i = 1

    # if down-regulated
    elif up_or_down == 1:
        # loop to put data to the correct list
        while i < len(table[0]):
            if table[len(table) - 2][i] == 0 and table[len(table) - 1][i] == 0:
                for x in table:
                    del x[i]
            elif table[len(table) - 2][i] >= 0.05 or table[len(table) - 1][i] >= -0.5849:
                for x in table:
                    del x[i]
            else:
                i += 1
    return table


# convert data to table (all files can be converted)
def read_all_data(file):
    wb = xlrd.open_workbook(file)
    ws = wb.sheet_by_index(0)
    rows = ws.nrows
    cols = ws.ncols
    table = []
    for y in range(cols):
        record = []
        for x in range(rows):
            record.append(ws.cell(x, y).value)
        new_record = record
        table.append(new_record)

    return table

# produce data in new file with p value or p value and log
def produce_file_p_log(table, str1, str2, type):
    if type == 0:
        if str1 == "Control_Group.xlsx" and str2 == "Diabetes_Group.xlsx":
            workbook = xlsxwriter.Workbook('C_DM1_p_value.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()
        elif str1 == "Control_Group.xlsx" and str2 == "Diabetes_Insulin_Group.xlsx":
            workbook = xlsxwriter.Workbook('C_DM1+I_p_value.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()
        elif str1 == "Diabetes_Group.xlsx" and str2 == "Diabetes_Insulin_Group.xlsx":
            workbook = xlsxwriter.Workbook('D_DM1+I_p_value.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()
    elif type == 1:
        if str1 == "Control_Group.xlsx" and str2 == "Diabetes_Group.xlsx":
            workbook = xlsxwriter.Workbook('C_DM1_p_value_log2.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()
        elif str1 == "Control_Group.xlsx" and str2 == "Diabetes_Insulin_Group.xlsx":
            workbook = xlsxwriter.Workbook('C_DM1+I_p_value_log2.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()
        elif str1 == "Diabetes_Group.xlsx" and str2 == "Diabetes_Insulin_Group.xlsx":
            workbook = xlsxwriter.Workbook('D_DM1+I_p_value_log2.xlsx')
            worksheet = workbook.add_worksheet()
            for x in range(len(table)):
                worksheet.write_column(0, x, table[x])
            workbook.close()


# get std
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

# defining function for random
# string id with parameter
# def ran_gen(size, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for x in range(size))
#
#
# # function call for random string
# # generation with size 8 and string
#
# for x in range(5):
#     print(ran_gen(1, "CD") + ran_gen(5, "0123456789"))

# print(read_data("Raw_data_and_steps_Diabetes_data.xlsx")[0])

# print(separating_group(read_data("Raw_data_and_steps_Diabetes_data.xlsx"), "Control")[0])

# print(read_group_data_with_average("Control_Group.xlsx")[6])

