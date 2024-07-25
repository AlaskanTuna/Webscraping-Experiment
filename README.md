# Webscraping Experiment 0.0.1

## How To Run
1. Download ZIP, unzip, then open the folder (`-main`) with any IDE.
2. Run the `.py` script from the repository (`src\101\webscraping_101` or `src\102\webscraping_102`). 101 is hardcoded (WIP) whereas 102 has terminal interface (WIP).

## Why Do We Create This
This is an experiment to create a program in order to scrape website information into useful data for research and analysis purposes.

## 101 and 102
101 is our initial proposal demo. 102 is our cutting-edge demo. Both are still WIP.

### 102 Features
- **Dynamic URL Input:** Prompts the user to enter multiple URLs for scraping (preferably from the same website).
- **Header Selection:** Displays all headers (h1 to h6) from the first URL and allows the user to select which headers to scrape.
- **Data Scraping:** Scrapes data based on the selected headers from the provided URLs.
- **Data Cleaning:** Checks for and removes rows with missing values in critical columns.
- **CSV Export:** Exports the cleaned data to a CSV file in a user-specified directory.
- **HTML Save:** Saves the HTML content of the first URL as `scraped_website.html` in the same directory as the CSV file (`scraped_data.csv`).
- **UTF-8 Encoding:** Ensures all CSV files are saved with UTF-8 encoding to support a wide range of characters.
- **Minimal Quoting:** Uses minimal quoting in the CSV files to maintain readability and compatibility.

## Website to View CSV in Table Format
https://codebeautify.org/csv-viewer

## Contributors
Discord: osnxw & ikantenggiri