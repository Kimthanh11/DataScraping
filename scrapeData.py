from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)
driver.get("https://tiki.vn/nha-cua-doi-song/c1883")

data = []


# Wait for the overlay/loading element to disappear
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "server-loading"))
)  
time.sleep(3)

# Select danh mục
contents = ["Trang trí nhà cửa", "Đồ dùng phòng ngủ", "Ngoài trời & sân vườn", "Nội thất"]

for content in contents:
    count = 1
    link_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//a[contains(text(), "{content}")]'))
    )
    link_element.click()
    time.sleep(3)

    ban_chay_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Bán chạy")]'))
        )
    ban_chay_element.click()
    time.sleep(3)
    while count <= 200:
        time.sleep(3)
        products_list = driver.find_elements(By.CSS_SELECTOR, 'a.style__ProductLink-sc-7xd6qw-2')
    
        links_in_container = []

        for product in products_list:
            try:
                element = product.find_element(By.XPATH, ".//p[contains(text(), 'Tài trợ')]")
            except NoSuchElementException:
                links_in_container.append(product)

        for index, link_element in enumerate(links_in_container):  
            product_data = {}
            link_href = link_element.get_attribute("href")
            product_data['Link'] = link_href
            print(link_href)
            driver.execute_script("window.open('{}', '_blank');".format(link_href))
            driver.switch_to.window(driver.window_handles[-1])

            
            name_element = driver.find_element(By.CLASS_NAME, "Title__TitledStyled-sc-1kxsq5b-0")
            name = name_element.text
            product_data['Name'] = name

            brand_element = driver.find_element(By.CSS_SELECTOR, 'a[data-view-id="pdp_details_view_brand"]')
            brand_name = brand_element.text
            product_data['Brand'] = brand_name

            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-price__current-price"))
            )
            price = price_element.text
            product_data['Price'] = price

            try:
                sale_element = driver.find_element(By.CLASS_NAME, "styles__StyledQuantitySold-sc-1swui9f-3")
                if sale_element:
                    sale = sale_element.text
                    product_data['Sale'] = sale
            except NoSuchElementException:
                product_data['Sale'] = None

            try:
                stars_div = driver.find_element(By.CSS_SELECTOR, 'div[style="margin-right:4px;font-size:14px;line-height:150%;font-weight:500"]')
                stars = stars_div.text
                product_data['Stars'] = stars
            except NoSuchElementException:
                product_data['Stars'] = None

            # Find discount
            driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")
            time.sleep(3)  # Wait for the page to load after scrolling

            try:
                numberOfCoupon_element = driver.find_element(By.XPATH, '//div[@data-view-id="pdp_main_discount_coupon"]/span')
                numberOfCoupon = numberOfCoupon_element.text

                # Get the number
                numberOfCoupon = numberOfCoupon.split()[0]
                numberOfCoupon = int(numberOfCoupon)

                product_data['NumberOfCoupon'] = numberOfCoupon
            except NoSuchElementException:
                product_data['NumberOfCoupon'] = None
                

            # Stars
            
            if product_data['Stars'] != None:
                driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")
                time.sleep(3)  # Wait for the page to load after scrolling
                # Find the main div with class 'review-rating__detail'
                main_div = driver.find_element(By.CLASS_NAME, 'review-rating__detail')

                # Find all child divs with class 'review-rating__number'
                child_divs = main_div.find_elements(By.CLASS_NAME, 'review-rating__number')

                # Extract content from each child div
                i = 5
                for child_div in child_divs:
                    content = child_div.text
                    if i == 1:
                        content_column = "1 star"
                    else:
                        content_column = str(i) + " stars"
                    product_data[content_column] = content
                    i=i-1
            else:
                product_data["5 stars"] = None
                product_data["4 stars"] = None
                product_data["3 stars"] = None
                product_data["2 stars"] = None
                product_data["1 star"] = None
                product_data['Reviews'] = None
            
            print(count)
            count = count + 1
            data.append(product_data) 
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        
        time.sleep(3)
        arrow_right_image = driver.find_element(By.XPATH, '//img[contains(@alt, "arrow-right")]')
        arrow_right_image.click()
        print("No more ", content)
    
    df = pd.DataFrame(data)
    df.to_csv("trangtrinhacua.csv", index=False)
    driver.switch_to.window(driver.window_handles[0])

driver.quit()

# df = pd.DataFrame(data)
# df.to_csv('tiki1.csv', index=False)  

# print(df)  # Display the DataFrame