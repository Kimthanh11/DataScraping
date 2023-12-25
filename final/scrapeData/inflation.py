from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/52/cpi.htm"
driver.get(url)

# Locate the select element by name for month
select_month_element = driver.find_element(By.NAME, "from")
select_month = Select(select_month_element)
select_month.select_by_value('12')
time.sleep(3)

# Locate the select element by name for year
select_year_element = driver.find_element(By.NAME, "fromYear")
select_year = Select(select_year_element)
select_year.select_by_value('2022')
time.sleep(3)

# Find and click the 'Xem' button to trigger the date filter
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tbl-macro-data")))

# Get all th elements (months)
th_elements = table.find_elements(By.XPATH, "//th[contains(@class, 'text-right')]")
th_text = [th.text.replace("Tháng", "").strip() for th in th_elements]

# Get all td elements (inflation values)
td_elements = table.find_elements(By.XPATH, "//tr[1]//td[contains(@class, 'text-right')]")
td_text = [td.text.strip() for td in td_elements]

# Create a DataFrame for inflation data
inflation_data = {'month': th_text, 'inflation': td_text}
inflation_df = pd.DataFrame(inflation_data)

# Define date range
start_date = datetime.strptime("26/12/2022", "%d/%m/%Y")
end_date = datetime.strptime("25/12/2023", "%d/%m/%Y")
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
# Filter out Saturdays and Sundays from the date range
date_range = [date for date in date_range if date.weekday() not in [5, 6]]  # 5: Saturday, 6: Sunday

# Fetch inflation for each date in the range
data = []
for date in date_range:
    # Find the corresponding inflation for the month
    month = date.strftime("%m/%Y")
    matching_month = inflation_df[inflation_df['month'] == month]
    if not matching_month.empty:
        inflation = float(matching_month['inflation'].values[0])
    else:
        inflation = None
    data.append({"date": date.strftime("%d/%m/%Y"), "inflation": inflation})

# Create DataFrame
df = pd.DataFrame(data)
print(df) 
df.to_csv('final/dataset/inflation.csv', index=False)

driver.quit()
