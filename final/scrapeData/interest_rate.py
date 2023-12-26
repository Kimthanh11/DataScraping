# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configure options for the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-suat.htm"
driver.get(url)

# Click on the "Lãi suất" link to switch to the interest rate section
interest_rate_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-default' and contains(@href, '?tab=64')]"))
)
interest_rate_link.click()

# Scroll to find the date input field
driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")
date_input = driver.find_element(By.NAME, "fromDate")
date_input.clear()

# Input the specific date value
date_value = "26/12/2022"
date_input.send_keys(date_value)
time.sleep(3)

# Find and click the 'Xem' button to trigger the date filter
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tbl-macro-data"))
)

# Get all th elements containing date information
th_elements = table.find_elements(By.XPATH, "//th[contains(@class, 'text-right')]")
th_text = [th.text.strip() for th in th_elements]

# Get all td elements containing interest rate data
td_elements = table.find_elements(By.XPATH, "//tr[1]//td[contains(@class, 'text-right')]")
td_text = [td.text.strip() for td in td_elements]

# Create a DataFrame with the collected date and interest rate data
data = {'date': th_text, 'interest_rate': td_text}
df = pd.DataFrame(data)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Sort DataFrame by the 'date' column
df = df.sort_values('date')

# Save DataFrame to a CSV file named 'interest_rate.csv'
df.to_csv('final/dataset/interest_rate.csv', index=False)

# Close the browser window
driver.quit()
