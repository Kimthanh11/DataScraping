import pandas as pd

exchange_rate = pd.read_csv('final/dataset/exchange_rate.csv')
interest_rate = pd.read_csv('final/dataset/interest_rate.csv')
vcb = pd.read_csv('final/dataset/vcb.csv')
vnindex = pd.read_csv('final/dataset/vnindex.csv')
sp500 = pd.read_csv('final/dataset/sp500.csv')
gdp = pd.read_csv('final/dataset/gdp.csv')
inflation = pd.read_csv('final/dataset/inflation.csv')

# Merge DataFrames on the 'date' column
merged_data = exchange_rate.merge(interest_rate, on='date', how='outer')
merged_data = merged_data.merge(vcb, on='date', how='outer')
merged_data = merged_data.merge(vnindex, on='date', how='outer')
merged_data = merged_data.merge(sp500, on='date', how='outer')
merged_data = merged_data.merge(gdp, on='date', how='outer')
merged_data = merged_data.merge(inflation, on='date', how='outer')

# Sort merged data by the 'date' column
merged_data = merged_data.sort_values('date')

# Filter out rows where 'vcb_close' is empty
merged_data = merged_data.dropna(subset=['vcb_close'])

# Identify columns with missing values
columns_with_missing = ['exchange_rate', 'interest_rate', 'sp500_close']

# Convert 'date' column to datetime
merged_data['date'] = pd.to_datetime(merged_data['date'])

# Fill missing values with weekly means
for col in columns_with_missing:
    # Calculate the week number from the date
    merged_data['week_number'] = merged_data['date'].dt.isocalendar().week
    
    # Calculate the mean per week and fill missing values with the weekly mean
    merged_data[col] = merged_data.groupby('week_number')[col].transform(lambda x: x.fillna(x.mean().round(2)))

# Count the number of empty values in each column
empty_count = merged_data.isna().sum()

print(empty_count)

# To save the merged data to a CSV file
merged_file_path = 'final/main_data.csv'
merged_data.to_csv(merged_file_path, index=False)