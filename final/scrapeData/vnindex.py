import pandas as pd

# Define the path to the original Excel file
file_path = 'final/original_dataset/original_vnindex.xlsx'

# Read the Excel file, considering headers starting from row 8, and selecting columns C (Date) and G (Close)
df = pd.read_excel(file_path, header=8, usecols="C,G")

# Rename columns for clarity (optional)
df.columns = ['date', 'vnindex_close']

# Convert the 'date' column to datetime format using the specified date format (day/month/year)
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', dayfirst=True)

# Sort the DataFrame by the 'date' column
df = df.sort_values('date')

# Define the output path for the CSV file
output_file_path = 'final/dataset/vnindex.csv'

# Save the DataFrame as a CSV file without including the index column
df.to_csv(output_file_path, index=False)

