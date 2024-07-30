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

## Function to Get Folder Name and URLs from the User

```python
def get_folder_and_urls():
    folder_name = input("Enter the folder name to store the CSV files: ")
    urls = []
    while True:
        url = input("Please enter a URL: ")
        urls.append(url)
        break
    return folder_name, urls
```

- **get_folder_and_urls**: A function that prompts the user to enter a folder name and a URL, returning both.

## Function to Parse Div Classes from the HTML Content

```python
def get_div_classes(soup):
    div_classes = []
    divs = soup.find_all('div')
    for idx, div in enumerate(divs):
        if 'class' in div.attrs:
            class_name = '.'.join(div.attrs['class'])
            div_classes.append((class_name, div.get_text(strip=True)[:100]))  # Show first 100 characters as preview
    return div_classes
```

- **get_div_classes**: A function that finds all `div` tags with class attributes in the HTML content using BeautifulSoup and returns a list of these div classes along with a text preview.

## Function to Display Div Classes to the User and Get Their Choice

```python
def choose_div_class(div_classes):
    print("Available div classes:")
    unique_classes = {}
    index = 1
    for div_class, preview in div_classes:
        if div_class not in unique_classes:
            unique_classes[div_class] = []
        unique_classes[div_class].append(preview)
    
    for idx, (div_class, previews) in enumerate(unique_classes.items(), start=1):
        if len(previews) > 1:
            for i, preview in enumerate(previews):
                print(f"{idx}-{i + 1}. {div_class} ({i + 1}) - Preview: {preview}")
        else:
            print(f"{idx}. {div_class} - Preview: {previews[0]}")

    choices = input("Enter the number of the div class you want to scrape: ")
    if '-' in choices:
        chosen_index, instance = map(int, choices.strip().split('-'))
        chosen_class = list(unique_classes.keys())[chosen_index - 1]
        instance = instance - 1
    else:
        chosen_index = int(choices.strip()) - 1
        chosen_class = list(unique_classes.keys())[chosen_index]
        instance = 0
    return chosen_class, instance
```

- **choose_div_class**: A function that displays the available div classes to the user, prompts them to choose which div class to scrape, and returns the chosen class and instance.

## Function to Scrape Article Data Based on the Chosen Div Class

```python
def scrape_article_data(urls, chosen_class, instance, start_html_index):
    articles_data = []  # empty list

    for idx, url in enumerate(urls):
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Save the HTML content of the URL with an incrementing index
        html_file_name = f"scraped_website_{start_html_index + idx + 1}.html"
        with open(os.path.join(directory_path, html_file_name), 'wb') as file:
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
```

- **scrape_article_data**: A function that scrapes data from the given URLs based on the chosen div class. It also saves the HTML content of each URL with an incrementing index. It returns a list of dictionaries containing the scraped data.

## Main Function

```python
def main():
    global directory_path

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

    # Determine the starting HTML file index
    existing_html_files = [f for f in os.listdir(directory_path) if f.startswith("scraped_website_") and f.endswith(".html")]
    start_html_index = len(existing_html_files)

    # Scrape article data
    articles_data = scrape_article_data(urls, chosen_class, instance, start_html_index)

    # Define the CSV file path
    csv_file_path = os.path.join(directory_path, 'scraped_data.csv')

    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        # Load existing data and append new data
        existing_df = pd.read_csv(csv_file_path)
        new_df = pd.DataFrame(articles_data)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        # Create new DataFrame with scraped data
        combined_df = pd.DataFrame(articles_data)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(csv_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)

    print(f"Data has been saved to '{csv_file_path}'.")
```

- **main**: The main function that orchestrates the scraping process. It gets the folder name and URLs, fetches the first URL to display div classes for selection, scrapes article data, and saves the data to a CSV file.

## Initialize the Main Function and Continue Prompt

```python
if __name__ == "__main__":
    main()

    while True:
        print(
            "How would you like to continue?\n"
            "1. Add new URLs\n"
            "2. Exit"
        )
        user_confirmation = input("Enter your choice: ").strip().lower()
        if user_confirmation == "1":
            main()
        elif user_confirmation == "2":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
```

- **if __name__ == "__main__"**: This block checks if the script is being run directly (not imported as a module). If it is, it calls the `main` function and enters a loop to ask the user whether they want to add new URLs or exit the program.