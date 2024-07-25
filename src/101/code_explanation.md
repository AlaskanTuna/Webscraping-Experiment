# Explanation of Each Step

## Import Libraries

```python
import requests
from bs4 import BeautifulSoup
import csv

```

- **requests**: A library to send HTTP requests and receive responses.
- **BeautifulSoup**: A library to parse HTML and XML documents and extract data from them.
- **csv**: A library to handle CSV file operations such as reading from and writing to CSV files.

## Fetch the HTML Content

```python
# URL of the website to scrape
url = '<https://books.toscrape.com/>'

# Fetch the HTML content using requests
response = requests.get(url)

```

- **url**: The URL of the website you want to scrape.
- **requests.get(url)**: Sends a GET request to the specified URL and stores the server's response in the `response` variable.

## Parse the HTML Content

```python
# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

```

- **response.text**: The HTML content of the webpage.
- **BeautifulSoup(response.text, 'html.parser')**: Initializes BeautifulSoup with the HTML content and specifies the parser to use (`html.parser` in this case).

## Find All Book Listings

```python
# Find all book listings
books = soup.find_all('article', class_='product_pod')

```

- **soup.find_all('article', class_='product_pod')**: Finds all `<article>` tags with the class `product_pod`. Each `<article>` tag represents a single book listing.
- **books**: A list of BeautifulSoup objects, each representing a book listing.

## Initialize Lists to Store Book Data

```python
# Initialize lists to store book data
book_titles = []
book_prices = []
book_availabilities = []

```

- **book_titles**: A list to store the titles of the books.
- **book_prices**: A list to store the prices of the books.
- **book_availabilities**: A list to store the availability statuses of the books.

- **book_availabilities**: A list to store the availability statuses of the books.

## Extract and Store the Book Data

```python
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

```

- **for book in books**: Loops through each `book` in the `books` list.
- **book.h3.a['title']**: Finds the `<a>` tag within the `<h3>` tag of the current `book` and extracts the value of the `title` attribute. This is the book title.
- **book.find('p', class_='price_color').text.strip()**: Finds the `<p>` tag with the class `price_color` within the current `book`, extracts its text content, and removes any leading/trailing whitespace. This is the book price.
- **book.find('p', class_='instock availability').text.strip()**: Finds the `<p>` tag with the class `instock availability` within the current `book`, extracts its text content, and removes any leading/trailing whitespace. This is the book availability status.
- **book_titles.append(book_title)**: Appends the extracted book title to the `book_titles` list.
- **book_prices.append(book_price)**: Appends the extracted book price to the `book_prices` list.
- **book_availabilities.append(book_availability)**: Appends the extracted book availability status to the `book_availabilities` list.

## Write the Data to a CSV File

```python
# Write the data to a CSV file with UTF-8 encoding
with open('books2.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Availability"])
    for title, price, availability in zip(book_titles, book_prices, book_availabilities):
        writer.writerow([title, price, availability])

```

- **with open('books2.csv', 'w', newline='', encoding='utf-8') as f**: Opens a file named `books2.csv` in write mode with UTF-8 encoding and no additional newlines. The `with` statement ensures the file is properly closed after writing.
- **csv.writer(f)**: Creates a CSV writer object that will write to the file `f`.
- **writer.writerow(["Title", "Price", "Availability"])**: Writes the header row to the CSV file.
- **for title, price, availability in zip(book_titles, book_prices, book_availabilities)**: Loops through the zipped lists of book titles, prices, and availabilities.
    - **writer.writerow([title, price, availability])**: Writes a row for each book's title, price, and availability to the CSV file.

## Confirmation Message

```python
print("Data successfully written to books2.csv")

```

- **print()**: Outputs a confirmation message indicating that the data has been successfully written to the CSV file.

### Credits: https://shendai.notion.site/Web-Scraping-101-ca23bf20fd884dea84406ff0158e1081