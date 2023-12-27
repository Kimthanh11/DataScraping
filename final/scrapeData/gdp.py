# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
from datetime import datetime, timedelta
from date_range import get_start_year, get_end_year, get_start_quarter_year, get_end_quarter_year, start_day, end_day

start_year = get_start_year()
end_year = get_end_year()
start_quarter = get_start_quarter_year()
end_quarter = '4'

# Configure the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/43/thu-nhap.htm"
driver.get(url)

# Select month and year for the filter
select_quarter_element = driver.find_element(By.NAME, "from")
select_quarter = Select(select_quarter_element)
select_quarter.select_by_value(start_quarter)

select_year_element = driver.find_element(By.NAME, "fromYear")
select_year = Select(select_year_element)
select_year.select_by_value(start_year) 

select_to_quarter_element = driver.find_element(By.NAME, "to")
select_to_quarter = Select(select_to_quarter_element)
select_to_quarter.select_by_value(end_quarter)

select_to_year_element = driver.find_element(By.NAME, "toYear")
select_to_year = Select(select_to_year_element)
select_to_year.select_by_value(end_year)

# Trigger the filter by clicking the 'Xem' button
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tbl-macro-data")))

# Extracting gdp data from the table
th_elements = table.find_elements(By.XPATH, "//th[contains(@class, 'text-right')]")
th_text = [th.text for th in th_elements]

td_elements = table.find_elements(By.XPATH, "//tr[17]//td[contains(@class, 'text-right')]")
td_text = [pd.to_numeric(td.text.replace(",", "").strip()) for td in td_elements]

# Create a DataFrame for gdp data
gdp_dt= {'time': th_text, 'gdp': td_text}
gdp_data = [
    {'time': quarter, 'gdp': gdp}
    for quarter, gdp in zip(gdp_dt['time'], gdp_dt['gdp']) 
    if "Quý" in quarter
]

for entry in gdp_data:
    entry['time'] = entry['time'].replace("Quý", "").strip()

# Define the date range from 26/12/2022 to 25/12/2023
start_date = datetime.strptime(start_day, "%d/%m/%Y")
end_date = datetime.strptime(end_day, "%d/%m/%Y")
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

# Save the DataFrame
merged_df.to_csv(f'final/dataset/gdp.csv', index=False)
