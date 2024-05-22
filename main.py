from scraper import scrape_sales as scrape


head_option = True
allow_cookies = True
user_zip_code = 43220
items_list = ["King's Hawaiian", "Cheese Balls", "Hellmann's Mayo", "Chobani Yogurt Vanilla"]
result_amount = 4

scrape(
    headed=head_option,
    cookies=allow_cookies,
    zip_code=user_zip_code,
    items=items_list,
    results_requested=result_amount,
)


