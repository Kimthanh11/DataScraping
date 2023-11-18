from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from credentials import email, password
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)
driver.get("https://tiki.vn/nha-cua-doi-song/c1883")

try:
    
    # Wait for the overlay/loading element to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "server-loading"))
    )

    # Select bán chạy
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/nha-cua-doi-song/c1883?sort=top_seller"]'))
    )
    element.click()
    time.sleep(10) 

    # Iterate through 10 products
    # Wait for the container to load
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-view-id="product_list_container"]'))
    )


    # Find the <a> elements within the container
    links_in_container = container.find_elements(By.CSS_SELECTOR, 'a.style__ProductLink-sc-7xd6qw-2')

    for index, link_element in enumerate(links_in_container[:10]):  
        # Get the href attribute of the current link element
        link_href = link_element.get_attribute("href")

        # Open the link in a new tab
        driver.execute_script("window.open('{}', '_blank');".format(link_href))
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab

        # Perform actions within the link
        try:
            # Name
            h1_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Title__TitledStyled-sc-1kxsq5b-0"))
            )

            # Retrieve the text content of the h1 element
            h1_text = h1_element.text
            print(f"Index {index} Name: {h1_text}")  # Print the index and name

            # Other actions (Price, Brand, Stars, Sales, Shop, Discount)
            
        finally:
            # Close the tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
finally:
    driver.quit()
