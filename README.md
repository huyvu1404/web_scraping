# Web Scraping Project

This project involves scraping data from a website and storing it in JSON and CSV formats. The scraped data is then read and processed using PySpark to perform various transformations and analyses. The processed data is saved in JSON format and loaded into a MySQL database for further use and analysis.

1. Web Scraping: Scrape data from e-commerce websites and save it CSV formats.
2. Data Processing: Read the JSON files and process data using PySpark.
3. Data Storage: Save processed data in CSV format and load them into a MySQL database for further analysis and utilization.

## Deployment

 To run this project, you need to create a virtual environment and install neccesary libraries.

``` bash
  python3 -m venv venv

  source venv/bin/activate

  pip install -r requirements
```

Start MySQL containers
``` bash
  docker compose up -d
```

## Tech Stack

**Data Processing:** Python, PySpark

**Database:** MySQL

**Web Scraping:** Selenium, Beautiful Soup

**Containerization:** Docker


