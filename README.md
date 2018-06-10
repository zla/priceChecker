# priceChecker
Web stores scrapers + django app

At the start of 2017 I decided to replace my old laptop with a Microsoft Surface Pro 4 and I wanted something to track the 
evolution of the prices (or special offers) and buy it when the price was under a certain value.

At first I wrote a scraper that read the products list and saved the prices in a Google Sheets spreadsheet. 
Then I changed it to use a different spreadsheet for each product. But this required to much manual work to add new products so I 
switched to an SQLite db and I added a simple command line interface to manage it. The online spreadsheets were still updated to be 
able to access the prices from anywhere.
Then I tried to create a web interface to view and manage the database: this is how I created my first Django app (following the 
tutorial from the Django 2 documentation).
