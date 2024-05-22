from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Setup Variables
GROCERY_URL = "https://www.gianteagle.com/"
CHROMEDRIVER_PATH = "chromedriver.exe"
BRAVE_BINARY_LOCATION = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
WAIT_MAX = 10


# This is the main function
def scrape_sales(headed, cookies, zip_code, items, results_requested):

    # Check for head/headless driving of selenium
    if headed:
        driver = initialize_driver_headed()
    else:
        driver = initialize_driver_headless()

    driver.get(GROCERY_URL)
    if cookies:
        cookie_action = accept_cookies(driver)
        print(cookie_action)

    locate_action = locate_store(driver, zip_code)
    print(locate_action)

    search_nav = navigate_to_search(driver)
    print(search_nav)

    product_dictionary = {}
    for item in items:
        print(f"Item to be passed: {item}")
        result = search_items(driver=driver, product=item, results_number=results_requested)
        if result == "No sale":
            product_dictionary[item] = result
        elif result != "No sale":
            product_dictionary[item] = result
        time.sleep(2)

    print(f"{product_dictionary}\n")

    for product, details in product_dictionary.items():
        print(f"> Item: {product}\n")
        if isinstance(details, str):
            print(f"  {details}\n")
        else:
            for detail in details:
                print(f"  Description: {detail['description']}\n  Price: {detail['price']}\n")

    time.sleep(180)

    driver.quit()


# Parameter to run the driver without showing the browsing window.
def initialize_driver_headless():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = BRAVE_BINARY_LOCATION
        options.add_argument('--headless')  # Set Chrome to run in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        service = Service(CHROMEDRIVER_PATH)
        output_driver = webdriver.Chrome(service=service, options=options)
        return output_driver
    except Exception as e:
        raise Exception(f"Error initializing driver: {e}")


# Parameter to run the driver with the window so the user can view what is happening
def initialize_driver_headed():
    try:
        option = webdriver.ChromeOptions()
        option.binary_location = BRAVE_BINARY_LOCATION
        service = Service(CHROMEDRIVER_PATH)
        output_driver = webdriver.Chrome(service=service, options=option)
        return output_driver
    except Exception as e:
        raise Exception(f"Error initializing headless driver: {e}")


# Allows user to accept cookies, selenium will check "Allow cookies"
def accept_cookies(driver):
    wait = WebDriverWait(driver, timeout=2.5)
    accept_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cn-buttons .cm-button"))
    )
    try:
        accept_button.click()
        return "Cookies Accepted"
    except Exception as e:
        return f"Failed to confirm acceptance: {e}"


# Selenium will navigate to the "select store" option and enter the user supplied zip code and select store
def locate_store(driver, zip_code, timeout=5):
    wait = WebDriverWait(driver, timeout=2.5)

    user_menu_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='User Menu']"))
    )
    user_menu_button.click()
    print("User Menu Clicked")

    select_store_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='StoreChooserButton']"))
    )
    select_store_button.click()
    print("select store button clicked")

    zipcode_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-test-id='FindYourStore_zipcode']"))
    )
    zipcode_input.click()
    zipcode_input.send_keys(zip_code)
    print("zip code entered")

    choose_store_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Make my store"]'))
    )
    choose_store_button.click()
    print("First store clicked")

    # So stores do not offer online delivery, this notification covers the screen which must be agreed to.
    try:
        in_store_only_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="continue"]'))
        )
        in_store_only_button.click()
        return ("Locate store tasks complete, your store is set with this caution"
                ": In store option only for this location")
    except (TimeoutException, NoSuchElementException):
        return "Locate store tasks complete, your store set"


# Once store is picked, This take selenium to the search bar to begin searching for sales
def navigate_to_search(driver):
    wait = WebDriverWait(driver, timeout=2.5)

    saving_options_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="SavingsQuickNavCta"]'))
        )
    saving_options_button.click()
    print("Saving options button clicked")

    all_savings_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/savings"]'))
        )
    all_savings_button.click()
    print("All savings button clicked")
    return "Navigated to search!"


