from scraper import scrape_sales as scrape
from database import get_all_logged_products
import random
import time

# Parameters for the scrape function
HEAD_OPTION = False
ALLOW_COOKIES = True
USER_ZIP_CODE = 43201  # Change this to your desired location
RESULT_AMOUNT = 8

# List of specific items to test scraping
ITEMS_LIST = ["Clorox Wipes", "Red Velvet Cookies", "Duck Tape", "Heavy Whipping Cream"]

# Frequently ordered items list
FREQUENTLY_ORDERED = [
    "Giant Eagle Water", "Giant Eagle Turkey Ground, 93%", "Planet Oat Original Oatmilk",
    "Giant Eagle Chicken Thighs", "Fresh Express Chopped Salad", "Produce Bananas",
    "Pure Leaf Unsweetened", "Clorox Wipes", "Celsius Energy Drink Sparkling",
    "Giant Eagle Breakfast Sausage", "New York Croutons", "Chobani Greek Yogurt", "Bacon",
    "Baguette", "Market District Wild Cod Fillet", "Giant Eagle Lemon", "Produce Green Onion",
    "Hand Soap", "Daisy Sour Cream", "Large Eggs", "Fresh Express Pesto Caesar", "Giant Eagle Salmon",
    "King's Hawaiian Rolls", "Charmin Ultra Soft Toilet Paper", "Chiquita Banana Bread Mix",
    "Cucumber", "Paper Towel Rolls", "Simply Lemonade", "Johnsonville Sausage", "Progresso Soup",
    "Fresh Mozzarella", "Yellow Onion", "Pepper Jack Cheese", "Giant Eagle Whey Protein", "Prego",
    "Pringles", "Red Onion", "Ciabatta Bread", "Pure Leaf Sweet Tea", "Turkey Breast",
    "Produce Celery", "Heinz Tomato Ketchup", "Jif Peanut Butter", "Mrs. T's Pierogies",
    "Ritz Party Size", "Banana Peppers", "Sensodyne", "Non-Dairy Oatmilk Dessert", "Jalapeno Slices",
    "Kielbasa", "Cantaloupe", "Produce Lime", "Mild Cheddar Cheese", "Doritos", "Produce Pepper",
    "Flour Tortilla", "Bread Crumbs", "Stuffed Shells", "Puff Pastry", "Barilla Pasta",
    "Petite Potatoes", "Hummus", "Digiorno", "Strawberry Ice Cream", "Peppercorns",
    "Mandarin Oranges", "Broccoli Florets", "Lay's Potato Chips", "Fish Sticks",
    "Pure Vanilla Extract", "Cilantro", "Avocado Ranch Salad", "Pork Tenderloin",
    "Avocado Caesar Salad", "Olipop Soda", "Frozen Fruit", "Sharp Cheddar Cheese",
    "Buffalo Wild Wings", "Q-tips", "CeraVe", "Canned Corn", "Bugles", "Opti-Free Multi-Purpose",
    "Blue Bunny", "Utz Snacks", "Dawn Dish Soap", "Andes Creme de Menthe", "LED Light Bulbs",
    "Ken's Dressing", "Morton Salt", "Downy Beads", "Minced Garlic", "Lint Roller", "Chicken Breast",
    "Arizona Green Tea", "Provolone Cheese", "Produce Broccoli Crowns", "Velveeta", "Chobani Oatmilk",
    "SPAM", "V8 Fruit", "Cheez-It Baked", "Rice Cakes", "Produce Mushrooms", "Watermelon",
    "Orville Redenbacher", "Sparkling Ice", "Jasmine Rice", "Red Velvet Cookies", "Sugar Snap Peas",
    "Basil", "Texas Toast", "Produce Garlic", "Garlic Powder", "Chick Fil A", "Italian Sausage",
    "Ranch Dressing", "Lemon Caesar Salad", "Brillo Sponge", "Rotisserie Chicken",
    "Ground Beef Patty", "Oven Roasted Turkey Breast", "Sweet Butter Salad", "Unsalted Butter",
    "Blueberry Muffins", "Baby Swiss Cheese", "String Cheese", "Philadelphia Cream Cheese",
    "Heavy Whipping Cream", "Whole Wheat Bread", "Chocolate Chip Muffins", "Pork Boston Butt",
    "Goldfish", "Ruffles", "Pillsbury Crescents", "Orange Juice", "Reclosable Sandwich Bags",
    "Danimals", "Snack Factory Pretzels", "Dole Frozen Fruit", "Giant Eagle Salsa", "Pork Loin",
    "Salmon Burger", "Beef Hot Dogs", "Coca-Cola", "Chicken Stock", "Smucker's Jam", "Olive Oil",
    "Tomato Paste", "Avocado Oil", "All Purpose Flour", "Corn on the Cob", "Hot Dog Buns",
    "Frozen Pineapple Chunks", "Onion Rings", "Klondike Bars", "Honey Bunches of Oats",
    "Simply Fruit Juice", "Vitamin Water", "Listerine", "Poppi Soda", "Totino's", "Fajita Seasoning",
    "Taco Seasoning", "Spinach", "Sister Schubert's Rolls", "Market District Tortilla Chips",
    "Coconut Milk", "Dill Pickles", "Brioche Buns", "Betty Crocker Brownies", "Heinz Mustard",
    "Gruyere Cheese", "Dove Antiperspirant Deodorant Stick",
    "Old Spice Antiperspirant Deodorant Stick", "Ghiradelli Brownies", "Jumbo Cotton Balls",
    "Pizza Sauce", "Mustard Powder", "Oatly Frozen Dessert", "Gluten Free Pizza",
    "Parmigiano Reggiano", "Tooth Brush", "Duck Tape", "Sauerkraut", "Paprika Seasoning"
]


# Function to break a list into chunks of specified size
def chunk_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


# Main script execution
if __name__ == '__main__':
    # Testing specific items
    scrape(
        headed=HEAD_OPTION,
        cookies=ALLOW_COOKIES,
        zip_code=USER_ZIP_CODE,
        items=ITEMS_LIST,
        results_requested=RESULT_AMOUNT
    )

    # Randomly selecting items from frequently ordered list
    frequently_ordered_amount = 4
    random_grocery_sample = random.choices(FREQUENTLY_ORDERED, k=frequently_ordered_amount)

    # Uncomment to run scrape on randomly selected frequently ordered items
    # scrape(
    #     headed=HEAD_OPTION,
    #     cookies=ALLOW_COOKIES,
    #     zip_code=USER_ZIP_CODE,
    #     items=random_grocery_sample,
    #     results_requested=RESULT_AMOUNT
    # )

    # Batch scraping of a large list to limit traffic
    chunk_amount = 10
    chunks = chunk_list(FREQUENTLY_ORDERED, chunk_amount)
    count = 0
    # for sub_chunk in chunks:
    #     scrape(
    #         headed=HEAD_OPTION,
    #         cookies=ALLOW_COOKIES,
    #         zip_code=USER_ZIP_CODE,
    #         items=sub_chunk,
    #         results_requested=RESULT_AMOUNT
    #     )
    #     count += 1
    #     print(f"Chunk {count} finished")
    #     time.sleep(10)  # Pause to limit traffic

    # Scrape prices of products already in the database | This could take a while if DB has many products
    current_logged_products = get_all_logged_products()
    random.shuffle(current_logged_products)
    # scrape(
    #     headed=HEAD_OPTION,
    #     cookies=ALLOW_COOKIES,
    #     zip_code=USER_ZIP_CODE,
    #     items=current_logged_products,
    #     results_requested=RESULT_AMOUNT
    # )
