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
merged_data['date'] = pd.to_datetime(merged_data['date'])
merged_data = merged_data.sort_values('date')

# Filter out rows where 'vcb_close' is empty
merged_data = merged_data.dropna(subset=['vcb_close'])

# Identify columns with missing values
columns_with_missing = ['exchange_rate', 'interest_rate', 'sp500_close']

# Fill missing values with weekly means
for col in columns_with_missing:
    # Calculate the week number from the date
    merged_data['week_number'] = merged_data['date'].dt.isocalendar().week
    
    # Calculate the mean per week and fill missing values with the weekly mean
    merged_data[col] = merged_data.groupby('week_number')[col].transform(lambda x: x.fillna(x.mean().round(2)))

# Rearrange columns
column_order = ['date', 'vcb_close', 'vnindex_close', 'exchange_rate', 'interest_rate', 'gdp', 'inflation', 'sp500_close']
merged_data = merged_data[column_order]


# Calculate GDP growth and add it as a new column
merged_data['gdp_growth'] = merged_data['gdp'].ffill()  # Forward fill missing values
merged_data['gdp_growth'] = merged_data['gdp_growth'].diff() / merged_data['gdp_growth'].shift(1)  # Compute growth rate

# Convert vcb close
merged_data['vcb_close'] = merged_data['vcb_close'] / 1000


# To save the merged data to a CSV file
merged_file_path = 'final/main_data.csv'
merged_data.to_csv(merged_file_path, index=False)