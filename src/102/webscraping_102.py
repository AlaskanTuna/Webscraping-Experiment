import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# Function to scrape article data from a list of URLs
def scrape_article_data(urls):
    articles_data = []  # empty list

    # Loop through the URLs
    for url in urls:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the title of the article
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else 'N/A'

        # Extract Character
        character_tag = soup.find('h1', id='article-name')
        character = character_tag.text if character_tag else 'N/A'

        # Extract Overview
        overview_tag = soup.find('h2', id='h2_0')
        overview = overview_tag.find_next_sibling('p').text if overview_tag else 'N/A'

        # Extract Personality
        personality_tag = soup.find('h2', id='h2_1')
        personality = personality_tag.find_next_sibling('p').text if personality_tag else 'N/A'

        # Extract History
        history_tag = soup.find('h2', id='h2_2')
        history = history_tag.find_next_sibling('p').text if history_tag else 'N/A'

        # Extract Etymology
        etymology_tag = soup.find('h2', id='h2_3')
        etymology = etymology_tag.find_next_sibling('p').text if etymology_tag else 'N/A'

        # Data that we want to store in the CSV file
        articles_data.append({
            'URL': url,
            'Title': title,
            'Character': character,
            'Overview': overview,
            'Personality': personality,
            'History': history,
            'Etymology': etymology
        })
    return articles_data

# Prompt the user for a folder name
folder_name = input("Enter the folder name to store the CSV files: ")

# Define the directory path
directory_path = os.path.join('Documents', 'csv_files', folder_name)

# Create the directory if it does not exist
os.makedirs(directory_path, exist_ok=True)

# List of URLs (Recommended to be from the same website)
urls = [
    'https://dic.pixiv.net/en/a/Kaguya%20Shinomiya',
]

# Scrape article data
articles_data = scrape_article_data(urls)

# Define the CSV file path
csv_file_path = os.path.join(directory_path, 'scraped_data.csv')

# Write scraped data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV headers
    fieldnames = ['URL', 'Title', 'Character', 'Overview', 'Personality', 'History', 'Etymology']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write each row of scraped data
    writer.writerows(articles_data)

print("Scraped data has been written to", csv_file_path)

# Load scraped data into DataFrame
scraped = pd.read_csv(csv_file_path)
print(scraped)

# Check for NaN values per column
nan_counts = scraped.isnull().sum()
print('Number of NaN values per column:\n', nan_counts)

# Check if there is any null value in the DataFrame
has_null = scraped.isnull().any().any()
print("Are there any null values in the DataFrame?", has_null)

# Drop rows with NaN values
scraped_cleaned = scraped.dropna(subset=['Title', 'Character', 'Overview', 'Personality', 'History', 'Etymology'])

# Verify the rows have been dropped
print("Number of rows after dropping NaNs:", len(scraped_cleaned))

# Save the cleaned DataFrame to a new CSV file
csv_file_path_cleaned = os.path.join(directory_path, 'cleaned_articles.csv')
scraped_cleaned.to_csv(csv_file_path_cleaned, index=False, encoding='utf-8')

print(f"Cleaned data has been saved to '{csv_file_path_cleaned}'.")

# Load cleaned data
clean_scraped = pd.read_csv(csv_file_path_cleaned)
print(clean_scraped)

# Save cleaned data again
csv_file_path_cleaned_final = os.path.join(directory_path, 'scraped_cleaned_articles.csv')
clean_scraped.to_csv(csv_file_path_cleaned_final, index=False, encoding='utf-8')
print(f"Cleaned data has been saved to '{csv_file_path_cleaned_final}'.")

# Load cleaned data again
scraped_cleaned_article = pd.read_csv(csv_file_path_cleaned_final)
print(scraped_cleaned_article)