import pandas as pd

file_path = 'final/original_dataset/original_vcb.xlsx'

# Read the Excel file starting from row 7 and select columns 1 (Date) and 5 (Close)
df = pd.read_excel(file_path, header=5, usecols="A,E")

# Rename columns for better readability (optional)
df.columns = ['Date', 'Close']

# Store the DataFrame as a CSV file
output_file_path = 'final/dataset/vcb.csv'
df.to_csv(output_file_path, index=False)  # index=False to avoid saving the index column

# Display the contents of the DataFrame
print(df)
