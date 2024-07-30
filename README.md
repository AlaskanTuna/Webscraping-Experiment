# Webscraping Experiment v1.1

## How To Run
1. Download ZIP, unzip, then open the folder (`-main`) with any IDE.
2. Run the `.py` script from the repository (`src\model\webscraper_beta.py`). The beta version provides a terminal interface for web scraping.

## Why Do We Create This
This is an experiment to create a program in order to scrape website information into useful data for research and analysis purposes.

### Webscraper (Beta)
- **Dynamic URL Input:** Prompts the user to enter multiple URLs for scraping.
- **Div Class Selection:** Displays all div classes from the first URL and allows the user to select which div class to scrape.
- **Data Scraping:** Scrapes data based on the selected div class from the provided URLs.
- **CSV Export:** Exports the scraped data to a CSV file in a user-specified directory.
- **HTML Save:** Saves the HTML content of each URL as `scraped_website_[index].html` in the same directory as the CSV file (`scraped_data.csv`).
- **UTF-8 Encoding:** Ensures all CSV files are saved with UTF-8 encoding to support a wide range of characters.
- **Minimal Quoting:** Uses minimal quoting in the CSV files to maintain readability and compatibility.
- **Appends Data:** Allows adding new URLs and appends the new data to the existing CSV file.

## Website to View CSV in Table Format
https://codebeautify.org/csv-viewer

## Contributors
Discord: osnxw & ikantenggiri