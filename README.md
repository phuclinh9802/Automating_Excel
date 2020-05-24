# Automating_Excel
 Automate Excel using Python and Tkinkter to help scientists be more convenient when calculating data

This project is to help phD Researchers get more convenient when calculating large amount of molecules data
# A. Generate xlsx file to calculate Metabolomic data
## Step 1: Using xlrd library to access to the excel file: 
- "readData" function is to process the calculation with the formula of ``` result = data of each cell - blank data ```
```
  def readData(str):
    # Load excel file to calculate
    wb = xlrd.open_workbook(str)
    ws = wb.sheet_by_index(0)
```
-  These lines open the original excel file that the researchers have sent to the developers.

- ```ws = wb.sheet_by_index(0)``` opens the first worksheet in the file
- Next, we have these lines of code: 
```rows = ws.nrows
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
 ```
   - The lines below are to get number of rows and columns of the table:
   ```
      rows = ws.nrows
      cols = ws.ncols
   ``` 
   - We use nested for loop to go through each cells to calculate and update the cells in the worksheet.
   ```
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
  ```
  - Specifically:
  ```
  if isinstance(ws.cell(x, y).value, float) and isinstance(ws.cell(x, 16).value, float):
                    record.append(ws.cell(x, y).value - ws.cell(x, 16).value)
  else:
                    record.append(ws.cell(x, y).value)
  ```
  - The if statement is to check if the cell value is of type ```float``` or not.
    - If the condition satisfies, we append the difference between group data and blank data to ```record``` list
    - If not, we simply append the value available in the cell.
  - Instead of directly append the ```record``` list to ```table```, we store in another variable ```new_record```, then we append the list to the ```table```.
  - Then, we need to automate the replacement of the cell in which the value is 0.01 or 0:
  ```
  replace_empty(table)
  ```
  - Explicitly, we work on this function by using nested loop:
  ```
  def replace_empty(lists):
    table_len = len(lists)
    element_len = len(lists[0])
    for y in range(table_len):
        for x in range(element_len):
            if lists[y][x] == 0:
                lists[y][x] = None
  ```
 - The last step in ```readData(str)``` function is to generate a new "xlsx" file with new data using ```new_file_generated``` function:
 ```
 def new_file_calculated(lists, cols):
    workbook = xlsxwriter.Workbook('calculated_data_2.xlsx')
    worksheet = workbook.add_worksheet()

    for x in range(cols):
        worksheet.write_column(0, x, lists[x])
    workbook.close()
```
- We use ```xlsxwriter``` library to create a new Excel Workbook
  - ```worksheet = workbook.add_worksheet()``` is to create a new worksheet in the new xlsx file.
  - Then we implement a for loop and ```write_column``` method to write the 2-d list as columns
  - ```workbook.close()``` to save and close the newly created workbook.
 
 ## Step 2: Use tkinter library to create a GUI that generates xlsx file:
 - We have the code below:
 ```
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
 ```
 
 - In this project, we will use ```ttk.Notebook(window)``` to build tabs for the GUI: 
   - To talk about step 2 of the project, to begin with, we will mention ```tab1``` first. This tab is to execute the ```readData``` function above. These lines demonstrate the work:
   
   ```
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Calculate Step 1")
    tab_control.pack(expand=YES, fill="both")
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
   
   ```
   - The code above will create a GUI like the image below: 
   
   <p align="center">
    <img src="First_Tab.png" width=500>
   </p>
   
   - Now, ```clicked()``` function specifies the event after you click on button ```Generate```. In this project's step 1, as you can see, it will generate a new data in ```calculated_data_2.xlsx``` file:
   
   <p align="center">
    <img src="Generate_Step_1.png" width=800>
   </p>
   
