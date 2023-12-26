import pandas as pd

# Define the path to the Excel file
file_path = 'final/original_dataset/original_vcb.xlsx'

# Read the Excel file starting from row 7 and select columns 1 (Date) and 5 (Close)
df = pd.read_excel(file_path, header=5, usecols="A,E")

# Rename columns for better readability (optional)
df.columns = ['date', 'vcb_close']

# Convert 'date' column to datetime type with specified format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', dayfirst=True)

# Sort DataFrame by the 'date' column
df = df.sort_values('date')

# Transform 'vcb_close' column to thousands and format to 2 decimal places
df['vcb_close'] = (df['vcb_close'] * 0.001).map('{:.2f}'.format)

# Define the output file path for the CSV file
output_file_path = 'final/dataset/vcb.csv'

# Store the DataFrame as a CSV file
df.to_csv(output_file_path, index=False) 
