# Postcode-scrab
collect all the postcode in the range of the fixed location
# Sydney Postcode Cleaner

A Python script to clean up and deduplicate postcodes in an Excel file, focusing specifically on postcodes in Sydney.

## Dependencies:

- **pandas**: For reading, manipulating and writing data.
- **openpyxl**: An Excel reading/writing library used as an engine by pandas.

You can install the necessary libraries using pip:

```bash
pip install pandas openpyxl
```
# How the Script Works:
1. Load the Data: The script starts by loading the Excel file named sydney-postcode.xlsx.
2. Deduplicate Across Columns: For each column (excluding the last one), the script removes any values that are present in subsequent columns. This ensures that a unique postcode remains in its earliest appearance and gets removed from any following columns.
3. Data Transformation: Converts the data to a string format, ensuring that whole numbers don't have a .0 suffix and removing any "nan" entries.
4. Reformat the Data: The script then reconstructs the DataFrame, ensuring there are no 'NaN' entries and that each column has the same number of rows, filling any additional rows with 'NaN'.
5. Save the Modified Data: The cleaned data is saved back into an Excel file named sydney-postcode_modified.xlsx.

# Usage:
To use the script, ensure that you have an Excel file named sydney-postcode.xlsx in the same directory as the script.

Run the script:
```bash
python delete-vic.py
```

Once the script completes its execution, you will find a cleaned Excel file named sydney-postcode_modified.xlsx in the same directory.

# License:
MIT (or whichever license you prefer)

### Notice：
Follow the step,if u have some issues, just contact with me.
