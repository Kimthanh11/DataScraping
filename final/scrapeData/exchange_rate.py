# Import necessary libraries from Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from date_range import start_day, end_day

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 

# Initialize the Chrome webdriver
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-suat.htm"
driver.get(url)

# Scroll to the date input field and clear any existing value
driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")

# Input the desired date
start_day_input = driver.find_element(By.NAME, "fromDate")
start_day_input.clear()
start_day_input.send_keys(start_day)

end_day_input = driver.find_element(By.NAME, "toDate")
end_day_input.clear()
end_day_input.send_keys(end_day)

# Find and click the 'Xem' button to trigger the date filter
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tbl-macro-data"))
)

# Get all th elements (table header)
th_elements = table.find_elements(By.XPATH, "//th[contains(@class, 'text-right')]")
th_text = [th.text.strip() for th in th_elements]

# Get all td elements (table data)
td_elements = table.find_elements(By.XPATH, "//tr[@class='group']/following-sibling::tr[1]//td[contains(@class, 'text-right')]")
td_text = [float(td.text.strip().replace(',', '')) for td in td_elements]

# Create a DataFrame from the extracted data
data = {'date': th_text, 'exchange_rate': td_text}
df = pd.DataFrame(data)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Sort DataFrame by the 'date' column
df = df.sort_values('date')

# Save DataFrame to a CSV file
df.to_csv('final/dataset/exchange_rate.csv', index=False)

# Close the browser window
driver.quit()