def search_items(driver, product, results_number):
    print(f"Products passed to search item func: {product}")
    wait = WebDriverWait(driver, timeout=2.5)

    search_bar = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Search products"]'))
    )

    # Focus on the search bar and clear it
    search_bar.click()
    driver.execute_script("arguments[0].value = '';", search_bar)
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.BACK_SPACE)

    # Ensure the search bar is cleared
    time.sleep(0.5)  # Small delay to ensure clearing is complete

    # Enter new search query
    search_bar.send_keys(product)
    search_bar.send_keys(Keys.RETURN)
    print(f"{product} searched")
    time.sleep(2)

    try:
        sales_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="checkbox"][id="On Sale"]'))
        )
        # Scroll to the sales box element
        driver.execute_script("arguments[0].scrollIntoView(true);", sales_box)
        sales_box.click()
        print("Sales box clicked")
    except TimeoutException:
        print("Sales box not found or not clickable")
        return "No sale"

    time.sleep(3)
    # Wait for the results to load
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.tabular, h3[data-test-id="ProductTile_title"]'))
    )

    # Initialize lists for prices and descriptions
    prices = []
    descriptions = []

    try:
        print("Checking for BOGOs")
        bogo_amount_elements = driver.find_elements(By.CSS_SELECTOR,
                                                    'span[data-test-id="SharedProductPricingDetails_promoQty"]')
        bogo_price_elements = driver.find_elements(By.CSS_SELECTOR,
                                                   'span[data-test-id="SharedProductPricingDetails_salePrice"]')

        # Combine BOGO amount and price elements and append to prices list
        for bogo_amount, bogo_price in zip(bogo_amount_elements, bogo_price_elements):
            bogo_text = f"{bogo_amount.text} {bogo_price.text}"
            bogo_text = bogo_text.replace("Current price:", "").strip()
            bogo_text = bogo_text.replace("\n", "").strip()
            prices.append(bogo_text)
    except Exception as e:
        print(f"Error retrieving BOGOs: {e}")

    time.sleep(1)

    try:
        # Try to retrieve elements with the class 'tabular'
        sales_elements = driver.find_elements(By.CSS_SELECTOR, 'span.tabular')
        prices.extend([price.text for price in sales_elements])
    except Exception as e:
        print(f"Error retrieving sale prices: {e}")

    time.sleep(1)

    try:
        # Retrieve elements with the class 'ProductTile_title'
        description_elements = driver.find_elements(By.CSS_SELECTOR, 'h3[data-test-id="ProductTile_title"]')
        descriptions = [description.text for description in description_elements]
    except Exception as e:
        print(f"Error retrieving descriptions: {e}")

    # Check if no prices or descriptions were found
    if not prices or not descriptions:
        print(f"No prices or descriptions found for item: {product}")
        return "No sale"

    print(f"Found {len(prices)} prices and {len(descriptions)} descriptions")

    # Handle case where prices and descriptions count mismatch
    if len(prices) != len(descriptions):
        print("Mismatch in the number of prices and descriptions")
        lowest_pair = min(len(prices), len(descriptions))
    else:
        lowest_pair = len(prices)

    print(f"Lowest pair: {lowest_pair}")

    result_constraint = min(lowest_pair, results_number)

    # Create a list of dictionaries to store the results
    product_list = []
    for i in range(result_constraint):
        product_list.append({
            'description': descriptions[i],
            'price': prices[i]
        })

    # Clear search bar for next function call using JavaScript and backspace
    search_bar.click()
    driver.execute_script("arguments[0].value = '';", search_bar)
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.BACK_SPACE)
    time.sleep(1)  # Ensure the search bar is clear before the next iteration

    return product_list


"""<span data-test-id="SharedProductPricingDetails_salePrice" class="sc-fhBANE jra-DGs"><span class="sc-bFqpvU gHIAos">Current price: </span><span class="tabular">$7.99</span></span>
"""


if __name__ == '__main__':
    pass
