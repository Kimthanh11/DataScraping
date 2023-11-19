from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(options=options)
driver.get("https://tiki.vn/nha-cua-doi-song/c1883")

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
            link_href = link_element.get_attribute("href")
            driver.execute_script("window.open('{}', '_blank');".format(link_href))
            driver.switch_to.window(driver.window_handles[-1])

            try:
                name_element = driver.find_element(By.CLASS_NAME, "Title__TitledStyled-sc-1kxsq5b-0")
                name = name_element.text
                print(f"Index {index} Name: {name}")


                brand_element = driver.find_element(By.CSS_SELECTOR, 'a[data-view-id="pdp_details_view_brand"]')
                brand_name = brand_element.text
                print(f"Index {index} Brand name: {brand_name}")

                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-price__current-price"))
                )
                price = price_element.text
                print(f"Index {index} Price: {price}")

                try:
                    sale_element = driver.find_element(By.CLASS_NAME, "styles__StyledQuantitySold-sc-1swui9f-3")
                    if sale_element:
                        sale = sale_element.text
                        print(f"Index {index} Sales: {sale}")
                except NoSuchElementException:
                    print("Sale not found")

                try:
                    stars_div = driver.find_element(By.CSS_SELECTOR, 'div[style="margin-right:4px;font-size:14px;line-height:150%;font-weight:500"]')
                    stars = stars_div.text
                    print(f"Stars: {stars}")
                except NoSuchElementException:
                    print("Stars not found")

                # Find discount
                driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 3);")
                time.sleep(3)  # Wait for the page to load after scrolling

                 # Find all elements with the specified class that contain the desired content
                try:
                    # Find the div containing "Ưu đãi khác"
                    parent_div = driver.find_element(By.XPATH, '//div[contains(@class, "WidgetTitle__WidgetContainerStyled") and .//div[text()="Ưu đãi khác"]]')

                    # Find all child divs within the parent div
                    child_divs = parent_div.find_elements(By.XPATH, './div[@class="WidgetTitle__WidgetContentStyled-sc-1ikmn8z-2 jMQTPW"]')

                    for child_div in child_divs:
                        ma_giam_gia_div = driver.find_element(By.ID, 'ma-giam-gia')
                        # Main coupon
                        if ma_giam_gia_div:
                            if ma_giam_gia_div:
                                print("Found the 'Mã Giảm Giá' div")
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

                                        print(f"Index {index} h4 content: {h4_text}")
                                        print(f"Index {index} p content: {p_text}")
                                    
                                    except NoSuchElementException:
                                        print("h4 or p element not found in the div")
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

                                print(f"Index {index} span content: {span_text}")
                                print(f"Index {index} div content: {div_text}")

                            except NoSuchElementException:
                                print("Span or div element not found in the div")

                except NoSuchElementException:
                    print("Parent div with 'Ưu đãi khác' not found")
                

                # Stars
                driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 1);")
                time.sleep(3)  # Wait for the page to load after scrolling
                
                try:
                    # Find the main div with class 'review-rating__detail'
                    main_div = driver.find_element(By.CLASS_NAME, 'review-rating__detail')

                    # Find all child divs with class 'review-rating__number'
                    child_divs = main_div.find_elements(By.CLASS_NAME, 'review-rating__number')

                    # Extract content from each child div
                    i = 5
                    for child_div in child_divs:
                        content = child_div.text
                        print(f"Content of {i} star(s): {content}")
                        i=i-1

                except NoSuchElementException:
                    print("Main div 'review-rating__detail' not found")

            
                # Reviews
                driver.execute_script("window.scrollTo(0, window.scrollY + window.innerHeight * 0.5);")
                time.sleep(3)  # Wait for the page to load after scrolling
                try:
                    stars_2_element =  driver.find_element(By.XPATH, '//div[@class="filter-review__item  "][@data-view-index="6"]')
                    stars_1_element =  driver.find_element(By.XPATH, '//div[@class="filter-review__item  "][@data-view-index="7"]')
   
                    if stars_2_element and stars_1_element:
                        stars_2_element.click()
                        stars_1_element.click()
                        time.sleep(3)

                except NoSuchElementException:
                    print("Divs not found")

            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            time.sleep(10)
        driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()
