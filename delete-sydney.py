import pandas as pd

# Read the excel file
df = pd.read_excel("sydney-postcode.xlsx", engine='openpyxl')

# From left to right, remove duplicates
for col_index, col_name in enumerate(df.columns[:-1]):  # We exclude the last column because there's no column to its right
    for next_col in df.columns[col_index + 1:]:
        # Get unique postcodes from the current column
        current_col_unique_values = df[col_name].dropna().unique()

        # Set the value in the next column to None if it exists in the current column
        df[next_col] = df[next_col].apply(lambda x: None if x in current_col_unique_values else x)

# Convert the data to string, while ensuring whole numbers don't have a decimal point
def convert_to_str(val):
    if pd.isna(val):
        return None
    elif isinstance(val, float) and val.is_integer():
        return str(int(val))
    else:
        return str(val)

df = df.applymap(convert_to_str)

# Remove NaN values from columns and reset indices
df_cleaned = pd.DataFrame()
for col in df.columns:
    df_cleaned[col] = df[col].dropna().reset_index(drop=True)

# Ensure there are no empty gaps in the DataFrame
# By aligning lengths
max_length = max(df_cleaned.count())
df_cleaned = df_cleaned.reindex(range(max_length))

# Save the modified dataframe back to Excel
df_cleaned.to_excel("sydney-postcode_modified.xlsx", index=False, engine='openpyxl')




