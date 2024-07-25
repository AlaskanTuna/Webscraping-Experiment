# Explanation of Each Step

## Import Libraries

```python
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
```

- **requests**: A library to send HTTP requests and receive responses.
- **BeautifulSoup**: A library to parse HTML and XML documents and extract data from them.
- **csv**: A library to handle CSV file operations such as reading from and writing to CSV files.
- **pandas**: A library for data manipulation and analysis.
- **os**: A library to interact with the operating system and manage directories and files.

## Function to Get URLs from the User

```python
def get_urls():
    urls = []
    while True:
        url = input("Please enter a URL: ")
        urls.append(url)
        more_urls = input("Do you still want to add URL? [Y/N]: ").strip().lower()
        if more_urls != 'y':
            break
    return urls
```

- **get_urls**: A function that prompts the user to enter multiple URLs, returning a list of URLs.

## Function to Parse Headers from the HTML Content

```python
def get_headers(soup):
    headers = []
    for i in range(1, 7):  # h1 to h6
        headers.extend(soup.find_all(f'h{i}'))
    return headers
```

- **get_headers**: A function that finds all header tags (h1 to h6) in the HTML content using BeautifulSoup and returns a list of these headers.

## Function to Display Headers to the User and Get Their Choices

```python
def choose_headers(headers):
    print("Available headers:")
    for idx, header in enumerate(headers):
        print(f"{idx + 1}. {header.text.strip()}")
    
    choices = input("Enter the numbers of the headers you want to scrape (comma-separated): ")
    chosen_indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
    return [headers[idx] for idx in chosen_indices]
```

- **choose_headers**: A function that displays the headers to the user and prompts them to choose which headers to scrape. It returns a list of the chosen headers.

## Function to Scrape Article Data Based on Chosen Headers

```python
def scrape_article_data(urls, chosen_headers):
    articles_data = []  # empty list

    for url in urls:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Save the HTML content of the first URL
        if url == urls[0]:
            with open(os.path.join(directory_path, 'scraped_website.html'), 'wb') as file:
                file.write(html_content)

        # Extract the title of the article
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else 'N/A'

        article_data = {
            'URL': url,
            'Title': title
        }

        for header in chosen_headers:
            header_text = header.text.strip()
            content = []
            sibling = header.find_next_sibling()
            while sibling and sibling.name != header.name:
                if sibling.name == 'p':
                    content.append(sibling.text.strip())
                sibling = sibling.find_next_sibling()
            article_data[header_text] = ' '.join(content)

        articles_data.append(article_data)
    return articles_data
```

- **scrape_article_data**: A function that scrapes data from the given URLs based on the chosen headers. It also saves the HTML content of the first URL. It returns a list of dictionaries containing the scraped data.

## Main Script

```python
# Get URLs from the user
urls = get_urls()

# Fetch the first URL to display headers for selection
response = requests.get(urls[0])
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Get and display headers
headers = get_headers(soup)
chosen_headers = choose_headers(headers)

# Prompt the user for a folder name
folder_name = input("Enter the folder name to store the CSV files: ")

# Define the directory path
directory_path = os.path.join('Documents', 'csv_files', folder_name)

# Create the directory if it does not exist
os.makedirs(directory_path, exist_ok=True)

# Scrape article data
articles_data = scrape_article_data(urls, chosen_headers)

# Convert scraped data to DataFrame
scraped_df = pd.DataFrame(articles_data)

# Check for NaN values per column
nan_counts = scraped_df.isnull().sum()
print('Number of NaN values per column:\n', nan_counts)

# Check if there is any null value in the DataFrame
has_null = scraped_df.isnull().any().any()
print("Are there any null values in the DataFrame?", has_null)

# Drop rows with NaN values
scraped_cleaned_df = scraped_df.dropna(subset=['Title'] + [header.text.strip() for header in chosen_headers])

# Verify the rows have been dropped
print("Number of rows after dropping NaNs:", len(scraped_cleaned_df))

# Define the CSV file path for the final cleaned data
csv_file_path = os.path.join(directory_path, 'scraped_data.csv')

# Save the cleaned DataFrame to a CSV file
scraped_cleaned_df.to_csv(csv_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)

print(f"Cleaned data has been saved to '{csv_file_path}'.")
```

- **urls = get_urls()**: Gets the list of URLs from the user.
- **response = requests.get(urls[0])**: Fetches the HTML content of the first URL.
- **headers = get_headers(soup)**: Parses and gets the headers from the HTML content.
- **chosen_headers = choose_headers(headers)**: Prompts the user to choose headers to scrape.
- **folder_name = input("Enter the folder name to store the CSV files: ")**: Prompts the user for a folder name.
- **directory_path = os.path.join('Documents', 'csv_files', folder_name)**: Defines the directory path for storing the CSV files.
- **os.makedirs(directory_path, exist_ok=True)**: Creates the directory if it does not exist.
- **articles_data = scrape_article_data(urls, chosen_headers)**: Scrapes the article data based on the chosen headers.
- **scraped_df = pd.DataFrame(articles_data)**: Converts the scraped data to a DataFrame.
- **nan_counts = scraped_df.isnull().sum()**: Checks for NaN values per column.
- **has_null = scraped_df.isnull().any().any()**: Checks if there are any null values in the DataFrame.
- **scraped_cleaned_df = scraped_df.dropna(subset=['Title'] + [header.text.strip() for header in chosen_headers])**: Drops rows with NaN values in the specified columns.
- **csv_file_path = os.path.join(directory_path, 'scraped_data.csv')**: Defines the CSV file path for the cleaned data.
- **scraped_cleaned_df.to_csv(csv_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)**: Saves the cleaned DataFrame to a CSV file.
- **print(f"Cleaned data has been saved to '{csv_file_path}'.")**: Prints a confirmation message indicating that the cleaned data has been saved.