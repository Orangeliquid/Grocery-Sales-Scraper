# Grocery Sales Scraper
The Grocery Sales Scraper is a Python-based web scraping tool designed to help users find and compare prices of grocery items across different stores. It automates the process of searching for items, collecting price data, and logging the results, making it easier to track sales and save money on groceries.

## Features
- Automated Web Scraping: Uses Selenium WebDriver to navigate store websites and search for items.
- Configurable Parameters: Allows users to customize search parameters, including zip code, items to search, and the number of results.
- Database Integration: Saves and retrieves logged product data from a MongoDB database.
- Randomized Item Selection: Selects a random sample of frequently ordered items for scraping.
- Batch Processing: Supports chunking of large item lists to manage scraping traffic and avoid overloading the server.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Orangeliquid/Grocery-Sales-Scraper.git
cd Grocery-Sales-Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up MongoDB:
Ensure you have MongoDB installed and running. Update the database connection settings in database.py if necessary.
I like to use MongoDBCompass.

## Usage
Parameters
- headed: Boolean to display the WebDriver (True) or run headless (False).
- cookies: Boolean to accept cookies (currently only True is implemented).
- zip_code: Integer representing the zip code for the store search.
- items: List of strings, representing the grocery products to search.
- results_requested: Integer representing the number of sales results to attempt to scrape and return.

## Example
1. Single Run with Specific Items
```bash
from scraper import scrape_sales as scrape

head_option = False
allow_cookies = True
user_zip_code = 43220
items_list = ["Clorox Wipes", "Red Velvet Cookies", "Duck Tape", "Heavy Whipping Cream"]
result_amount = 8

scrape(
    headed=head_option,
    cookies=allow_cookies,
    zip_code=user_zip_code,
    items=items_list,
    results_requested=result_amount
)
```
2. Randomized Item Selection from Frequently Ordered List
```bash
import random
from scraper import scrape_sales as scrape

frequently_ordered = ["Giant Eagle Water", "Giant Eagle Turkey Ground, 93%", "Planet Oat Original Oatmilk", ...]

frequently_ordered_amount = 4
random_grocery_sample = random.choices(frequently_ordered, k=frequently_ordered_amount)

scrape(
    headed=head_option,
    cookies=allow_cookies,
    zip_code=user_zip_code,
    items=random_grocery_sample,
    results_requested=result_amount
)
```
3. Batch Processing with Chunked List
```bash
from scraper import scrape_sales as scrape

def chunk_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

chunk_amount = 10
chunks = chunk_list(frequently_ordered, chunk_amount)

for count, sub_chunk in enumerate(chunks, start=1):
    scrape(
        headed=head_option,
        cookies=allow_cookies,
        zip_code=user_zip_code,
        items=sub_chunk,
        results_requested=result_amount
    )
    print(f"Chunk {count} finished")
    time.sleep(10)
```
4. Scraping Prices of Products Already Logged in Database
```bash
from scraper import scrape_sales as scrape
from database import get_all_logged_products

current_logged_products = get_all_logged_products()
random.shuffle(current_logged_products)

scrape(
    headed=head_option,
    cookies=allow_cookies,
    zip_code=user_zip_code,
    items=current_logged_products,
    results_requested=result_amount
)
```

## License

This project is licensed under the [MIT License](LICENSE.txt).
