import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Define the URL of the Amazon search page
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Extract page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

# Find all product containers
resultset = soup.find_all('div', {'data-component-type': 's-search-result'})

# Initialize lists to store product details
product_names = []
product_urls = []
product_prices = []
product_ratings = []
product_review_counts = []

# Extract details for each product
for item in resultset:
    name = item.find("span", class_="a-size-medium a-color-base a-text-normal")
    name = name.text if name else ""

    url = item.find("a", class_="a-link-normal a-text-normal")
    url = "https://www.amazon.in" + url["href"] if url else ""

    price = item.find("span", class_="a-offscreen")
    price = price.text if price else ""

    rating = item.find("span", class_="a-icon-alt")
    rating = rating.text if rating else ""

    review_count = item.find("div", class_="a-section a-text-center")
    review_count = review_count.text if review_count else ""

    product_names.append(name)
    product_urls.append(url)
    product_prices.append(price)
    product_ratings.append(rating)
    product_review_counts.append(review_count)

# Write the data to a CSV file
filename = "products3.csv"
header = ['Product Name', 'URL', 'Price', 'Rating', 'Review Count']

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(zip(product_names, product_urls, product_prices, product_ratings, product_review_counts))

print(f"Data has been written to {filename}")
