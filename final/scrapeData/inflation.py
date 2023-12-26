# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from datetime import datetime, timedelta

# Configure the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/52/cpi.htm"
driver.get(url)

# Select month and year for the filter
select_month_element = driver.find_element(By.NAME, "from")
select_month = Select(select_month_element)
select_month.select_by_value('12')  # December

select_year_element = driver.find_element(By.NAME, "fromYear")
select_year = Select(select_year_element)
select_year.select_by_value('2022')  # 2022

# Trigger the filter by clicking the 'Xem' button
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tbl-macro-data")))

# Extracting inflation data from the table
th_elements = table.find_elements(By.XPATH, "//th[contains(@class, 'text-right')]")
th_text = [th.text.replace("Tháng", "").strip() for th in th_elements]

td_elements = table.find_elements(By.XPATH, "//tr[1]//td[contains(@class, 'text-right')]")
td_text = [td.text.strip() for td in td_elements]

# Create a DataFrame for inflation data
inflation_dt= {'month': th_text, 'inflation': td_text}
inflation_data = [
    {'month': month, 'inflation': inflation}
    for month, inflation in zip(inflation_dt['month'], inflation_dt['inflation'])
]

# Define the date range from 26/12/2022 to 25/12/2023
start_date = datetime.strptime("26/12/2022", "%d/%m/%Y")
end_date = datetime.strptime("25/12/2023", "%d/%m/%Y")
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Filter out Saturdays and Sundays from the date range
date_range = [date for date in date_range if date.weekday() not in [5, 6]]  # 5: Saturday, 6: Sunday

# Create a DataFrame structure for the filtered date range
inflation_df = pd.DataFrame({"date": date_range})

# Function to get month and year from date
def get_month_year(date):
    month_year = date.strftime("%m/%Y")
    return month_year.lstrip("0").replace("/0", "/")

# Apply the function to the Date column to get the corresponding month and year
inflation_df["month"] = inflation_df["date"].apply(get_month_year)

# Merge the DataFrame with inflation data
merged_inflation_df = pd.merge(inflation_df, pd.DataFrame(inflation_data), on="month", how="left").drop(columns=["month"])

# Convert 'date' column to datetime type
merged_inflation_df['date'] = pd.to_datetime(merged_inflation_df['date'], format='%Y-%m-%d')

# Sort DataFrame by the 'date' column
merged_inflation_df = merged_inflation_df.sort_values('date')

# Save the DataFrame as needed
merged_inflation_df.to_csv('final/dataset/inflation.csv', index=False)

# Close the browser window
driver.quit()
