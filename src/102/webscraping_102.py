import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# Function to get folder name and URLs from the user
def get_folder_and_urls():
    folder_name = input("Enter the folder name to store the CSV files: ")
    urls = []
    while True:
        url = input("Please enter a URL: ")
        urls.append(url)
        more_urls = input("Do you still want to add URL? [Y/N]: ").strip().lower()
        if more_urls != 'y':
            break
    return folder_name, urls

# Function to parse div classes from the HTML content
def get_div_classes(soup):
    div_classes = []
    divs = soup.find_all('div')
    for idx, div in enumerate(divs):
        if 'class' in div.attrs:
            class_name = '.'.join(div.attrs['class'])
            div_classes.append(class_name)
    return div_classes

# Function to display div classes to the user and get their choice
def choose_div_class(div_classes):
    print("Available div classes:")
    unique_classes = list(set(div_classes))
    for idx, div_class in enumerate(unique_classes):
        occurrences = div_classes.count(div_class)
        if occurrences > 1:
            for i in range(occurrences):
                print(f"{idx + 1}-{i + 1}. {div_class} ({i + 1})")
        else:
            print(f"{idx + 1}. {div_class}")

    choices = input("Enter the number of the div class you want to scrape: ")
    if '-' in choices:
        chosen_index, instance = map(int, choices.strip().split('-'))
        chosen_class = unique_classes[chosen_index - 1]
        instance = instance - 1
    else:
        chosen_index = int(choices.strip()) - 1
        chosen_class = unique_classes[chosen_index]
        instance = 0
    return chosen_class, instance

# Function to scrape article data based on the chosen div class
def scrape_article_data(urls, chosen_class, instance):
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

        # Extract the content inside the chosen div class
        divs = soup.find_all('div', class_=chosen_class.split('.'))
        if instance < len(divs):
            content = divs[instance].get_text(strip=True)
        else:
            content = ''

        article_data = {
            'URL': url,
            'Title': title,
            'Description': content
        }

        articles_data.append(article_data)
    return articles_data

# Get folder name and URLs from the user
folder_name, urls = get_folder_and_urls()

# Define the directory path
directory_path = os.path.join('Documents', 'csv_files', folder_name)

# Create the directory if it does not exist
os.makedirs(directory_path, exist_ok=True)

# Fetch the first URL to display div classes for selection
response = requests.get(urls[0])
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Get and display div classes
div_classes = get_div_classes(soup)
chosen_class, instance = choose_div_class(div_classes)

# Scrape article data
articles_data = scrape_article_data(urls, chosen_class, instance)

# Convert scraped data to DataFrame
scraped_df = pd.DataFrame(articles_data)

# Define the CSV file path for the final cleaned data
csv_file_path = os.path.join(directory_path, 'scraped_data.csv')

# Save the cleaned DataFrame to a CSV file
scraped_df.to_csv(csv_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)

print(f"Cleaned data has been saved to '{csv_file_path}'.")

# Load cleaned data for verification (if needed)
# cleaned_data = pd.read_csv(csv_file_path)
# print(cleaned_data)