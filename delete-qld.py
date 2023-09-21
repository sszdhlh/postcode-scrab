import pandas as pd

# Read the excel file
df = pd.read_excel("qld-postcode.xlsx", engine='openpyxl')

# Ensure data is of string type for set operations
df = df.astype(str)

# From left to right, remove duplicates
seen = set()
for col in df.columns:
    df[col] = df[col].apply(lambda x: x if x not in seen else None)
    seen.update(df[col].dropna().tolist())

# Remove NaN values from columns and reset indices
df_cleaned = pd.DataFrame()
for col in df.columns:
    df_cleaned[col] = df[col].dropna().reset_index(drop=True)

# Ensure there are no empty gaps in the DataFrame
# By aligning lengths
max_length = max(df_cleaned.count())
df_cleaned = df_cleaned.reindex(range(max_length))

# Save the modified dataframe back to Excel
df_cleaned.to_excel("qld-postcode_modified.xlsx", index=False, engine='openpyxl')


