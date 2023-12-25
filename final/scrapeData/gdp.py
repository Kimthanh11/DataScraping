import pandas as pd
from datetime import datetime, timedelta

# Provided GDP data
gdp_data = [
    {"time": "4/2022", "gdp": 2669131},
    {"time": "1/2023", "gdp": 2300882},
    {"time": "2/2023", "gdp": 2444649},
    {"time": "3/2023", "gdp": 2540588},
    {"time": "4/2023", "gdp": None},
]

# Define the date range from 26/12/2022 to 25/12/2023
start_date = datetime.strptime("26/12/2022", "%d/%m/%Y")
end_date = datetime.strptime("25/12/2023", "%d/%m/%Y")
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Filter out Saturdays and Sundays from the date range
date_range = [date for date in date_range if date.weekday() not in [5, 6]]  # 5: Saturday, 6: Sunday

# Create a DataFrame structure for the filtered date range
quarter_df = pd.DataFrame({"date": date_range})

# Function to get quarter and year from date
def get_quarter_year(date):
    quarter = (date.month - 1) // 3 + 1
    year = date.year
    return f"{quarter}/{year}"

# Apply the function to the Date column to get the corresponding quarter and year
quarter_df["time"] = quarter_df["date"].apply(get_quarter_year)

# Merge the DataFrame with GDP data
merged_df = pd.merge(quarter_df, pd.DataFrame(gdp_data), on="time", how="left").drop(columns=["time"])

# Display or save the DataFrame as needed
print(merged_df)
merged_df.to_csv('final/dataset/gdp.csv', index=False)
