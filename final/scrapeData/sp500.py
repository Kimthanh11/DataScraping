import pandas as pd

# Path to the original CSV file
file_path = 'final/original_dataset/original_sp500.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Select specific columns ("Ngày" and "Lần cuối")
df = data[["Ngày", "Lần cuối"]]

# Rename the columns to "date" and "sp500_close"
df = df.rename(columns={"Ngày": "date", "Lần cuối": "sp500_close"})

# Convert 'date' column to datetime format, considering the specified format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', dayfirst=True)

# Convert 'sp500_close' column to numeric after removing commas
df['sp500_close'] = df['sp500_close'].replace(',', '', regex=True).astype(float)

# Sort DataFrame by the 'date' column
df = df.sort_values('date')

# Define the path for the output CSV file
output_file_path = 'final/dataset/sp500.csv'

# Save the DataFrame as a CSV file without the index
df.to_csv(output_file_path, index=False)
