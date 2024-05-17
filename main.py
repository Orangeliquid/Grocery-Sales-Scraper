from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import datetime

# Setup Variables
GROCERY_URL = "https://www.gianteagle.com/"
CHROMEDRIVER_PATH = "chromedriver.exe"
BRAVE_BINARY_LOCATION = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
WAIT_MAX = 10


def scrape_sales(headed, cookies, zip_code):

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

    time.sleep(50)

    driver.quit()


def accept_cookies(driver):
    wait = WebDriverWait(driver, 2.5)
    accept_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cn-buttons .cm-button"))
    )
    try:
        accept_button.click()
        return "Cookies Accepted"
    except Exception as e:
        return f"Failed to confirm acceptance: {e}"


def locate_store(driver, zip_code, timeout=5):
    wait = WebDriverWait(driver, 2.5)

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

    try:
        in_store_only_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="continue"]'))
        )
        in_store_only_button.click()
        return "Locate store tasks complete, your store is set with this caution: In store option only for this location"
    except (TimeoutException, NoSuchElementException):
        return "Locate store tasks complete, your store set"


def navigate_to_search(driver):
    wait = WebDriverWait(driver, 2.5)

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


"""l"""


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


def initialize_driver_headed():
    try:
        option = webdriver.ChromeOptions()
        option.binary_location = BRAVE_BINARY_LOCATION
        service = Service(CHROMEDRIVER_PATH)
        output_driver = webdriver.Chrome(service=service, options=option)
        return output_driver
    except Exception as e:
        raise Exception(f"Error initializing headless driver: {e}")


if __name__ == '__main__':
    head_option = True
    allow_cookies = True
    user_zip_code = 43220
    scrape_sales(headed=head_option, cookies=allow_cookies, zip_code=user_zip_code)
