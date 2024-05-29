from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
import re
from database import store_in_database

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Variables for scrape_sales function
GROCERY_URL = "https://www.gianteagle.com/"
CHROMEDRIVER_PATH = "chromedriver.exe"
BRAVE_BINARY_LOCATION = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
WAIT_MAX = 10


def scrape_sales(headed, cookies, zip_code, items, results_requested):
    driver = initialize_driver(headed)

    driver.get(GROCERY_URL)
    if cookies:
        cookie_action = accept_cookies(driver)
        logging.info(cookie_action)

    locate_action = locate_store(driver, zip_code)
    logging.info(locate_action)

    search_nav = navigate_to_search(driver)
    logging.info(search_nav)

    product_dictionary = {}
    for item in items:
        logging.info(f"Item to be passed: {item}")
        result = search_items(driver, product=item, results_number=results_requested)
        product_dictionary[item] = result
        time.sleep(2)

    logging.info(f"{product_dictionary}\n")

    for product, details in product_dictionary.items():
        logging.info(f"> Item: {product}\n")
        if isinstance(details, str):
            logging.info(f"  {details}\n")
        elif details is None:
            logging.info(f"  No details found for {product}\n")
        else:
            for detail in details:
                logging.info(f"  Description: {detail['description']}\n"
                             f"  Price: {detail['price']}\n"
                             f"  Quantity: {detail['quantity']}\n")

    for product, details in product_dictionary.items():
        store_in_database(product, details)

    time.sleep(3)
    driver.quit()


def parse_price(price_str, process):
    logging.info(f"Parse_Price String: {price_str}")
    if process.lower() == "price_parse":
        price_str = price_str.replace("Current price:", "").replace("$", "").strip()
        try:
            return float(price_str)
        except ValueError as e:
            logging.error(f"Error parsing price: {e}")
            price_str = price_str.replace("\n", ".")
            return float(price_str)
    elif process.lower() == "quantity_parse":
        if "for" in price_str:
            parts = re.split(r'\s*for\s*', price_str)
            if len(parts) == 2:
                quantity = int(parts[0])
                logging.info(f"Quantity: {quantity}")
                return quantity
        return 1


def initialize_driver(headed):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = BRAVE_BINARY_LOCATION
        if not headed:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        raise Exception(f"Error initializing driver: {e}")


def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 2.5)
        accept_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cn-buttons .cm-button"))
        )
        accept_button.click()
        return "Cookies Accepted"
    except Exception as e:
        return f"Failed to confirm acceptance: {e}"


def locate_store(driver, zip_code, timeout=5):
    try:
        wait = WebDriverWait(driver, 2.5)
        user_menu_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='User Menu']"))
        )
        user_menu_button.click()
        logging.info("User Menu Clicked")

        select_store_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='StoreChooserButton']"))
        )
        select_store_button.click()
        logging.info("Select store button clicked")

        zipcode_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-test-id='FindYourStore_zipcode']"))
        )
        zipcode_input.click()
        zipcode_input.send_keys(zip_code)
        logging.info("Zip code entered")

        choose_store_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Make my store"]'))
        )
        choose_store_button.click()
        logging.info("First store clicked")

        try:
            in_store_only_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="continue"]'))
            )
            in_store_only_button.click()
            return "Locate store tasks complete, your store is set with this caution: In store option only for this location"
        except (TimeoutException, NoSuchElementException):
            return "Locate store tasks complete, your store set"
    except Exception as e:
        return f"Error in locating store: {e}"


def navigate_to_search(driver):
    try:
        wait = WebDriverWait(driver, 2.5)
        saving_options_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="SavingsQuickNavCta"]'))
        )
        saving_options_button.click()
        logging.info("Saving options button clicked")

        all_savings_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/savings"]'))
        )
        all_savings_button.click()
        logging.info("All savings button clicked")
        return "Navigated to search!"
    except Exception as e:
        return f"Error navigating to search: {e}"


def create_product_list(descriptions, prices, result_constraint, quantities):
    product_list = []
    for i in range(result_constraint):
        product_list.append({
            'description': descriptions[i],
            'price': parse_price(prices[i], "price_parse"),
            'quantity': quantities[i],
        })
    return product_list


def search_items(driver, product, results_number):
    logging.info(f"Products passed to search item func: {product}")
    wait = WebDriverWait(driver, 5)

    try:
        search_bar = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Search products"]'))
        )
        clear_search_bar(search_bar)
        search_bar.send_keys(product)
        search_bar.send_keys(Keys.RETURN)
        logging.info(f"{product} searched")
        time.sleep(2)

        try:
            sales_box = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="checkbox"][id="On Sale"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sales_box)
            sales_box.click()
            logging.info("Sales box clicked")
        except TimeoutException:
            logging.info("Sales box not found or not clickable")
            return "No sale"

        time.sleep(3)
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-index]'))
        )

        descriptions, prices, quantities = [], [], []
        total_index_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
        results_number = min(results_number, len(total_index_elements))

        for index in range(results_number):
            try:
                item = driver.find_element(By.CSS_SELECTOR, f'div[data-index="{index}"]')
                description_element = item.find_element(By.CSS_SELECTOR, 'h3[data-test-id="ProductTile_title"]')
                descriptions.append(description_element.text)

                try:
                    price_element = item.find_element(By.CSS_SELECTOR, 'span[data-test-id="SharedProductPricingDetails_salePrice"]')
                    prices.append(price_element.text)
                except NoSuchElementException:
                    logging.info(f"No sale price found for item at index {index}")
                    continue

                try:
                    bogo_element = item.find_element(By.CSS_SELECTOR, 'span[data-test-id="SharedProductPricingDetails_promoQty"]')
                    bogo_text = bogo_element.text  # Define the bogo_text variable
                    quantities.append(parse_price(bogo_text, "quantity_parse"))
                except NoSuchElementException:
                    quantities.append(1)

            except NoSuchElementException as e:
                logging.error(f"Error retrieving data for item at index {index}: {e}")
                continue

        if not prices or not descriptions:
            logging.info(f"No prices or descriptions found for item: {product}")
            return "No sale"

        logging.info(f"Found {len(prices)} prices and {len(descriptions)} descriptions")
        return create_product_list(descriptions, prices, results_number, quantities)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def clear_search_bar(search_bar):
    search_bar.click()
    search_bar.clear()
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.BACK_SPACE)
    time.sleep(0.5)


if __name__ == '__main__':
    pass
