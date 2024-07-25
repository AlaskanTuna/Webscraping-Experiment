import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = 'https://books.toscrape.com/'

# Fetch the HTML content using requests
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book listings
books = soup.find_all('article', class_='product_pod')

# Initialize lists to store book data
book_titles = []
book_prices = []
book_availabilities = []

# Extract and store the book data
for book in books:
    # Extract book title
    book_title = book.h3.a['title']
    
    # Extract book price
    book_price = book.find('p', class_='price_color').text.strip()
    
    # Extract book availability
    book_availability = book.find('p', class_='instock availability').text.strip()
    
    # Append the data to the lists
    book_titles.append(book_title)
    book_prices.append(book_price)
    book_availabilities.append(book_availability)

# Write the data to a CSV file with UTF-8 encoding
with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Availability"])
    for title, price, availability in zip(book_titles, book_prices, book_availabilities):
        writer.writerow([title, price, availability])

print("Data successfully written to books2.csv")