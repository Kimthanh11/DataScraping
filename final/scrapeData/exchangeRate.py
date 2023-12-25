from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-suat.htm"
driver.get(url)

# Wait for the date input field to be present
date_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "fromDate"))
)

# Input the date
date_value = "26/12/2021"
date_input.send_keys(date_value)

# Find and click the 'Xem' button to trigger the date filter
xem_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem')]")
xem_button.click()

# Close the browser window
driver.quit()
