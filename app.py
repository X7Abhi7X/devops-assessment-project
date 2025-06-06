# Import the tools we need
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import random

# Create an instance of the Flask application
app = Flask(__name__)

# This function does the web scraping
def scrape_quotes_from_web():
    """
    This function scrapes quotes from a special website made for testing scrapers.
    """
    # The URL of the website we want to scrape
    website_url = "http://quotes.toscrape.com"
    
    # We use a try/except block to handle errors, like if your internet is down
    # or the website is unavailable. This makes our app more robust.
    try:
        # Send a request to the website to get its HTML content
        response = requests.get(website_url)
        # This will raise an error if the request was not successful (e.g., 404 Not Found)
        response.raise_for_status() 

        # Use BeautifulSoup to parse the HTML content we received
        soup_parser = BeautifulSoup(response.content, 'html.parser')
        
        # Create an empty list where we will store the quotes we find
        found_quotes = []
        
        # The website organises each quote in a 'div' with the class 'quote'
        # We find all of these quote sections.
        all_quote_containers = soup_parser.find_all('div', class_='quote')
        
        # Loop through each quote section we found
        for quote_container in all_quote_containers:
            # Inside each section, the quote text is in a 'span' with class 'text'
            quote_text = quote_container.find('span', class_='text').get_text(strip=True)
            # The author's name is in a 'small' tag with class 'author'
            author_name = quote_container.find('small', class_='author').get_text(strip=True)
            # Combine them into a nice string and add to our list
            found_quotes.append(f"{quote_text} - {author_name}")
        
        # Return the list of quotes we found
        return found_quotes

    except requests.exceptions.RequestException as error:
        # If anything went wrong with the web request, print an error message
        print(f"Could not scrape quotes from the web. Error: {error}")
        # And return a default list of quotes so the app doesn't crash
        return [
            "Scraping failed, so here is a default quote. The only way to do great work is to love what you do. - Steve Jobs",
            "Houston, we have a problem. - Apollo 13"
        ]

# This is the main page of our website (the "route")
@app.route('/')
def home_page():
    # Call our function to get the list of quotes
    quotes_list = scrape_quotes_from_web()
    # Choose one quote from the list at random
    random_quote = random.choice(quotes_list)
    # Render the HTML page and pass the chosen quote to it
    return render_template('index.html', quote_to_display=random_quote)

# This makes sure the app runs when we execute the python script
if __name__ == '__main__':
    # Run the app. host='0.0.0.0' makes it accessible from outside the Docker container later.
    app.run(host='0.0.0.0', port=5000)