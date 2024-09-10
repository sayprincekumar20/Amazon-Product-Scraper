import csv
import mysql.connector
from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(url)

# Extract page content and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find product items
resultset = soup.find_all('div', {'data-component-type': 's-search-result'})

product_names = []
product_prices = []
product_actual_prices= []
product_ratings = []
product_review_counts = []

for item in resultset:
    name = item.find("span", class_="a-size-medium a-color-base a-text-normal")
    name = name.text if name is not None else ""

    discount_price = item.find("span", class_="a-price-whole")
    discount_price = discount_price.text if discount_price is not None else ""

    actual_price =item.find("span" ,class_="a-price a-text-price")
    actual_price = actual_price.text if actual_price is not None else ""

    rating = item.find("span", class_="a-icon-alt")
    rating = rating.text if rating is not None else ""

    review_count = item.find("span", class_="a-size-base s-underline-text")
    review_count = review_count.text if review_count is not None else ""

    product_names.append(name)
    product_prices.append(discount_price)
    product_actual_prices.append(actual_price)
    product_ratings.append(rating)
    product_review_counts.append(review_count)

# Close the WebDriver
driver.quit()

# Connect to MySQL database
cnx = mysql.connector.connect(
    user='root', 
    password='123',
    host='localhost',
    database='mysql'
)
cursor = cnx.cursor()

# Insert data into the database
add_product = ("INSERT INTO phone_products "
               "(product_name, dis_price,actual_price, rating, review_count) "
               "VALUES (%s,  %s, %s, %s, %s)")

for i in range(len(product_names)):
    data_product = (product_names[i], product_prices[i],product_actual_prices[i],
                    product_ratings[i], product_review_counts[i])
    cursor.execute(add_product, data_product)

# Commit the transaction
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
