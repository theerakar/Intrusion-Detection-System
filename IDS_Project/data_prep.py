import pandas as pd
import glob

# Use glob to find all CSV files in the folder you extracted from the zip
path = r'./data'
all_files = glob.glob(path + "/*.csv")

li = []

# Loop through each CSV file and read it into a pandas DataFrame
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

# Concatenate all the DataFrames into a single one
main_df = pd.concat(li, axis=0, ignore_index=True)

# Clean up column names by removing leading/trailing spaces
main_df.columns = main_df.columns.str.strip()

# Print a summary of loaded data
print("All files successfully loaded and combined.")
print("\nFirst 5 rows of the combined data:")
print(main_df.head())
print("\nData information:")
print(main_df.info())

# Save the combined DataFrame to a new CSV file for easier use later
main_df.to_csv("all_traffic_data.csv", index=False)