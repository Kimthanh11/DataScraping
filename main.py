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
try:
    # Wait for the overlay/loading element to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "server-loading"))
    )  
    time.sleep(3)

    # Select danh mục
    contents = ["Dụng cụ nhà bếp", "Trang trí nhà cửa", "Đồ dùng phòng ngủ", "Ngoài trời & sân vườn", "Nội thất"]

    for content in contents:
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

        products_list = driver.find_elements(By.CSS_SELECTOR, 'a.style__ProductLink-sc-7xd6qw-2')

        links_in_container = []

        for product in products_list:
            try:
                element = product.find_element(By.XPATH, ".//p[contains(text(), 'Tài trợ')]")
            except NoSuchElementException:
                links_in_container.append(product)

        for index, link_element in enumerate(links_in_container[:10]):  
            product_data = {}
            link_href = link_element.get_attribute("href")
            product_data['Link'] = link_href
            driver.execute_script("window.open('{}', '_blank');".format(link_href))
            driver.switch_to.window(driver.window_handles[-1])

            try:
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

                 # Find all elements with the specified class that contain the desired content
                try:
                    # Find the div containing "Ưu đãi khác"
                    parent_div = driver.find_element(By.XPATH, '//div[contains(@class, "WidgetTitle__WidgetContainerStyled") and .//div[text()="Ưu đãi khác"]]')

                    # Find all child divs within the parent div
                    child_divs = parent_div.find_elements(By.XPATH, './div[@class="WidgetTitle__WidgetContentStyled-sc-1ikmn8z-2 jMQTPW"]')
                    coupon_list = []
                    for child_div in child_divs:
                        
                        counpon_div = driver.find_element(By.ID, 'ma-giam-gia')
                        # Main coupon
                        if counpon_div:
                            img_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="right-icon" and @width="24" and @height="24"]')))
                            img_element.click()
                            time.sleep(3)

                            div_elements = driver.find_elements(By.XPATH, '//div[h4[@class="sc-lmgQwP cKclwG"]]')
                            time.sleep(3)
                            for div_element in div_elements:
                                try:
                                    # Extract h4 and p content within each div
                                    h4_element = div_element.find_element(By.XPATH, './/h4')
                                    p_element = div_element.find_element(By.XPATH, './/p')

                                    h4_text = h4_element.text
                                    p_text = p_element.text

                                    coupon = h4_text + " " + p_text
                                    coupon_list.append(coupon)
                                
                                except NoSuchElementException:
                                    pass
                            close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'coupon-list__close'))
)
                            # Click the close button
                            close_button.click()
                        # Addon coupon
                        else:
                            try:
                                # Extract content of each div within the same parent
                                span_text = child_div.find_element(By.TAG_NAME, 'span').text
                                div_text = child_div.find_element(By.TAG_NAME, 'div').text

                                coupon = span_text + " " + div_text
                                coupon_list.append(coupon)

                            except NoSuchElementException:
                                pass
                    product_data['Coupon'] = coupon_list

                except NoSuchElementException:
                    product_data['Coupon'] = None
                

                # Stars
                
                if product_data['Stars'] != None:
                    driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 1);")
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
                    # Reviews
                    driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")
                    time.sleep(3)  # Wait for the page to load after scrolling

                    
                    if product_data["1 star"] != '0' and product_data["2 stars"] != '0':
                        stars_2_element =  driver.find_element(By.XPATH, '//div[@class="filter-review__item  "][@data-view-index="6"]')
                        stars_1_element =  driver.find_element(By.XPATH, '//div[@class="filter-review__item  "][@data-view-index="7"]')
    
                        if stars_2_element and stars_1_element:
                            stars_2_element.click()
                            stars_1_element.click()
                            time.sleep(3)
                            reviews = []
                            for _ in range(10):
                                comments_list = driver.find_elements(By.CLASS_NAME, 'review-comment')
                                for comment in comments_list:
                                    try:
                                        show_more_element = comment.find_element(By.CSS_SELECTOR, 'span.show-more-content') 
                                        if show_more_element:
                                            show_more_element.click()
                                            content_element = comment.find_element(By.XPATH, './/div[@class="review-comment__content"]//div//span[not(@class)]')
                                            content = content_element.text
                                            reviews.append(content)
                                        
                                    except NoSuchElementException:
                                        content_element = comment.find_element(By.XPATH, './/div[@class="review-comment__content"]')
                                        content = content_element.text
                                        reviews.append(content)

                                driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 1);")
                                time.sleep(6)  # Wait for the page to load after scrolling
                                try:
                                    # Find the button with class name 'btn next'
                                    btn_next = driver.find_element(By.CSS_SELECTOR, 'a.btn.next')

                                    # Click the button
                                    btn_next.click()
                                    time.sleep(5)

                                except NoSuchElementException:
                                    break  # Break the loop if the element is not found
                            product_data['Reviews'] = reviews

                    else:
                        product_data['Reviews'] = None
                else:
                    product_data["5 stars"] = None
                    product_data["4 stars"] = None
                    product_data["3 stars"] = None
                    product_data["2 stars"] = None
                    product_data["1 star"] = None
                    product_data['Reviews'] = None



            finally:
                data.append(product_data) 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            
        driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()

df = pd.DataFrame(data)
df.to_csv('tiki.csv', index=False)  

print(df)  # Display the DataFrame