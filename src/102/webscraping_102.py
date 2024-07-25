import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# Function to get URLs from the user
def get_urls():
    urls = []
    while True:
        url = input("Please enter a URL: ")
        urls.append(url)
        more_urls = input("Do you still want to add URL? [Y/N]: ").strip().lower()
        if more_urls != 'y':
            break
    return urls

# Function to parse headers from the HTML content
def get_headers(soup):
    headers = []
    for i in range(1, 7):  # h1 to h6
        headers.extend(soup.find_all(f'h{i}'))
    return headers

# Function to display headers to the user and get their choices
def choose_headers(headers):
    print("Available headers:")
    for idx, header in enumerate(headers):
        print(f"{idx + 1}. {header.text.strip()}")
    
    choices = input("Enter the numbers of the headers you want to scrape (comma-separated): ")
    chosen_indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
    return [headers[idx] for idx in chosen_indices]

# Function to scrape article data based on chosen headers
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

'''# Load cleaned data for verification (if needed)
cleaned_data = pd.read_csv(csv_file_path)
print(cleaned_data)'''