# B. Separate each group in a new Excel file
 - Now we are done with generating new data, we might as well want to separate just to be more comfortable when working with each group.
 ## Step 1: Implement a ```separate_group()``` function
 - The lines below help us separate between groups, and adding the data associated with ```group_name``` in the new list:
 ```
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
 ```
   - To begin with, it would be nice if we can include m/z column in every single group data file. Here, I used ```slice()``` function to get the m/z column so the researchers can be more convenient when analyzing the data.
   - We use nested loop to loop through each element in the 2-d list. Explicitly, in the line ```if table[y][0] == string:```, we want to check if the group name matches the input or not. If so, we can check the data if they are either of type ```float``` or ```None```, then we can append to ```record``` list. After that, we store ```record``` list in another variable ```new_record``` and then append it to a new table ```tab``` to create a new table. This implementation is the same as the step in ```readData(str)``` function (looping step)
   - Also, to make life easier for the last step of the project, we append ```count_table``` list to the ```tab``` table above. ```count_table``` list counts the appearance of data in each row. 
   ## Step 2: Create a new tab to generate group data with count
   - These lines of code below illustrate what we are doing:
   ```
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Separate Group")
    
    lbl_2 = Label(tab2, text="Group Name")
    lbl_2.pack(padx=2, pady=2)

    txt_2 = Entry(tab2, width=40)
    txt_2.pack(padx=2, pady=2)

    def separate():
        res = "Group name has been entered"
        failed_msg = 'There is no such group. Please try again'
        text = txt_2.get()
        if text == "Control" or text == "Diabetes" or text == "Diabetes+Insulin":
            produce_count_data(text)
            messagebox.showinfo('Success!', res)

    btn_2 = Button(tab2, text="Generate", command=separate)
    btn_2.pack(padx=5, pady=5)
   ```
   - The same implementation happens in this second tab. We have ```Label```, ```Entry``` for filling in the group name, and the ```Generate``` button. However, the difference is the ```separate``` function:
   ```
   def separate():
        res = "Group name has been entered"
        failed_msg = 'There is no such group. Please try again'
        text = txt_2.get()
        if text == "Control" or text == "Diabetes" or text == "Diabetes+Insulin":
            produce_count_data(text)
            messagebox.showinfo('Success!', res)
   ```
   - The ```if``` statement check if the input matches the groups we have in the original data. In this case, they are ```Control```, ```Diabetes```, and ```Diabetes+Insulin```. The image below shows the result:
    <p align="center">
    <img src="Step_2.png" width=500>
   </p>
   
   - And below is the example of ```Control``` table after being processed:
    <p align="center">
    <img src="Generate_Step_2.png" width=800>
   </p>
   
   - Now we are done with Step 2, let's move on to the last step of the project!
 # C. Check the percentage of the appearance of data and update file
 ## Step 1: Implementing ```check_percentage()``` function to certify the percentage existence of the data in a particular row:
 - Particularly, if the data in one row exists more than 65% of the whole row. For instance, if there is only 1 empty cell in a row out of 5 column, then we do not have to do anything. However, if the empty cells are more than 1, so the appearance of the data will be 3 out of 5, which is 60% < 65%. Then, the whole row will be reset. In other words, the cells will be changed to empty and the ```count``` column will be reset to 0. Here is the code:
 ```
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
 ```
 - In this function, we used ```openpyxl``` library to open the Excel Workbook (```openpyxl.load_workbook(filename=string)```). 
 - Moving on to the for loop, we want to use ```if``` statement to check if the appearance of data in a row exceeds 65% or not.
 - Finally, we save the updated workbook using ```wb.save(string)```.
 - The function will be implemented in ```tkinter``` window, which is the next step!!!
 ## Step 2: Add the ```Check Percentage``` tab to the tkinter window:
 ```
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
 ```
 - Skipping to the ```check()``` function to process the ```btn_3```, as we can see, we are using ```if elif else``` statement to check the legitimacy of the group name. If exists, we can update the file associated to the group name. For instance, if we type ```Control``` in the ```Entry```, the program will generate, i.e update the existing xlsx file ```Control_Group.xlsx``` to empty rows using ```check_percentage()``` function.
 - Following these lines of code, similarly to first and second tab above, we have something like this:
 <p align="center">
    <img src="Step_3.png" width=500>
   </p>
   
 - After clicking the ```Generate``` button, this event will happen:
 <p align="center">
    <img src="Generate_Step_3.png" width=800>
   </p>
   
 - As you can see in line 78 of the ```Control_Group.xlsx``` file, the line originally exists 1 data, hence ```count = 1```. After step 3, the data is set to empty, and ```count``` column is reset to 0. 
 
 # D. Saving data to ```csv``` file
 - In this step, we do not need many functions to perform the generation of data. We only have to implement:
   - ```read_group_data_with_average()``` function
   - ```save_csv()``` function, and
   - Add a new tab to the desktop application to generate ```final_data.csv```
  ## Step 1: Read each group data, including average of each row data.
   ```
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
   ```
   - As I said, we are going to read all of the data in ```Control_Group.xlsx```, ```Diabetes_Group.xlsx```, and ```Diabetes+Insulin_Group.xlsx``` files.
   - ```average_column = calculate_average(str)``` is to get the ```Avg``` column from the function ```calculate_average(str)``` with ```str``` parameter being the name of the xlsx file:
   ```
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

   ```
   - In this function, I used ```openpyxl``` library to load and read the file. Next, I calculate the average of each row data which is the sum of all data in a row and divided by the number of data in that row, which is 5.
   - Going back to ```read_group_data_with_average(str)``` function, I continue to append each column of the group data into ```table``` list. Finally, I append ```average_column``` to ```table``` so that we have a group data with average.
   ## Step 2: Create a function ```save_csv()``` to save to a csv file after adding all group data (with average) into a large table list.
    ```
       # save to csv file
       def save_csv(table):
          export_data = zip_longest(*table, fillvalue='')
          with open('final_data.csv', 'w', newline='') as file:
              writer = csv.writer(file, quoting=csv.QUOTE_ALL)
              writer.writerows(export_data)
          file.close()
    ```
    - In this function, we just export the data into ```final_data.csv``` file after looping data using ```itertools``` library. For more information, you can read https://docs.python.org/3.0/library/itertools.html to learn more about itertools.
   ## Step 3: Create a new tab in the desktop application to generate ```final_data.csv```.
   - In ```tkinter_window()``` function, we continue to add another tab using this code:
   ```
    tab4 = ttk.Frame(tab_control)
    tab_control.add(tab4, text="Final Data")
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

   ```
   - Particularly, the ```final()``` function is to add all data into a large table ```final_table```; also, we use this table as a parameter for ```save_csv(final_table)``` function so that we can generate a csv file as we want.
   - Then, we add Label and Button as usual.
   
   
