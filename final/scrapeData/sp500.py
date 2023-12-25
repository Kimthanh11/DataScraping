import pandas as pd

file_path = 'final/original_dataset/original_sp500.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Select the columns "Ngày" and "Lần cuối"
df = data[["Ngày", "Lần cuối"]]

# Rename the columns to "date" and "close"
df = df.rename(columns={"Ngày": "date", "Lần cuối": "close"})

# Convert 'date' column to datetime type with specified format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', dayfirst=True)

# Convert 'close' column to numeric after removing commas
df['close'] = df['close'].replace(',', '', regex=True).astype(float)

# Sort DataFrame by the 'date' column
df = df.sort_values('date')

# Store the DataFrame as a CSV file
output_file_path = 'final/dataset/sp500.csv'
df.to_csv(output_file_path, index=False)
