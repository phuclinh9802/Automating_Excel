# Automating_Excel
 Automate Excel using Python and Tkinkter to help scientists be more convenient when calculating data

This project is to help phD Researchers get more convenient when calculating large amount of molecules data

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
 
 
 
