 # Brand
    #             brand_element = driver.find_element(By.CSS_SELECTOR, 'a[data-view-id="pdp_details_view_brand"]')

    #             # Get the text content of the brand
    #             brand_name = brand_element.text
    #             print(f"Index {index} Brand name: {brand_name}")

    #             # Price
    #             price_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "product-price__current-price"))
    # )
    #             price = price_element.text
    #             print(f"Index {index} Price: {price}")

    #             # Sales
    #             sale_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "styles__StyledQuantitySold-sc-1swui9f-3"))
    # )
    #             sale = sale_element.text
    #             print(f"Index {index} Sales: {sale}")

    #             # Discount
    #             # try:
    #             #     other_promotions_div = WebDriverWait(driver, 1000).until(
    #             #         EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "WidgetTitle__WidgetTitleStyled-sc-1ikmn8z-1") and contains(text(), "Ưu đãi khác")]'))
    #             #     )
    #             #     print("other promotion dive")

    #             #     if other_promotions_div:
    #             #         try:
    #             #             discount_coupon_div = WebDriverWait(driver, 10).until(
    #             #                 EC.visibility_of_element_located((By.ID, 'ma-giam-gia'))
    #             #             )
    #             #             print("discount coupon")

    #             #             if discount_coupon_div.is_displayed():
    #             #                 img_element = driver.find_element(By.CSS_SELECTOR, 'img[alt="right-icon"]')
    #             #                 img_element.click()

    #             #                 similar_divs = WebDriverWait(driver, 10).until(
    #             #                     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[style="padding-right: 28px;"]'))
    #             #                 )
    #             #                 for div in similar_divs:
    #             #                     h4_text_element = div.find_element(By.CSS_SELECTOR, 'h4.sc-iwajpm.SBdky')
    #             #                     h4_text = h4_text_element.text

    #             #                     p_text_element = div.find_element(By.CSS_SELECTOR, 'p.sc-cxNHIi.fHUQtx')
    #             #                     p_text = p_text_element.text

    #             #                     print(f"Header: {h4_text}\nParagraph: {p_text}\n")

    #             #         except NoSuchElementException:
    #             #             print("No main discount coupon div found. Skipping...")

    #             #         try:
    #             #             widget_element = driver.find_element(By.CLASS_NAME, "WidgetTitle__WidgetContentRowStyled-sc-1ikmn8z-3")
    #             #             widget_text = widget_element.text
    #             #             print(widget_text)

    #             #         except NoSuchElementException:
    #             #             print("Other promotions element not found. Skipping...")

    #             #     else:
    #             #         print("Div 'Ưu đãi khác' not found. Skipping...")

    #             # except TimeoutException:
    #             #     print("Timeout occurred while waiting for elements. Skipping...")

    #             # except NoSuchElementException:
    #             #     print("Element not found. Skipping...")


    #             # Free ship
                
    #             # Stars
    #             stars_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//div[@style="margin-right:4px;font-size:14px;'
    #                                               'line-height:150%;font-weight:500"]'))
    # )           
    #             stars = stars_element.text